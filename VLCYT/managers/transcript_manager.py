"""
Transcript manager for VLCYT application.

This module contains the TranscriptManager class that handles video transcript
fetching, parsing, and display.
"""

import logging
import re
from typing import Dict, List, Optional

try:
    from PySide6.QtCore import QObject, Signal

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False
    print("PySide6 not available - running in test mode")

    # Mock QObject and Signal for testing
    class QObject:
        def __init__(self):
            pass

    class Signal:
        def __init__(self, *args):
            pass

        def connect(self, func):
            pass

        def emit(self, *args):
            pass


# Import ThreadManager
from ..managers.thread_manager import ThreadManager


class TranscriptEntry:
    """
    Class representing a single transcript entry.

    Each entry has a start time, end time, and text content.
    """

    def __init__(self, start_time: float, end_time: float, text: str):
        """
        Initialize transcript entry.

        Args:
            start_time: Start time in seconds
            end_time: End time in seconds
            text: Entry text content
        """
        self.start_time = start_time
        self.end_time = end_time
        self.text = text

    def __str__(self) -> str:
        """
        String representation of transcript entry.

        Returns:
            Formatted string with time and text
        """
        from ..utils.format_utils import format_time

        return f"[{format_time(int(self.start_time))}] {self.text}"

    def to_dict(self) -> Dict:
        """
        Convert entry to dictionary.

        Returns:
            Dictionary representation of entry
        """
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "text": self.text,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "TranscriptEntry":
        """
        Create entry from dictionary.

        Args:
            data: Dictionary representation of entry

        Returns:
            TranscriptEntry instance
        """
        return cls(
            start_time=data.get("start_time", 0),
            end_time=data.get("end_time", 0),
            text=data.get("text", ""),
        )


class TranscriptManager(QObject):
    """
    Manager for video transcripts.

    This class handles fetching, parsing, and accessing video transcripts.
    """

    # Define signals if Qt is available
    if PYSIDE6_AVAILABLE:
        transcript_ready = Signal(list)  # List of TranscriptEntry objects
        transcript_error = Signal(str)  # Error message
        transcript_cleared = Signal()  # No arguments

    def __init__(self, thread_manager: ThreadManager):
        """
        Initialize transcript manager.

        Args:
            thread_manager: Thread manager for background tasks
        """
        super().__init__()
        self.thread_manager = thread_manager
        self.logger = logging.getLogger("vlcyt.transcript")

        self.current_video_id = None
        self.current_transcript_entries = []
        self.current_transcript_language = None
        self.available_transcript_languages = []

        # Initialize transcript fetcher (lazy import to avoid circular dependencies)
        self._transcript_fetcher = None

    def _get_transcript_fetcher(self):
        """
        Lazy initialize transcript fetcher.

        Returns:
            Transcript fetcher instance
        """
        if self._transcript_fetcher is None:
            from ..utils.transcript_fetcher import TranscriptFetcher

            self._transcript_fetcher = TranscriptFetcher()
        return self._transcript_fetcher

    def fetch_transcript(self, video_id: str, language_code: str = None) -> None:
        """
        Fetch transcript for a video.

        Args:
            video_id: YouTube video ID
            language_code: Language code to fetch, None for default
        """
        if not video_id:
            self.logger.error("Cannot fetch transcript: No video ID provided")
            if PYSIDE6_AVAILABLE:
                self.transcript_error.emit("No video ID provided")
            return

        # Clear current transcript
        self.clear_transcript()

        # Save current video ID
        self.current_video_id = video_id

        # Start a background thread to fetch transcript
        def fetch_task():
            try:
                # Get transcript fetcher
                fetcher = self._get_transcript_fetcher()

                # Get available languages first
                self.available_transcript_languages = fetcher.list_languages(video_id)

                # If no specific language requested, use the first available
                if language_code is None and self.available_transcript_languages:
                    language_code = self.available_transcript_languages[0]["code"]
                elif language_code is None:
                    language_code = "en"  # Default fallback

                # Fetch transcript
                if language_code:
                    transcript_data = fetcher.get_transcript(video_id, language_code)
                    entries = self._parse_transcript_data(transcript_data)

                    # Save language
                    self.current_transcript_language = language_code

                    # Save entries
                    self.current_transcript_entries = entries

                    # Emit signal with entries
                    if PYSIDE6_AVAILABLE:
                        self.transcript_ready.emit(entries)

                    return entries
                else:
                    raise ValueError("No transcript available for this video")
            except Exception as e:
                self.logger.error(f"Error fetching transcript: {str(e)}")
                if PYSIDE6_AVAILABLE:
                    self.transcript_error.emit(f"Error fetching transcript: {str(e)}")
                return None

        # Run the task in a background thread
        self.thread_manager.run_in_thread(
            task=fetch_task,
            task_name=f"transcript_fetch_{video_id}",
            priority=ThreadManager.PRIORITY_NORMAL,
        )

    def _parse_transcript_data(
        self, transcript_data: List[Dict]
    ) -> List[TranscriptEntry]:
        """
        Parse raw transcript data into TranscriptEntry objects.

        Args:
            transcript_data: Raw transcript data from API

        Returns:
            List of TranscriptEntry objects
        """
        entries = []

        for item in transcript_data:
            start = item.get("start", 0)
            duration = item.get("duration", 0)
            text = item.get("text", "").strip()

            # Create entry
            entry = TranscriptEntry(
                start_time=start, end_time=start + duration, text=text
            )

            entries.append(entry)

        return entries

    def clear_transcript(self) -> None:
        """Clear current transcript data."""
        self.current_transcript_entries = []
        self.current_transcript_language = None
        self.available_transcript_languages = []

        if PYSIDE6_AVAILABLE:
            self.transcript_cleared.emit()

    def get_current_transcript_data(self) -> List[TranscriptEntry]:
        """
        Get current transcript entries.

        Returns:
            List of TranscriptEntry objects
        """
        return self.current_transcript_entries

    def get_available_languages(self) -> List[Dict]:
        """
        Get available transcript languages.

        Returns:
            List of language dictionaries with 'code' and 'name' keys
        """
        return self.available_transcript_languages

    def get_current_language(self) -> Optional[str]:
        """
        Get current transcript language code.

        Returns:
            Language code or None if no transcript loaded
        """
        return self.current_transcript_language

    def find_entry_at_time(self, time_seconds: float) -> Optional[TranscriptEntry]:
        """
        Find transcript entry at a specific time.

        Args:
            time_seconds: Time in seconds

        Returns:
            TranscriptEntry at the given time, or None if not found
        """
        if not self.current_transcript_entries:
            return None

        # Find entry where time falls between start and end times
        for entry in self.current_transcript_entries:
            if entry.start_time <= time_seconds < entry.end_time:
                return entry

        # If not found, return the closest entry before the given time
        closest_entry = None
        closest_diff = float("inf")

        for entry in self.current_transcript_entries:
            if entry.start_time <= time_seconds:
                diff = time_seconds - entry.start_time
                if diff < closest_diff:
                    closest_diff = diff
                    closest_entry = entry

        return closest_entry

    def search_transcript(self, query: str) -> List[TranscriptEntry]:
        """
        Search transcript for a specific query.

        Args:
            query: Search string

        Returns:
            List of matching TranscriptEntry objects
        """
        if not query or not self.current_transcript_entries:
            return []

        # Case insensitive search
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        matching_entries = []

        for entry in self.current_transcript_entries:
            if pattern.search(entry.text):
                matching_entries.append(entry)

        return matching_entries

    def export_transcript(self, file_path: str, format_type: str = "text") -> bool:
        """
        Export transcript to a file.

        Args:
            file_path: Path to save the transcript
            format_type: Format type ('text', 'srt', or 'json')

        Returns:
            True if successful, False otherwise
        """
        if not self.current_transcript_entries:
            self.logger.error("Cannot export transcript: No transcript loaded")
            return False

        try:
            if format_type == "srt":
                content = self._format_as_srt()
            elif format_type == "json":
                import json

                entries_dict = [
                    entry.to_dict() for entry in self.current_transcript_entries
                ]
                content = json.dumps(entries_dict, indent=2)
            else:  # Default to text
                content = self._format_as_text()

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            return True
        except Exception as e:
            self.logger.error(f"Error exporting transcript: {str(e)}")
            return False

    def _format_as_text(self) -> str:
        """
        Format transcript as plain text.

        Returns:
            Formatted text
        """
        from ..utils.format_utils import format_time

        lines = []

        for entry in self.current_transcript_entries:
            start_time = format_time(int(entry.start_time))
            lines.append(f"[{start_time}] {entry.text}")

        return "\n".join(lines)

    def _format_as_srt(self) -> str:
        """
        Format transcript as SRT format.

        Returns:
            Formatted SRT text
        """
        lines = []

        for i, entry in enumerate(self.current_transcript_entries):
            # Entry number
            lines.append(str(i + 1))

            # Time range
            start = self._format_srt_time(entry.start_time)
            end = self._format_srt_time(entry.end_time)
            lines.append(f"{start} --> {end}")

            # Text
            lines.append(entry.text)

            # Empty line between entries
            lines.append("")

        return "\n".join(lines)

    def _format_srt_time(self, seconds: float) -> str:
        """
        Format time in seconds to SRT time format (HH:MM:SS,mmm).

        Args:
            seconds: Time in seconds

        Returns:
            Formatted time string
        """
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((seconds - int(seconds)) * 1000)

        return (
            f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"
        )
