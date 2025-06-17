"""
Settings manager for VLCYT application.

This module contains the SettingsManager class that handles application settings.
"""

from typing import Dict, List

try:
    from PySide6.QtCore import QPoint, QSettings, QSize

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False
    print("PySide6 not available - running in test mode")

    # Mock QSettings for testing
    class QSettings:
        def __init__(self, organization, application):
            self._settings = {}

        def setValue(self, key, value):
            self._settings[key] = value

        def value(self, key, defaultValue=None, type_=None):
            value = self._settings.get(key, defaultValue)
            if type_ is not None and value is not None:
                try:
                    return type_(value)
                except (ValueError, TypeError):
                    return defaultValue
            return value

        def contains(self, key):
            return key in self._settings

        def beginGroup(self, prefix):
            pass

        def endGroup(self):
            pass

        def beginWriteArray(self, prefix):
            pass

        def endArray(self):
            pass

        def setArrayIndex(self, i):
            pass

        def sync(self):
            pass

    class QSize:
        def __init__(self, width, height):
            self.width = width
            self.height = height

    class QPoint:
        def __init__(self, x, y):
            self.x = x
            self.y = y


# Import constants
from ..constants import (
    DEFAULT_VOLUME,
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
    DEFAULT_WINDOW_X,
    DEFAULT_WINDOW_Y,
)


class SettingsManager:
    """
    Manager for application settings.

    This class handles loading, saving, and accessing application settings
    such as window size, position, volume level, playback settings, etc.
    """

    def __init__(self, qsettings: QSettings):
        """
        Initialize settings manager with QSettings instance.

        Args:
            qsettings: Qt settings instance
        """
        self.qsettings = qsettings
        self._initialize_default_settings()

    def _initialize_default_settings(self):
        """Initialize default settings if not already set."""
        # Window settings
        if not self.qsettings.contains("window/size"):
            self.set_window_size(QSize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT))

        if not self.qsettings.contains("window/position"):
            self.set_window_position(QPoint(DEFAULT_WINDOW_X, DEFAULT_WINDOW_Y))

        # Playback settings
        if not self.qsettings.contains("playback/volume"):
            self.set_volume(DEFAULT_VOLUME)

        if not self.qsettings.contains("playback/remember_position"):
            self.set_remember_position(True)

        if not self.qsettings.contains("playback/default_quality"):
            self.set_default_quality("best")

        # UI settings
        if not self.qsettings.contains("ui/start_maximized"):
            self.set_start_maximized(False)

        if not self.qsettings.contains("transcript/auto_scroll"):
            self.set_transcript_auto_scroll(True)

        # Network settings
        if not self.qsettings.contains("network/streaming_enabled"):
            self.set_streaming_enabled(True)

    # Window settings
    def get_window_size(self) -> QSize:
        """
        Get saved window size.

        Returns:
            Window size as QSize object
        """
        size = self.qsettings.value(
            "window/size", QSize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        )
        return size

    def set_window_size(self, size: QSize) -> None:
        """
        Save window size.

        Args:
            size: Window size to save
        """
        self.qsettings.setValue("window/size", size)

    def get_window_position(self) -> QPoint:
        """
        Get saved window position.

        Returns:
            Window position as QPoint object
        """
        position = self.qsettings.value(
            "window/position", QPoint(DEFAULT_WINDOW_X, DEFAULT_WINDOW_Y)
        )
        return position

    def set_window_position(self, position: QPoint) -> None:
        """
        Save window position.

        Args:
            position: Window position to save
        """
        self.qsettings.setValue("window/position", position)

    def get_start_maximized(self) -> bool:
        """
        Check if window should start maximized.

        Returns:
            True if window should start maximized
        """
        return self.qsettings.value("ui/start_maximized", False, bool)

    def set_start_maximized(self, maximized: bool) -> None:
        """
        Set window start maximized setting.

        Args:
            maximized: Whether window should start maximized
        """
        self.qsettings.setValue("ui/start_maximized", maximized)

    # Playback settings
    def get_volume(self) -> int:
        """
        Get saved volume level.

        Returns:
            Volume level (0-100)
        """
        return self.qsettings.value("playback/volume", DEFAULT_VOLUME, int)

    def set_volume(self, volume: int) -> None:
        """
        Save volume level.

        Args:
            volume: Volume level to save (0-100)
        """
        self.qsettings.setValue("playback/volume", max(0, min(100, volume)))

    def get_remember_position(self) -> bool:
        """
        Check if player should remember video position.

        Returns:
            True if player should remember position
        """
        return self.qsettings.value("playback/remember_position", True, bool)

    def set_remember_position(self, remember: bool) -> None:
        """
        Set remember video position setting.

        Args:
            remember: Whether to remember position
        """
        self.qsettings.setValue("playback/remember_position", remember)

    def get_default_quality(self) -> str:
        """
        Get default video quality.

        Returns:
            Default quality setting
        """
        return self.qsettings.value("playback/default_quality", "best", str)

    def set_default_quality(self, quality: str) -> None:
        """
        Set default video quality.

        Args:
            quality: Default quality to use
        """
        self.qsettings.setValue("playback/default_quality", quality)

    # Transcript settings
    def get_transcript_auto_scroll(self) -> bool:
        """
        Check if transcript should auto-scroll during playback.

        Returns:
            True if auto-scroll enabled
        """
        return self.qsettings.value("transcript/auto_scroll", True, bool)

    def set_transcript_auto_scroll(self, auto_scroll: bool) -> None:
        """
        Set transcript auto-scroll setting.

        Args:
            auto_scroll: Whether to auto-scroll transcript
        """
        self.qsettings.setValue("transcript/auto_scroll", auto_scroll)

    # Network settings
    def get_streaming_enabled(self) -> bool:
        """
        Check if audio streaming is enabled.

        Returns:
            True if streaming enabled
        """
        return self.qsettings.value("network/streaming_enabled", True, bool)

    def set_streaming_enabled(self, enabled: bool) -> None:
        """
        Set audio streaming enabled setting.

        Args:
            enabled: Whether streaming is enabled
        """
        self.qsettings.setValue("network/streaming_enabled", enabled)

    # History settings
    def save_video_history(self, history_items: List[Dict[str, str]]) -> None:
        """
        Save video history.

        Args:
            history_items: List of history items with title and URL
        """
        self.qsettings.beginWriteArray("history/videos")

        for i, item in enumerate(history_items):
            self.qsettings.setArrayIndex(i)
            self.qsettings.setValue("title", item.get("title", ""))
            self.qsettings.setValue("url", item.get("url", ""))

        self.qsettings.endArray()
        self.qsettings.sync()

    def load_video_history(self) -> List[Dict[str, str]]:
        """
        Load video history.

        Returns:
            List of history items with title and URL
        """
        history_items = []
        history_count = self.qsettings.beginReadArray("history/videos")

        for i in range(history_count):
            self.qsettings.setArrayIndex(i)
            title = self.qsettings.value("title", "")
            url = self.qsettings.value("url", "")

            if url:  # Only add items with a valid URL
                history_items.append({"title": title, "url": url})

        self.qsettings.endArray()
        return history_items

    def add_video_to_history(self, title: str, url: str) -> None:
        """
        Add a video to history.

        This method loads the current history, adds the new item,
        removes duplicates, limits history size, and saves it back.

        Args:
            title: Video title
            url: Video URL
        """
        # Load current history
        history_items = self.load_video_history()

        # Create new item
        new_item = {"title": title, "url": url}

        # Remove existing entries with same URL to avoid duplicates
        history_items = [item for item in history_items if item.get("url") != url]

        # Add new item at the beginning
        history_items.insert(0, new_item)

        # Limit history size to 100 items
        history_items = history_items[:100]

        # Save updated history
        self.save_video_history(history_items)

    # Playlists
    def save_playlists(self, playlists: Dict[str, List[Dict[str, str]]]) -> None:
        """
        Save playlists.

        Args:
            playlists: Dictionary with playlist name as key and list of items as value
        """
        # First, remove all existing playlists
        self.qsettings.beginGroup("playlists")
        self.qsettings.remove("")  # Remove all keys in this group
        self.qsettings.endGroup()

        # Now save the playlists
        for playlist_name, playlist_items in playlists.items():
            array_name = f"playlists/{playlist_name}"
            self.qsettings.beginWriteArray(array_name)

            for i, item in enumerate(playlist_items):
                self.qsettings.setArrayIndex(i)
                self.qsettings.setValue("title", item.get("title", ""))
                self.qsettings.setValue("url", item.get("url", ""))

            self.qsettings.endArray()

        self.qsettings.sync()

    def load_playlists(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Load all playlists.

        Returns:
            Dictionary with playlist name as key and list of items as value
        """
        playlists = {}

        # Get all keys in the playlists group to find playlist names
        self.qsettings.beginGroup("playlists")
        playlist_names = self.qsettings.childGroups()
        self.qsettings.endGroup()

        # Load each playlist
        for name in playlist_names:
            array_name = f"playlists/{name}"
            item_count = self.qsettings.beginReadArray(array_name)

            playlist_items = []
            for i in range(item_count):
                self.qsettings.setArrayIndex(i)
                title = self.qsettings.value("title", "")
                url = self.qsettings.value("url", "")

                if url:  # Only add items with a valid URL
                    playlist_items.append({"title": title, "url": url})

            self.qsettings.endArray()

            if playlist_items:  # Only add playlists with items
                playlists[name] = playlist_items

        return playlists

    def save_video_positions(self, positions: Dict[str, int]) -> None:
        """
        Save video positions.

        Args:
            positions: Dictionary with video URL as key and position in seconds as value
        """
        self.qsettings.beginGroup("video_positions")

        for url, position in positions.items():
            # Use URL hash as key to avoid issues with special characters
            url_key = str(hash(url))
            self.qsettings.setValue(url_key, position)

        self.qsettings.endGroup()
        self.qsettings.sync()

    def load_video_positions(self) -> Dict[str, int]:
        """
        Load saved video positions.

        Returns:
            Dictionary with video URL as key and position in seconds as value
        """
        positions = {}

        # We need to maintain a mapping from hash to original URL
        url_to_hash_map = self.load_url_hash_map()

        self.qsettings.beginGroup("video_positions")
        url_keys = self.qsettings.childKeys()

        for url_key in url_keys:
            position = self.qsettings.value(url_key, 0, int)

            # Find original URL from hash
            original_url = None
            for url, url_hash in url_to_hash_map.items():
                if url_hash == url_key:
                    original_url = url
                    break

            if original_url:
                positions[original_url] = position

        self.qsettings.endGroup()
        return positions

    def save_url_hash_map(self, url_map: Dict[str, str]) -> None:
        """
        Save URL to hash map for video positions.

        Args:
            url_map: Dictionary with URL as key and hash as value
        """
        self.qsettings.beginWriteArray("url_hash_map")

        i = 0
        for url, url_hash in url_map.items():
            self.qsettings.setArrayIndex(i)
            self.qsettings.setValue("url", url)
            self.qsettings.setValue("hash", url_hash)
            i += 1

        self.qsettings.endArray()
        self.qsettings.sync()

    def load_url_hash_map(self) -> Dict[str, str]:
        """
        Load URL to hash map for video positions.

        Returns:
            Dictionary with URL as key and hash as value
        """
        url_map = {}

        count = self.qsettings.beginReadArray("url_hash_map")

        for i in range(count):
            self.qsettings.setArrayIndex(i)
            url = self.qsettings.value("url", "")
            url_hash = self.qsettings.value("hash", "")

            if url and url_hash:
                url_map[url] = url_hash

        self.qsettings.endArray()
        return url_map

    def update_video_position(self, url: str, position: int) -> None:
        """
        Update position for a specific video.

        Args:
            url: Video URL
            position: Position in seconds
        """
        if not self.get_remember_position():
            return

        # Use URL hash as key to avoid issues with special characters
        url_hash = str(hash(url))

        # Update hash map
        url_map = self.load_url_hash_map()
        url_map[url] = url_hash
        self.save_url_hash_map(url_map)

        # Update position
        self.qsettings.beginGroup("video_positions")
        self.qsettings.setValue(url_hash, position)
        self.qsettings.endGroup()
        self.qsettings.sync()

    def get_video_position(self, url: str) -> int:
        """
        Get saved position for a specific video.

        Args:
            url: Video URL

        Returns:
            Position in seconds, 0 if not found
        """
        if not self.get_remember_position():
            return 0

        # Use URL hash as key
        url_hash = str(hash(url))

        self.qsettings.beginGroup("video_positions")
        position = self.qsettings.value(url_hash, 0, int)
        self.qsettings.endGroup()

        return position

    # Generic settings methods
    def get_setting(self, key: str, default=None):
        """
        Get a setting value by key.

        Args:
            key: Setting key
            default: Default value if key doesn't exist

        Returns:
            Setting value or default
        """
        return self.qsettings.value(key, default)

    def set_setting(self, key: str, value) -> None:
        """
        Set a setting value by key.

        Args:
            key: Setting key
            value: Value to set
        """
        self.qsettings.setValue(key, value)
