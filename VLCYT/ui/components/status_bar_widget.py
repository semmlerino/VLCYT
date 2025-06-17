"""
Status bar widget component for VLCYT.

This module contains the StatusBarWidget class which handles the application
status bar with progress indication and status messages.
"""

try:
    from PySide6.QtWidgets import (
        QLabel,
        QProgressBar,
        QStatusBar,
    )

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False

    class QLabel:
        def __init__(self, text="", parent=None):
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

        def setValue(self, value):
            pass

    class QStatusBar:
        def addWidget(self, widget):
            pass

        def addPermanentWidget(self, widget):
            pass


class StatusBarWidget:
    """
    Application status bar with progress indication.

    Provides:
    - Status message display
    - Progress bar for loading operations
    - Easy status updates
    """

    def __init__(self, status_bar: QStatusBar):
        """
        Initialize status bar widget.

        Args:
            status_bar: QStatusBar instance from main window
        """
        self.status_bar = status_bar
        self._setup_ui()

    def _setup_ui(self):
        """Setup status bar UI components."""
        # Status message label
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)

        # Progress bar for loading operations
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.status_bar.addPermanentWidget(self.progress_bar)

    def update_status(self, message: str):
        """
        Update status message.

        Args:
            message: Status message to display
        """
        self.status_label.setText(message)

    def show_progress(self, show: bool = True):
        """
        Show or hide progress bar.

        Args:
            show: True to show progress bar, False to hide
        """
        self.progress_bar.setVisible(show)

    def set_progress_range(self, minimum: int, maximum: int):
        """
        Set progress bar range.

        Args:
            minimum: Minimum value
            maximum: Maximum value
        """
        self.progress_bar.setRange(minimum, maximum)

    def set_progress_value(self, value: int):
        """
        Set progress bar value.

        Args:
            value: Progress value
        """
        self.progress_bar.setValue(value)

    def start_loading(self, message: str = "Loading..."):
        """
        Start loading indication.

        Args:
            message: Loading message to display
        """
        self.update_status(message)
        self.set_progress_range(0, 100)
        self.show_progress(True)

    def stop_loading(self, message: str = "Ready"):
        """
        Stop loading indication.

        Args:
            message: Final status message
        """
        self.show_progress(False)
        self.update_status(message)
