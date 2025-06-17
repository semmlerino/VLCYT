"""
Main application window for VLCYT.

This module contains the ModernYouTubePlayer class which is the main window
of the application.
"""

# Try to import Qt for UI
try:
    from PySide6.QtCore import QSettings, Qt, QTimer
    from PySide6.QtGui import QKeySequence, QShortcut
    from PySide6.QtWidgets import (
        QMainWindow,
        QMessageBox,
        QVBoxLayout,
        QWidget,
    )

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False
    print("PySide6 not available - running in test mode")

    # Create dummy classes for testing
    class QMainWindow:
        def __init__(self):
            pass

        def setWindowTitle(self, title):
            pass

        def resize(self, width, height):
            pass

        def setCentralWidget(self, widget):
            pass

        def statusBar(self):
            return DummyStatusBar()

        def restoreGeometry(self, geometry):
            pass

        def saveGeometry(self):
            return b""

        def show(self):
            pass

        def setStyleSheet(self, style):
            pass

    class QSettings:
        def __init__(self, *args):
            self._data = {}

        def contains(self, key):
            return key in self._data

        def setValue(self, key, value):
            self._data[key] = value

        def value(self, key, default=None):
            return self._data.get(key, default)

    class QTimer:
        def __init__(self):
            self.timeout = DummySignal()

        def start(self, ms):
            pass

        def stop(self):
            pass

        @staticmethod
        def singleShot(ms, func):
            pass

    class DummyStatusBar:
        def addWidget(self, widget):
            pass

        def addPermanentWidget(self, widget):
            pass

    class DummySignal:
        def connect(self, func):
            pass

    class QMessageBox:
        @staticmethod
        def warning(*args):
            pass

        @staticmethod
        def critical(*args):
            pass

        @staticmethod
        def information(*args):
            pass

    class QWidget:
        def __init__(self, parent=None):
            pass

        def setObjectName(self, name):
            pass

        def setMaximumHeight(self, height):
            pass

        def setMinimumHeight(self, height):
            pass

        def setFixedHeight(self, height):
            pass

        def setAttribute(self, attr):
            pass

        def setParent(self, parent):
            pass

        def showFullScreen(self):
            pass

        def showNormal(self):
            pass

        def setFocus(self):
            pass

        def winId(self):
            return 12345

        def setSizePolicy(self, horizontal, vertical):
            pass

    class QVBoxLayout:
        def __init__(self, parent=None):
            pass

        def setSpacing(self, spacing):
            pass

        def setContentsMargins(self, *args):
            pass

        def addWidget(self, widget):
            pass

        def addLayout(self, layout):
            pass

    class QHBoxLayout:
        def __init__(self, parent=None):
            pass

        def setSpacing(self, spacing):
            pass

        def setContentsMargins(self, *args):
            pass

        def addWidget(self, widget):
            pass

        def addStretch(self):
            pass

    class QTabWidget:
        def __init__(self, parent=None):
            pass

        def addTab(self, widget, title):
            pass

    class QLineEdit:
        def __init__(self, parent=None):
            self.returnPressed = DummySignal()

        def setObjectName(self, name):
            pass

        def setPlaceholderText(self, text):
            pass

        def setMinimumWidth(self, width):
            pass

        def text(self):
            return ""

        def setText(self, text):
            pass

        def clear(self):
            pass

    class QComboBox:
        def __init__(self, parent=None):
            pass

        def setObjectName(self, name):
            pass

        def addItems(self, items):
            pass

        def setCurrentText(self, text):
            pass

        def currentText(self):
            return "720p"

        def setMaximumWidth(self, width):
            pass

        def setToolTip(self, tip):
            pass

    class QLabel:
        def __init__(self, text="", parent=None):
            pass

        def setObjectName(self, name):
            pass

        def setText(self, text):
            pass

    class QProgressBar:
        def __init__(self, parent=None):
            pass

        def setVisible(self, visible):
            pass

        def setMaximumWidth(self, width):
            pass

        def setRange(self, min_val, max_val):
            pass

    class Qt:
        WA_DontCreateNativeAncestors = 0
        WA_NativeWindow = 1

    class QShortcut:
        def __init__(self, key, parent):
            self.activated = DummySignal()

    class QKeySequence:
        @staticmethod
        def __call__(key):
            return key

    class QSizePolicy:
        Expanding = 0
        Fixed = 1


# Local imports - use relative imports in refactored structure
from ..constants import (
    DEFAULT_VOLUME,
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
    POSITION_UPDATE_INTERVAL_MS,
    STANDARD_SPACING,
)
from ..core.vlc_player import VLCPlayer
from ..managers.playback_manager import PlaybackManager
from ..managers.thread_manager import ThreadManager
from ..utils.format_utils import format_time


class ModernYouTubePlayer(QMainWindow):
    """
    Modern YouTube Player main window.

    A Qt-based YouTube video player with VLC backend that supports:
    - Video playback from YouTube URLs
    - Audio streaming to network devices
    - Playlist management
    - Video transcript viewing and searching
    - History tracking
    """

    def __init__(self):
        """Initialize the main application window."""
        super().__init__()

        # Initialize logging system first
        from ..utils.logging_config import get_logger, initialize_logging

        self.log_manager = initialize_logging("VLCYT")
        self.logger = get_logger("vlcyt.main")
        self.logger.info("Starting Modern YouTube Player application")

        # Core components initialization
        self.qsettings = QSettings("ModernYouTubePlayer", "Settings")
        self.vlc_player = VLCPlayer()
        self.thread_manager = ThreadManager(max_threads=8)

        # Initialize managers
        from ..managers.settings_manager import SettingsManager
        from ..managers.transcript_manager import TranscriptManager
        from ..managers.streaming_manager import StreamingManager

        self.settings_manager = SettingsManager(self.qsettings)
        self.playback_manager = PlaybackManager(self.vlc_player, self.thread_manager)
        self.transcript_manager = TranscriptManager(self.thread_manager)
        self.streaming_manager = StreamingManager(self.vlc_player)

        # Initialize position timer for progress bar updates
        self.position_timer = QTimer()
        self.position_timer.timeout.connect(self.update_position)

        # UI state
        self.is_muted = False
        self.volume_before_mute = DEFAULT_VOLUME
        self.current_playlist_index = -1

        # Current video info and state
        self.current_video_info = None
        self.current_url = None

        # UI components (will be initialized in setup_ui)
        self.toolbar = None
        self.player_widget = None
        self.tab_container = None
        self.status_bar_widget = None

        # Check if streaming was disabled due to initialization issues
        if hasattr(self.vlc_player, "_streaming_disabled_on_init"):
            self.logger.warning("Streaming was disabled during VLC initialization")
            QMessageBox.warning(
                self,
                "Streaming Disabled",
                "Audio streaming was disabled during VLC initialization.\n"
                "You can try enabling it again from the video controls.",
            )

        # Setup UI and connections
        self.setup_ui()
        self.apply_theme()
        self.setup_shortcuts()
        self.setup_manager_connections()  # After UI components are created

        # Load settings and show welcome
        self.load_settings()
        self.load_playlists()

        # Update history tab with loaded data
        self.update_history_tab()
        self.status_bar_widget.update_status("Welcome to Modern YouTube Player")

    def apply_theme(self):
        """Apply light theme to the application."""
        from .theme import ThemeManager

        theme_manager = ThemeManager()
        theme_manager.apply_theme(self)

    def setup_ui(self):
        """Setup the modern user interface using extracted components."""
        # Set window properties
        self.setWindowTitle("Modern YouTube Player")
        self.resize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(STANDARD_SPACING)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create UI components using extracted classes
        self._create_toolbar(main_layout)
        self._create_player_widget(main_layout)
        self._create_status_bar()
        self._create_tab_container(main_layout)

        # Setup video player embedding
        self.setup_vlc_embedding()

        # Connect component signals
        self._connect_component_signals()

    def _connect_component_signals(self):
        """Connect signals from extracted components."""
        if not PYSIDE6_AVAILABLE:
            return

        # Toolbar signals - check existence
        if hasattr(self, "toolbar") and self.toolbar:
            self.toolbar.play_requested.connect(self._on_toolbar_play_requested)
            self.toolbar.quick_add_requested.connect(self.quick_add_to_playlist)
            self.toolbar.settings_requested.connect(self.show_settings)

        # Video controls signals - check existence
        if hasattr(self, "video_controls") and self.video_controls:
            self.video_controls.volume_changed.connect(self.change_volume)
            self.video_controls.progress_pressed.connect(self.on_progress_pressed)
            self.video_controls.progress_released.connect(self.on_progress_released)
            self.video_controls.progress_moved.connect(self.on_progress_moved)
            if hasattr(self.video_controls, "stream_button"):
                self.video_controls.stream_button.clicked.connect(self.toggle_streaming)
            if hasattr(self.video_controls, "mute_button"):
                self.video_controls.mute_button.clicked.connect(self.toggle_mute)

    def _on_toolbar_play_requested(self, url, quality):
        """Handle play request from toolbar."""
        # Update internal state from toolbar
        self.current_url = url
        self.play_video_thread()

    def update_position(self):
        """Update position display based on current playback position."""
        if not self.playback_manager.is_playing():
            return

        position = self.playback_manager.get_position()
        length = self.playback_manager.get_length()
        time = self.playback_manager.get_time()

        if length > 0:
            position_value = int(position * 1000)
            self.video_controls.progress_slider.setValue(position_value)

            self.video_controls.current_time_label.setText(format_time(time // 1000))
            self.video_controls.total_time_label.setText(format_time(length // 1000))

            # Auto-scroll transcript if enabled
            if (
                self.transcript_tab.auto_scroll_check.isChecked()
                and self.transcript_manager.get_current_transcript_data()
            ):
                self.sync_transcript_to_time(time // 1000)

    def _create_toolbar(self, main_layout):
        """Create toolbar using extracted Toolbar component."""
        from .components.toolbar import Toolbar

        self.toolbar = Toolbar(self)
        main_layout.addWidget(self.toolbar)

    def _create_player_widget(self, main_layout):
        """Create player widget using extracted PlayerWidget component."""
        from .components.player_widget import PlayerWidget

        self.player_widget = PlayerWidget(self)
        main_layout.addWidget(self.player_widget, 2)

        # Get references to nested components for compatibility
        self.video_frame = self.player_widget.get_video_frame()
        self.video_controls = self.player_widget.get_video_controls()

        # Connect video controls callbacks
        self.video_controls.set_callbacks(
            play_pause_callback=self.toggle_play_pause,
            stop_callback=self.stop_video,
            prev_callback=self.previous_video,
            next_callback=self.next_video,
        )

    def _set_video_placeholder_visibility(self, visible: bool):
        """Controls the visibility of the video placeholder.

        Args:
            visible: True to show the placeholder, False to hide it
        """
        if hasattr(self, "player_widget"):
            self.player_widget.set_placeholder_visible(visible)

    def _create_status_bar(self):
        """Create status bar using extracted StatusBarWidget component."""
        from .components.status_bar_widget import StatusBarWidget

        self.status_bar_widget = StatusBarWidget(self.statusBar())

        # Keep references for compatibility
        self.status_label = self.status_bar_widget.status_label
        self.progress_bar = self.status_bar_widget.progress_bar

    def setup_vlc_embedding(self):
        """Setup VLC player embedding in video frame."""
        if self.vlc_player and hasattr(self, "player_widget"):
            success = self.player_widget.setup_vlc_embedding(self.vlc_player)
            if success:
                self.logger.info("VLC player embedded successfully")
            else:
                self.logger.warning("VLC player embedding failed")

    def setup_manager_connections(self):
        """Connect manager signals to UI handlers."""
        try:
            # Playback manager connections
            self.playback_manager.playback_started.connect(self.on_playback_started)
            self.playback_manager.playback_stopped.connect(self.on_playback_stopped)
            self.playback_manager.playback_paused.connect(self.on_playback_paused)
            self.playback_manager.playback_error.connect(self.on_playback_error)
            self.playback_manager.position_changed.connect(self.on_position_changed)
            self.playback_manager.volume_changed.connect(self.on_volume_changed)

            # Transcript manager connections
            self.transcript_manager.transcript_ready.connect(self.on_transcript_ready)
            self.transcript_manager.transcript_error.connect(self.on_transcript_error)

            # Streaming manager connections
            self.streaming_manager.streaming_enabled.connect(self.on_streaming_enabled)
            self.streaming_manager.streaming_disabled.connect(
                self.on_streaming_disabled
            )

            # Tab signal connections - check existence
            if hasattr(self, "playlist_tab") and self.playlist_tab:
                self.playlist_tab.playlist_item_selected.connect(
                    self.play_playlist_item
                )
                self.playlist_tab.playlist_cleared.connect(self.on_playlist_cleared)
            if hasattr(self, "transcript_tab") and self.transcript_tab:
                self.transcript_tab.transcript_fetch_requested.connect(
                    self.fetch_transcript
                )
                self.transcript_tab.transcript_seek_requested.connect(self.seek_to_time)
            if hasattr(self, "history_tab") and self.history_tab:
                self.history_tab.play_from_history_requested.connect(
                    self.play_from_history
                )
                self.history_tab.clear_history_requested.connect(self.clear_history)
        except AttributeError as e:
            self.logger.warning(f"Failed to connect some manager signals: {e}")

    def setup_shortcuts(self):
        """Configure keyboard shortcuts."""
        if PYSIDE6_AVAILABLE:
            # Playback shortcuts
            QShortcut(QKeySequence("Space"), self).activated.connect(
                self.toggle_play_pause
            )
            QShortcut(QKeySequence("Escape"), self).activated.connect(
                self.exit_fullscreen
            )
            QShortcut(QKeySequence("F"), self).activated.connect(
                self.toggle_video_fullscreen
            )
            QShortcut(QKeySequence("M"), self).activated.connect(self.toggle_mute)

            # Seek shortcuts
            QShortcut(QKeySequence("Left"), self).activated.connect(
                lambda: self.seek_relative(-10)
            )
            QShortcut(QKeySequence("Right"), self).activated.connect(
                lambda: self.seek_relative(10)
            )
            QShortcut(QKeySequence("Shift+Left"), self).activated.connect(
                lambda: self.seek_relative(-60)
            )
            QShortcut(QKeySequence("Shift+Right"), self).activated.connect(
                lambda: self.seek_relative(60)
            )

            # Volume shortcuts
            QShortcut(QKeySequence("Up"), self).activated.connect(
                lambda: self.change_volume(
                    self.video_controls.volume_slider.value() + 5
                )
            )
            QShortcut(QKeySequence("Down"), self).activated.connect(
                lambda: self.change_volume(
                    self.video_controls.volume_slider.value() - 5
                )
            )

    def _create_tab_container(self, main_layout):
        """Create tab container using extracted TabContainer component."""
        from .components.tab_container import TabContainer

        self.tab_container = TabContainer(self)
        main_layout.addWidget(self.tab_container, 1)

        # Get references to individual tabs for compatibility
        self.info_tab = self.tab_container.get_info_tab()
        self.playlist_tab = self.tab_container.get_playlist_tab()
        self.transcript_tab = self.tab_container.get_transcript_tab()
        self.history_tab = self.tab_container.get_history_tab()

        # Keep reference to tabs widget for compatibility
        self.tabs = self.tab_container.tabs

    # Core functionality methods
    def play_video_thread(self):
        """Start video playback using the PlaybackManager."""
        from ..exceptions import SecurityError, ValidationError
        from ..validators import URLValidator

        # Get URL from toolbar or use stored URL
        url = getattr(self, "current_url", None) or self.toolbar.get_url()
        if not url:
            return

        self.logger.info(f"Starting video playback: {url}")

        # Show progress
        self.status_bar_widget.start_loading("Loading video...")

        # Validate URL
        try:
            self.current_url = URLValidator.validate_youtube_url(url)
            self.toolbar.set_url(self.current_url)
            self.logger.debug(f"Validated URL: {self.current_url}")
        except (ValidationError, SecurityError) as e:
            self.logger.error(f"URL validation failed: {e}")
            self.on_fetch_error(str(e))
            return

        # Use PlaybackManager for playback
        success = self.playback_manager.play_url(self.current_url)

        if success:
            # Update UI
            self.toolbar.set_play_button_enabled(False)
            if hasattr(self.transcript_tab, "fetch_transcript_button"):
                self.transcript_tab.fetch_transcript_button.setEnabled(True)
        else:
            self.logger.warning("Failed to start video playback")
            self.status_bar_widget.stop_loading("Failed to load video")

    def toggle_play_pause(self):
        """Toggle play/pause state."""
        if self.playback_manager.is_playing():
            if self.playback_manager.is_paused():
                self.playback_manager.resume()
            else:
                self.playback_manager.pause()
        else:
            # If no video is loaded, try to play from URL entry
            if hasattr(self, "current_url") and self.current_url:
                self.playback_manager.play_url(self.current_url)

    def stop_video(self):
        """Stop video playback."""
        self.playback_manager.stop()
        self.position_timer.stop()

    def previous_video(self):
        """Play previous video in playlist."""
        # TODO: Implement playlist navigation
        pass

    def next_video(self):
        """Play next video in playlist."""
        # TODO: Implement playlist navigation
        pass

    def seek_relative(self, seconds):
        """Seek relative to current position."""
        if self.playback_manager.is_playing():
            current_time = self.playback_manager.get_time()
            new_time = max(
                0, current_time + (seconds * 1000)
            )  # Convert to milliseconds
            self.playback_manager.seek_time(new_time // 1000)

    def seek_to_time(self, time_seconds):
        """Seek to specific time."""
        if self.playback_manager.is_playing():
            self.playback_manager.seek_time(int(time_seconds))

    def change_volume(self, volume):
        """Change playback volume."""
        self.playback_manager.set_volume(volume)
        self.video_controls.volume_slider.setValue(volume)

    def toggle_mute(self):
        """Toggle mute state."""
        if self.is_muted:
            self.playback_manager.set_volume(self.volume_before_mute)
            self.is_muted = False
            self.video_controls.mute_button.setText("🔊")
        else:
            self.volume_before_mute = self.playback_manager.get_volume()
            self.playback_manager.set_volume(0)
            self.is_muted = True
            self.video_controls.mute_button.setText("🔇")

    def toggle_streaming(self):
        """Toggle audio streaming."""
        if self.streaming_manager.is_streaming_enabled():
            self.streaming_manager.disable_streaming()
        else:
            port = self.video_controls.stream_port_input.value()
            self.streaming_manager.enable_streaming(port)

    def toggle_video_fullscreen(self):
        """Toggle video fullscreen mode."""
        if self.player_widget.is_fullscreen:
            self.exit_fullscreen()
        else:
            self.enter_video_fullscreen()

    def enter_video_fullscreen(self):
        """Enter fullscreen mode."""
        self.player_widget.enter_fullscreen()

    def exit_fullscreen(self):
        """Exit fullscreen mode."""
        self.player_widget.exit_fullscreen(self.player_widget)

    # Event handlers
    def on_playback_started(self, video_info=None):
        """Handle playback started event."""
        self.logger.info("Playback started")
        self.video_controls.play_pause_button.setText("⏸")
        self.toolbar.set_play_button_enabled(True)
        self.status_bar_widget.stop_loading()

        # Hide video placeholder when playback starts
        self._set_video_placeholder_visibility(False)

        # Start position timer
        self.position_timer.start(POSITION_UPDATE_INTERVAL_MS)

        # Update video info
        if video_info:
            self.current_video_info = video_info
            self.update_video_info(video_info)

        self.update_status("Playing video")

    def on_playback_stopped(self):
        """Handle playback stopped event."""
        self.logger.info("Playback stopped")
        self.video_controls.play_pause_button.setText("▶")
        self.position_timer.stop()

        # Show video placeholder when playback stops
        self._set_video_placeholder_visibility(True)

        self.update_status("Stopped")

    def on_playback_paused(self, is_paused):
        """Handle playback paused/resumed event."""
        if is_paused:
            self.video_controls.play_pause_button.setText("▶")
            self.position_timer.stop()
            self.update_status("Paused")
        else:
            self.video_controls.play_pause_button.setText("⏸")
            self.position_timer.start(POSITION_UPDATE_INTERVAL_MS)
            self.update_status("Playing")

    def on_playback_error(self, error_message):
        """Handle playback error event."""
        self.logger.error(f"Playback error: {error_message}")
        self.on_fetch_error(error_message)

    def on_position_changed(self, position, length):
        """Handle position change event."""
        # This is handled by update_position timer method
        pass

    def on_volume_changed(self, volume):
        """Handle volume change event."""
        self.video_controls.volume_slider.setValue(volume)

    def on_fetch_error(self, error_message):
        """Handle fetch errors with user feedback."""
        self.logger.error(f"Fetch error: {error_message}")

        # Determine error type and provide appropriate feedback
        if "network" in error_message.lower():
            title = "Network Error"
            msg = f"{error_message}\n\nPlease check your internet connection."
        elif "video" in error_message.lower():
            title = "Video Error"
            msg = f"{error_message}\n\nVideo may be private or unavailable."
        else:
            title = "Error"
            msg = error_message

        QMessageBox.critical(self, title, msg)
        self.toolbar.set_play_button_enabled(True)
        self.status_bar_widget.stop_loading("Error occurred")

    def on_transcript_ready(self, transcript_data):
        """Handle transcript ready event."""
        self.transcript_tab.set_transcript_data(transcript_data)
        self.update_status("Transcript loaded")

    def on_transcript_error(self, error_message):
        """Handle transcript error event."""
        self.logger.warning(f"Transcript error: {error_message}")
        self.update_status(f"Transcript error: {error_message}")

    def on_streaming_enabled(self):
        """Handle streaming enabled event."""
        status, message = self.streaming_manager.get_streaming_status()
        self.update_status(f"Streaming enabled: {message}")

    def on_streaming_disabled(self):
        """Handle streaming disabled event."""
        self.update_status("Streaming disabled")

    # Progress bar handlers
    def on_progress_pressed(self):
        """Handle progress bar press."""
        self.position_timer.stop()

    def on_progress_released(self):
        """Handle progress bar release."""
        if self.playback_manager.is_playing():
            self.position_timer.start(POSITION_UPDATE_INTERVAL_MS)

    def on_progress_moved(self, value):
        """Handle progress bar movement."""
        if self.playback_manager.is_playing():
            length = self.playback_manager.get_length()
            if length > 0:
                position = value / 1000.0  # Convert from slider range
                new_time = int(position * length)
                self.playback_manager.set_time(new_time)

    # Utility methods
    def update_video_info(self, video_info):
        """Update video information display."""
        self.info_tab.update_info(video_info)
        self.history_tab.add_to_history(video_info)

    def update_status(self, message):
        """Update status bar message."""
        self.status_bar_widget.update_status(message)
        self.logger.debug(f"Status: {message}")

    # Quick actions
    def quick_add_to_playlist(self):
        """Quick add current URL to playlist."""
        url = self.toolbar.get_url()
        if url and hasattr(self, "current_video_info"):
            from ..models import PlaylistItem

            item = PlaylistItem(
                title=self.current_video_info.get("title", "Unknown"),
                url=url,
                duration=self.current_video_info.get("duration", 0),
            )
            self.playlist_tab.add_item(item)
            self.update_status("Added to playlist")

    def show_settings(self):
        """Show settings dialog."""
        # For now, show a simple message
        QMessageBox.information(
            self,
            "Settings",
            "Settings dialog not yet implemented in refactored version.",
        )

    # Playlist handlers
    def play_playlist_item(self, index):
        """Play item from playlist."""
        item = self.playlist_tab.get_current_item()
        if item:
            self.toolbar.set_url(item.url)
            self.play_video_thread()

    def on_playlist_cleared(self):
        """Handle playlist cleared event."""
        self.update_status("Playlist cleared")

    # History handlers
    def play_from_history(self, video_info):
        """Play video from history."""
        if video_info and video_info.get("url"):
            self.toolbar.set_url(video_info["url"])
            self.play_video_thread()

    def clear_history(self):
        """Clear video history."""
        self.history_tab.clear_history()
        self.update_status("History cleared")

    # Transcript handlers
    def fetch_transcript(self):
        """Fetch transcript for current video."""
        if hasattr(self, "current_url") and self.current_url:
            self.transcript_manager.fetch_transcript(self.current_url)
            self.update_status("Fetching transcript...")

    def sync_transcript_to_time(self, time_seconds):
        """Sync transcript display to current time."""
        self.transcript_tab.update_current_position(time_seconds)

    # Settings management
    def load_settings(self):
        """Load application settings."""
        try:
            # Load window geometry
            geometry = self.settings_manager.get_setting("window_geometry")
            if geometry:
                self.restoreGeometry(geometry)

            # Load other settings
            volume = self.settings_manager.get_setting("volume", DEFAULT_VOLUME)
            self.change_volume(volume)

            self.logger.info("Settings loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load settings: {e}")

    def save_settings(self):
        """Save application settings."""
        try:
            # Save window geometry
            self.settings_manager.set_setting("window_geometry", self.saveGeometry())

            # Save other settings
            if hasattr(self, "video_controls") and hasattr(
                self.video_controls, "volume_slider"
            ):
                volume = self.video_controls.volume_slider.value()
                self.settings_manager.set_setting("volume", volume)

            self.logger.info("Settings saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save settings: {e}")

    def load_playlists(self):
        """Load saved playlists."""
        # Delegated to settings manager
        pass

    def update_history_tab(self):
        """Update history tab with loaded data."""
        # History is managed by the history tab itself
        pass

    def load_url(self, url):
        """Load URL from command line or external source."""
        if url:
            self.toolbar.set_url(url)
            # Auto-play if URL is provided
            QTimer.singleShot(
                1000, self.play_video_thread
            )  # Small delay to ensure UI is ready

    def resizeEvent(self, event):
        """Handle window resize events to maintain proper layout."""
        super().resizeEvent(event)

        # Maintain aspect ratio for video frame if needed
        if hasattr(self, "video_frame") and self.video_frame:
            # Allow video frame to scale naturally with the window
            # The layout system will handle the sizing automatically
            pass

    def closeEvent(self, event):
        """Handle application shutdown."""
        self.logger.info("Application closing")

        # Save settings
        self.save_settings()

        # Stop playback
        if self.playback_manager.is_playing():
            self.playback_manager.stop()

        # Cleanup managers
        self.thread_manager.cancel_all_threads()

        # Accept the close event
        event.accept()
