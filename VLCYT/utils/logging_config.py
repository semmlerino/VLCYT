"""
Logging configuration for VLCYT application.

This module provides logging setup for the application.
"""

import datetime
import logging
import os
import sys
from typing import Dict, Optional

# Global logger instances cache
_loggers: Dict[str, logging.Logger] = {}


def initialize_logging(
    app_name: str = "VLCYT", log_level: int = logging.INFO
) -> logging.Logger:
    """
    Initialize logging for the application.

    Sets up console and file handlers with formatting.

    Args:
        app_name: Application name for log file
        log_level: Default logging level

    Returns:
        Root logger instance
    """
    # Get root logger
    root_logger = logging.getLogger()

    # Clear any existing handlers to avoid duplicates
    if root_logger.handlers:
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

    # Set log level
    root_logger.setLevel(log_level)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # Check if debug mode is enabled via environment variable
    if os.environ.get("VLCYT_DEBUG", "").lower() in ("1", "true", "yes"):
        console_handler.setLevel(logging.DEBUG)
        root_logger.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    # Add console handler to root logger
    root_logger.addHandler(console_handler)

    # Create file handler
    try:
        # Determine log directory
        if sys.platform == "win32":
            log_dir = os.path.join(os.environ.get("APPDATA", "."), app_name, "logs")
        else:
            log_dir = os.path.join(
                os.path.expanduser("~"), f".{app_name.lower()}", "logs"
            )

        # Ensure log directory exists
        os.makedirs(log_dir, exist_ok=True)

        # Create log file with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = os.path.join(log_dir, f"{app_name.lower()}_{timestamp}.log")

        # Set up file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

        # Add file handler to root logger
        root_logger.addHandler(file_handler)

        # Log the start message
        root_logger.info(f"Logging initialized for {app_name}")
        root_logger.info(f"Log file: {log_file}")
    except Exception as e:
        root_logger.error(f"Failed to set up file logging: {e}")
        root_logger.warning("Continuing with console logging only")

    # Cache the root logger
    _loggers["root"] = root_logger

    # Return the root logger
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    # Check if logger already exists in cache
    if name in _loggers:
        return _loggers[name]

    # Create and cache the logger
    logger = logging.getLogger(name)
    _loggers[name] = logger

    return logger


def set_log_level(level: int, logger_name: Optional[str] = None) -> None:
    """
    Set the log level for a specific logger or the root logger.

    Args:
        level: Log level
        logger_name: Logger name or None for root logger
    """
    if logger_name is None:
        logger = logging.getLogger()
    else:
        logger = logging.getLogger(logger_name)

    logger.setLevel(level)

    # Update handler levels as well
    for handler in logger.handlers:
        handler.setLevel(level)


def enable_debug_mode() -> None:
    """Enable debug logging for all loggers."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    for handler in root_logger.handlers:
        handler.setLevel(logging.DEBUG)

    root_logger.info("Debug logging enabled")


def disable_debug_mode() -> None:
    """Disable debug logging for all loggers."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    for handler in root_logger.handlers:
        handler.setLevel(logging.INFO)

    root_logger.info("Debug logging disabled")


def get_log_file_path() -> Optional[str]:
    """
    Get the current log file path if file logging is enabled.

    Returns:
        Log file path or None if file logging is disabled
    """
    # Get the root logger
    root_logger = logging.getLogger()

    # Check for file handlers
    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            return handler.baseFilename

    return None
