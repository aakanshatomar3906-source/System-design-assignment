

from abc import ABC, abstractmethod
from typing import List, Optional

class MarksUpdateObserver(ABC):
    """
    Abstract observer interface for marks update notifications.
    """

    @abstractmethod
    def update(self, student_id: str, new_marks: float) -> None:
        """Receive marks update notification."""
        pass


class EmailNotifier(MarksUpdateObserver):
    """
    Observer that sends email notifications when marks are updated.
    """

    def update(self, student_id: str, new_marks: float) -> None:
        # In real code, this would call an email service.
        print(f"[EmailNotifier] Sending email to student {student_id} about new marks: {new_marks}")


class AuditLogNotifier(MarksUpdateObserver):
    """
    Observer that logs marks updates to an audit system.
    """

    def update(self, student_id: str, new_marks: float) -> None:
        print(f"[AuditLogNotifier] Logging marks update for student {student_id}: {new_marks}")


class MarksUpdateNotifier:
    """
    Subject (publisher) that maintains a list of observers and notifies them
    when marks are updated.
    """

    def __init__(self) -> None:
        self._observers: List[MarksUpdateObserver] = []

    def register(self, observer: MarksUpdateObserver) -> None:
        """Register a new observer."""
        self._observers.append(observer)

    def deregister(self, observer: MarksUpdateObserver) -> None:
        """Remove an observer."""
        self._observers = [o for o in self._observers if o is not observer]

    def notify(self, student_id: str, new_marks: float) -> None:
        """Notify all registered observers about a marks update."""
        for observer in self._observers:
            observer.update(student_id, new_marks)




