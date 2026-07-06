# TASK 2.3 A

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

# -------------------------
# Student class
# -------------------------

@dataclass
class Student:
    """
    Represents a student in the system.
    Attributes:
        - student_id: str
        - name: str
        - email: str
        - enrolled_courses: List[Enrollment]
    """
    student_id: str
    name: str
    email: str
    enrolled_courses: List["Enrollment"]

    def add_enrollment(self, enrollment: "Enrollment") -> None:
        """Add an enrollment to the student's list."""
        self.enrolled_courses.append(enrollment)

    def get_enrolled_course_ids(self) -> List[str]:
        """Return list of course IDs this student is enrolled in."""
        return [e.course_id for e in self.enrolled_courses]

    # NOTE: This class does NOT contain any email notification methods.
    # This embodies the **Interface Separation Principle (ISP)**:
    # Student should not be forced to implement unrelated behavior like sending emails.
    # Email sending is delegated to a separate notification service.


# -------------------------
# Enrollment class and extension
# -------------------------

class Enrollment(ABC):
    """
    Base class for course enrollments.
    Attributes:
        - student_id: str
        - course_id: str
        - enrollment_date: str (ISO date)
    Methods:
        - is_active() -> bool
    """
    def __init__(self, student_id: str, course_id: str, enrollment_date: str):
        self.student_id: str = student_id
        self.course_id: str = course_id
        self.enrollment_date: str = enrollment_date

    @abstractmethod
    def is_active(self) -> bool:
        """Return True if this enrollment is currently active."""
        pass

    # This base class is open for extension via subclasses (e.g., WaitlistedEnrollment).
    # New behaviors can be added by creating new subclasses without modifying Enrollment.
    # This embodies the **Open/Closed Principle (OCP)**.


@dataclass
class RegularEnrollment(Enrollment):
    """
    A regular (non-waitlisted) enrollment.
    """
    grade: str | None = None

    def is_active(self) -> bool:
        # Assume active if not withdrawn; simplified logic.
        return True


@dataclass
class WaitlistedEnrollment(Enrollment):
    """
    A waitlisted enrollment (extension of Enrollment).
    """
    waitlist_position: int

    def is_active(self) -> bool:
        # Waitlisted is not active until moved to regular.
        return False


# TASK 2.3 B

class EnrollmentRepository(ABC):
    """
    Interface for database operations related to enrollments.
    Methods:
        - save(enrollment: Enrollment) -> None
        - get_by_student_id(student_id: str) -> List[Enrollment]
        - get_by_course_id(course_id: str) -> List[Enrollment]
    """

    @abstractmethod
    def save(self, enrollment: Enrollment) -> None:
        """Persist an enrollment to the database."""
        pass

    @abstractmethod
    def get_by_student_id(self, student_id: str) -> List[Enrollment]:
        """Return all enrollments for a given student."""
        pass

    @abstractmethod
    def get_by_course_id(self, course_id: str) -> List[Enrollment]:
        """Return all enrollments for a given course."""
        pass
