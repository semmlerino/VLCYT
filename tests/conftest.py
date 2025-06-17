"""
Pytest configuration and fixtures for VLCYT test suite.
"""

import pytest
import sys
import os
from unittest.mock import MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def mock_vlc():
    """Mock VLC module for testing without VLC dependency."""
    mock_vlc = MagicMock()
    mock_vlc.Instance.return_value = MagicMock()
    mock_vlc.MediaPlayer.return_value = MagicMock()
    mock_vlc.Media.return_value = MagicMock()
    return mock_vlc


@pytest.fixture
def mock_pyside6():
    """Mock PySide6 for testing without Qt dependency."""
    mock_pyside6 = MagicMock()
    return mock_pyside6


@pytest.fixture
def mock_yt_dlp():
    """Mock yt-dlp for testing without network dependency."""
    mock_yt_dlp = MagicMock()
    mock_yt_dlp.YoutubeDL.return_value = MagicMock()
    return mock_yt_dlp


@pytest.fixture
def sample_video_info():
    """Sample video information for testing."""
    return {
        "id": "test_video_id",
        "title": "Test Video Title",
        "duration": 300,
        "formats": [
            {"format_id": "720p", "height": 720, "url": "test_url_720p"},
            {"format_id": "480p", "height": 480, "url": "test_url_480p"},
        ],
        "thumbnail": "test_thumbnail_url",
        "description": "Test video description",
    }


@pytest.fixture
def sample_transcript():
    """Sample transcript data for testing."""
    return [
        {"text": "Hello world", "start": 0.0, "duration": 2.0},
        {"text": "This is a test", "start": 2.0, "duration": 3.0},
        {"text": "Video transcript", "start": 5.0, "duration": 2.5},
    ]


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment with necessary mocks."""
    # Mock vlc at sys.modules level to avoid import issues
    import sys

    mock_vlc = MagicMock()
    mock_vlc.Instance.return_value = MagicMock()
    mock_vlc.MediaPlayer.return_value = MagicMock()
    sys.modules["vlc"] = mock_vlc

    # Also mock PySide6 to avoid Qt initialization
    mock_pyside6 = MagicMock()
    sys.modules["PySide6"] = mock_pyside6
    sys.modules["PySide6.QtWidgets"] = mock_pyside6
    sys.modules["PySide6.QtCore"] = mock_pyside6

    try:
        yield
    finally:
        # Clean up mocks
        if "vlc" in sys.modules:
            del sys.modules["vlc"]
        for module in ["PySide6", "PySide6.QtWidgets", "PySide6.QtCore"]:
            if module in sys.modules:
                del sys.modules[module]
