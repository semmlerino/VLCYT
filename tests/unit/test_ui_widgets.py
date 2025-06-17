"""Tests for UI widgets."""

from unittest.mock import patch
from VLCYT.ui.widgets import ModernButton


class TestModernButton:
    """Tests for ModernButton widget."""

    def test_modern_button_creation_basic(self):
        """Test basic ModernButton creation."""
        button = ModernButton("Test Button")

        assert button is not None
        # Should have animation properties
        assert hasattr(button, "_hover_progress")

    def test_modern_button_with_parent(self):
        """Test ModernButton creation with parent."""
        from unittest.mock import MagicMock

        mock_parent = MagicMock()

        button = ModernButton("Test", parent=mock_parent)

        assert button is not None

    def test_modern_button_with_icon(self):
        """Test ModernButton with icon text."""
        button = ModernButton("Test", icon_text="🎵")

        assert button is not None
        assert button.icon_text == "🎵"

    @patch("VLCYT.ui.widgets.PYSIDE6_AVAILABLE", True)
    def test_modern_button_hover_effects_available(self):
        """Test ModernButton hover effects when PySide6 available."""
        button = ModernButton("Hover Test")

        # Should have animation property
        assert hasattr(button, "_animation")

        # Test enter event
        from unittest.mock import MagicMock

        mock_event = MagicMock()
        button.enterEvent(mock_event)  # Should not crash

        # Test leave event
        button.leaveEvent(mock_event)  # Should not crash

    @patch("VLCYT.ui.widgets.PYSIDE6_AVAILABLE", False)
    def test_modern_button_fallback_mode(self):
        """Test ModernButton in fallback mode without PySide6."""
        button = ModernButton("Fallback Button")

        assert button is not None

        # Test fallback hover methods
        from unittest.mock import MagicMock

        mock_event = MagicMock()
        button.enterEvent(mock_event)  # Should not crash
        button.leaveEvent(mock_event)  # Should not crash


class TestModernButtonFunctionality:
    """Tests for ModernButton functionality and behavior."""

    def test_modern_button_text_setting(self):
        """Test ModernButton text functionality."""
        # Test without icon
        button = ModernButton("Initial Text")
        assert button is not None

        # Test with icon
        button_with_icon = ModernButton("Text", icon_text="📀")
        assert button_with_icon is not None

    def test_modern_button_hover_progress_property(self):
        """Test hover progress property."""
        button = ModernButton("Test")

        # Test default value
        assert button.hover_progress() == 0.0

    @patch("VLCYT.ui.widgets.PYSIDE6_AVAILABLE", True)
    def test_modern_button_property_animation(self):
        """Test property animation setup."""
        button = ModernButton("Animation Test")

        # Should have animation setup
        assert hasattr(button, "_animation")
        assert hasattr(button, "_hover_progress")

        # Test initial value
        assert button._hover_progress == 0.0
