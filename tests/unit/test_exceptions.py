"""Tests for custom exception classes."""

import pytest
from VLCYT.exceptions import (
    VLCYTError,
    NetworkError,
    VideoExtractionError,
    VLCError,
    ValidationError,
    SecurityError,
    ThreadError,
    TranscriptError,
)


class TestVLCYTError:
    """Tests for base VLCYTError exception."""

    def test_basic_exception(self):
        """Test basic exception creation."""
        error = VLCYTError("Test error message")

        assert str(error) == "Test error message"
        assert error.message == "Test error message"
        assert error.details is None
        assert error.user_message == "Test error message"

    def test_exception_with_details(self):
        """Test exception with details."""
        error = VLCYTError("Test error", details="Additional details")

        assert error.message == "Test error"
        assert error.details == "Additional details"
        assert error.user_message == "Test error"

    def test_exception_with_user_message(self):
        """Test exception with custom user message."""
        error = VLCYTError("Technical error", user_message="User-friendly error")

        assert error.message == "Technical error"
        assert error.user_message == "User-friendly error"
        assert error.get_user_friendly_message() == "User-friendly error"

    def test_exception_with_all_parameters(self):
        """Test exception with all parameters."""
        error = VLCYTError(
            "Technical error",
            details="Stack trace details",
            user_message="Something went wrong",
        )

        assert error.message == "Technical error"
        assert error.details == "Stack trace details"
        assert error.user_message == "Something went wrong"


class TestNetworkError:
    """Tests for NetworkError exception."""

    def test_basic_network_error(self):
        """Test basic network error."""
        error = NetworkError("Connection failed")

        assert "Network error: Connection failed" in error.user_message
        assert error.url is None
        assert error.status_code is None

    def test_network_error_with_url(self):
        """Test network error with URL."""
        error = NetworkError("Request failed", url="https://example.com")

        assert error.url == "https://example.com"
        assert "Network error: Request failed" in error.user_message

    def test_network_error_with_status_code(self):
        """Test network error with HTTP status code."""
        error = NetworkError("Not found", status_code=404)

        assert error.status_code == 404
        assert "HTTP 404" in error.user_message
        assert "Network error: Not found" in error.user_message

    def test_network_error_with_all_parameters(self):
        """Test network error with all parameters."""
        error = NetworkError(
            "Server error", url="https://api.example.com", status_code=500
        )

        assert error.url == "https://api.example.com"
        assert error.status_code == 500
        assert "Network error: Server error (HTTP 500)" == error.user_message


class TestVideoExtractionError:
    """Tests for VideoExtractionError exception."""

    def test_basic_video_extraction_error(self):
        """Test basic video extraction error."""
        error = VideoExtractionError("Failed to extract video")

        assert error.message == "Failed to extract video"
        assert error.video_url is None
        assert error.reason is None

    def test_video_extraction_error_with_url(self):
        """Test video extraction error with URL."""
        error = VideoExtractionError(
            "Extraction failed", video_url="https://youtube.com/watch?v=test"
        )

        assert error.video_url == "https://youtube.com/watch?v=test"
        assert error.message == "Extraction failed"

    def test_video_extraction_error_with_reason(self):
        """Test video extraction error with reason."""
        error = VideoExtractionError("Extraction failed", reason="Video is private")

        assert error.reason == "Video is private"
        assert error.message == "Extraction failed"

    def test_video_extraction_error_all_parameters(self):
        """Test video extraction error with all parameters."""
        error = VideoExtractionError(
            "Cannot extract video",
            video_url="https://youtube.com/watch?v=private",
            reason="Access denied",
        )

        assert error.message == "Cannot extract video"
        assert error.video_url == "https://youtube.com/watch?v=private"
        assert error.reason == "Access denied"


class TestVLCError:
    """Tests for VLCError exception."""

    def test_basic_vlc_error(self):
        """Test basic VLC error."""
        error = VLCError("VLC initialization failed")

        assert error.message == "VLC initialization failed"
        assert isinstance(error, VLCYTError)

    def test_vlc_error_with_operation(self):
        """Test VLC error with operation."""
        error = VLCError("Playback failed", operation="play")

        assert error.operation == "play"
        assert error.message == "Playback failed"

    def test_vlc_error_inheritance(self):
        """Test VLC error inheritance."""
        error = VLCError("Test error")

        assert isinstance(error, VLCYTError)
        assert isinstance(error, Exception)


class TestValidationError:
    """Tests for ValidationError exception."""

    def test_basic_validation_error(self):
        """Test basic validation error."""
        error = ValidationError("Invalid input")

        assert error.message == "Invalid input"
        assert error.field is None
        assert error.value is None

    def test_validation_error_with_field(self):
        """Test validation error with field name."""
        error = ValidationError("Invalid URL", field="url")

        assert error.field == "url"
        assert error.message == "Invalid URL"

    def test_validation_error_with_value(self):
        """Test validation error with invalid value."""
        error = ValidationError("Invalid port", value=99999)

        assert error.value == 99999
        assert error.message == "Invalid port"

    def test_validation_error_all_parameters(self):
        """Test validation error with all parameters."""
        error = ValidationError("Port out of range", field="port", value=70000)

        assert error.message == "Port out of range"
        assert error.field == "port"
        assert error.value == 70000


class TestSecurityError:
    """Tests for SecurityError exception."""

    def test_basic_security_error(self):
        """Test basic security error."""
        error = SecurityError("Unsafe operation detected")

        assert error.message == "Unsafe operation detected"
        assert error.security_issue is None

    def test_security_error_with_security_issue(self):
        """Test security error with security issue."""
        error = SecurityError("Path traversal detected", security_issue="file_access")

        assert error.security_issue == "file_access"
        assert error.message == "Path traversal detected"


class TestThreadError:
    """Tests for ThreadError exception."""

    def test_basic_thread_error(self):
        """Test basic thread error."""
        error = ThreadError("Thread execution failed")

        assert error.message == "Thread execution failed"
        assert error.thread_id is None
        assert error.thread_type is None

    def test_thread_error_with_thread_id(self):
        """Test thread error with thread ID."""
        error = ThreadError("Thread timeout", thread_id="worker_1")

        assert error.thread_id == "worker_1"
        assert error.message == "Thread timeout"

    def test_thread_error_with_thread_type(self):
        """Test thread error with thread type."""
        error = ThreadError("Operation failed", thread_type="video_fetch")

        assert error.thread_type == "video_fetch"
        assert error.message == "Operation failed"

    def test_thread_error_all_parameters(self):
        """Test thread error with all parameters."""
        error = ThreadError(
            "Thread crashed", thread_id="bg_worker_2", thread_type="transcript_fetch"
        )

        assert error.message == "Thread crashed"
        assert error.thread_id == "bg_worker_2"
        assert error.thread_type == "transcript_fetch"


class TestTranscriptError:
    """Tests for TranscriptError exception."""

    def test_basic_transcript_error(self):
        """Test basic transcript error."""
        error = TranscriptError("Transcript not available")

        assert error.message == "Transcript not available"
        assert error.video_id is None
        assert error.reason is None

    def test_transcript_error_with_video_id(self):
        """Test transcript error with video ID."""
        error = TranscriptError("No captions found", video_id="dQw4w9WgXcQ")

        assert error.video_id == "dQw4w9WgXcQ"
        assert error.message == "No captions found"

    def test_transcript_error_with_reason(self):
        """Test transcript error with reason."""
        error = TranscriptError("Language not supported", reason="es not available")

        assert error.reason == "es not available"
        assert error.message == "Language not supported"

    def test_transcript_error_all_parameters(self):
        """Test transcript error with all parameters."""
        error = TranscriptError(
            "Auto-generated captions disabled",
            video_id="abc123",
            reason="disabled by uploader",
        )

        assert error.message == "Auto-generated captions disabled"
        assert error.video_id == "abc123"
        assert error.reason == "disabled by uploader"


class TestExceptionInheritance:
    """Tests for exception inheritance hierarchy."""

    def test_all_exceptions_inherit_from_vlcyt_error(self):
        """Test that all custom exceptions inherit from VLCYTError."""
        exceptions = [
            NetworkError("test"),
            VideoExtractionError("test"),
            VLCError("test"),
            ValidationError("test"),
            SecurityError("test"),
            ThreadError("test"),
            TranscriptError("test"),
        ]

        for exc in exceptions:
            assert isinstance(exc, VLCYTError)
            assert isinstance(exc, Exception)

    def test_exception_str_representation(self):
        """Test string representation of exceptions."""
        error = VLCYTError("Test message")
        assert str(error) == "Test message"

        network_error = NetworkError("Network issue")
        assert "Network issue" in str(network_error)

    def test_exception_with_context(self):
        """Test exceptions can be raised and caught properly."""
        with pytest.raises(VLCYTError) as exc_info:
            raise ValidationError("Test validation error")

        assert exc_info.value.message == "Test validation error"
        assert isinstance(exc_info.value, ValidationError)
        assert isinstance(exc_info.value, VLCYTError)
