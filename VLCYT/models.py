from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class PlaylistItem:
    """Data class for playlist items"""

    url: str
    title: str
    duration: int = 0
    thumbnail: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "title": self.title,
            "duration": self.duration,
            "thumbnail": self.thumbnail,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlaylistItem":
        return cls(**data)
