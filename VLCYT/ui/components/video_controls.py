"""
Video controls component for VLCYT.

This module contains the VideoControls class that manages video playback controls.
"""

from typing import Callable, Optional

# Try to import Qt for UI
try:
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtWidgets import (
        QComboBox,
        QHBoxLayout,
        QLabel,
        QProgressBar,
        QPushButton,
        QSizePolicy,
        QSlider,
        QSpinBox,
        QVBoxLayout,
        QWidget,
    )

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False
    print("PySide6 not available - running in test mode")

    # Create dummy classes for testing
    class QWidget:
        def __init__(self, parent=None):
            pass

        def setFixedHeight(self, height):
            pass

        def setObjectName(self, name):
            pass

        def setLayout(self, layout):
            pass

    class QHBoxLayout:
        def __init__(self, parent=None):
            pass

        def addWidget(self, widget, stretch=0):
            pass

        def addStretch(self, stretch=0):
            pass

        def addLayout(self, layout):
            pass

        def setContentsMargins(self, *args):
            pass

        def setSpacing(self, spacing):
            pass

    class QVBoxLayout(QHBoxLayout):
        pass

    class QPushButton:
        def __init__(self, text="", parent=None):
            pass

        def clicked(self):
            return DummySignal()

        def setIcon(self, icon):
            pass

        def setEnabled(self, enabled):
            pass

        def setCheckable(self, checkable):
            pass

        def setFixedWidth(self, width):
            pass

        def setFixedHeight(self, height):
            pass

        def setText(self, text):
            pass

    class QSlider:
        def __init__(self, orientation, parent=None):
            pass

        def setValue(self, value):
            pass

        def value(self):
            return 0

        def setMaximum(self, maximum):
            pass

        def sliderPressed(self):
            return DummySignal()

        def sliderReleased(self):
            return DummySignal()

        def sliderMoved(self):
            return DummySignal()

        def setEnabled(self, enabled):
            pass

    class QLabel:
        def __init__(self, text="", parent=None):
            pass

        def setText(self, text):
            pass

        def setAlignment(self, alignment):
            pass

    class QComboBox:
        def __init__(self, parent=None):
            pass

        def addItems(self, items):
            pass

        def currentText(self):
            return ""

        def setCurrentText(self, text):
            pass

        def currentIndexChanged(self):
            return DummySignal()

        def clear(self):
            pass

    class QProgressBar:
        def __init__(self, parent=None):
            pass

        def setValue(self, value):
            pass

        def setMaximum(self, maximum):
            pass

        def value(self):
            return 0

        def setTextVisible(self, visible):
            pass

    class QSizePolicy:
        Expanding = 0
        Fixed = 0
        Preferred = 0

        def __init__(self, horizontal, vertical):
            pass

    class Qt:
        Horizontal = 0
        AlignCenter = 0

    class Signal:
        def __init__(self, *args):
            pass

        def connect(self, func):
            pass

        def emit(self, *args):
            pass

    class DummySignal:
        def connect(self, func):
            pass

    class QSpinBox:
        def __init__(self, parent=None):
            pass

        def setMinimum(self, minimum):
            pass

        def setMaximum(self, maximum):
            pass

        def setValue(self, value):
            pass

        def value(self):
            return 8080

        def setFixedWidth(self, width):
            pass


# Import constants
from ...constants import (
    CONTROL_BUTTON_SIZE,
    DEFAULT_VOLUME,
    GROUP_SPACING,
    INPUT_HEIGHT,
    PROGRESS_BAR_MAX,
    QUALITY_COMBO_WIDTH,
    QUALITY_LABEL_WIDTH,
    STANDARD_MARGIN,
    STANDARD_SPACING,
    STREAM_LABEL_WIDTH,
    STREAM_PORT_WIDTH,
    TIME_LABEL_WIDTH,
    VIDEO_CONTROLS_HEIGHT,
    VOLUME_ICON_WIDTH,
    VOLUME_SLIDER_MAX,
    VOLUME_SLIDER_WIDTH,
)

# Import utility functions


class VideoControls(QWidget):
    """
    Video playback controls component.

    This widget provides controls for video playback, including play/pause,
    seek, volume, and quality settings.
    """

    # Define custom signals if Qt is available
    if PYSIDE6_AVAILABLE:
        progress_pressed = Signal()
        progress_released = Signal()
        progress_moved = Signal(int)
        volume_changed = Signal(int)
        quality_changed = Signal(str)

    def __init__(self, parent=None):
        """
        Initialize video controls.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # State tracking
        self._current_quality = "best"
        self._progress_pressed = False

        # Create UI
        self._init_ui()

    def _init_ui(self):
        """Initialize the user interface."""
        # Set minimum height for the controls, allow flexible sizing
        self.setMinimumHeight(VIDEO_CONTROLS_HEIGHT)
        self.setObjectName("videoControlsContainer")
        if PYSIDE6_AVAILABLE:
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Create main layout - single row for better organization
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(STANDARD_MARGIN * 2, STANDARD_MARGIN, STANDARD_MARGIN * 2, STANDARD_MARGIN)
        main_layout.setSpacing(GROUP_SPACING)

        # Create playback buttons group
        playback_group = QWidget()
        playback_group.setObjectName("playbackGroup")
        playback_layout = QHBoxLayout(playback_group)
        playback_layout.setContentsMargins(0, 0, 0, 0)
        playback_layout.setSpacing(STANDARD_SPACING)

        self.prev_button = QPushButton("⏮")
        self.play_pause_button = QPushButton("▶")
        self.stop_button = QPushButton("⏹")
        self.next_button = QPushButton("⏭")

        # Set consistent button styling
        control_buttons = [
            self.prev_button,
            self.play_pause_button,
            self.stop_button,
            self.next_button,
        ]

        for button in control_buttons:
            button.setFixedWidth(CONTROL_BUTTON_SIZE)
            button.setFixedHeight(CONTROL_BUTTON_SIZE)
            button.setObjectName("controlButton")

        # Add buttons to playback group
        playback_layout.addWidget(self.prev_button)
        playback_layout.addWidget(self.play_pause_button)
        playback_layout.addWidget(self.stop_button)
        playback_layout.addWidget(self.next_button)

        main_layout.addWidget(playback_group)
        
        # Add stretch between playback and progress groups
        main_layout.addStretch()

        # Progress section with time labels and slider
        progress_group = QWidget()
        progress_group.setObjectName("progressGroup")
        progress_layout = QHBoxLayout(progress_group)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.setSpacing(GROUP_SPACING)

        # Current time label
        self.current_time_label = QLabel("00:00")
        self.current_time_label.setObjectName("timeLabel")
        self.current_time_label.setAlignment(Qt.AlignCenter)
        self.current_time_label.setFixedWidth(TIME_LABEL_WIDTH)
        progress_layout.addWidget(self.current_time_label)

        # Progress slider (for seeking)
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setObjectName("progressSlider")
        self.progress_slider.setMaximum(PROGRESS_BAR_MAX)
        self.progress_slider.setValue(0)
        self.progress_slider.setMinimumHeight(24)
        progress_layout.addWidget(self.progress_slider, 1)

        # Total time label
        self.total_time_label = QLabel("00:00")
        self.total_time_label.setObjectName("timeLabel")
        self.total_time_label.setAlignment(Qt.AlignCenter)
        self.total_time_label.setFixedWidth(TIME_LABEL_WIDTH)
        progress_layout.addWidget(self.total_time_label)

        main_layout.addWidget(progress_group, 2)  # Give progress section more space
        
        # Add stretch between progress and volume groups
        main_layout.addStretch()

        # Volume control group
        volume_group = QWidget()
        volume_group.setObjectName("volumeGroup")
        volume_layout = QHBoxLayout(volume_group)
        volume_layout.setContentsMargins(0, 0, 0, 0)
        volume_layout.setSpacing(STANDARD_SPACING)

        # Mute button (placed before slider)
        self.mute_button = QPushButton("🔊")
        self.mute_button.setObjectName("muteButton")
        self.mute_button.setFixedWidth(CONTROL_BUTTON_SIZE)
        self.mute_button.setFixedHeight(CONTROL_BUTTON_SIZE)
        volume_layout.addWidget(self.mute_button)

        # Volume slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setObjectName("volumeSlider")
        self.volume_slider.setMaximum(VOLUME_SLIDER_MAX)
        self.volume_slider.setValue(DEFAULT_VOLUME)
        self.volume_slider.setFixedWidth(VOLUME_SLIDER_WIDTH)
        self.volume_slider.setMinimumHeight(24)
        volume_layout.addWidget(self.volume_slider)

        # Volume label (shows current volume)
        self.volume_label = QLabel("🔊")
        self.volume_label.setObjectName("volumeIcon")
        self.volume_label.setFixedWidth(VOLUME_ICON_WIDTH)
        self.volume_label.setAlignment(Qt.AlignCenter)
        volume_layout.addWidget(self.volume_label)

        main_layout.addWidget(volume_group)
        
        # Add stretch between volume and settings groups
        main_layout.addStretch()

        # Settings and streaming group
        settings_group = QWidget()
        settings_group.setObjectName("settingsGroup")
        settings_layout = QHBoxLayout(settings_group)
        settings_layout.setContentsMargins(0, 0, 0, 0)
        settings_layout.setSpacing(GROUP_SPACING)

        # Quality dropdown with label
        quality_container = QWidget()
        quality_layout = QHBoxLayout(quality_container)
        quality_layout.setContentsMargins(0, 0, 0, 0)
        quality_layout.setSpacing(6)

        quality_label = QLabel("Quality:")
        quality_label.setObjectName("settingLabel")
        quality_label.setFixedWidth(QUALITY_LABEL_WIDTH)
        quality_layout.addWidget(quality_label)

        self.quality_combo = QComboBox()
        self.quality_combo.setObjectName("qualityCombo")
        self.quality_combo.addItems(["best", "720p", "480p", "360p", "audio"])
        self.quality_combo.setCurrentText("best")
        self.quality_combo.setFixedWidth(QUALITY_COMBO_WIDTH)
        self.quality_combo.setFixedHeight(INPUT_HEIGHT)
        quality_layout.addWidget(self.quality_combo)

        settings_layout.addWidget(quality_container)

        # Streaming controls with label
        stream_container = QWidget()
        stream_layout = QHBoxLayout(stream_container)
        stream_layout.setContentsMargins(0, 0, 0, 0)
        stream_layout.setSpacing(6)

        stream_label = QLabel("Port:")
        stream_label.setObjectName("settingLabel")
        stream_label.setFixedWidth(STREAM_LABEL_WIDTH)
        stream_layout.addWidget(stream_label)

        self.stream_port_input = QSpinBox()
        self.stream_port_input.setObjectName("portInput")
        self.stream_port_input.setMinimum(1024)
        self.stream_port_input.setMaximum(65535)
        self.stream_port_input.setValue(8080)
        self.stream_port_input.setFixedWidth(STREAM_PORT_WIDTH)
        self.stream_port_input.setFixedHeight(INPUT_HEIGHT)
        stream_layout.addWidget(self.stream_port_input)

        self.stream_button = QPushButton("📡")
        self.stream_button.setObjectName("streamButton")
        self.stream_button.setCheckable(True)
        self.stream_button.setFixedWidth(CONTROL_BUTTON_SIZE)
        self.stream_button.setFixedHeight(CONTROL_BUTTON_SIZE)
        self.stream_button.setToolTip("Toggle audio streaming")
        stream_layout.addWidget(self.stream_button)

        settings_layout.addWidget(stream_container)
        main_layout.addWidget(settings_group)

        # Connect signals if using PySide6
        if PYSIDE6_AVAILABLE:
            # Connect progress slider events
            self.progress_slider.sliderPressed.connect(self._on_progress_pressed)
            self.progress_slider.sliderReleased.connect(self._on_progress_released)
            self.progress_slider.sliderMoved.connect(self._on_progress_moved)

            # Connect volume slider events
            self.volume_slider.valueChanged.connect(self._on_volume_changed)

            # Connect quality combo events
            self.quality_combo.currentTextChanged.connect(self._on_quality_changed)

    def _on_progress_pressed(self):
        """Handle progress bar press event."""
        self._progress_pressed = True
        if PYSIDE6_AVAILABLE:
            self.progress_pressed.emit()

    def _on_progress_released(self):
        """Handle progress bar release event."""
        self._progress_pressed = False
        if PYSIDE6_AVAILABLE:
            self.progress_released.emit()

    def _on_progress_moved(self, value):
        """
        Handle progress bar movement event.

        Args:
            value: New progress bar value
        """
        if self._progress_pressed and PYSIDE6_AVAILABLE:
            self.progress_moved.emit(value)

    def _on_volume_changed(self, value):
        """
        Handle volume slider change event.

        Args:
            value: New volume level
        """
        if PYSIDE6_AVAILABLE:
            self.volume_changed.emit(value)

            # Update volume icon based on level
            if value == 0:
                self.volume_label.setText("🔇")
            elif value < 30:
                self.volume_label.setText("🔈")
            elif value < 70:
                self.volume_label.setText("🔉")
            else:
                self.volume_label.setText("🔊")

    def _on_quality_changed(self, text):
        """
        Handle quality combo change event.

        Args:
            text: Selected quality option
        """
        if PYSIDE6_AVAILABLE and text != self._current_quality:
            self._current_quality = text
            self.quality_changed.emit(text)

    def set_play_state(self, is_playing: bool, is_paused: bool) -> None:
        """
        Update play/pause button based on playback state.

        Args:
            is_playing: Whether media is currently loaded/playing
            is_paused: Whether playback is paused
        """
        if not is_playing:
            self.play_pause_button.setText("▶")
            self.progress_slider.setValue(0)
            self.current_time_label.setText("00:00")
            self.total_time_label.setText("00:00")
            self.stop_button.setEnabled(False)
        else:
            if is_paused:
                self.play_pause_button.setText("▶")
            else:
                self.play_pause_button.setText("⏸")
            self.stop_button.setEnabled(True)

    def set_playlist_state(self, has_prev: bool, has_next: bool) -> None:
        """
        Update playlist navigation buttons based on playlist state.

        Args:
            has_prev: Whether there is a previous item in the playlist
            has_next: Whether there is a next item in the playlist
        """
        self.prev_button.setEnabled(has_prev)
        self.next_button.setEnabled(has_next)

    def set_quality_options(self, qualities: list) -> None:
        """
        Set available quality options.

        Args:
            qualities: List of available quality options
        """
        # Save current selection
        current = self.quality_combo.currentText()

        # Update combo box items
        self.quality_combo.clear()
        self.quality_combo.addItems(qualities)

        # Restore selection if available, otherwise set to best
        if current in qualities:
            self.quality_combo.setCurrentText(current)
        else:
            self.quality_combo.setCurrentText("best")

    def set_volume(self, volume: int) -> None:
        """
        Set volume slider value without triggering signals.

        Args:
            volume: Volume level (0-100)
        """
        # Block signals to avoid feedback loop
        old_state = self.volume_slider.blockSignals(True)
        self.volume_slider.setValue(volume)
        self.volume_slider.blockSignals(old_state)

        # Update volume icon
        if volume == 0:
            self.volume_label.setText("🔇")
        elif volume < 30:
            self.volume_label.setText("🔈")
        elif volume < 70:
            self.volume_label.setText("🔉")
        else:
            self.volume_label.setText("🔊")

    def get_volume(self) -> int:
        """
        Get current volume setting.

        Returns:
            Current volume level (0-100)
        """
        return self.volume_slider.value()

    def set_callbacks(
        self,
        play_pause_callback: Optional[Callable] = None,
        stop_callback: Optional[Callable] = None,
        prev_callback: Optional[Callable] = None,
        next_callback: Optional[Callable] = None,
    ) -> None:
        """
        Set callback functions for control buttons.
        Disconnects existing signals to prevent duplication.

        Args:
            play_pause_callback: Function to call when play/pause is clicked
            stop_callback: Function to call when stop is clicked
            prev_callback: Function to call when previous is clicked
            next_callback: Function to call when next is clicked
        """
        # Disconnect existing signals to prevent duplication
        if PYSIDE6_AVAILABLE:
            # Disconnect each button individually and silently ignore if no connections exist
            buttons_with_callbacks = [
                (self.play_pause_button, play_pause_callback),
                (self.stop_button, stop_callback),
                (self.prev_button, prev_callback),
                (self.next_button, next_callback)
            ]
            
            for button, callback in buttons_with_callbacks:
                if callback:  # Only disconnect if we're going to reconnect
                    try:
                        button.clicked.disconnect()
                    except (RuntimeError, TypeError):
                        # No existing connections or signal doesn't exist, which is fine
                        pass
        
        # Connect new callbacks
        if play_pause_callback:
            self.play_pause_button.clicked.connect(play_pause_callback)

        if stop_callback:
            self.stop_button.clicked.connect(stop_callback)

        if prev_callback:
            self.prev_button.clicked.connect(prev_callback)

        if next_callback:
            self.next_button.clicked.connect(next_callback)
