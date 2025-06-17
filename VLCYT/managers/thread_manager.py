"""
Thread Manager for VLCYT.

This module provides centralized thread management to prevent resource leaks
and ensure proper cleanup of background tasks.
"""

import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, Dict, Generic, List, Optional, Tuple, TypeVar

# Try to import Qt for signals support
try:
    from PySide6.QtCore import QObject, Signal

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False

    # Create mock classes if PySide6 is not available
    class QObject:
        """Mock QObject for testing"""

        pass

    class Signal:
        """Mock Signal for testing"""

        def __init__(self, *args):
            self.args = args

        def connect(self, func):
            """Mock connect method"""
            pass

        def emit(self, *args):
            """Mock emit method"""
            pass


# Type variable for generic return types
T = TypeVar("T")


class ManagedThread(threading.Thread, Generic[T]):
    """
    A managed thread with result and error handling.

    This class extends threading.Thread with additional features
    for result retrieval and error handling.
    """

    def __init__(
        self,
        target: Callable[..., T],
        args: Tuple = (),
        kwargs: Dict[str, Any] = None,
        name: str = None,
    ):
        """
        Initialize managed thread.

        Args:
            target: Function to execute in the thread
            args: Arguments to pass to the target function
            kwargs: Keyword arguments to pass to the target function
            name: Thread name for debugging
        """
        if kwargs is None:
            kwargs = {}

        super().__init__(target=target, args=args, kwargs=kwargs, name=name)
        self.daemon = True
        self._result: Optional[T] = None
        self._exception: Optional[Exception] = None
        self._canceled = False
        self._completed = False

    def run(self) -> None:
        """Run the thread with result and exception handling."""
        if self._canceled:
            return

        try:
            # Call the target function with args and kwargs
            self._result = self._target(*self._args, **self._kwargs)
            self._completed = True
        except Exception as e:
            # Store any exception that occurs
            self._exception = e
        finally:
            # Avoid circular references that prevent garbage collection
            del self._target, self._args, self._kwargs

    def cancel(self) -> bool:
        """
        Cancel the thread before it starts or while it's running.

        Returns:
            True if thread was canceled, False otherwise
        """
        # We can only prevent execution if thread hasn't started
        if not self.is_alive():
            self._canceled = True
            return True
        # For running threads, we can only set a flag and hope
        # the target function checks it periodically
        self._canceled = True
        return False

    def is_canceled(self) -> bool:
        """
        Check if thread was canceled.

        Returns:
            True if thread was canceled, False otherwise
        """
        return self._canceled

    def is_completed(self) -> bool:
        """
        Check if thread completed successfully.

        Returns:
            True if thread completed without exceptions, False otherwise
        """
        return self._completed

    def get_result(self) -> Optional[T]:
        """
        Get the result of the thread execution.

        Returns:
            Result of the target function, or None if not completed
        """
        return self._result

    def get_exception(self) -> Optional[Exception]:
        """
        Get any exception that occurred during execution.

        Returns:
            Exception that occurred, or None if no exception
        """
        return self._exception


class ThreadManager:
    """
    Thread and resource manager for background tasks.

    This class provides centralized management of threads to prevent
    resource leaks and ensure proper cleanup.
    """

    def __init__(self, max_threads: int = 8):
        """
        Initialize thread manager.

        Args:
            max_threads: Maximum number of concurrent threads
        """
        self._max_threads = max_threads
        self._executor = ThreadPoolExecutor(max_workers=max_threads)
        self._active_threads: List[ManagedThread] = []
        self._futures: List[Future] = []
        self._lock = threading.RLock()
        self._shutdown_flag = False

    def submit(self, func: Callable, *args, **kwargs) -> ManagedThread:
        """
        Submit a task to be executed in a managed thread.

        Args:
            func: Function to execute
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function

        Returns:
            ManagedThread instance for tracking the task
        """
        with self._lock:
            # Clean up completed threads first
            self._clean_completed_threads()

            if self._shutdown_flag:
                raise RuntimeError("ThreadManager is shutting down")

            thread = ManagedThread(func, args, kwargs)
            self._active_threads.append(thread)
            thread.start()

            return thread

    def submit_task(self, func: Callable, *args, **kwargs) -> Future:
        """
        Submit a task to the thread pool.

        This uses the internal ThreadPoolExecutor.

        Args:
            func: Function to execute
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function

        Returns:
            Future instance for tracking the task
        """
        with self._lock:
            if self._shutdown_flag:
                raise RuntimeError("ThreadManager is shutting down")

            future = self._executor.submit(func, *args, **kwargs)
            self._futures.append(future)

            return future

    def _clean_completed_threads(self) -> None:
        """Clean up completed or canceled threads."""
        with self._lock:
            # Keep only active threads
            self._active_threads = [
                t for t in self._active_threads if t.is_alive() and not t.is_canceled()
            ]

    def cancel_all_threads(self) -> None:
        """Cancel all active threads."""
        with self._lock:
            for thread in self._active_threads:
                thread.cancel()

            for future in self._futures:
                future.cancel()

    def wait_for_all(self, timeout: Optional[float] = None) -> bool:
        """
        Wait for all threads to complete.

        Args:
            timeout: Maximum time to wait in seconds, or None for no limit

        Returns:
            True if all threads completed, False if timed out
        """
        start_time = time.time()

        while True:
            # Check if we've exceeded the timeout
            if timeout is not None and time.time() - start_time > timeout:
                return False

            with self._lock:
                self._clean_completed_threads()
                if not self._active_threads:
                    return True

            # Sleep briefly to avoid busy waiting
            time.sleep(0.1)

    def shutdown(self) -> None:
        """Shut down thread manager and clean up resources."""
        with self._lock:
            self._shutdown_flag = True

            # Cancel all active threads
            self.cancel_all_threads()

            # Wait for a short time for threads to respond to cancellation
            self.wait_for_all(timeout=2.0)

            # Shut down the executor
            self._executor.shutdown(wait=False)

            # Clear all references
            self._active_threads.clear()
            self._futures.clear()


# If using Qt, we can create special thread classes that emit signals
if PYSIDE6_AVAILABLE:

    class PlaylistInfoThreadManaged(QObject):
        """
        Thread for fetching playlist item information.

        This is a Qt-based thread that emits signals when complete.
        """

        info_ready = Signal(str, dict)  # URL, info dict
        error = Signal(str)  # Error message

        def __init__(self, thread_manager, url: str):
            """
            Initialize playlist info thread.

            Args:
                thread_manager: ThreadManager instance
                url: URL of the playlist item to fetch info for
            """
            super().__init__()
            self._thread_manager = thread_manager
            self._url = url
            self._future: Optional[Future] = None

        def start(self) -> None:
            """Start the thread."""
            # This will be implemented with proper video info fetching
            pass

        def cancel(self) -> None:
            """Cancel the thread."""
            if self._future:
                self._future.cancel()
