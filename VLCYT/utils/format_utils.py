"""
Format utilities for VLCYT.

This module contains formatting utilities for time, URLs, and other data.
"""

import re
from typing import List, Optional


def format_time(seconds: int) -> str:
    """
    Format time in seconds to hh:mm:ss or mm:ss format.

    Args:
        seconds: Time in seconds

    Returns:
        Formatted time string (hh:mm:ss or mm:ss)
    """
    if seconds < 0:
        return "00:00"

    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"


def parse_playlist_urls(text: str) -> List[str]:
    """
    Parse playlist URLs from text.

    Args:
        text: Text containing URLs

    Returns:
        List of extracted URLs
    """
    # Handle various YouTube URL formats
    youtube_pattern = re.compile(
        r"(?:https?://)?(?:www\.)?"
        r"(?:youtube\.com/(?:watch\?v=|playlist\?list=|shorts/)|"
        r"youtu\.be/)([a-zA-Z0-9_-]+)"
    )

    urls = []

    # Handle multi-line input
    for line in text.split("\n"):
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Try to match YouTube URLs
        match = youtube_pattern.search(line)
        if match:
            # Extract full URL
            start, end = match.span()
            url = line[start:end]

            # Ensure URL has proper scheme
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            urls.append(url)
        elif line.startswith(("http://", "https://")):
            # Other valid URLs
            urls.append(line)

    return urls


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text to a maximum length, adding ellipsis if needed.

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in bytes to human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string (e.g., "2.5 MB")
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"

    size_kb = size_bytes / 1024
    if size_kb < 1024:
        return f"{size_kb:.1f} KB"

    size_mb = size_kb / 1024
    if size_mb < 1024:
        return f"{size_mb:.1f} MB"

    size_gb = size_mb / 1024
    return f"{size_gb:.2f} GB"


def extract_video_id(url: str) -> Optional[str]:
    """
    Extract YouTube video ID from URL.

    Args:
        url: YouTube URL

    Returns:
        Video ID or None if not found
    """
    patterns = [
        # Standard YouTube URL
        r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)",
        # Short YouTube URL
        r"(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]+)",
        # YouTube Shorts URL
        r"(?:https?://)?(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def extract_playlist_id(url: str) -> Optional[str]:
    """
    Extract YouTube playlist ID from URL.

    Args:
        url: YouTube playlist URL

    Returns:
        Playlist ID or None if not found
    """
    pattern = r"(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=([a-zA-Z0-9_-]+)"
    match = re.search(pattern, url)

    if match:
        return match.group(1)

    return None


def format_youtube_title(title: str) -> str:
    """
    Format YouTube video title for display.

    Args:
        title: Original video title

    Returns:
        Formatted title
    """
    # Remove common YouTube patterns like "- YouTube" at the end
    title = re.sub(r"\s*-\s*YouTube\s*$", "", title)

    # Replace HTML entities
    title = title.replace("&amp;", "&")
    title = title.replace("&lt;", "<")
    title = title.replace("&gt;", ">")
    title = title.replace("&quot;", '"')
    title = title.replace("&#39;", "'")

    return title.strip()


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Replace invalid filename characters with underscores
    invalid_chars = r'[\\/*?:"<>|]'
    sanitized = re.sub(invalid_chars, "_", filename)

    # Remove leading/trailing whitespace and dots
    sanitized = sanitized.strip(". ")

    # Limit length to avoid filesystem issues
    if len(sanitized) > 200:
        sanitized = sanitized[:197] + "..."

    return sanitized or "untitled"
