"""
Modern UI widgets for VLCYT.

This module contains custom Qt widgets used throughout the application.
"""

try:
    from PySide6.QtCore import Property, QEasingCurve, QPropertyAnimation, Qt
    from PySide6.QtGui import QColor, QPainter
    from PySide6.QtWidgets import QPushButton

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False

    # Dummy classes for testing
    class Qt:
        PointingHandCursor = 0

    class QPropertyAnimation:
        def __init__(self, *args):
            pass

        def setDuration(self, duration):
            pass

        def setEasingCurve(self, curve):
            pass

        def setStartValue(self, value):
            pass

        def setEndValue(self, value):
            pass

        def start(self):
            pass

    class QEasingCurve:
        OutCubic = 0

    def Property(prop_type):
        def decorator(func):
            class PropertyWrapper:
                def __init__(self, getter):
                    self.getter = getter
                    self._setter = None

                def setter(self, setter_func):
                    self._setter = setter_func
                    return self

                def __get__(self, obj, objtype=None):
                    if obj is None:
                        return self
                    return self.getter(obj)

                def __set__(self, obj, value):
                    if self._setter:
                        self._setter(obj, value)

            return PropertyWrapper(func)

        return decorator

    class QPainter:
        pass

    class QColor:
        pass

    class QPushButton:
        def __init__(self, parent=None):
            self.clicked = DummySignal()

        def setText(self, text):
            pass

        def setCursor(self, cursor):
            pass

        def update(self):
            pass

        def setObjectName(self, name):
            pass

        def setToolTip(self, tip):
            pass

        def setEnabled(self, enabled):
            pass

        def setCheckable(self, checkable):
            pass
        
        def setStyleSheet(self, style):
            pass

    class DummySignal:
        def connect(self, func):
            pass


class ModernButton(QPushButton):
    """Custom modern-styled button with hover animations."""

    def __init__(self, text="", icon_text="", parent=None):
        """
        Initialize modern button.

        Args:
            text: Button text
            icon_text: Icon text (emoji/unicode)
            parent: Parent widget
        """
        super().__init__(parent)
        self.icon_text = icon_text
        self.setText(text)
        if PYSIDE6_AVAILABLE:
            self.setCursor(Qt.PointingHandCursor)

        # Animation properties
        self._hover_progress = 0.0
        if PYSIDE6_AVAILABLE:
            self._animation = QPropertyAnimation(self, b"hover_progress")
            self._animation.setDuration(150)
            self._animation.setEasingCurve(QEasingCurve.OutCubic)

            # Add modern styling (Qt-compatible)
            self.setStyleSheet(
                """
                ModernButton {
                    font-weight: 500;
                    border-radius: 6px;
                    padding: 8px 16px;
                    background-color: #ffffff;
                    border: 2px solid #dee2e6;
                    color: #495057;
                }
                ModernButton:hover {
                    background-color: #e9ecef;
                    border: 2px solid #adb5bd;
                }
                ModernButton:pressed {
                    background-color: #dee2e6;
                    border: 2px solid #6c757d;
                }
            """
            )

    def setText(self, text):
        """Set button text with optional icon."""
        if self.icon_text:
            super().setText(f"{self.icon_text} {text}")
        else:
            super().setText(text)

    if PYSIDE6_AVAILABLE:

        @Property(float)
        def hover_progress(self):
            """Get hover animation progress."""
            return self._hover_progress

        @hover_progress.setter
        def hover_progress(self, value):
            """Set hover animation progress."""
            self._hover_progress = value
            self.update()

        def enterEvent(self, event):
            """Handle mouse enter event."""
            self._animation.setStartValue(self._hover_progress)
            self._animation.setEndValue(1.0)
            self._animation.start()
            super().enterEvent(event)

        def leaveEvent(self, event):
            """Handle mouse leave event."""
            self._animation.setStartValue(self._hover_progress)
            self._animation.setEndValue(0.0)
            self._animation.start()
            super().leaveEvent(event)

    else:
        # Dummy methods for test environment
        def hover_progress(self):
            return 0.0

        def enterEvent(self, event):
            pass

        def leaveEvent(self, event):
            pass
