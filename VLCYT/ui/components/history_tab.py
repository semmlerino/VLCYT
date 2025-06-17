"""
History tab component for VLCYT.

This module contains the HistoryTab class which provides recently played
videos management functionality including history display and playback.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    from PySide6.QtCore import Signal
    from PySide6.QtWidgets import QHBoxLayout, QLabel, QListWidget, QVBoxLayout

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

    class QHBoxLayout:
        def __init__(self, parent=None):
            pass

        def setSpacing(self, spacing):
            pass

        def addWidget(self, widget):
            pass

        def addStretch(self):
            pass

        def addLayout(self, layout):
            pass

    class QLabel:
        def __init__(self, text="", parent=None):
            pass

        def setObjectName(self, name):
            pass

        def setWordWrap(self, enabled):
            pass

        def setStyleSheet(self, style):
            pass

    class QListWidget:
        def __init__(self, parent=None):
            pass

        def setObjectName(self, name):
            pass

        def setAlternatingRowColors(self, enabled):
            pass

        def setSelectionMode(self, mode):
            pass

        def setStyleSheet(self, style):
            pass

        def clear(self):
            pass

        def addItem(self, item):
            pass

        def count(self):
            return 0

        def selectedItems(self):
            return []

        def row(self, item):
            return 0

        def itemSelectionChanged(self):
            return Signal()

        def itemDoubleClicked(self):
            return Signal()

        SingleSelection = 1

    class QVBoxLayout:
        def __init__(self, parent=None):
            pass

        def setSpacing(self, spacing):
            pass

        def addWidget(self, widget):
            pass

        def addLayout(self, layout):
            pass

        def addStretch(self):
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

        def setEnabled(self, enabled):
            pass

        def clicked(self):
            return Signal()


class HistoryTab(BaseTab):
    """
    Recently played videos tab widget.

    Provides functionality for:
    - Displaying recently played videos
    - Playing videos from history
    - Clearing history
    - Resume playback from saved position
    """

    # Signals
    play_from_history_requested = Signal(dict)  # Video info dictionary
    clear_history_requested = Signal()

    def __init__(self, parent=None):
        """
        Initialize history tab.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.recently_played: List[Dict[str, Any]] = []
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Set up the history tab UI."""
        # Header
        header = QLabel("Recently Played Videos")
        header.setObjectName("sectionHeader")
        self.main_layout.addWidget(header)

        # List widget to display recently played videos
        self.history_list = QListWidget()
        self.history_list.setObjectName("historyList")
        self.history_list.setAlternatingRowColors(True)
        self.history_list.setSelectionMode(QListWidget.SingleSelection)
        self.history_list.setStyleSheet(
            """
            QListWidget {
                background-color: #f5f5f5;
                border-radius: 6px;
                border: 1px solid #ddd;
                padding: 2px;
            }
            QListWidget::item {
                border-bottom: 1px solid #eee;
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #e6f2ff;
                color: #000;
            }
        """
        )
        self.main_layout.addWidget(self.history_list)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Play selected button
        self.play_selected_button = ModernButton("Play Selected", "▶", self)
        self.play_selected_button.setObjectName("playSelectedButton")
        self.play_selected_button.setEnabled(False)
        buttons_layout.addWidget(self.play_selected_button)

        # Clear history button
        self.clear_history_button = ModernButton("Clear History", "🗑", self)
        self.clear_history_button.setObjectName("clearHistoryButton")
        buttons_layout.addWidget(self.clear_history_button)

        buttons_layout.addStretch()
        self.main_layout.addLayout(buttons_layout)

        # Description of the feature
        help_text = QLabel(
            "The last 10 played videos are saved here. Click on a video to play it from where you left off."
        )
        help_text.setObjectName("helpText")
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: #666; font-style: italic;")
        self.main_layout.addWidget(help_text)

        self.main_layout.addStretch()

    def _connect_signals(self):
        """Connect internal signals."""
        if PYSIDE6_AVAILABLE:
            self.play_selected_button.clicked.connect(self._play_selected_video)
            self.clear_history_button.clicked.connect(self._clear_history)
            self.history_list.itemSelectionChanged.connect(self._on_selection_changed)
            self.history_list.itemDoubleClicked.connect(self._play_selected_video)

    def _play_selected_video(self):
        """Play the selected video from history."""
        selected_video = self.get_selected_video()
        if selected_video:
            self.play_from_history_requested.emit(selected_video)

    def _clear_history(self):
        """Clear the history."""
        self.clear_history_requested.emit()

    def _on_selection_changed(self):
        """Handle selection changes in history list."""
        has_selection = bool(self.history_list.selectedItems())
        self.play_selected_button.setEnabled(has_selection)

    def update_history(self, recently_played_list: List[Dict[str, Any]]):
        """
        Update the recently played videos list.

        Args:
            recently_played_list: List of video info dictionaries
        """
        self.recently_played = recently_played_list
        self.history_list.clear()

        for video in self.recently_played:
            title = video.get("title", "Unknown Title")
            duration = format_time(video.get("duration", 0))
            last_played = video.get("last_played", "")

            # Format last played date if available
            date_str = ""
            if last_played:
                try:
                    dt = datetime.fromisoformat(last_played)
                    date_str = f" - {dt.strftime('%Y-%m-%d %H:%M')}"
                except (ValueError, TypeError):
                    pass

            # Create display text
            display_text = f"{title} ({duration}){date_str}"

            # Add to list with video data stored
            self.history_list.addItem(display_text)

        # Enable/disable play button based on selection
        self.play_selected_button.setEnabled(self.history_list.count() > 0)

    def get_selected_video(self) -> Optional[Dict[str, Any]]:
        """
        Get the selected video from history.

        Returns:
            Dict containing video info or None if nothing selected
        """
        selected_items = self.history_list.selectedItems()
        if not selected_items:
            return None

        selected_index = self.history_list.row(selected_items[0])
        if 0 <= selected_index < len(self.recently_played):
            return self.recently_played[selected_index]

        return None

    def add_to_history(self, video_info: Dict[str, Any]):
        """
        Add a video to the history.

        Args:
            video_info: Video information dictionary
        """
        # Add current timestamp
        video_info["last_played"] = datetime.now().isoformat()

        # Remove if already exists to avoid duplicates
        existing_index = -1
        for i, video in enumerate(self.recently_played):
            if video.get("url") == video_info.get("url"):
                existing_index = i
                break

        if existing_index >= 0:
            self.recently_played.pop(existing_index)

        # Add to beginning of list
        self.recently_played.insert(0, video_info)

        # Keep only last 10 items
        self.recently_played = self.recently_played[:10]

        # Update display
        self.update_history(self.recently_played)

    def clear_history(self):
        """Clear all history items."""
        self.recently_played.clear()
        self.history_list.clear()
        self.play_selected_button.setEnabled(False)

    def get_history_data(self) -> List[Dict[str, Any]]:
        """
        Get current history data.

        Returns:
            List of video info dictionaries
        """
        return self.recently_played.copy()

    def load_history_data(self, history_data: List[Dict[str, Any]]):
        """
        Load history from external data.

        Args:
            history_data: List of video info dictionaries
        """
        self.recently_played = history_data[:10]  # Keep only last 10
        self.update_history(self.recently_played)

    def clear(self):
        """Clear tab contents."""
        self.clear_history()

    def handle_video_loaded(self, video_info=None):
        """
        Update tab when a video is loaded.

        Args:
            video_info: Video information dictionary
        """
        if video_info:
            self.add_to_history(video_info)

    def get_video_count(self) -> int:
        """
        Get number of videos in history.

        Returns:
            Number of videos in history
        """
        return len(self.recently_played)

    def get_video_at_index(self, index: int) -> Optional[Dict[str, Any]]:
        """
        Get video at specific index.

        Args:
            index: Index of video to get

        Returns:
            Video info dictionary or None
        """
        if 0 <= index < len(self.recently_played):
            return self.recently_played[index]
        return None

    def remove_video_at_index(self, index: int):
        """
        Remove video at specific index.

        Args:
            index: Index of video to remove
        """
        if 0 <= index < len(self.recently_played):
            self.recently_played.pop(index)
            self.update_history(self.recently_played)
