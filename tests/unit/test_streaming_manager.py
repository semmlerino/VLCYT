"""Tests for Streaming Manager functionality."""

from unittest.mock import MagicMock, patch, Mock
from VLCYT.managers.streaming_manager import StreamingManager


class TestStreamingManager:
    """Tests for StreamingManager class."""

    def test_streaming_manager_initialization(self):
        """Test StreamingManager initialization."""
        mock_vlc_player = MagicMock()

        with patch("VLCYT.managers.streaming_manager.socket") as mock_socket:
            # Mock socket for local IP detection
            mock_socket.socket.return_value.getsockname.return_value = (
                "192.168.1.100",
                12345,
            )

            manager = StreamingManager(mock_vlc_player)

            assert manager.vlc_player == mock_vlc_player
            assert manager.is_streaming_enabled is True
            assert manager.stream_port == 8080
            assert manager.stream_host == "192.168.1.100"
            assert manager.stream_url == "http://192.168.1.100:8080/stream.mp3"

    def test_get_local_ip_success(self):
        """Test successful local IP detection."""
        mock_vlc_player = MagicMock()

        with patch("VLCYT.managers.streaming_manager.socket") as mock_socket:
            mock_sock = Mock()
            mock_sock.getsockname.return_value = ("10.0.0.5", 54321)
            mock_socket.socket.return_value = mock_sock

            manager = StreamingManager(mock_vlc_player)

            # Verify socket operations
            mock_socket.socket.assert_called_with(
                mock_socket.AF_INET, mock_socket.SOCK_DGRAM
            )
            mock_sock.connect.assert_called_with(("8.8.8.8", 80))
            mock_sock.close.assert_called_once()

            assert manager.stream_host == "10.0.0.5"

    def test_get_local_ip_exception(self):
        """Test local IP detection with exception."""
        mock_vlc_player = MagicMock()

        with patch("VLCYT.managers.streaming_manager.socket") as mock_socket:
            # Make socket creation raise an exception
            mock_socket.socket.side_effect = Exception("Network error")

            with patch("VLCYT.managers.streaming_manager.logger") as mock_logger:
                manager = StreamingManager(mock_vlc_player)

                # Should fallback to localhost
                assert manager.stream_host == "127.0.0.1"
                mock_logger.error.assert_called_once()

    def test_toggle_streaming_disable(self):
        """Test disabling streaming."""
        mock_vlc_player = MagicMock()

        with patch("VLCYT.managers.streaming_manager.socket"):
            manager = StreamingManager(mock_vlc_player)

            # Mock the signal
            if hasattr(manager, "streaming_disabled"):
                manager.streaming_disabled = MagicMock()

            # Initially enabled, so toggle should disable
            result = manager.toggle_streaming()

            assert result[0] is False  # is_enabled
            assert "disabled" in result[1].lower()  # status message
            assert manager.is_streaming_enabled is False
            mock_vlc_player.disable_streaming.assert_called_once()

    def test_toggle_streaming_enable(self):
        """Test enabling streaming."""
        mock_vlc_player = MagicMock()

        with patch("VLCYT.managers.streaming_manager.socket"):
            manager = StreamingManager(mock_vlc_player)

            # Mock the signal
            if hasattr(manager, "streaming_enabled"):
                manager.streaming_enabled = MagicMock()

            # First disable, then enable
            manager.is_streaming_enabled = False

            result = manager.toggle_streaming()

            assert result[0] is True  # is_enabled
            assert "enabled" in result[1].lower()  # status message
            assert manager.is_streaming_enabled is True
            mock_vlc_player.enable_streaming.assert_called_once()

    def test_get_streaming_status_enabled(self):
        """Test getting streaming status when enabled."""
        mock_vlc_player = MagicMock()

        with patch("VLCYT.managers.streaming_manager.socket") as mock_socket:
            mock_socket.socket.return_value.getsockname.return_value = (
                "192.168.1.100",
                12345,
            )

            manager = StreamingManager(mock_vlc_player)

            result = manager.get_streaming_status()

            assert result[0] is True  # is_enabled
            assert "enabled" in result[1].lower()
            assert "192.168.1.100:8080" in result[1]

    def test_get_streaming_status_disabled(self):
        """Test getting streaming status when disabled."""
        mock_vlc_player = MagicMock()

        with patch("VLCYT.managers.streaming_manager.socket"):
            manager = StreamingManager(mock_vlc_player)

            # Disable streaming
            manager.is_streaming_enabled = False

            result = manager.get_streaming_status()

            assert result[0] is False  # is_enabled
            assert "disabled" in result[1].lower()

    def test_get_stream_url(self):
        """Test get stream URL method."""
        mock_vlc_player = MagicMock()

        with patch("VLCYT.managers.streaming_manager.socket") as mock_socket:
            mock_socket.socket.return_value.getsockname.return_value = (
                "192.168.1.50",
                12345,
            )

            manager = StreamingManager(mock_vlc_player)

            result = manager.get_stream_url()
            assert result == "http://192.168.1.50:8080/stream.mp3"

    def test_set_stream_port(self):
        """Test setting stream port."""
        mock_vlc_player = MagicMock()

        with patch("VLCYT.managers.streaming_manager.socket") as mock_socket:
            mock_socket.socket.return_value.getsockname.return_value = (
                "192.168.1.50",
                12345,
            )

            manager = StreamingManager(mock_vlc_player)

            manager.set_stream_port(9090)

            assert manager.stream_port == 9090
            assert manager.stream_url == "http://192.168.1.50:9090/stream.mp3"

    def test_set_stream_port_invalid(self):
        """Test setting invalid stream port."""
        mock_vlc_player = MagicMock()

        with patch("VLCYT.managers.streaming_manager.socket"):
            manager = StreamingManager(mock_vlc_player)

            # Test ports outside valid range
            result1 = manager.set_stream_port(1023)  # Too low
            result2 = manager.set_stream_port(65536)  # Too high
            result3 = manager.set_stream_port(-1)  # Negative

            assert result1 is False
            assert result2 is False
            assert result3 is False
            # Port should remain unchanged
            assert manager.stream_port == 8080

    def test_check_streaming_compatibility(self):
        """Test checking streaming compatibility."""
        mock_vlc_player = MagicMock()
        mock_vlc_player.is_streaming_supported.return_value = True

        with patch("VLCYT.managers.streaming_manager.socket") as mock_socket:
            # Mock successful socket binding
            mock_test_socket = MagicMock()
            mock_socket.socket.return_value = mock_test_socket
            mock_test_socket.getsockname.return_value = ("192.168.1.100", 12345)

            manager = StreamingManager(mock_vlc_player)

            result = manager.check_streaming_compatibility()

            assert result[0] is True
            assert "available" in result[1].lower()

    def test_check_streaming_compatibility_not_supported(self):
        """Test checking streaming compatibility when not supported."""
        mock_vlc_player = MagicMock()
        mock_vlc_player.is_streaming_supported.return_value = False

        with patch("VLCYT.managers.streaming_manager.socket"):
            manager = StreamingManager(mock_vlc_player)

            result = manager.check_streaming_compatibility()

            assert result[0] is False
            assert "not supported" in result[1].lower()

    def test_scan_for_available_ports(self):
        """Test scanning for available ports."""
        mock_vlc_player = MagicMock()

        with patch("VLCYT.managers.streaming_manager.socket") as mock_socket:
            mock_socket.socket.return_value.getsockname.return_value = (
                "192.168.1.100",
                12345,
            )

            # Mock successful port binding
            mock_test_socket = MagicMock()
            mock_socket.socket.return_value = mock_test_socket

            manager = StreamingManager(mock_vlc_player)

            result = manager.scan_for_available_ports()

            assert isinstance(result, list)
            # Should return some ports (exact number depends on mock setup)

    @patch("VLCYT.managers.streaming_manager.PYSIDE6_AVAILABLE", False)
    def test_initialization_without_pyside6(self):
        """Test initialization without PySide6."""
        mock_vlc_player = MagicMock()

        with patch("VLCYT.managers.streaming_manager.socket") as mock_socket:
            mock_socket.socket.return_value.getsockname.return_value = (
                "127.0.0.1",
                12345,
            )

            manager = StreamingManager(mock_vlc_player)

            # Should still initialize properly
            assert manager.vlc_player == mock_vlc_player
            assert manager.is_streaming_enabled is True
            # Should not have Qt signals
            assert not hasattr(manager, "streaming_enabled") or not callable(
                getattr(manager, "streaming_enabled", None)
            )

    def test_streaming_port_validation(self):
        """Test streaming port validation."""
        mock_vlc_player = MagicMock()

        with patch("VLCYT.managers.streaming_manager.socket"):
            manager = StreamingManager(mock_vlc_player)

            # Test valid port
            result = manager.set_stream_port(9090)
            assert result is True
            assert manager.stream_port == 9090

            # Test invalid ports
            result_low = manager.set_stream_port(1023)
            result_high = manager.set_stream_port(65536)

            assert result_low is False
            assert result_high is False
            # Port should remain unchanged
            assert manager.stream_port == 9090
