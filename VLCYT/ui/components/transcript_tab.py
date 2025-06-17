"""
Transcript tab component for VLCYT.

This module contains the TranscriptTab class which provides transcript display
and management functionality including search, auto-scroll, and synchronization.
"""

import re
from typing import Any, Dict, List

try:
    from PySide6.QtCore import QTimer, Signal
    from PySide6.QtWidgets import (
        QCheckBox,
        QHBoxLayout,
        QLineEdit,
        QTextBrowser,
        QVBoxLayout,
    )

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False
    print("PySide6 not available - running in test mode")

    # Create dummy classes for testing
    class Signal:
        def __init__(self, *args):
            pass

        def connect(self, func):
            pass

        def emit(self, *args):
            pass

    class QTimer:
        def __init__(self):
            pass

        def timeout(self):
            return Signal()

        def start(self, ms):
            pass

        def stop(self):
            pass

    class QCheckBox:
        def __init__(self, text="", parent=None):
            pass

        def setChecked(self, checked):
            pass

        def setToolTip(self, tip):
            pass

        def isChecked(self):
            return True

    class QHBoxLayout:
        def __init__(self, parent=None):
            pass

        def setSpacing(self, spacing):
            pass

        def addWidget(self, widget):
            pass

        def addStretch(self):
            pass

    class QLineEdit:
        def __init__(self, parent=None):
            pass

        def setPlaceholderText(self, text):
            pass

        def text(self):
            return ""

    class QTextBrowser:
        def __init__(self, parent=None):
            pass

        def setObjectName(self, name):
            pass

        def setOpenExternalLinks(self, enabled):
            pass

        def setHtml(self, html):
            pass

    class QVBoxLayout:
        def __init__(self, parent=None):
            pass

        def setSpacing(self, spacing):
            pass

        def addLayout(self, layout):
            pass

        def addWidget(self, widget):
            pass


from .base_tab import BaseTab

# Import utilities - these will need to be properly imported
try:
    from ...utils.format_utils import format_time
    from ..widgets import ModernButton
except ImportError:
    # Fallback for testing
    def format_time(seconds):
        return "00:00"

    class ModernButton:
        def __init__(self, text="", icon="", parent=None):
            pass

        def setObjectName(self, name):
            pass

        def setToolTip(self, tip):
            pass

        def setEnabled(self, enabled):
            pass


class TranscriptTab(BaseTab):
    """
    Transcript display and management tab widget.

    Provides functionality for:
    - Fetching video transcripts
    - Searching within transcripts
    - Auto-scroll synchronization with video playback
    - Clickable transcript navigation
    """

    # Signals
    transcript_fetch_requested = Signal()
    transcript_seek_requested = Signal(float)  # Seek to timestamp

    def __init__(self, parent=None):
        """
        Initialize transcript tab.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.transcript_data: List[Dict[str, Any]] = []
        self.current_position = 0.0
        self.search_timer = QTimer() if PYSIDE6_AVAILABLE else None
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Set up the transcript tab UI."""
        # Top controls (compact)
        top_controls = QHBoxLayout()
        top_controls.setSpacing(5)

        self.fetch_transcript_button = ModernButton("", "⌘", self)
        self.fetch_transcript_button.setObjectName("transcriptButton")
        self.fetch_transcript_button.setEnabled(False)
        self.fetch_transcript_button.setToolTip("Fetch transcript")
        top_controls.addWidget(self.fetch_transcript_button)

        self.auto_scroll_check = QCheckBox("⟲ Sync")
        self.auto_scroll_check.setChecked(True)
        self.auto_scroll_check.setToolTip("Auto-scroll with video")
        top_controls.addWidget(self.auto_scroll_check)

        top_controls.addStretch()
        self.main_layout.addLayout(top_controls)

        # Search bar
        self.search_transcript = QLineEdit()
        self.search_transcript.setPlaceholderText("⌕ Search transcript...")
        self.main_layout.addWidget(self.search_transcript)

        # Transcript display (main area)
        self.transcript_display = QTextBrowser()
        self.transcript_display.setObjectName("transcriptDisplay")
        self.transcript_display.setOpenExternalLinks(False)
        self.main_layout.addWidget(self.transcript_display)

        # HTML template for transcript styling (light theme compatible)
        self.transcript_html_template = """
        <style>
            body { 
                color: #212529; 
                background-color: #ffffff;
                font-family: Arial, sans-serif; 
                line-height: 1.6; 
                margin: 0;
                padding: 10px;
            }
            .transcript-line { 
                padding: 8px 12px; 
                margin: 4px 0; 
                border-radius: 5px; 
                cursor: pointer;
                transition: background-color 0.2s;
                color: #212529;
            }
            .transcript-line:hover { 
                background-color: #f8f9fa; 
                border: 1px solid #dee2e6;
            }
            .time { 
                color: #0d6efd; 
                font-weight: bold; 
                margin-right: 10px;
                font-size: 12px;
            }
            .current { 
                background-color: #cff4fc;
                border-left: 3px solid #0d6efd;
            }
            .highlight {
                background-color: #fff3cd;
                color: #856404;
                padding: 0 2px;
                border-radius: 2px;
            }
        </style>
        """

    def _connect_signals(self):
        """Connect internal signals."""
        if PYSIDE6_AVAILABLE:
            self.fetch_transcript_button.clicked.connect(self._request_transcript_fetch)
            self.search_transcript.textChanged.connect(self._on_search_text_changed)
            self.transcript_display.anchorClicked.connect(self._on_transcript_clicked)

            # Setup search timer for delayed search
            if self.search_timer:
                self.search_timer.timeout.connect(self._perform_search)
                self.search_timer.setSingleShot(True)

    def _request_transcript_fetch(self):
        """Request transcript fetch from parent."""
        self.transcript_fetch_requested.emit()

    def _on_search_text_changed(self, text: str):
        """Handle search text changes with delay."""
        if self.search_timer:
            self.search_timer.stop()
            self.search_timer.start(300)  # 300ms delay
        else:
            self._perform_search()

    def _perform_search(self):
        """Perform the actual search."""
        search_term = self.search_transcript.text() if PYSIDE6_AVAILABLE else ""
        self.search_in_transcript(search_term)

    def _on_transcript_clicked(self, url):
        """Handle clicks on transcript entries."""
        url_str = url.toString() if hasattr(url, "toString") else str(url)
        if url_str.startswith("#seek:"):
            try:
                timestamp = float(url_str.split(":", 1)[1])
                self.transcript_seek_requested.emit(timestamp)
            except (ValueError, IndexError):
                pass

    def set_transcript_data(self, data: List[Dict[str, Any]]):
        """
        Set transcript data.

        Args:
            data: List of transcript entries with 'start', 'text' keys
        """
        self.transcript_data = data
        self.display_transcript()
        self.fetch_transcript_button.setEnabled(bool(data))

    def display_transcript(self, search_term: str = ""):
        """
        Display transcript with optional search highlighting.

        Args:
            search_term: Term to highlight in transcript
        """
        html = self.transcript_html_template + "<body>"

        for i, entry in enumerate(self.transcript_data):
            time = format_time(int(entry.get("start", 0)))
            text = entry.get("text", "")

            # Highlight search term if provided
            if search_term and search_term.lower() in text.lower():
                pattern = re.compile(re.escape(search_term), re.IGNORECASE)
                text = pattern.sub(
                    lambda m: f'<span class="highlight">{m.group()}</span>', text
                )

            # Add current line highlighting
            line_class = "transcript-line"
            start_time = entry.get("start", 0)
            if self._is_current_line(start_time):
                line_class += " current"

            # Create clickable transcript line
            html += f"""
            <div class="{line_class}" id="line_{i}" onclick="window.location='#seek:{start_time}'">
                <span class="time">[{time}]</span>
                <span class="text">{text}</span>
            </div>
            """

        html += "</body>"
        self.transcript_display.setHtml(html)

    def _is_current_line(self, start_time: float) -> bool:
        """
        Check if a transcript line is currently playing.

        Args:
            start_time: Start time of the transcript line

        Returns:
            True if this line should be highlighted as current
        """
        # Simple logic - could be enhanced based on next line's start time
        return abs(self.current_position - start_time) < 2.0  # Within 2 seconds

    def search_in_transcript(self, text: str):
        """
        Search within transcript.

        Args:
            text: Search term
        """
        if self.transcript_data:
            self.display_transcript(text)

    def update_current_position(self, position: float):
        """
        Update current playback position for auto-scroll.

        Args:
            position: Current position in seconds
        """
        self.current_position = position

        # Update display if auto-scroll is enabled
        if self.auto_scroll_check.isChecked():
            self.display_transcript(self.search_transcript.text())

    def clear(self):
        """Clear tab contents."""
        self.transcript_data.clear()
        self.transcript_display.setHtml("")
        self.search_transcript.clear()
        self.current_position = 0.0
        self.fetch_transcript_button.setEnabled(False)

    def handle_video_loaded(self, video_info=None):
        """
        Update tab when a video is loaded.

        Args:
            video_info: Video information dictionary
        """
        self.clear()
        if video_info:
            self.fetch_transcript_button.setEnabled(True)

    def handle_playback_state_changed(self, is_playing, is_paused):
        """
        Handle playback state changes.

        Args:
            is_playing: Whether media is loaded/playing
            is_paused: Whether playback is paused
        """
        # Could add visual indicators for playback state
        pass

    def get_transcript_text(self) -> str:
        """
        Get full transcript as plain text.

        Returns:
            Complete transcript text
        """
        if not self.transcript_data:
            return ""

        text_parts = []
        for entry in self.transcript_data:
            timestamp = format_time(int(entry.get("start", 0)))
            text = entry.get("text", "")
            text_parts.append(f"[{timestamp}] {text}")

        return "\n".join(text_parts)

    def export_transcript(self, filename: str):
        """
        Export transcript to file.

        Args:
            filename: Target file path
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.get_transcript_text())
        except Exception as e:
            print(f"Failed to export transcript: {e}")

    def on_tab_activated(self):
        """Called when tab is activated."""
        super().on_tab_activated()
        # Refresh display when tab becomes active
        if self.transcript_data:
            self.display_transcript(self.search_transcript.text())
