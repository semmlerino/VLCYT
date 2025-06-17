"""
Custom exception classes for the VLCYT application.
Provides specific error types for better error handling and user feedback.
"""

from typing import Optional


class VLCYTError(Exception):
    """Base exception for all VLCYT-related errors."""

    def __init__(
        self,
        message: str,
        details: Optional[str] = None,
        user_message: Optional[str] = None,
    ):
        super().__init__(message)
        self.message = message
        self.details = details
        self.user_message = user_message or message

    def get_user_friendly_message(self) -> str:
        """Get a user-friendly error message."""
        return self.user_message


class NetworkError(VLCYTError):
    """Raised when network operations fail."""

    def __init__(
        self, message: str, url: Optional[str] = None, status_code: Optional[int] = None
    ):
        user_msg = f"Network error: {message}"
        if status_code:
            user_msg += f" (HTTP {status_code})"

        super().__init__(message, user_message=user_msg)
        self.url = url
        self.status_code = status_code


class VideoExtractionError(VLCYTError):
    """Raised when video URL extraction fails."""

    def __init__(
        self,
        message: str,
        video_url: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        user_msg = "Could not extract video stream"
        if reason:
            user_msg += f": {reason}"

        super().__init__(message, user_message=user_msg)
        self.video_url = video_url
        self.reason = reason


class TranscriptError(VLCYTError):
    """Raised when transcript operations fail."""

    def __init__(
        self, message: str, video_id: Optional[str] = None, reason: Optional[str] = None
    ):
        user_msg = "Transcript not available"
        if reason:
            user_msg += f": {reason}"

        super().__init__(message, user_message=user_msg)
        self.video_id = video_id
        self.reason = reason


class VLCError(VLCYTError):
    """Raised when VLC operations fail."""

    def __init__(self, message: str, operation: Optional[str] = None):
        user_msg = "Media player error"
        if operation:
            user_msg += f" during {operation}"

        super().__init__(message, user_message=user_msg)
        self.operation = operation


class ValidationError(VLCYTError):
    """Raised when input validation fails."""

    def __init__(
        self, message: str, field: Optional[str] = None, value: Optional[str] = None
    ):
        user_msg = f"Invalid input: {message}"

        super().__init__(message, user_message=user_msg)
        self.field = field
        self.value = value


class SecurityError(VLCYTError):
    """Raised when security checks fail."""

    def __init__(self, message: str, security_issue: Optional[str] = None):
        user_msg = "Security check failed"
        if security_issue:
            user_msg += f": {security_issue}"

        super().__init__(message, user_message=user_msg)
        self.security_issue = security_issue


class PlaylistError(VLCYTError):
    """Raised when playlist operations fail."""

    def __init__(
        self,
        message: str,
        playlist_item: Optional[str] = None,
        operation: Optional[str] = None,
    ):
        user_msg = "Playlist error"
        if operation:
            user_msg += f" during {operation}"

        super().__init__(message, user_message=user_msg)
        self.playlist_item = playlist_item
        self.operation = operation


class ConfigurationError(VLCYTError):
    """Raised when configuration issues occur."""

    def __init__(
        self, message: str, setting: Optional[str] = None, value: Optional[str] = None
    ):
        user_msg = f"Configuration error: {message}"

        super().__init__(message, user_message=user_msg)
        self.setting = setting
        self.value = value


class ThreadError(VLCYTError):
    """Raised when thread management fails."""

    def __init__(
        self,
        message: str,
        thread_type: Optional[str] = None,
        thread_id: Optional[str] = None,
    ):
        user_msg = "Background operation failed"
        if thread_type:
            user_msg += f" ({thread_type})"

        super().__init__(message, user_message=user_msg)
        self.thread_type = thread_type
        self.thread_id = thread_id


class ResourceError(VLCYTError):
    """Raised when resource management fails."""

    def __init__(
        self,
        message: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
    ):
        user_msg = "Resource error"
        if resource_type:
            user_msg += f" with {resource_type}"

        super().__init__(message, user_message=user_msg)
        self.resource_type = resource_type
        self.resource_id = resource_id


# Exception mapping for external libraries
def map_external_exception(exc: Exception, context: str = "") -> VLCYTError:
    """
    Map external exceptions to appropriate VLCYT exceptions.

    Args:
        exc: The original exception
        context: Additional context about where the exception occurred

    Returns:
        Appropriate VLCYTError subclass
    """
    exc_type = type(exc).__name__
    exc_msg = str(exc)

    # Network-related exceptions
    if exc_type in ["RequestException", "HTTPError", "ConnectionError", "Timeout"]:
        return NetworkError(f"{context}: {exc_msg}")

    # YouTube/yt-dlp related exceptions
    elif exc_type in ["ExtractorError", "DownloadError", "YoutubeDLError"]:
        return VideoExtractionError(f"{context}: {exc_msg}")

    # Transcript API exceptions
    elif exc_type in ["TranscriptsDisabled", "NoTranscriptFound", "VideoUnavailable"]:
        return TranscriptError(f"{context}: {exc_msg}")

    # VLC-related exceptions
    elif "vlc" in exc_msg.lower() or "media" in exc_msg.lower():
        return VLCError(f"{context}: {exc_msg}")

    # File/IO exceptions
    elif exc_type in ["FileNotFoundError", "PermissionError", "IOError"]:
        return ResourceError(f"{context}: {exc_msg}", resource_type="file")

    # Generic mapping
    else:
        return VLCYTError(f"{context}: {exc_msg}")


def handle_exception_with_context(func):
    """
    Decorator to automatically handle and map exceptions with context.

    Usage:
        @handle_exception_with_context
        def some_method(self):
            # method code here
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except VLCYTError:
            # Re-raise VLCYT exceptions as-is
            raise
        except Exception as e:
            # Map other exceptions
            context = f"{func.__name__}"
            if args and hasattr(args[0], "__class__"):
                context = f"{args[0].__class__.__name__}.{func.__name__}"
            raise map_external_exception(e, context)

    return wrapper


class ErrorCollector:
    """Utility class to collect and manage multiple errors."""

    def __init__(self):
        self.errors: list[VLCYTError] = []

    def add_error(self, error: VLCYTError):
        """Add an error to the collection."""
        self.errors.append(error)

    def add_exception(self, exc: Exception, context: str = ""):
        """Add an exception (automatically mapped to VLCYTError)."""
        if isinstance(exc, VLCYTError):
            self.errors.append(exc)
        else:
            self.errors.append(map_external_exception(exc, context))

    def has_errors(self) -> bool:
        """Check if any errors have been collected."""
        return len(self.errors) > 0

    def get_error_count(self) -> int:
        """Get the number of collected errors."""
        return len(self.errors)

    def get_errors_by_type(self, error_type: type) -> list[VLCYTError]:
        """Get all errors of a specific type."""
        return [err for err in self.errors if isinstance(err, error_type)]

    def get_user_messages(self) -> list[str]:
        """Get all user-friendly error messages."""
        return [err.get_user_friendly_message() for err in self.errors]

    def clear(self):
        """Clear all collected errors."""
        self.errors.clear()

    def raise_if_errors(self, message: str = "Multiple errors occurred"):
        """Raise a combined exception if any errors were collected."""
        if self.has_errors():
            user_messages = self.get_user_messages()
            combined_message = f"{message}:\n" + "\n".join(
                f"- {msg}" for msg in user_messages
            )
            raise VLCYTError(combined_message, user_message=combined_message)
