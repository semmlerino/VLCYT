"""Extended tests for format utilities to improve coverage."""

from VLCYT.utils.format_utils import (
    parse_playlist_urls,
    truncate_text,
    extract_video_id,
    extract_playlist_id,
    format_youtube_title,
)


class TestParsePlaylistUrls:
    """Tests for parse_playlist_urls function."""

    def test_parse_single_youtube_url(self):
        """Test parsing a single YouTube URL."""
        text = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = parse_playlist_urls(text)
        assert result == ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]

    def test_parse_multiple_youtube_urls(self):
        """Test parsing multiple YouTube URLs."""
        text = """
        https://www.youtube.com/watch?v=dQw4w9WgXcQ
        https://youtu.be/abc123
        https://youtube.com/shorts/xyz789
        """
        result = parse_playlist_urls(text)
        assert len(result) == 3
        assert "https://www.youtube.com/watch?v=dQw4w9WgXcQ" in result
        assert "https://youtu.be/abc123" in result
        assert "https://youtube.com/shorts/xyz789" in result

    def test_parse_url_without_scheme(self):
        """Test parsing URL without http/https scheme."""
        text = "www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = parse_playlist_urls(text)
        assert result == ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]

    def test_parse_empty_lines(self):
        """Test parsing text with empty lines."""
        text = """
        
        https://www.youtube.com/watch?v=test1
        
        https://youtu.be/test2
        
        """
        result = parse_playlist_urls(text)
        assert len(result) == 2

    def test_parse_non_youtube_urls(self):
        """Test parsing non-YouTube URLs."""
        text = """
        https://example.com/video.mp4
        http://another.com/stream
        """
        result = parse_playlist_urls(text)
        assert len(result) == 2
        assert "https://example.com/video.mp4" in result
        assert "http://another.com/stream" in result

    def test_parse_mixed_content(self):
        """Test parsing mixed YouTube and other URLs."""
        text = """
        https://www.youtube.com/watch?v=yt123
        https://example.com/video.mp4
        some random text
        youtu.be/yt456
        """
        result = parse_playlist_urls(text)
        assert len(result) == 3
        assert "https://www.youtube.com/watch?v=yt123" in result
        assert "https://example.com/video.mp4" in result
        assert "https://youtu.be/yt456" in result

    def test_parse_empty_text(self):
        """Test parsing empty text."""
        result = parse_playlist_urls("")
        assert result == []

    def test_parse_playlist_url(self):
        """Test parsing YouTube playlist URL."""
        text = "https://www.youtube.com/playlist?list=PLtest123"
        result = parse_playlist_urls(text)
        assert result == ["https://www.youtube.com/playlist?list=PLtest123"]


class TestTruncateText:
    """Tests for truncate_text function."""

    def test_truncate_short_text(self):
        """Test truncating text shorter than max length."""
        result = truncate_text("Hello", 10)
        assert result == "Hello"

    def test_truncate_exact_length(self):
        """Test truncating text at exact max length."""
        result = truncate_text("Hello", 5)
        assert result == "Hello"

    def test_truncate_long_text(self):
        """Test truncating text longer than max length."""
        result = truncate_text("This is a very long text", 10)
        assert result == "This is..."
        assert len(result) == 10

    def test_truncate_with_default_length(self):
        """Test truncating with default max length."""
        long_text = "a" * 60
        result = truncate_text(long_text)
        assert len(result) == 50
        assert result.endswith("...")

    def test_truncate_empty_string(self):
        """Test truncating empty string."""
        result = truncate_text("", 10)
        assert result == ""


class TestExtractVideoId:
    """Tests for extract_video_id function."""

    def test_extract_from_standard_url(self):
        """Test extracting video ID from standard YouTube URL."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = extract_video_id(url)
        assert result == "dQw4w9WgXcQ"

    def test_extract_from_short_url(self):
        """Test extracting video ID from short YouTube URL."""
        url = "https://youtu.be/dQw4w9WgXcQ"
        result = extract_video_id(url)
        assert result == "dQw4w9WgXcQ"

    def test_extract_from_shorts_url(self):
        """Test extracting video ID from YouTube Shorts URL."""
        url = "https://www.youtube.com/shorts/dQw4w9WgXcQ"
        result = extract_video_id(url)
        assert result == "dQw4w9WgXcQ"

    def test_extract_from_url_without_scheme(self):
        """Test extracting video ID from URL without scheme."""
        url = "www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = extract_video_id(url)
        assert result == "dQw4w9WgXcQ"

    def test_extract_from_url_with_additional_params(self):
        """Test extracting video ID from URL with additional parameters."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s&list=PLtest"
        result = extract_video_id(url)
        assert result == "dQw4w9WgXcQ"

    def test_extract_from_invalid_url(self):
        """Test extracting video ID from invalid URL."""
        url = "https://example.com/not-youtube"
        result = extract_video_id(url)
        assert result is None

    def test_extract_from_empty_url(self):
        """Test extracting video ID from empty URL."""
        result = extract_video_id("")
        assert result is None


class TestExtractPlaylistId:
    """Tests for extract_playlist_id function."""

    def test_extract_from_playlist_url(self):
        """Test extracting playlist ID from YouTube playlist URL."""
        url = "https://www.youtube.com/playlist?list=PLrAXtmRdnEQy4Q1rQZGzCc5Q1rQz5Q"
        result = extract_playlist_id(url)
        assert result == "PLrAXtmRdnEQy4Q1rQZGzCc5Q1rQz5Q"

    def test_extract_from_playlist_url_without_scheme(self):
        """Test extracting playlist ID from URL without scheme."""
        url = "www.youtube.com/playlist?list=PLtest123"
        result = extract_playlist_id(url)
        assert result == "PLtest123"

    def test_extract_from_playlist_url_with_additional_params(self):
        """Test extracting playlist ID from URL with additional parameters."""
        url = "https://www.youtube.com/playlist?list=PLtest123&index=5&t=30s"
        result = extract_playlist_id(url)
        assert result == "PLtest123"

    def test_extract_from_non_playlist_url(self):
        """Test extracting playlist ID from non-playlist URL."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = extract_playlist_id(url)
        assert result is None

    def test_extract_from_invalid_url(self):
        """Test extracting playlist ID from invalid URL."""
        url = "https://example.com/not-youtube"
        result = extract_playlist_id(url)
        assert result is None

    def test_extract_from_empty_url(self):
        """Test extracting playlist ID from empty URL."""
        result = extract_playlist_id("")
        assert result is None


class TestFormatYoutubeTitle:
    """Tests for format_youtube_title function."""

    def test_format_title_with_youtube_suffix(self):
        """Test formatting title with YouTube suffix."""
        title = "Amazing Video - YouTube"
        result = format_youtube_title(title)
        assert result == "Amazing Video"

    def test_format_title_with_spaced_youtube_suffix(self):
        """Test formatting title with spaced YouTube suffix."""
        title = "Great Content  -  YouTube  "
        result = format_youtube_title(title)
        assert result == "Great Content"

    def test_format_title_without_youtube_suffix(self):
        """Test formatting title without YouTube suffix."""
        title = "Normal Video Title"
        result = format_youtube_title(title)
        assert result == "Normal Video Title"

    def test_format_title_with_html_entities(self):
        """Test formatting title with HTML entities."""
        title = (
            "Video &amp; More &lt;Content&gt; &quot;Quotes&quot; &#39;Apostrophe&#39;"
        )
        result = format_youtube_title(title)
        expected = "Video & More <Content> \"Quotes\" 'Apostrophe'"
        assert result == expected

    def test_format_title_with_html_entities_and_youtube_suffix(self):
        """Test formatting title with both HTML entities and YouTube suffix."""
        title = "Test &amp; Video - YouTube"
        result = format_youtube_title(title)
        assert result == "Test & Video"

    def test_format_empty_title(self):
        """Test formatting empty title."""
        result = format_youtube_title("")
        assert result == ""

    def test_format_title_with_only_whitespace(self):
        """Test formatting title with only whitespace."""
        title = "   \t\n   "
        result = format_youtube_title(title)
        assert result == ""

    def test_format_title_complex_case(self):
        """Test formatting complex title case."""
        title = "  Complex &amp; Video &lt;Title&gt; - YouTube  "
        result = format_youtube_title(title)
        assert result == "Complex & Video <Title>"
