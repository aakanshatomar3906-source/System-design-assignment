# System-design-assignment
# SARS – Software System Design

This repository contains the high-level and low-level design for the **Student Academic Result System (SARS)**, a public-facing web application expected to serve 50,000 concurrent users during examination result publication.

---

## Architecture Decisions (Task 2.1)

### Why Microservices?

SARS is designed using a **microservices architecture** rather than a monolithic one. The main reasons are:

- **Independent deployment**: Each module (Authentication, Student Portal, Admin Panel, Email Notification, Audit Log) can be developed, tested, and deployed independently. This allows faster iteration and reduces the risk of impacting the entire system when updating a single feature.
- **Fault isolation**: Failures in one service (e.g., Email Notification) do not bring down the entire application. In a monolithic design, a failure in any component can crash the whole system, which is unacceptable during result publication.
- **Scalability**: High-concurrency modules (especially Student Portal) can be scaled independently by adding more instances, rather than scaling the entire application.

While microservices introduce higher operational complexity (service discovery, distributed logging, monitoring), these costs are justified by the need for high availability, scalability, and resilience under 50,000 concurrent users.

### Scaling and Load Balancing

- **Horizontal scaling** is used for web servers: multiple identical instances are added or removed based on demand, rather than upgrading a single server.
- A **load balancer** distributes traffic using the **round-robin algorithm**, which evenly distributes requests across available servers and is suitable when servers are homogeneous and request costs are similar.

### Elasticity

Elasticity allows SARS to:
- **Scale up** automatically during peak periods (e.g., result publication) by adding more web server instances.
- **Scale down** during off-peak periods (e.g., semester breaks) to reduce costs, while still maintaining minimal availability.

---

## SOLID Principles Application (Task 2.3a–b)

### Interface Separation Principle (ISP)

- The **Student** class does **not** contain methods for sending email notifications.
- Email sending is delegated to a separate notification service (e.g., `EmailNotifier`).
- This ensures that `Student` only exposes behavior relevant to student data and enrollments, avoiding “unnecessary” methods that other clients do not need.

### Open/Closed Principle (OCP)

- The **Enrollment** base class is designed as an abstract class, open for extension via subclasses such as `RegularEnrollment` and `WaitlistedEnrollment`.
- New enrollment behaviors can be added by creating new subclasses without modifying the existing `Enrollment` class.
- This keeps the base class stable while allowing the system to evolve.

### Dependency Inversion Principle (DIP)

- The `Enrollment` class (and services that use it) depends on the **`EnrollmentRepository` interface**, not on a concrete database implementation.
- High-level modules (business logic) depend on abstractions, and low-level modules (database access) also implement these abstractions.
- This allows swapping database implementations (e.g., SQL, NoSQL, or test mocks) without changing business logic.

---

## Observer Pattern Rationale (Task 2.3d)

The **Observer pattern** is used to notify the Email Service and Audit Log Service whenever a student’s marks are updated.

### Structure

- **Subject**: `MarksUpdateNotifier` maintains a list of observers and notifies them when marks change.
- **Observers**: `EmailNotifier` and `AuditLogNotifier` implement the `MarksUpdateObserver` interface with an 
