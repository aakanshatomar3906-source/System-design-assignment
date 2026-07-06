# System-design-assignment

"""
Observer Pattern Role (Task 2.3d):

The Observer pattern allows the Admin Panel (via MarksUpdateNotifier) to emit
a single "marks updated" event without knowing which services need to react.
EmailNotifier and AuditLogNotifier are registered as observers and decide
how to handle the event.

This keeps the Admin Panel loosely coupled from the notification services:
- The Admin Panel does not import or directly call Email Service or Audit Log Service.
- New notification services can be added by implementing MarksUpdateObserver and
  registering them, without changing the Admin Panel code.
- This improves modularity, maintainability, and extensibility.
"""
