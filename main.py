"""
Main entry point for VLCYT (VLC YouTube Player) application.

This module initializes and starts the application.
"""

import os
import sys
from typing import List, Optional


def setup_environment() -> None:
    """Set up environment variables and paths."""
    # Add the parent directory to sys.path to make VLCYT package importable
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    # Check for debug mode from environment variable
    debug_env = os.environ.get("VLCYT_DEBUG", "").lower()
    if debug_env in ("1", "true", "yes"):
        print("Debug mode enabled via environment variable")


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the application.

    Args:
        args: Command line arguments

    Returns:
        Exit code
    """
    # Set up environment
    setup_environment()

    # Import Qt components
    try:
        from PySide6.QtCore import Qt
        from PySide6.QtWidgets import QApplication
    except ImportError:
        print("Error: PySide6 is required but not installed.")
        print("Please install it using: pip install PySide6")
        return 1

    # Import logging configuration
    from VLCYT.utils.logging_config import get_logger, initialize_logging

    # Initialize logging
    initialize_logging("VLCYT")
    logger = get_logger("vlcyt.main")

    # Log startup
    logger.info("Starting VLCYT - Modern YouTube Player")

    # Parse command line arguments
    if args is None:
        args = sys.argv[1:]

    # Set up Qt application
    app = QApplication(args)
    app.setApplicationName("Modern YouTube Player")
    app.setOrganizationName("VLCYT")

    # Set high DPI scaling (AA_EnableHighDpiScaling is deprecated in Qt 6.0+)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Import and create main window
    try:
        from VLCYT.ui.main_window import ModernYouTubePlayer

        window = ModernYouTubePlayer()
        window.show()

        # If URL was provided as command line argument, load it
        if len(args) > 0 and args[0].startswith(("http://", "https://")):
            logger.info(f"Loading URL from command line: {args[0]}")
            window.load_url(args[0])

        # Execute application
        return app.exec()
    except Exception as e:
        logger.exception(f"Error starting application: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
