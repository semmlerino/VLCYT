"""
VLC Player implementation for VLCYT.

This module provides a wrapper around the python-vlc library for media playback.
"""

import os
import sys
from typing import Optional, Tuple, Union

# Try to import vlc library
try:
    import vlc

    VLC_AVAILABLE = True
except ImportError:
    VLC_AVAILABLE = False
    print("Warning: python-vlc not available, running in limited mode")

# Try to import Qt for embedding
try:
    from PySide6.QtWidgets import QWidget

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False
    print("Warning: PySide6 not available, running in limited mode")


class VLCPlayer:
    """
    VLC media player wrapper for video playback and streaming.

    This class wraps the VLC Python bindings to provide a simpler interface
    for video playback and streaming functionality.
    """

    def __init__(self):
        """Initialize VLC player instance and related resources."""
        self._instance = None
        self._media_player = None
        self._media = None
        self._embed_handle = None
        self._streaming_disabled = False

        # Initialize VLC if available
        if VLC_AVAILABLE:
            try:
                # Create VLC instance with appropriate arguments
                args = []

                # Set log level
                if not os.environ.get("VLCYT_DEBUG"):
                    args.extend(["--quiet", "--no-interact"])

                # Initialize VLC instance
                self._instance = vlc.Instance(args)
                self._media_player = self._instance.media_player_new()

            except Exception as e:
                print(f"Error initializing VLC: {e}")
                self._streaming_disabled_on_init = True
                self._streaming_disabled = True
        else:
            # Mock implementation for when VLC is not available
            self._streaming_disabled_on_init = True
            self._streaming_disabled = True

    def setup_embedding(self, widget: Union["QWidget", int]) -> bool:
        """
        Set up video embedding in a Qt widget or window handle.

        Args:
            widget: Either a Qt widget or a window handle (int)

        Returns:
            True if embedding was successful, False otherwise
        """
        if not VLC_AVAILABLE or not self._media_player:
            return False

        try:
            # Handle different types of widget
            if PYSIDE6_AVAILABLE and isinstance(widget, QWidget):
                if sys.platform == "win32":
                    self._media_player.set_hwnd(int(widget.winId()))
                elif sys.platform == "darwin":  # macOS
                    self._media_player.set_nsobject(int(widget.winId()))
                else:  # Linux and others
                    self._media_player.set_xwindow(widget.winId())
                self._embed_handle = widget
                return True
            elif isinstance(widget, int):
                if sys.platform == "win32":
                    self._media_player.set_hwnd(widget)
                elif sys.platform == "darwin":  # macOS
                    self._media_player.set_nsobject(widget)
                else:  # Linux and others
                    self._media_player.set_xwindow(widget)
                self._embed_handle = widget
                return True
        except Exception as e:
            print(f"Error setting up VLC embedding: {e}")

        return False

    def play(self, url: Optional[str] = None) -> bool:
        """
        Play media from a URL, or resume if paused.

        Args:
            url: Media URL to play, or None to resume paused playback

        Returns:
            True if operation was successful, False otherwise
        """
        if not VLC_AVAILABLE or not self._media_player:
            return False

        try:
            if url:
                # Create a new media item and play it
                self._media = self._instance.media_new(url)
                self._media_player.set_media(self._media)
                return self._media_player.play() == 0
            else:
                # Resume paused playback
                return self._media_player.play() == 0
        except Exception as e:
            print(f"Error playing media: {e}")

        return False

    def pause(self) -> bool:
        """
        Pause media playback.

        Returns:
            True if operation was successful, False otherwise
        """
        if not VLC_AVAILABLE or not self._media_player:
            return False

        try:
            self._media_player.pause()
            return True
        except Exception as e:
            print(f"Error pausing media: {e}")

        return False

    def stop(self) -> bool:
        """
        Stop media playback.

        Returns:
            True if operation was successful, False otherwise
        """
        if not VLC_AVAILABLE or not self._media_player:
            return False

        try:
            self._media_player.stop()
            return True
        except Exception as e:
            print(f"Error stopping media: {e}")

        return False

    def is_playing(self) -> bool:
        """
        Check if media is currently playing.

        Returns:
            True if media is playing, False otherwise
        """
        if not VLC_AVAILABLE or not self._media_player:
            return False

        try:
            return bool(self._media_player.is_playing())
        except Exception:
            return False

    def get_length(self) -> int:
        """
        Get media length in milliseconds.

        Returns:
            Length in milliseconds, 0 if unavailable
        """
        if not VLC_AVAILABLE or not self._media_player:
            return 0

        try:
            length = self._media_player.get_length()
            return max(0, length)
        except Exception:
            return 0

    def get_time(self) -> int:
        """
        Get current playback time in milliseconds.

        Returns:
            Current time in milliseconds, 0 if unavailable
        """
        if not VLC_AVAILABLE or not self._media_player:
            return 0

        try:
            time = self._media_player.get_time()
            return max(0, time)
        except Exception:
            return 0

    def set_time(self, ms: int) -> bool:
        """
        Seek to a specific time in milliseconds.

        Args:
            ms: Time in milliseconds

        Returns:
            True if operation was successful, False otherwise
        """
        if not VLC_AVAILABLE or not self._media_player:
            return False

        try:
            self._media_player.set_time(ms)
            return True
        except Exception:
            return False

    def get_position(self) -> float:
        """
        Get current position as a percentage.

        Returns:
            Position as a float between 0.0 and 1.0
        """
        if not VLC_AVAILABLE or not self._media_player:
            return 0.0

        try:
            position = self._media_player.get_position()
            return max(0.0, min(1.0, position))
        except Exception:
            return 0.0

    def set_position(self, position: float) -> bool:
        """
        Set position as a percentage.

        Args:
            position: Position as a float between 0.0 and 1.0

        Returns:
            True if operation was successful, False otherwise
        """
        if not VLC_AVAILABLE or not self._media_player:
            return False

        position = max(0.0, min(1.0, position))
        try:
            self._media_player.set_position(position)
            return True
        except Exception:
            return False

    def get_volume(self) -> int:
        """
        Get current volume level.

        Returns:
            Volume level from 0 to 100
        """
        if not VLC_AVAILABLE or not self._media_player:
            return 0

        try:
            volume = self._media_player.audio_get_volume()
            return max(0, min(100, volume))
        except Exception:
            return 0

    def set_volume(self, volume: int) -> bool:
        """
        Set volume level.

        Args:
            volume: Volume level from 0 to 100

        Returns:
            True if operation was successful, False otherwise
        """
        if not VLC_AVAILABLE or not self._media_player:
            return False

        volume = max(0, min(100, volume))
        try:
            self._media_player.audio_set_volume(volume)
            return True
        except Exception:
            return False

    def setup_streaming(self, port: int = 8080) -> Tuple[bool, str]:
        """
        Set up HTTP streaming on the specified port.

        Args:
            port: HTTP port number for streaming

        Returns:
            Tuple of (success, stream_url_or_error_message)
        """
        if not VLC_AVAILABLE or self._streaming_disabled:
            return False, "VLC streaming is not available"

        try:
            # Get local IP address
            import socket

            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)

            # Set up streaming options
            sout = f"#duplicate{{{{dst=display,dst=http{{{{mux=ts,dst=:{port}/}}}}}}}}"
            self._media_player.set_mrl(self._media.get_mrl(), sout=sout)

            # Return success and stream URL
            stream_url = f"http://{ip_address}:{port}/"
            return True, stream_url
        except Exception as e:
            return False, f"Error setting up streaming: {e}"

    def disable_streaming(self) -> bool:
        """
        Disable HTTP streaming.

        Returns:
            True if operation was successful, False otherwise
        """
        if not VLC_AVAILABLE or not self._media_player:
            return False

        try:
            # Reset the media without streaming options
            if self._media:
                mrl = self._media.get_mrl()
                self._media = self._instance.media_new(mrl)
                self._media_player.set_media(self._media)
            return True
        except Exception:
            return False

    def cleanup(self) -> None:
        """Clean up VLC resources."""
        if VLC_AVAILABLE:
            try:
                if self._media_player:
                    self._media_player.stop()
                self._media = None
                self._media_player = None
                self._instance = None
            except Exception as e:
                print(f"Error cleaning up VLC resources: {e}")
