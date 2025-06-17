"""Tests for VLCYT models."""

from VLCYT.models import PlaylistItem


class TestPlaylistItem:
    """Tests for PlaylistItem model."""

    def test_playlist_item_creation(self):
        """Test creating a PlaylistItem."""
        item = PlaylistItem(
            url="https://youtube.com/watch?v=test",
            title="Test Video",
            duration=300,
            thumbnail="test_thumb.jpg",
        )

        assert item.url == "https://youtube.com/watch?v=test"
        assert item.title == "Test Video"
        assert item.duration == 300
        assert item.thumbnail == "test_thumb.jpg"

    def test_playlist_item_equality(self):
        """Test PlaylistItem equality comparison."""
        item1 = PlaylistItem(
            url="https://youtube.com/watch?v=test", title="Test Video", duration=300
        )
        item2 = PlaylistItem(
            url="https://youtube.com/watch?v=test", title="Test Video", duration=300
        )
        item3 = PlaylistItem(
            url="https://youtube.com/watch?v=different",
            title="Different Video",
            duration=200,
        )

        assert item1 == item2
        assert item1 != item3

    def test_playlist_item_repr(self):
        """Test PlaylistItem string representation."""
        item = PlaylistItem(
            url="https://youtube.com/watch?v=test", title="Test Video", duration=300
        )

        repr_str = repr(item)
        assert "PlaylistItem" in repr_str
        assert "Test Video" in repr_str
