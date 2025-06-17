"""
Toolbar component for VLCYT.

This module contains the Toolbar class which handles the main application toolbar
with URL input, quality selection, and quick action buttons.
"""

try:
    from PySide6.QtCore import Signal
    from PySide6.QtWidgets import (
        QComboBox,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QWidget,
    )

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False

    class Signal:
        def __init__(self, *args):
            pass

        def connect(self, func):
            pass

        def emit(self, *args):
            pass

    class QWidget:
        def __init__(self, parent=None):
            pass

        def setObjectName(self, name):
            pass

        def setMinimumHeight(self, height):
            pass

    class QHBoxLayout:
        def __init__(self, parent=None):
            pass

        def setContentsMargins(self, *args):
            pass

        def setSpacing(self, spacing):
            pass

        def addWidget(self, widget):
            pass

        def addStretch(self):
            pass

    class QLabel:
        def __init__(self, text="", parent=None):
            pass

        def setObjectName(self, name):
            pass

    class QLineEdit:
        def __init__(self, parent=None):
            self.returnPressed = Signal()

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


from ...constants import (
    MIN_URL_ENTRY_WIDTH,
    STANDARD_MARGIN,
    STANDARD_SPACING,
)
from ..widgets import ModernButton


class Toolbar(QWidget):
    """
    Main application toolbar with URL input and controls.

    Provides:
    - URL input field with validation
    - Quality selection dropdown
    - Play button
    - Quick action buttons (add to playlist, settings)
    """

    # Signals
    play_requested = Signal(str, str)  # url, quality
    quick_add_requested = Signal()
    settings_requested = Signal()

    def __init__(self, parent=None):
        """
        Initialize toolbar.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Setup toolbar UI components."""
        self.setObjectName("toolbar")
        self.setMinimumHeight(60)

        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            STANDARD_MARGIN * 2, STANDARD_MARGIN, STANDARD_MARGIN * 2, STANDARD_MARGIN
        )
        layout.setSpacing(STANDARD_SPACING * 2)

        # Logo/Title
        title = QLabel("▶ YouTube Player")
        title.setObjectName("appTitle")
        layout.addWidget(title)

        layout.addStretch()

        # URL input container
        self._create_url_container(layout)

        layout.addStretch()

        # Quick action buttons
        self._create_actions_container(layout)

    def _create_url_container(self, main_layout):
        """Create URL input container with controls."""
        url_container = QWidget()
        url_container.setObjectName("urlContainer")
        url_layout = QHBoxLayout(url_container)
        url_layout.setContentsMargins(
            STANDARD_MARGIN // 2,
            STANDARD_MARGIN // 2,
            STANDARD_MARGIN // 2,
            STANDARD_MARGIN // 2,
        )
        url_layout.setSpacing(STANDARD_SPACING)

        # URL input field
        self.url_entry = QLineEdit()
        self.url_entry.setObjectName("urlEntry")
        self.url_entry.setPlaceholderText(
            "⌁ Paste YouTube URL and press Enter to play..."
        )
        self.url_entry.setMinimumWidth(MIN_URL_ENTRY_WIDTH)
        url_layout.addWidget(self.url_entry)

        # Quality selector
        self.quality_combo = QComboBox()
        self.quality_combo.setObjectName("qualityCombo")
        self.quality_combo.addItems(["Auto", "720p", "1080p", "480p", "360p", "144p"])
        self.quality_combo.setCurrentText("720p")
        self.quality_combo.setMaximumWidth(80)
        self.quality_combo.setToolTip("Video quality")
        url_layout.addWidget(self.quality_combo)

        # Play button
        self.play_button = ModernButton("Play", "▶", self)
        self.play_button.setObjectName("playButton")
        url_layout.addWidget(self.play_button)

        main_layout.addWidget(url_container)

    def _create_actions_container(self, main_layout):
        """Create quick action buttons container."""
        actions_container = QWidget()
        actions_layout = QHBoxLayout(actions_container)
        actions_layout.setContentsMargins(STANDARD_MARGIN // 2, 0, 0, 0)
        actions_layout.setSpacing(STANDARD_SPACING)

        # Quick add to playlist button
        self.quick_add_button = ModernButton("", "➕", self)
        self.quick_add_button.setObjectName("quickButton")
        self.quick_add_button.setToolTip("Quick add to playlist")
        actions_layout.addWidget(self.quick_add_button)

        # Settings button
        self.settings_button = ModernButton("", "⚙", self)
        self.settings_button.setObjectName("settingsButton")
        self.settings_button.setToolTip("Settings")
        actions_layout.addWidget(self.settings_button)

        main_layout.addWidget(actions_container)

    def _connect_signals(self):
        """Connect internal signals."""
        if PYSIDE6_AVAILABLE:
            self.url_entry.returnPressed.connect(self._on_play_requested)
            self.play_button.clicked.connect(self._on_play_requested)
            self.quick_add_button.clicked.connect(self.quick_add_requested.emit)
            self.settings_button.clicked.connect(self.settings_requested.emit)

    def _on_play_requested(self):
        """Handle play request from URL entry or play button."""
        url = self.url_entry.text().strip()
        quality = self.quality_combo.currentText()
        if url:
            self.play_requested.emit(url, quality)

    def get_url(self) -> str:
        """Get current URL from input field."""
        return self.url_entry.text().strip()

    def set_url(self, url: str):
        """Set URL in input field."""
        self.url_entry.setText(url)

    def get_quality(self) -> str:
        """Get selected quality."""
        return self.quality_combo.currentText()

    def set_quality(self, quality: str):
        """Set selected quality."""
        self.quality_combo.setCurrentText(quality)

    def set_play_button_enabled(self, enabled: bool):
        """Enable/disable play button."""
        if hasattr(self.play_button, "setEnabled"):
            self.play_button.setEnabled(enabled)
