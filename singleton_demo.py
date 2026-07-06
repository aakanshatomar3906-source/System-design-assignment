

import threading
from typing import Optional

class DatabaseConnection:
    """
    Singleton class representing a shared database connection.
    - Only one instance is created, even under concurrent access.
    - Provides get_connection() to retrieve the shared instance.
    """

    _instance: Optional["DatabaseConnection"] = None
    _lock: threading.Lock = threading.Lock()
    _initialized: bool = False

    def __new__(cls) -> "DatabaseConnection":
        # Outline:
        # 1. If instance already exists, return it.
        # 2. Otherwise, acquire lock and create instance safely.
        if cls._instance is not None:
            return cls._instance

        with cls._lock:
            # Double-check inside lock (double-checked locking).
            if cls._instance is None:
                cls._instance = super(DatabaseConnection, cls).__new__(cls)
                cls._initialized = True
        return cls._instance

    def __init__(self) -> None:
        # Prevent re-initialization if __new__ created the instance.
        if not self._initialized:
            # Actual connection setup would happen here.
            self.connection_string: str = "postgresql://user:pass@localhost/sars"
            # Mark as initialized so future calls don't re-run __init__.
            DatabaseConnection._initialized = True

    @classmethod
    def get_connection(cls) -> "DatabaseConnection":
        """
        Returns the shared DatabaseConnection instance.
        Thread-safe via double-checked locking in __new__.
        """
        return cls()

    # Explanation comment:
    # If we used naive lazy initialization without locking:
    #   if _instance is None:
    #       _instance = DatabaseConnection()
    # Two threads could both see _instance as None and create separate instances,
    # violating the singleton property. The lock ensures only one thread can create
    # the instance, and the double-check avoids creating it multiple times if
    # multiple threads wait on the lock.
