"""
Video information tab component for VLCYT.

This module contains the InfoTab class that displays video metadata.
"""

from typing import Any, Dict, Optional

# Try to import Qt for UI
try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (
        QFrame,
        QHBoxLayout,
        QLabel,
        QScrollArea,
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

    class QVBoxLayout:
        def __init__(self, parent=None):
            pass

        def addWidget(self, widget):
            pass

        def addLayout(self, layout):
            pass
        
        def setContentsMargins(self, *args):
            pass
        
        def setSpacing(self, spacing):
            pass
        
        def setAlignment(self, alignment):
            pass

    class QHBoxLayout(QVBoxLayout):
        pass

    class QLabel:
        def __init__(self, text="", parent=None):
            pass

        def setText(self, text):
            pass

        def setWordWrap(self, wrap):
            pass

        def setAlignment(self, align):
            pass

        def setTextFormat(self, format):
            pass

        def setOpenExternalLinks(self, open):
            pass

        def setTextInteractionFlags(self, flags):
            pass
        
        def setObjectName(self, name):
            pass
        
        def setVisible(self, visible):
            pass

    class QScrollArea(QWidget):
        def setWidgetResizable(self, resizable):
            pass

        def setWidget(self, widget):
            pass

    class QFrame(QWidget):
        def setLayout(self, layout):
            pass
        
        def setObjectName(self, name):
            pass

    class Qt:
        AlignTop = 0
        AlignCenter = 0
        TextBrowserInteraction = 0


class InfoTab(QWidget):
    """
    Tab for displaying video information and metadata.

    This tab shows information about the currently playing video,
    including title, channel, description, and other metadata.
    """

    def __init__(self, parent=None):
        """
        Initialize the info tab.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._video_info: Dict[str, Any] = {}
        self._init_ui()

    def _init_ui(self):
        """Initialize the user interface."""
        # Create main layout with improved spacing
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Create header section with title and channel
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)

        self.title_label = QLabel("No video loaded")
        self.title_label.setObjectName("infoTitle")
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.title_label)

        self.channel_label = QLabel("")
        self.channel_label.setObjectName("infoChannel")
        self.channel_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.channel_label)

        main_layout.addLayout(header_layout)

        # Create scrollable area for details
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create content frame for scroll area
        content_frame = QFrame()
        content_frame.setObjectName("infoContentFrame")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.setSpacing(16)
        content_layout.setAlignment(Qt.AlignTop)

        # Create metadata labels with object names for styling
        self.upload_date_label = QLabel("")
        self.upload_date_label.setObjectName("infoMetadata")
        content_layout.addWidget(self.upload_date_label)

        self.view_count_label = QLabel("")
        self.view_count_label.setObjectName("infoMetadata")
        content_layout.addWidget(self.view_count_label)

        self.like_count_label = QLabel("")
        self.like_count_label.setObjectName("infoMetadata")
        content_layout.addWidget(self.like_count_label)

        # Add placeholder message for empty state
        self.placeholder_label = QLabel()
        self.placeholder_label.setObjectName("infoPlaceholder")
        self.placeholder_label.setText(
            "<div style='text-align: center; padding: 20px;'>"
            "<h3 style='color: #757575; margin-bottom: 12px;'>No Video Loaded</h3>"
            "<p style='color: #9e9e9e; line-height: 1.5;'>Load a video to see its information, description, and metadata here.</p>"
            "</div>"
        )
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.placeholder_label.setWordWrap(True)
        content_layout.addWidget(self.placeholder_label)

        # Description label with styling
        self.description_title = QLabel("Description:")
        self.description_title.setObjectName("infoSectionTitle")
        self.description_title.setVisible(False)
        content_layout.addWidget(self.description_title)

        self.description_label = QLabel("")
        self.description_label.setObjectName("infoDescription")
        self.description_label.setWordWrap(True)
        self.description_label.setTextFormat(Qt.TextFormat.AutoText)
        self.description_label.setOpenExternalLinks(True)
        self.description_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.description_label.setVisible(False)
        content_layout.addWidget(self.description_label)

        # Add content frame to scroll area
        scroll_area.setWidget(content_frame)
        main_layout.addWidget(scroll_area)

    def update_info(self, video_info: Optional[Dict[str, Any]]) -> None:
        """
        Update the info tab with video metadata.

        Args:
            video_info: Dictionary containing video metadata
        """
        if not video_info:
            self._clear_info()
            return

        self._video_info = video_info

        # Hide placeholder when video is loaded
        self.placeholder_label.setVisible(False)

        # Update title and channel
        title = video_info.get("title", "Unknown Title")
        self.title_label.setText(f"<h2>{title}</h2>")

        channel = video_info.get("channel", "Unknown Channel")
        channel_url = video_info.get("channel_url", "")

        if channel_url:
            self.channel_label.setText(f'<a href="{channel_url}">{channel}</a>')
        else:
            self.channel_label.setText(channel)

        # Update metadata
        upload_date = video_info.get("upload_date", "")
        if upload_date:
            # Format upload date from YYYYMMDD to YYYY-MM-DD
            try:
                year = upload_date[:4]
                month = upload_date[4:6]
                day = upload_date[6:8]
                formatted_date = f"{year}-{month}-{day}"
                self.upload_date_label.setText(f"<b>Uploaded:</b> {formatted_date}")
            except (IndexError, ValueError):
                self.upload_date_label.setText(f"<b>Uploaded:</b> {upload_date}")
        else:
            self.upload_date_label.setText("")

        # View count
        view_count = video_info.get("view_count", 0)
        if view_count:
            self.view_count_label.setText(f"<b>Views:</b> {view_count:,}")
        else:
            self.view_count_label.setText("")

        # Like count
        like_count = video_info.get("like_count", 0)
        if like_count:
            self.like_count_label.setText(f"<b>Likes:</b> {like_count:,}")
        else:
            self.like_count_label.setText("")

        # Description
        description = video_info.get("description", "")
        if description:
            # Process description text: convert URLs to hyperlinks
            processed_description = self._process_description(description)
            self.description_label.setText(processed_description)
            self.description_title.setVisible(True)
            self.description_label.setVisible(True)
        else:
            self.description_label.setText("")
            self.description_title.setVisible(False)
            self.description_label.setVisible(False)

    def _clear_info(self) -> None:
        """Clear all information labels."""
        self.title_label.setText("No video loaded")
        self.channel_label.setText("")
        self.upload_date_label.setText("")
        self.view_count_label.setText("")
        self.like_count_label.setText("")
        self.description_label.setText("")
        self.description_title.setVisible(False)
        self.description_label.setVisible(False)
        self.placeholder_label.setVisible(True)
        self._video_info = {}

    def _process_description(self, description: str) -> str:
        """
        Process description text to make URLs clickable.

        Args:
            description: Raw description text

        Returns:
            Processed description text with clickable links
        """
        import re

        # Simple URL pattern
        url_pattern = r"(https?://[^\s]+)"

        # Replace URLs with HTML links
        processed = re.sub(url_pattern, r'<a href="\1">\1</a>', description)

        # Convert newlines to HTML breaks
        processed = processed.replace("\n", "<br/>")

        return processed

    def get_video_info(self) -> Dict[str, Any]:
        """
        Get the currently displayed video info.

        Returns:
            Dictionary containing video metadata
        """
        return self._video_info
