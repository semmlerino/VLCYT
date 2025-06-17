"""
Playlist tab component for VLCYT.

This module contains the PlaylistTab class which provides playlist management
functionality including adding, removing, saving, and loading playlists.
"""

import json
from typing import List, Optional

try:
    from PySide6.QtCore import Signal
    from PySide6.QtWidgets import (
        QFileDialog,
        QHBoxLayout,
        QLineEdit,
        QListWidget,
        QMessageBox,
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

    class QFileDialog:
        @staticmethod
        def getSaveFileName(*args):
            return "", ""

        @staticmethod
        def getOpenFileName(*args):
            return "", ""

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

    class QListWidget:
        def __init__(self, parent=None):
            pass

        def setObjectName(self, name):
            pass

        def addItem(self, item):
            pass

        def clear(self):
            pass

    class QMessageBox:
        @staticmethod
        def warning(*args):
            pass

        @staticmethod
        def critical(*args):
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

# Import models and widgets - these will need to be properly imported
try:
    from ...models import PlaylistItem
    from ...utils.format_utils import format_time
    from ..widgets import ModernButton
except ImportError:
    # Fallback for testing
    class PlaylistItem:
        def __init__(self, title="", duration=0):
            self.title = title
            self.duration = duration

        @staticmethod
        def from_dict(data):
            return PlaylistItem()

        def to_dict(self):
            return {}

    def format_time(seconds):
        return "00:00"

    class ModernButton:
        def __init__(self, text="", icon="", parent=None):
            pass

        def setObjectName(self, name):
            pass

        def setToolTip(self, tip):
            pass

        def setCheckable(self, checkable):
            pass


class PlaylistTab(BaseTab):
    """
    Playlist management tab widget.

    Provides functionality for:
    - Adding videos to playlist
    - Saving/loading playlists
    - Playlist navigation and controls
    - Shuffle and repeat functionality
    """

    # Signals
    playlist_item_selected = Signal(int)  # Index of selected item
    playlist_cleared = Signal()
    playlist_loaded = Signal(list)  # List of PlaylistItem objects

    def __init__(self, parent=None):
        """
        Initialize playlist tab.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.playlist_items: List[PlaylistItem] = []
        self.current_playlist_index = -1
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Set up the playlist tab UI."""
        # File operations (compact row)
        file_layout = QHBoxLayout()
        file_layout.setSpacing(5)

        self.new_playlist_button = ModernButton("", "🆕", self)
        self.new_playlist_button.setObjectName("playlistButton")
        self.new_playlist_button.setToolTip("New playlist")
        file_layout.addWidget(self.new_playlist_button)

        self.save_playlist_button = ModernButton("", "💾", self)
        self.save_playlist_button.setObjectName("playlistButton")
        self.save_playlist_button.setToolTip("Save playlist")
        file_layout.addWidget(self.save_playlist_button)

        self.load_playlist_button = ModernButton("", "📁", self)
        self.load_playlist_button.setObjectName("playlistButton")
        self.load_playlist_button.setToolTip("Load playlist")
        file_layout.addWidget(self.load_playlist_button)

        file_layout.addStretch()

        # Playlist controls (compact)
        self.shuffle_button = ModernButton("", "🔀", self)
        self.shuffle_button.setObjectName("playlistControlButton")
        self.shuffle_button.setToolTip("Shuffle playlist")
        file_layout.addWidget(self.shuffle_button)

        self.repeat_button = ModernButton("", "🔁", self)
        self.repeat_button.setObjectName("playlistControlButton")
        self.repeat_button.setCheckable(True)
        self.repeat_button.setToolTip("Repeat playlist")
        file_layout.addWidget(self.repeat_button)

        self.clear_playlist_button = ModernButton("", "🗑", self)
        self.clear_playlist_button.setObjectName("playlistControlButton")
        self.clear_playlist_button.setToolTip("Clear playlist")
        file_layout.addWidget(self.clear_playlist_button)

        self.main_layout.addLayout(file_layout)

        # URL input for playlist (simplified)
        add_layout = QHBoxLayout()
        add_layout.setSpacing(5)

        self.playlist_url_entry = QLineEdit()
        self.playlist_url_entry.setPlaceholderText("⌁ Add URLs to playlist...")
        add_layout.addWidget(self.playlist_url_entry)

        self.add_to_playlist_button = ModernButton("", "➕", self)
        self.add_to_playlist_button.setToolTip("Add to playlist")
        add_layout.addWidget(self.add_to_playlist_button)

        self.main_layout.addLayout(add_layout)

        # Playlist items (main area)
        self.playlist_widget = QListWidget()
        self.playlist_widget.setObjectName("playlistWidget")
        self.main_layout.addWidget(self.playlist_widget)

    def _connect_signals(self):
        """Connect internal signals."""
        if PYSIDE6_AVAILABLE:
            self.new_playlist_button.clicked.connect(self.clear_playlist)
            self.save_playlist_button.clicked.connect(self.save_playlist)
            self.load_playlist_button.clicked.connect(self.load_playlist)
            self.clear_playlist_button.clicked.connect(self.clear_playlist)
            self.add_to_playlist_button.clicked.connect(self._add_current_url)
            self.playlist_widget.itemDoubleClicked.connect(self._on_item_double_clicked)

    def _add_current_url(self):
        """Add URL from input field to playlist."""
        url = self.playlist_url_entry.text().strip()
        if url:
            # Create a basic playlist item - this would need to be enhanced
            # to actually fetch video info
            item = PlaylistItem(title=f"Video from {url}", duration=0)
            self.add_item(item)
            self.playlist_url_entry.clear()

    def _on_item_double_clicked(self, item):
        """Handle double-click on playlist item."""
        index = self.playlist_widget.row(item)
        if 0 <= index < len(self.playlist_items):
            self.current_playlist_index = index
            self.playlist_item_selected.emit(index)

    def add_item(self, item: PlaylistItem):
        """
        Add item to playlist.

        Args:
            item: PlaylistItem to add
        """
        self.playlist_items.append(item)
        display_text = f"{item.title} ({format_time(item.duration)})"
        self.playlist_widget.addItem(display_text)

    def clear_playlist(self):
        """Clear all playlist items."""
        self.playlist_items.clear()
        self.playlist_widget.clear()
        self.current_playlist_index = -1
        self.playlist_cleared.emit()

    def save_playlist(self):
        """Save playlist to file."""
        if not self.playlist_items:
            QMessageBox.warning(self, "Empty Playlist", "No items to save.")
            return

        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Playlist", "", "Playlist Files (*.json)"
        )
        if filename:
            try:
                playlist_data = [item.to_dict() for item in self.playlist_items]
                with open(filename, "w") as f:
                    json.dump(playlist_data, f, indent=2)
                QMessageBox.information(self, "Success", "Playlist saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save playlist: {e}")

    def load_playlist(self):
        """Load playlist from file."""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Load Playlist", "", "Playlist Files (*.json)"
        )
        if filename:
            try:
                with open(filename, "r") as f:
                    playlist_data = json.load(f)

                self.clear_playlist()
                for item_data in playlist_data:
                    item = PlaylistItem.from_dict(item_data)
                    self.add_item(item)

                self.playlist_loaded.emit(self.playlist_items)
                QMessageBox.information(
                    self, "Success", "Playlist loaded successfully."
                )

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load playlist: {e}")

    def get_current_item(self) -> Optional[PlaylistItem]:
        """
        Get currently selected playlist item.

        Returns:
            Current PlaylistItem or None
        """
        if 0 <= self.current_playlist_index < len(self.playlist_items):
            return self.playlist_items[self.current_playlist_index]
        return None

    def get_next_item(self) -> Optional[PlaylistItem]:
        """
        Get next playlist item.

        Returns:
            Next PlaylistItem or None
        """
        if (
            self.playlist_items
            and self.current_playlist_index < len(self.playlist_items) - 1
        ):
            return self.playlist_items[self.current_playlist_index + 1]
        return None

    def get_previous_item(self) -> Optional[PlaylistItem]:
        """
        Get previous playlist item.

        Returns:
            Previous PlaylistItem or None
        """
        if self.playlist_items and self.current_playlist_index > 0:
            return self.playlist_items[self.current_playlist_index - 1]
        return None

    def set_current_index(self, index: int):
        """
        Set current playlist index.

        Args:
            index: Index to set as current
        """
        if 0 <= index < len(self.playlist_items):
            self.current_playlist_index = index
            # Could add visual indication of current item here

    def clear(self):
        """Clear tab contents."""
        self.clear_playlist()
        self.playlist_url_entry.clear()
