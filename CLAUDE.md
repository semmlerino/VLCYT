# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VLCYT is a modern YouTube video player application built with PySide6 (Qt) and VLC media player. The application provides a YouTube-like interface for playing videos with features like transcripts, playlists, audio streaming, and modern UI controls.

**Key Features:**
- YouTube video playback with quality selection
- Audio streaming to network devices
- Transcript display with search and synchronization
- Playlist management with save/load functionality
- Modern light theme UI (following global preferences)
- Comprehensive error handling and validation
- Resource management with automatic cleanup
MyPy is in the venv
## Core Dependencies

- **PySide6** (≥6.0): GUI framework (Qt for Python)
- **vlc-python**: VLC media player bindings
- **yt-dlp**: YouTube video extraction
- **youtube-transcript-api**: For fetching video transcripts
- **requests**: HTTP requests for thumbnails and subtitles

**Installation:**
```bash
python setup.py  # Automated dependency installation
```

## Commands

From `codemcp.toml`:
- **Format code**: `black .` and `isort .`
- **Run tests**: `pytest`
- **Lint code**: `ruff .`

## Architecture

### Modular Structure

The application follows SOLID principles with clear separation of concerns:

#### Core Application
- **`VLCYT.py`**: Main application window and UI coordination
- **`models.py`**: Data classes (`PlaylistItem`)
- **`constants.py`**: Application constants and configuration

#### Backend Modules
- **`vlc_player.py`**: VLC player abstraction with platform-specific embedding
- **`managers.py`**: Business logic managers (Playback, Transcript, Streaming, Settings)
- **`workers.py`**: Background thread implementations
- **`thread_manager.py`**: Centralized thread lifecycle management

#### UI Components
- **`ui_components.py`**: Tab widgets (Info, Playlist, Transcript, VideoControls)
- **`widgets.py`**: Custom UI widgets (`ModernButton`)
- **`theme.py`**: Light theme styling (following global preferences)

#### Utilities & Support
- **`utils.py`**: Utility functions (time formatting, file operations)
- **`validators.py`**: Input validation and security checks
- **`exceptions.py`**: Custom exception hierarchy
- **`logging_config.py`**: Structured logging framework

### Manager Pattern (SOLID Architecture)

The application uses specialized manager classes for separation of concerns:

1. **`PlaybackManager`**: Video playback operations and state management
2. **`TranscriptManager`**: Transcript fetching, search, and synchronization
3. **`StreamingManager`**: Audio streaming configuration and control
4. **`SettingsManager`**: Application settings persistence and management
5. **`ThreadManager`**: Centralized thread lifecycle and resource management

### Thread Management

**Centralized Resource Management:**
- `ThreadManager` controls all background operations
- Automatic cleanup of completed threads (5-second timer)
- Thread limits prevent resource exhaustion (max 5 concurrent)
- Graceful cancellation with proper resource cleanup

**Managed Thread Types:**
- `VideoFetchThreadManaged`: YouTube URL extraction
- `TranscriptFetchThreadManaged`: Subtitle/transcript fetching
- `PlaylistInfoThreadManaged`: Playlist metadata fetching

### Security & Validation

**Input Validation:**
- URL validation with domain whitelisting (YouTube only)
- Network configuration validation (ports, IP addresses)
- File path validation preventing directory traversal
- Input sanitization against injection attacks

**Security Features:**
- Domain restriction to trusted YouTube domains
- Port validation for streaming (1024-65535)
- Filename sanitization for downloads
- Path traversal protection

### Error Handling

**Exception Hierarchy:**
- `VLCYTError`: Base application exception
- `VLCError`: VLC-specific errors
- `NetworkError`: Network/connection issues
- `ValidationError`: Input validation failures
- `SecurityError`: Security violations
- `ThreadError`: Thread management issues

**User-Friendly Messages:**
- Context-aware error messages
- Actionable error information
- Graceful degradation when possible

### Resource Management

**VLC Player:**
- Platform-specific initialization (Windows/Linux/macOS)
- Fallback strategies for problematic configurations
- Proper resource cleanup with media caching
- Streaming configuration management

**Memory Management:**
- Weak references for media caching
- Automatic thread cleanup
- Proper VLC instance lifecycle
- Resource leak prevention

## Development Guidelines

### Code Quality Standards

1. **Follow SOLID Principles**: Single responsibility, dependency injection
2. **Input Validation**: Always validate and sanitize user inputs
3. **Error Handling**: Use specific exception types with context
4. **Resource Management**: Proper cleanup in all operations
5. **Security First**: Validate all external inputs and configurations

### Threading Best Practices

1. **Use ThreadManager**: Never create threads directly
2. **Proper Cancellation**: Implement cancellation support in long-running operations
3. **Resource Cleanup**: Always clean up resources in thread completion
4. **Signal Communication**: Use Qt signals for thread-to-UI communication

### UI Development

1. **Light Theme**: Follow global preference for light theme only
2. **Responsive Design**: Ensure UI scales properly
3. **Error Feedback**: Provide clear error messages to users
4. **Progressive Enhancement**: Graceful degradation when features fail

### VLC Integration

1. **Platform Compatibility**: Test on Windows, Linux, macOS
2. **Fallback Strategies**: Handle VLC initialization failures gracefully
3. **Resource Cleanup**: Always clean up VLC instances properly
4. **Error Recovery**: Implement recovery strategies for VLC errors

### Common Patterns

**Manager Instantiation:**
```python
# In VLCYT.py __init__
self.playback_manager = PlaybackManager(self.vlc_player, self.thread_manager)
self.playback_manager.playback_started.connect(self.on_playback_started)
```

**Thread Management:**
```python
# Use ThreadManager for all background operations
thread = VideoFetchThreadManaged(url, quality)
thread_id = self.thread_manager.start_thread(thread, f"video_fetch_{url}")
```

**Error Handling:**
```python
@handle_exception_with_context
def some_operation(self):
    # Operation code here
    pass
```

**Input Validation:**
```python
validated_url = URLValidator.validate_youtube_url(user_input)
validated_port = NetworkValidator.validate_port(port_input)
```

## Testing Strategy

### Unit Testing
- Test individual components in isolation
- Mock external dependencies (VLC, network)
- Use dependency injection for testability

### Integration Testing
- Test manager interactions
- Verify thread communication
- Test UI-backend integration

### Security Testing
- Validate input sanitization
- Test URL validation edge cases
- Verify network configuration security

## Performance Considerations

1. **Thread Limits**: ThreadManager enforces concurrent thread limits
2. **Media Caching**: VLC media objects cached with weak references
3. **Lazy Loading**: UI components loaded on demand
4. **Resource Monitoring**: Logging tracks performance metrics

## Troubleshooting

### VLC Issues
- Check platform-specific VLC installation
- Verify VLC arguments for compatibility
- Review logs for initialization errors

### Thread Issues
- Check ThreadManager logs for thread lifecycle
- Verify proper thread cleanup
- Monitor resource usage

### Network Issues
- Validate streaming configuration
- Check firewall settings
- Verify network accessibility

## File Organization

```
VLCYT/
├── VLCYT.py              # Main application
├── models.py             # Data models
├── managers.py           # Business logic managers
├── vlc_player.py         # VLC abstraction
├── thread_manager.py     # Thread lifecycle management
├── ui_components.py      # UI tab components
├── widgets.py            # Custom widgets
├── theme.py              # Light theme styling
├── utils.py              # Utility functions
├── validators.py         # Input validation
├── exceptions.py         # Exception hierarchy
├── logging_config.py     # Logging framework
├── constants.py          # Configuration constants
└── workers.py            # Background threads
```

This architecture provides a robust, secure, and maintainable foundation for the YouTube player application.