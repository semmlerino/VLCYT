"""Tests for VLCYT utilities."""

from VLCYT.utils.format_utils import format_time, format_file_size, sanitize_filename


class TestFormatUtils:
    """Tests for format utilities."""

    def test_format_time(self):
        """Test time formatting."""
        test_cases = [
            (0, "00:00"),
            (30, "00:30"),
            (60, "01:00"),
            (90, "01:30"),
            (3600, "01:00:00"),
            (3661, "01:01:01"),
            (7200, "02:00:00"),
        ]

        for seconds, expected in test_cases:
            assert format_time(seconds) == expected

    def test_format_time_invalid(self):
        """Test time formatting with invalid input."""
        # Only test negative input, as format_time expects integer
        result = format_time(-1)
        assert result == "00:00"

    def test_format_file_size(self):
        """Test file size formatting."""
        test_cases = [
            (0, "0 B"),
            (1024, "1.0 KB"),
            (1048576, "1.0 MB"),
            (1073741824, "1.00 GB"),  # GB uses 2 decimal places
            (1536, "1.5 KB"),
            (2621440, "2.5 MB"),
        ]

        for bytes_size, expected in test_cases:
            assert format_file_size(bytes_size) == expected

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        test_cases = [
            ("normal_file.mp4", "normal_file.mp4"),
            ("file with spaces.mp4", "file with spaces.mp4"),
            ("file<>name.mp4", "file__name.mp4"),
            ("file|name.mp4", "file_name.mp4"),
            ("file:name.mp4", "file_name.mp4"),
        ]

        for input_name, expected in test_cases:
            assert sanitize_filename(input_name) == expected
