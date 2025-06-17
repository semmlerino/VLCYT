"""
Streaming manager for VLCYT application.

This module contains the StreamingManager class that handles audio streaming
to network devices.
"""

import logging
import socket
from typing import List, Tuple

try:
    from PySide6.QtCore import QObject, Signal

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False
    print("PySide6 not available - running in test mode")

    # Mock QObject and Signal for testing
    class QObject:
        def __init__(self):
            pass

    class Signal:
        def __init__(self, *args):
            pass

        def connect(self, func):
            pass

        def emit(self, *args):
            pass


# Import VLCPlayer
from ..core.vlc_player import VLCPlayer

# Get logger
logger = logging.getLogger("vlcyt.streaming")


class StreamingManager(QObject):
    """
    Manager for audio streaming functionality.

    This class handles streaming audio to network devices via HTTP.
    """

    # Define signals if Qt is available
    if PYSIDE6_AVAILABLE:
        streaming_enabled = Signal()
        streaming_disabled = Signal()

    def __init__(self, vlc_player: VLCPlayer):
        """
        Initialize streaming manager.

        Args:
            vlc_player: VLC player instance
        """
        super().__init__()
        self.vlc_player = vlc_player
        self.is_streaming_enabled = True
        self.stream_port = 8080
        self.stream_host = self._get_local_ip()
        self.stream_url = f"http://{self.stream_host}:{self.stream_port}/stream.mp3"

    def _get_local_ip(self) -> str:
        """
        Get local IP address.

        Returns:
            Local IP address as string
        """
        try:
            # Create a socket to determine the local IP address
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # This doesn't actually establish a connection
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            logger.error(f"Failed to get local IP address: {str(e)}")
            return "127.0.0.1"  # Fallback to localhost

    def toggle_streaming(self) -> Tuple[bool, str]:
        """
        Toggle audio streaming on/off.

        Returns:
            Tuple of (bool: is_enabled, str: status_message)
        """
        if self.is_streaming_enabled:
            # Disable streaming
            self.is_streaming_enabled = False
            self.vlc_player.disable_streaming()
            if PYSIDE6_AVAILABLE:
                self.streaming_disabled.emit()
            return False, "Audio streaming disabled"
        else:
            # Try to enable streaming
            try:
                self.is_streaming_enabled = True
                success = self.vlc_player.enable_streaming(
                    host=self.stream_host, port=self.stream_port
                )

                if success:
                    if PYSIDE6_AVAILABLE:
                        self.streaming_enabled.emit()
                    return True, f"Audio streaming enabled at {self.stream_url}"
                else:
                    self.is_streaming_enabled = False
                    return False, "Failed to enable audio streaming"
            except Exception as e:
                self.is_streaming_enabled = False
                logger.error(f"Error enabling streaming: {str(e)}")
                return False, f"Error enabling streaming: {str(e)}"

    def get_streaming_status(self) -> Tuple[bool, str]:
        """
        Get current streaming status.

        Returns:
            Tuple of (bool: is_enabled, str: status_message)
        """
        if self.is_streaming_enabled:
            return True, f"Audio streaming enabled at {self.stream_url}"
        else:
            return False, "Audio streaming disabled"

    def get_stream_url(self) -> str:
        """
        Get the current streaming URL.

        Returns:
            Streaming URL as string
        """
        return self.stream_url

    def set_stream_port(self, port: int) -> bool:
        """
        Set the streaming port.

        This will restart streaming if it's currently enabled.

        Args:
            port: Port number to use for streaming

        Returns:
            True if successful, False otherwise
        """
        if port < 1024 or port > 65535:
            logger.error(f"Invalid port number: {port}")
            return False

        # Save current streaming state
        was_streaming = self.is_streaming_enabled

        # Disable streaming if active
        if was_streaming:
            self.vlc_player.disable_streaming()

        # Update port
        self.stream_port = port
        self.stream_url = f"http://{self.stream_host}:{self.stream_port}/stream.mp3"

        # Restart streaming if it was active
        if was_streaming:
            try:
                success = self.vlc_player.enable_streaming(
                    host=self.stream_host, port=self.stream_port
                )
                if not success:
                    logger.error("Failed to restart streaming with new port")
                    self.is_streaming_enabled = False
                    return False
            except Exception as e:
                logger.error(f"Error restarting streaming: {str(e)}")
                self.is_streaming_enabled = False
                return False

        return True

    def check_streaming_compatibility(self) -> Tuple[bool, str]:
        """
        Check if streaming is compatible with the current setup.

        Returns:
            Tuple of (bool: is_compatible, str: status_message)
        """
        if not self.vlc_player.is_streaming_supported():
            return False, "Streaming is not supported with the current VLC setup"

        # Test if we can bind to the port
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(1)
            test_socket.bind((self.stream_host, self.stream_port))
            test_socket.close()
            return True, "Streaming is available"
        except socket.error as e:
            logger.error(
                f"Streaming port {self.stream_port} is not available: {str(e)}"
            )
            return False, f"Streaming port {self.stream_port} is not available"

    def scan_for_available_ports(self) -> List[int]:
        """
        Scan for available ports for streaming.

        Returns:
            List of available ports
        """
        available_ports = []
        port_range = range(8080, 8100)  # Check a limited range for performance

        for port in port_range:
            try:
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_socket.settimeout(0.1)
                test_socket.bind((self.stream_host, port))
                test_socket.close()
                available_ports.append(port)

                # If we found a few ports, that's enough
                if len(available_ports) >= 5:
                    break
            except socket.error:
                continue

        return available_ports
