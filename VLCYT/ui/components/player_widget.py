"""
Player widget component for VLCYT.

This module contains the PlayerWidget class which handles the video player
display area with placeholder content and VLC embedding.
"""

try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (
        QLabel,
        QSizePolicy,
        QVBoxLayout,
        QWidget,
    )

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False

    class Qt:
        WA_DontCreateNativeAncestors = 0
        WA_NativeWindow = 1
        AlignCenter = 0

    class QWidget:
        def __init__(self, parent=None):
            pass

        def setObjectName(self, name):
            pass

        def setMinimumHeight(self, height):
            pass

        def setSizePolicy(self, horizontal, vertical):
            pass

        def setAttribute(self, attr):
            pass

        def setVisible(self, visible):
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

    class QVBoxLayout:
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

        def insertWidget(self, index, widget):
            pass

    class QLabel:
        def __init__(self, text="", parent=None):
            pass

        def setObjectName(self, name):
            pass

        def setAlignment(self, alignment):
            pass

        def setWordWrap(self, wrap):
            pass

    class QSizePolicy:
        Expanding = 0


from ...constants import (
    MIN_VIDEO_FRAME_HEIGHT,
    STANDARD_MARGIN,
    STANDARD_SPACING,
)
from .video_controls import VideoControls


class PlayerWidget(QWidget):
    """
    Video player widget container.

    Provides:
    - Video frame for VLC embedding
    - Placeholder content when no video is loaded
    - Video controls integration
    - Fullscreen mode support
    """

    def __init__(self, parent=None):
        """
        Initialize player widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.is_fullscreen = False
        self._setup_ui()

    def _setup_ui(self):
        """Setup player widget UI components."""
        self.setObjectName("playerContainer")

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(
            STANDARD_MARGIN, STANDARD_MARGIN, STANDARD_MARGIN, STANDARD_MARGIN
        )
        self.layout.setSpacing(STANDARD_SPACING)

        # Create video frame
        self._create_video_frame()

        # Create video controls
        self.video_controls = VideoControls()
        self.layout.addWidget(self.video_controls)

    def _create_video_frame(self):
        """Create video frame with placeholder content."""
        # Video player container
        self.video_frame = QWidget()
        self.video_frame.setObjectName("videoFrame")
        self.video_frame.setMinimumHeight(MIN_VIDEO_FRAME_HEIGHT)

        if PYSIDE6_AVAILABLE:
            self.video_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.video_frame.setAttribute(Qt.WA_DontCreateNativeAncestors)
            self.video_frame.setAttribute(Qt.WA_NativeWindow)

        # Video frame layout
        video_frame_layout = QVBoxLayout(self.video_frame)
        video_frame_layout.setContentsMargins(0, 0, 0, 0)
        video_frame_layout.setSpacing(0)

        # Add placeholder content
        self._create_placeholder(video_frame_layout)

        self.layout.addWidget(self.video_frame)

    def _create_placeholder(self, video_frame_layout):
        """Create placeholder content for empty video frame."""
        # Center container for placeholder content
        placeholder_widget = QWidget()
        placeholder_layout = QVBoxLayout(placeholder_widget)
        placeholder_layout.setContentsMargins(24, 24, 24, 24)
        placeholder_layout.setSpacing(12)

        # Add stretch to center content vertically
        placeholder_layout.addStretch()

        # Main placeholder icon
        main_placeholder = QLabel("🎬")
        main_placeholder.setObjectName("videoPlaceholderIcon")
        if PYSIDE6_AVAILABLE:
            main_placeholder.setAlignment(Qt.AlignCenter)
        placeholder_layout.addWidget(main_placeholder)

        # Placeholder title
        title_placeholder = QLabel("No Video Loaded")
        title_placeholder.setObjectName("videoPlaceholder")
        if PYSIDE6_AVAILABLE:
            title_placeholder.setAlignment(Qt.AlignCenter)
        placeholder_layout.addWidget(title_placeholder)

        # Placeholder subtitle
        subtitle_placeholder = QLabel(
            "Paste a YouTube URL above and press Enter to start watching"
        )
        subtitle_placeholder.setObjectName("videoPlaceholderSub")
        if PYSIDE6_AVAILABLE:
            subtitle_placeholder.setAlignment(Qt.AlignCenter)
            subtitle_placeholder.setWordWrap(True)
        placeholder_layout.addWidget(subtitle_placeholder)

        # Add stretch to center content vertically
        placeholder_layout.addStretch()

        # Store reference to placeholder for show/hide
        self.video_placeholder = placeholder_widget
        video_frame_layout.addWidget(placeholder_widget)

    def set_placeholder_visible(self, visible: bool):
        """
        Control the visibility of the video placeholder.

        Args:
            visible: True to show the placeholder, False to hide it
        """
        if hasattr(self, "video_placeholder"):
            self.video_placeholder.setVisible(visible)

    def setup_vlc_embedding(self, vlc_player):
        """
        Setup VLC player embedding in video frame.

        Args:
            vlc_player: VLC player instance
        """
        if vlc_player and hasattr(self.video_frame, "winId"):
            try:
                success = vlc_player.setup_embedding(self.video_frame)
                return success
            except Exception as e:
                print(f"Failed to embed VLC player: {e}")
                return False
        return False

    def enter_fullscreen(self):
        """Enter fullscreen mode."""
        if not self.is_fullscreen:
            self.is_fullscreen = True
            self.video_frame.setParent(None)
            self.video_frame.showFullScreen()
            self.video_frame.setFocus()

    def exit_fullscreen(self, parent_container):
        """
        Exit fullscreen mode.

        Args:
            parent_container: Parent container to restore video frame to
        """
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.video_frame.setParent(parent_container)
            self.video_frame.showNormal()
            # Re-add video frame to layout
            if hasattr(parent_container, "layout") and parent_container.layout():
                parent_container.layout().insertWidget(0, self.video_frame)

    def get_video_frame(self):
        """Get the video frame widget for VLC embedding."""
        return self.video_frame

    def get_video_controls(self):
        """Get the video controls widget."""
        return self.video_controls
