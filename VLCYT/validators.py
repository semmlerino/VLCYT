"""
Input validation utilities for the VLCYT application.
Provides security-focused validation for user inputs.
"""

import re
import urllib.parse
from typing import List, Optional

from .exceptions import SecurityError, ValidationError


class URLValidator:
    """Validates YouTube URLs with security checks."""

    # Allowed YouTube domains
    ALLOWED_DOMAINS = {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "youtu.be",
        "www.youtu.be",
    }

    # YouTube URL patterns
    YOUTUBE_PATTERNS = [
        r"^https?://(www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})(&.*)?$",
        r"^https?://(www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})(\?.*)?$",
        r"^https?://(www\.)?youtu\.be/([a-zA-Z0-9_-]{11})(\?.*)?$",
        r"^https?://(m\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})(&.*)?$",
    ]

    @classmethod
    def validate_youtube_url(cls, url: str) -> str:
        """
        Validate and sanitize a YouTube URL.

        Args:
            url: The URL to validate

        Returns:
            The validated and normalized URL

        Raises:
            ValidationError: If URL is invalid
            SecurityError: If URL contains security risks
        """
        if not url or not isinstance(url, str):
            raise ValidationError("URL cannot be empty", field="url", value=str(url))

        url = url.strip()

        # Check for basic URL structure
        if not url.startswith(("http://", "https://")):
            # Try adding https prefix
            url = f"https://{url}"

        try:
            parsed = urllib.parse.urlparse(url)
        except Exception as e:
            raise ValidationError(
                f"Invalid URL format: {str(e)}", field="url", value=url
            )

        # Security checks
        cls._check_security_issues(parsed, url)

        # Domain validation
        domain = parsed.netloc.lower()
        if domain not in cls.ALLOWED_DOMAINS:
            raise ValidationError(
                f"Only YouTube URLs are allowed. Got domain: {domain}",
                field="url",
                value=url,
            )

        # Pattern validation
        if not any(
            re.match(pattern, url, re.IGNORECASE) for pattern in cls.YOUTUBE_PATTERNS
        ):
            raise ValidationError("Invalid YouTube URL format", field="url", value=url)

        # Extract and validate video ID
        video_id = cls._extract_video_id(url)
        if not video_id:
            raise ValidationError(
                "Could not extract video ID from URL", field="url", value=url
            )

        # Return normalized URL
        return cls._normalize_url(video_id)

    @classmethod
    def validate_playlist_urls(cls, urls_text: str) -> List[str]:
        """
        Validate multiple YouTube URLs from text input.

        Args:
            urls_text: Text containing one or more URLs

        Returns:
            List of validated URLs

        Raises:
            ValidationError: If any URL is invalid
        """
        if not urls_text or not isinstance(urls_text, str):
            raise ValidationError("URLs text cannot be empty")

        # Extract potential URLs
        lines = urls_text.strip().split("\n")
        urls = []

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue

            try:
                validated_url = cls.validate_youtube_url(line)
                urls.append(validated_url)
            except (ValidationError, SecurityError) as e:
                raise ValidationError(
                    f"Invalid URL on line {line_num}: {e.message}",
                    field="playlist_urls",
                    value=line,
                )

        if not urls:
            raise ValidationError("No valid URLs found in input")

        # Check for duplicates
        unique_urls = list(dict.fromkeys(urls))  # Preserve order
        if len(unique_urls) != len(urls):
            duplicates = len(urls) - len(unique_urls)
            raise ValidationError(f"Found {duplicates} duplicate URL(s)")

        return unique_urls

    @classmethod
    def _check_security_issues(
        cls, parsed_url: urllib.parse.ParseResult, original_url: str
    ):
        """Check for potential security issues in URL."""

        # Check for suspicious characters
        suspicious_chars = ["<", ">", '"', "'", "&lt;", "&gt;", "&quot;"]
        if any(char in original_url for char in suspicious_chars):
            raise SecurityError(
                "URL contains suspicious characters", security_issue="potential_xss"
            )

        # Check for overly long URLs (potential DoS)
        if len(original_url) > 2048:
            raise SecurityError("URL is too long", security_issue="potential_dos")

        # Check for suspicious query parameters
        if parsed_url.query:
            query_params = urllib.parse.parse_qs(parsed_url.query)
            for param, values in query_params.items():
                for value in values:
                    if any(char in value for char in suspicious_chars):
                        raise SecurityError(
                            f"Suspicious content in URL parameter: {param}",
                            security_issue="potential_xss",
                        )

        # Check for suspicious fragments
        if parsed_url.fragment and any(
            char in parsed_url.fragment for char in suspicious_chars
        ):
            raise SecurityError(
                "Suspicious content in URL fragment", security_issue="potential_xss"
            )

    @classmethod
    def _extract_video_id(cls, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL."""
        for pattern in cls.YOUTUBE_PATTERNS:
            match = re.match(pattern, url, re.IGNORECASE)
            if match:
                return match.group(2)  # Video ID is always in group 2
        return None

    @classmethod
    def _normalize_url(cls, video_id: str) -> str:
        """Convert video ID to normalized YouTube URL."""
        return f"https://www.youtube.com/watch?v={video_id}"


class NetworkValidator:
    """Validates network-related inputs."""

    @classmethod
    def validate_port(cls, port: int) -> int:
        """
        Validate network port number.

        Args:
            port: Port number to validate

        Returns:
            The validated port number

        Raises:
            ValidationError: If port is invalid
        """
        if not isinstance(port, int):
            try:
                port = int(port)
            except (ValueError, TypeError):
                raise ValidationError(
                    "Port must be a number", field="port", value=str(port)
                )

        if port < 1024:
            raise ValidationError(
                "Port must be 1024 or higher (privileged ports not allowed)",
                field="port",
                value=str(port),
            )

        if port > 65535:
            raise ValidationError(
                "Port must be 65535 or lower", field="port", value=str(port)
            )

        # Check for commonly dangerous ports
        dangerous_ports = {22, 23, 25, 53, 80, 110, 143, 443, 993, 995}
        if port in dangerous_ports:
            raise SecurityError(
                f"Port {port} is commonly used by system services",
                security_issue="dangerous_port",
            )

        return port

    @classmethod
    def validate_ip_address(cls, ip: str) -> str:
        """
        Validate IP address for network binding.

        Args:
            ip: IP address to validate

        Returns:
            The validated IP address

        Raises:
            ValidationError: If IP is invalid
            SecurityError: If IP has security implications
        """
        if not ip or not isinstance(ip, str):
            raise ValidationError(
                "IP address cannot be empty", field="ip", value=str(ip)
            )

        ip = ip.strip()

        # Basic format validation
        import ipaddress

        try:
            addr = ipaddress.ip_address(ip)
        except ValueError as e:
            raise ValidationError(
                f"Invalid IP address format: {str(e)}", field="ip", value=ip
            )

        # Security checks
        if addr.is_multicast:
            raise SecurityError(
                "Multicast addresses not allowed", security_issue="multicast_binding"
            )

        if addr.is_reserved:
            raise SecurityError(
                "Reserved addresses not allowed", security_issue="reserved_address"
            )

        # Warn about public IP binding
        if addr.is_global and ip != "0.0.0.0":
            raise SecurityError(
                "Binding to public IP addresses requires caution",
                security_issue="public_ip_binding",
            )

        return ip


class InputValidator:
    """General input validation utilities."""

    @classmethod
    def validate_filename(cls, filename: str) -> str:
        """
        Validate filename for saving.

        Args:
            filename: Filename to validate

        Returns:
            The sanitized filename

        Raises:
            ValidationError: If filename is invalid
        """
        if not filename or not isinstance(filename, str):
            raise ValidationError(
                "Filename cannot be empty", field="filename", value=str(filename)
            )

        filename = filename.strip()

        # Check length
        if len(filename) > 255:
            raise ValidationError(
                "Filename too long (max 255 characters)",
                field="filename",
                value=filename[:50] + "...",
            )

        # Check for dangerous characters
        dangerous_chars = ["<", ">", ":", '"', "|", "?", "*", "\\", "/"]
        if any(char in filename for char in dangerous_chars):
            raise ValidationError(
                f"Filename contains invalid characters: {', '.join(c for c in dangerous_chars if c in filename)}",
                field="filename",
                value=filename,
            )

        # Check for reserved names on Windows
        reserved_names = {
            "CON",
            "PRN",
            "AUX",
            "NUL",
            "COM1",
            "COM2",
            "COM3",
            "COM4",
            "COM5",
            "COM6",
            "COM7",
            "COM8",
            "COM9",
            "LPT1",
            "LPT2",
            "LPT3",
            "LPT4",
            "LPT5",
            "LPT6",
            "LPT7",
            "LPT8",
            "LPT9",
        }

        base_name = filename.split(".")[0].upper()
        if base_name in reserved_names:
            raise ValidationError(
                f"'{base_name}' is a reserved filename",
                field="filename",
                value=filename,
            )

        return filename

    @classmethod
    def validate_search_query(cls, query: str) -> str:
        """
        Validate search query input.

        Args:
            query: Search query to validate

        Returns:
            The sanitized query

        Raises:
            ValidationError: If query is invalid
        """
        if not query or not isinstance(query, str):
            raise ValidationError(
                "Search query cannot be empty", field="query", value=str(query)
            )

        query = query.strip()

        # Check length
        if len(query) > 1000:
            raise ValidationError(
                "Search query too long (max 1000 characters)",
                field="query",
                value=query[:50] + "...",
            )

        # Basic sanitization - remove potential script tags
        if "<script" in query.lower() or "javascript:" in query.lower():
            raise SecurityError(
                "Search query contains potentially malicious content",
                security_issue="script_injection",
            )

        return query


def validate_user_input(input_type: str, value, **kwargs):
    """
    General purpose input validation dispatcher.

    Args:
        input_type: Type of input to validate
        value: The value to validate
        **kwargs: Additional validation parameters

    Returns:
        The validated value

    Raises:
        ValidationError: If validation fails
        SecurityError: If security checks fail
    """
    validators = {
        "youtube_url": URLValidator.validate_youtube_url,
        "playlist_urls": URLValidator.validate_playlist_urls,
        "port": NetworkValidator.validate_port,
        "ip_address": NetworkValidator.validate_ip_address,
        "filename": InputValidator.validate_filename,
        "search_query": InputValidator.validate_search_query,
    }

    if input_type not in validators:
        raise ValidationError(f"Unknown input type: {input_type}")

    return validators[input_type](value, **kwargs)
