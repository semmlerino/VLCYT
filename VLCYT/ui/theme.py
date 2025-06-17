"""
Theme management for VLCYT application.

This module contains the ThemeManager class that handles styling of the UI.
Per user requirements, only a light theme is implemented.
"""

try:
    from PySide6.QtWidgets import QWidget

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False

    # Mock QWidget for testing mode
    class QWidget:
        """Mock QWidget for testing"""

        def setStyleSheet(self, style):
            """Mock setStyleSheet method"""
            pass


class ThemeManager:
    """
    Theme manager for the application UI.

    Handles application styling with a modern light theme.
    """

    def __init__(self):
        """Initialize theme manager with default styles."""
        # Color palette for consistent theming
        self.colors = {
            "background": "#ffffff",
            "surface": "#f8f9fa",
            "surface_variant": "#f1f3f4",
            "primary": "#1976d2",
            "primary_variant": "#1565c0",
            "secondary": "#424242",
            "text_primary": "#212121",
            "text_secondary": "#757575",
            "border": "#e0e0e0",
            "hover": "#f5f5f5",
            "focus": "#e3f2fd",
            "error": "#d32f2f",
            "success": "#388e3c",
            "warning": "#f57c00",
        }

        # Light theme stylesheet
        self.light_theme = f"""
            /* General application style */
            QMainWindow, QWidget {{
                background-color: {self.colors['background']};
                color: {self.colors['text_primary']};
                font-family: "Segoe UI", "San Francisco", system-ui, sans-serif;
                font-size: 13px;
            }}
            
            /* Toolbar style */
            QWidget#toolbar {{
                background-color: {self.colors['background']};
                border-bottom: 2px solid {self.colors['border']};
                border-radius: 0;
                min-height: 60px;
                max-height: 60px;
            }}
            
            QLabel#appTitle {{
                font-size: 16px;
                font-weight: bold;
                color: {self.colors['text_secondary']};
            }}
            
            QWidget#urlContainer {{
                background-color: {self.colors['surface']};
                border: 2px solid {self.colors['border']};
                border-radius: 12px;
                padding: 8px;
                min-height: 48px;
                margin: 4px;
            }}
            
            QWidget#urlContainer:hover {{
                border-color: {self.colors['primary']};
                background-color: {self.colors['hover']};
            }}
            
            QWidget#urlContainer:focus-within {{
                border-color: {self.colors['primary']};
            }}
            
            /* Button styles */
            QPushButton {{
                background-color: {self.colors['background']};
                border: 2px solid {self.colors['border']};
                border-radius: 8px;
                padding: 10px 16px;
                color: {self.colors['text_primary']};
                font-weight: 500;
                min-width: 80px;
                min-height: 36px;
                font-size: 13px;
            }}
            
            QPushButton:hover {{
                background-color: {self.colors['hover']};
                border-color: {self.colors['primary']};
                color: {self.colors['primary']};
            }}
            
            QPushButton:pressed {{
                background-color: {self.colors['focus']};
                border-color: {self.colors['primary_variant']};
                color: {self.colors['primary_variant']};
            }}
            
            QPushButton:disabled {{
                background-color: {self.colors['surface_variant']};
                border-color: {self.colors['border']};
                color: {self.colors['text_secondary']};
            }}
            
            QPushButton#playButton {{
                background-color: {self.colors['primary']};
                color: white;
                border: 2px solid {self.colors['primary_variant']};
                font-weight: bold;
                min-width: 100px;
            }}
            
            QPushButton#playButton:hover {{
                background-color: {self.colors['primary_variant']};
                border: 2px solid {self.colors['primary_variant']};
            }}
            
            QPushButton#playButton:pressed {{
                background-color: {self.colors['primary_variant']};
            }}
            
            QPushButton#quickButton, QPushButton#settingsButton {{
                min-width: 44px;
                min-height: 44px;
                border-radius: 22px;
                font-size: 16px;
                padding: 8px;
            }}
            
            /* Video control buttons */
            QPushButton#controlButton {{
                min-width: 44px;
                min-height: 44px;
                border-radius: 22px;
                font-size: 16px;
                padding: 8px;
                font-weight: bold;
            }}
            
            QPushButton#muteButton, QPushButton#streamButton {{
                min-width: 40px;
                min-height: 40px;
                border-radius: 20px;
                font-size: 14px;
                padding: 6px;
            }}
            
            /* Video controls container */
            QWidget#videoControlsContainer {{
                background-color: {self.colors['surface']};
                border: 2px solid {self.colors['border']};
                border-radius: 12px;
                margin: 8px;
            }}
            
            /* Control groups */
            QWidget#playbackGroup, QWidget#progressGroup, QWidget#volumeGroup, QWidget#settingsGroup {{
                background-color: transparent;
            }}
            
            /* Time labels */
            QLabel#timeLabel {{
                color: {self.colors['text_secondary']};
                font-size: 12px;
                font-weight: 500;
                font-family: "Courier New", monospace;
            }}
            
            /* Setting labels */
            QLabel#settingLabel {{
                color: {self.colors['text_secondary']};
                font-size: 12px;
                font-weight: 500;
            }}
            
            /* Volume icon */
            QLabel#volumeIcon {{
                color: {self.colors['text_secondary']};
                font-size: 16px;
            }}
            
            /* Enhanced Input Field Styling */
            QLineEdit {{
                background-color: {self.colors['background']};
                border: 2px solid {self.colors['border']};
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                selection-background-color: {self.colors['focus']};
                font-weight: 500;
            }}
            
            QLineEdit:focus {{
                background-color: {self.colors['background']};
                border: 2px solid {self.colors['primary']};
                outline: none;
            }}
            
            QLineEdit:hover {{
                border-color: {self.colors['primary']};
                background-color: {self.colors['hover']};
            }}
            
            QLineEdit#urlEntry {{
                background-color: {self.colors['background']};
                border: none;
                border-radius: 6px;
                padding: 12px 16px;
                font-size: 14px;
                selection-background-color: {self.colors['focus']};
                font-weight: 500;
            }}
            
            QLineEdit#urlEntry:focus {{
                background-color: {self.colors['background']};
                border: 2px solid {self.colors['primary']};
                outline: none;
            }}
            
            QLineEdit#urlEntry:hover {{
                background-color: {self.colors['hover']};
            }}
            
            /* Placeholder text styling */
            QLineEdit::placeholder {{
                color: {self.colors['text_secondary']};
                font-style: italic;
            }}
            
            /* Tab Widget Styling - Enhanced */
            QTabWidget::pane {{
                border: 2px solid {self.colors['border']};
                border-radius: 12px;
                background-color: {self.colors['surface']};
                margin-top: 8px;
                padding: 12px;
            }}

            QTabWidget::tab-bar {{
                alignment: center;
            }}

            QTabBar {{
                qproperty-drawBase: 0;
                border-radius: 8px;
                background-color: {self.colors['surface_variant']};
                margin: 4px;
            }}

            QTabBar::tab {{
                background-color: transparent;
                color: {self.colors['text_secondary']};
                padding: 14px 24px;
                margin: 3px 2px;
                border: none;
                border-radius: 8px;
                min-width: 100px;
                font-weight: 500;
                font-size: 14px;
            }}

            QTabBar::tab:selected {{
                background-color: {self.colors['primary']};
                color: white;
                font-weight: 600;
            }}

            QTabBar::tab:hover:!selected {{
                background-color: {self.colors['hover']};
                color: {self.colors['text_primary']};
            }}

            QTabBar::tab:focus {{
                outline: 2px solid {self.colors['focus']};
                outline-offset: 2px;
            }}

            #tabsContainer {{
                background-color: {self.colors['background']};
                border-radius: 12px;
                margin: 4px;
            }}
            
            /* Progress bar style */
            QProgressBar {{
                background-color: {self.colors['surface_variant']};
                border: none;
                border-radius: 6px;
                text-align: center;
                font-weight: 500;
            }}
            
            QProgressBar::chunk {{
                background-color: {self.colors['primary']};
                border-radius: 6px;
                margin: 1px;
            }}
            
            /* Slider style */
            QSlider#progressSlider::groove:horizontal {{
                height: 8px;
                background: {self.colors['surface_variant']};
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
            }}
            
            QSlider#progressSlider::handle:horizontal {{
                background: {self.colors['primary']};
                border: 2px solid {self.colors['primary_variant']};
                width: 20px;
                margin: -7px 0;
                border-radius: 10px;
            }}
            
            QSlider#progressSlider::handle:horizontal:hover {{
                background: {self.colors['primary_variant']};
                border: 2px solid {self.colors['primary_variant']};
            }}
            
            QSlider#volumeSlider::groove:horizontal {{
                height: 6px;
                background: {self.colors['surface_variant']};
                border: 1px solid {self.colors['border']};
                border-radius: 3px;
            }}
            
            QSlider#volumeSlider::handle:horizontal {{
                background: {self.colors['primary']};
                border: 2px solid {self.colors['primary_variant']};
                width: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }}
            
            QSlider#volumeSlider::handle:horizontal:hover {{
                background: {self.colors['primary_variant']};
                border: 2px solid {self.colors['primary_variant']};
            }}
            
            /* Status bar style */
            QStatusBar {{
                background-color: {self.colors['background']};
                border-top: 1px solid {self.colors['border']};
            }}
            
            /* List view style */
            QListView {{
                background-color: {self.colors['background']};
                alternate-background-color: {self.colors['surface']};
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
            }}
            
            QListView::item {{
                padding: 5px;
                border-bottom: 1px solid {self.colors['surface_variant']};
            }}
            
            QListView::item:selected {{
                background-color: {self.colors['focus']};
                color: {self.colors['text_primary']};
            }}
            
            /* Table view style */
            QTableView {{
                background-color: {self.colors['background']};
                alternate-background-color: {self.colors['surface']};
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                gridline-color: {self.colors['surface_variant']};
            }}
            
            QTableView::item {{
                padding: 5px;
            }}
            
            QTableView::item:selected {{
                background-color: {self.colors['focus']};
                color: {self.colors['text_primary']};
            }}
            
            QHeaderView::section {{
                background-color: {self.colors['surface']};
                border: 1px solid {self.colors['border']};
                padding: 5px;
            }}
            
            /* Scroll bar style */
            QScrollBar:vertical {{
                border: none;
                background: {self.colors['surface']};
                width: 10px;
                margin: 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background: {self.colors['text_secondary']};
                border-radius: 5px;
                min-height: 20px;
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar:horizontal {{
                border: none;
                background: {self.colors['surface']};
                height: 10px;
                margin: 0px;
            }}
            
            QScrollBar::handle:horizontal {{
                background: {self.colors['text_secondary']};
                border-radius: 5px;
                min-width: 20px;
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
            
            /* Enhanced Combo Box Styling */
            QComboBox {{
                background-color: {self.colors['background']};
                border: 2px solid {self.colors['border']};
                border-radius: 8px;
                padding: 10px 16px;
                min-width: 6em;
                font-weight: 500;
                font-size: 14px;
            }}
            
            QComboBox#qualityCombo {{
                min-width: 70px;
                max-width: 80px;
                padding: 8px 12px;
            }}
            
            QComboBox:hover {{
                border: 2px solid {self.colors['primary']};
                background-color: {self.colors['hover']};
            }}
            
            QComboBox:focus {{
                border: 2px solid {self.colors['primary']};
                outline: none;
            }}
            
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 28px;
                border-left: 2px solid {self.colors['border']};
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background-color: {self.colors['surface']};
            }}
            
            QComboBox::drop-down:hover {{
                background-color: {self.colors['primary']};
            }}
            
            QComboBox::down-arrow {{
                image: none;
                border: none;
                width: 0;
                height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {self.colors['text_secondary']};
                margin: 6px;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {self.colors['background']};
                border: 2px solid {self.colors['border']};
                border-radius: 8px;
                padding: 4px;
                outline: none;
            }}
            
            QComboBox QAbstractItemView::item {{
                background-color: transparent;
                padding: 8px 12px;
                border-radius: 4px;
                margin: 1px;
            }}
            
            QComboBox QAbstractItemView::item:selected {{
                background-color: {self.colors['primary']};
                color: white;
            }}
            
            QComboBox QAbstractItemView::item:hover {{
                background-color: {self.colors['hover']};
                color: {self.colors['text_primary']};
            }}
            
            /* Frame style */
            QFrame {{
                border: 2px solid {self.colors['border']};
                border-radius: 8px;
                background-color: {self.colors['background']};
            }}
            
            QWidget#videoFrame {{
                background-color: {self.colors['surface_variant']};
                border: 2px solid {self.colors['border']};
                border-radius: 8px;
                margin: 8px;
                min-height: 240px;
                max-height: 280px;
            }}
            
            QWidget#videoFrame:hover {{
                border-color: {self.colors['primary']};
                background-color: {self.colors['focus']};
            }}

            QWidget#playerContainer {{
                background-color: {self.colors['surface']};
                border-radius: 8px;
                margin: 6px;
                padding: 4px;
            }}
            
            /* Video placeholder styling */
            QLabel#videoPlaceholder {{
                color: {self.colors['text_secondary']};
                font-size: 18px;
                font-weight: 600;
                text-align: center;
                padding: 12px;
                margin: 8px 0;
            }}
            
            QLabel#videoPlaceholderSub {{
                color: {self.colors['text_secondary']};
                font-size: 14px;
                text-align: center;
                padding: 8px;
                margin: 4px 0;
                line-height: 1.4;
            }}
            
            QLabel#videoPlaceholderIcon {{
                font-size: 42px;
                color: {self.colors['primary']};
                text-align: center;
                padding: 16px;
                margin: 12px 0;
            }}
            
            /* Label style */
            QLabel {{
                color: {self.colors['text_primary']};
            }}
            
            /* Enhanced Info Tab Styling */
            QLabel#infoTitle {{
                font-size: 18px;
                font-weight: 600;
                color: {self.colors['text_primary']};
                padding: 8px;
                margin-bottom: 4px;
            }}
            
            QLabel#infoChannel {{
                font-size: 14px;
                font-weight: 500;
                color: {self.colors['primary']};
                padding: 4px;
            }}
            
            QLabel#infoChannel a {{
                color: {self.colors['primary']};
                text-decoration: none;
            }}
            
            QLabel#infoChannel a:hover {{
                text-decoration: underline;
            }}
            
            QFrame#infoContentFrame {{
                background-color: {self.colors['surface']};
                border: 1px solid {self.colors['border']};
                border-radius: 8px;
                margin: 4px;
            }}
            
            QLabel#infoMetadata {{
                font-size: 13px;
                color: {self.colors['text_secondary']};
                padding: 6px 12px;
                background-color: {self.colors['surface_variant']};
                border-radius: 6px;
                margin: 2px 0;
            }}
            
            QLabel#infoSectionTitle {{
                font-size: 15px;
                font-weight: 600;
                color: {self.colors['text_primary']};
                padding: 8px 0;
                margin-top: 8px;
                border-bottom: 2px solid {self.colors['border']};
            }}
            
            QLabel#infoDescription {{
                font-size: 13px;
                line-height: 1.4;
                color: {self.colors['text_primary']};
                padding: 8px;
                background-color: {self.colors['background']};
                border-radius: 6px;
                border: 1px solid {self.colors['border']};
            }}
            
            QLabel#infoDescription a {{
                color: {self.colors['primary']};
                text-decoration: none;
            }}
            
            QLabel#infoDescription a:hover {{
                text-decoration: underline;
            }}
            
            QLabel#infoPlaceholder {{
                font-size: 14px;
                color: {self.colors['text_secondary']};
                text-align: center;
                padding: 20px;
                margin: 12px;
                background-color: {self.colors['surface']};
                border-radius: 8px;
                border: 1px solid {self.colors['border']};
            }}
        """

    def apply_theme(self, widget: QWidget) -> None:
        """
        Apply the light theme to a widget.

        Per user requirements, only a light theme is implemented.

        Args:
            widget: Widget to apply the theme to
        """
        if PYSIDE6_AVAILABLE:
            widget.setStyleSheet(self.light_theme)
