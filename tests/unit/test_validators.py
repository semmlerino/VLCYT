"""Tests for VLCYT validators."""

import pytest
from VLCYT.validators import URLValidator, NetworkValidator, InputValidator
from VLCYT.exceptions import ValidationError, SecurityError


class TestURLValidator:
    """Tests for URL validation."""

    def test_valid_youtube_urls(self):
        """Test validation of valid YouTube URLs."""
        valid_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://m.youtube.com/watch?v=dQw4w9WgXcQ",
        ]

        # All URLs should be normalized to the same format
        expected_normalized = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

        for url in valid_urls:
            validated = URLValidator.validate_youtube_url(url)
            assert validated == expected_normalized

    def test_invalid_youtube_urls(self):
        """Test validation of invalid YouTube URLs."""
        invalid_urls = [
            "https://vimeo.com/123456",
            "https://example.com/watch?v=test",
            "not_a_url",
            "ftp://youtube.com/watch?v=test",
            "javascript:alert('xss')",
        ]

        for url in invalid_urls:
            with pytest.raises((ValidationError, SecurityError)):
                URLValidator.validate_youtube_url(url)

    def test_empty_url(self):
        """Test validation of empty URL."""
        with pytest.raises(ValidationError):
            URLValidator.validate_youtube_url("")

        with pytest.raises(ValidationError):
            URLValidator.validate_youtube_url(None)


class TestNetworkValidator:
    """Tests for network validation."""

    def test_valid_ports(self):
        """Test validation of valid port numbers."""
        valid_ports = [1024, 8081, 65535, "8081", "1024"]

        for port in valid_ports:
            validated = NetworkValidator.validate_port(port)
            assert isinstance(validated, int)
            assert 1024 <= validated <= 65535

    def test_invalid_ports(self):
        """Test validation of invalid port numbers."""
        invalid_ports = [0, 1023, 65536, -1, "invalid", None]

        for port in invalid_ports:
            with pytest.raises(ValidationError):
                NetworkValidator.validate_port(port)

    def test_valid_ip_addresses(self):
        """Test validation of valid IP addresses."""
        # Use only truly non-reserved private IPs
        valid_ips = ["192.168.1.100", "10.0.0.100"]

        for ip in valid_ips:
            validated = NetworkValidator.validate_ip_address(ip)
            assert validated == ip

    def test_invalid_ip_addresses(self):
        """Test validation of invalid IP addresses."""
        invalid_ips = ["256.1.1.1", "192.168.1", "not_an_ip", ""]

        for ip in invalid_ips:
            with pytest.raises(ValidationError):
                NetworkValidator.validate_ip_address(ip)


class TestInputValidator:
    """Tests for input validation."""

    def test_safe_filenames(self):
        """Test validation of safe filenames."""
        safe_names = ["video.mp4", "my_video.mp4", "test-video.mp4"]

        for name in safe_names:
            validated = InputValidator.validate_filename(name)
            assert validated == name

    def test_unsafe_filenames(self):
        """Test validation of unsafe filenames."""
        unsafe_names = ["con.txt", "aux.mp4", "video<>.mp4", "video|name.mp4"]

        for name in unsafe_names:
            with pytest.raises(ValidationError):
                InputValidator.validate_filename(name)

    def test_search_query_validation(self):
        """Test search query validation."""
        valid_queries = ["hello world", "test query", "video title"]

        for query in valid_queries:
            validated = InputValidator.validate_search_query(query)
            assert validated == query

        # Test malicious queries
        malicious_queries = ["<script>alert('xss')</script>", "javascript:alert('xss')"]

        for query in malicious_queries:
            with pytest.raises(SecurityError):
                InputValidator.validate_search_query(query)
