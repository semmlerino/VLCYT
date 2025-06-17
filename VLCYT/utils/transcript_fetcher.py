"""
Transcript fetcher utility for VLCYT.

This module provides functionality to fetch video transcripts from YouTube.
"""

from typing import Any, Dict, List, Optional

try:
    from youtube_transcript_api import YouTubeTranscriptApi

    TRANSCRIPT_API_AVAILABLE = True
except ImportError:
    TRANSCRIPT_API_AVAILABLE = False
    print("Warning: youtube-transcript-api not available")

from ..exceptions import NetworkError, ValidationError


class TranscriptFetcher:
    """
    Utility class for fetching video transcripts.
    """

    def __init__(self):
        """Initialize transcript fetcher."""
        self.available = TRANSCRIPT_API_AVAILABLE

    def fetch_transcript(self, video_url: str) -> List[Dict[str, Any]]:
        """
        Fetch transcript for a YouTube video.

        Args:
            video_url: YouTube video URL

        Returns:
            List of transcript entries with 'start', 'duration', 'text' keys

        Raises:
            NetworkError: If transcript fetching fails
            ValidationError: If video URL is invalid
        """
        if not self.available:
            raise NetworkError("Transcript API not available")

        try:
            # Extract video ID from URL
            video_id = self._extract_video_id(video_url)
            if not video_id:
                raise ValidationError("Invalid YouTube URL")

            # Fetch transcript
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # Try to get English transcript first, then auto-generated
            transcript = None
            try:
                transcript = transcript_list.find_manually_created_transcript(["en"])
            except Exception:
                try:
                    transcript = transcript_list.find_generated_transcript(["en"])
                except Exception:
                    # Get any available transcript
                    for t in transcript_list:
                        transcript = t
                        break

            if not transcript:
                raise NetworkError("No transcript available for this video")

            # Fetch transcript data
            transcript_data = transcript.fetch()

            # Format for consistency
            formatted_data = []
            for entry in transcript_data:
                formatted_data.append(
                    {
                        "start": entry.get("start", 0),
                        "duration": entry.get("duration", 0),
                        "text": entry.get("text", "").strip(),
                    }
                )

            return formatted_data

        except Exception as e:
            if isinstance(e, (NetworkError, ValidationError)):
                raise
            else:
                raise NetworkError(f"Failed to fetch transcript: {str(e)}")

    def _extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL.

        Args:
            url: YouTube video URL

        Returns:
            Video ID or None if extraction fails
        """
        import re

        # Various YouTube URL patterns
        patterns = [
            r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&]+)",
            r"(?:https?://)?(?:www\.)?youtu\.be/([^?]+)",
            r"(?:https?://)?(?:www\.)?youtube\.com/embed/([^?]+)",
            r"(?:https?://)?(?:www\.)?youtube\.com/v/([^?]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return None

    def is_available(self) -> bool:
        """
        Check if transcript fetching is available.

        Returns:
            True if transcript API is available
        """
        return self.available
