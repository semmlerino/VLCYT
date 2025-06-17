"""UI component modules for VLCYT"""

from .base_tab import BaseTab
from .history_tab import HistoryTab
from .info_tab import InfoTab
from .playlist_tab import PlaylistTab
from .transcript_tab import TranscriptTab
from .video_controls import VideoControls

__all__ = [
    "BaseTab",
    "InfoTab",
    "VideoControls",
    "PlaylistTab",
    "TranscriptTab",
    "HistoryTab",
]
