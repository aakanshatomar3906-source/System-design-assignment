Task 2.1 — Requirements and Architecture Choice
a. Functional and Non-Functional Requirements
Functional requirements:

Authentication: Users (students, faculty, admins) must be able to log in with a unique username/email and password, and the system must verify credentials and issue a session token.

Student Portal – View Marks: A logged-in student must be able to view their examination results (course code, course name, marks, grade) for selected semesters.

Student Portal – Course Enrollment: A logged-in student must be able to enroll in available courses for the current semester, subject to eligibility and capacity constraints.

Non-functional requirements:

Support 50,000 concurrent users during result publication

Primary design principle: Scalability

The system must handle high concurrency without performance degradation.

The system must remain available with at least 99.9% uptime during examination periods

Primary design principle: Availability

Minimal downtime is critical during result publication.

All student data and authentication credentials must be protected against unauthorized access and common web attacks

Primary design principle: Security

Includes encryption, secure authentication, and protection against OWASP-top risks.

(You could also add reliability or maintainability as additional non-functional requirements if needed.)

b. Monolithic vs Microservices Architecture
Comparison dimensions:

Independent deployment

Monolithic: All modules (Authentication, Student Portal, Admin Panel) are built, tested, and deployed as a single artifact. Changing one module usually requires redeploying the whole application.

Microservices: Each module is an independent service with its own codebase, build, and deployment pipeline. You can update the Student Portal without touching Authentication or Admin Panel.

Fault isolation

Monolithic: A bug or crash in any module can bring down the entire application. Failure in email notifications could block marks viewing.

Microservices: Services are isolated; if Email Notification crashes, Student Portal and Admin Panel can continue functioning. Failures are contained per service.

Management complexity

Monolithic: simpler to develop, test, and deploy initially; fewer operational concerns (no distributed tracing, service discovery, etc.).

Microservices: higher operational complexity: need load balancing, service discovery, distributed logging, monitoring, handling network failures, versioning, etc.

Recommendation for 50,000 concurrent users:

For SARS at this scale, microservices architecture is recommended. The high concurrency and critical availability during result publication demand strong fault isolation and the ability to scale individual modules (e.g., Student Portal) independently. While microservices increase management complexity, the benefits in scalability, independent deployment, and resilience outweigh this cost for a public-facing, high-stakes system. A monolith would be harder to scale and more fragile under load, where a single module failure could impact all users.

Task 2.2 — High-Level Design
a. Main Components and Interfaces
Authentication Service

Responsibility: Handle user registration, login, token issuance, and session validation.

Interface: REST API (e.g., /auth/login, /auth/validate-token) for other services; internal database access for user credentials.

Student Portal Service

Responsibility: Provide endpoints for students to view marks, enroll in courses, and view course details.

Interface: REST API (e.g., /students/marks, /students/enroll) for frontend; dependencies on Student DB, Course DB, and Enrollment Repository.

Admin Panel Service

Responsibility: Allow admins/faculty to manage students, courses, faculty, and update marks.

Interface: REST API (e.g., /admin/students, /admin/courses, /admin/marks) for admin frontend; dependencies on Student DB, Course DB, Faculty DB, and Marks DB.

Email Notification Service

Responsibility: Send emails for events like enrollment confirmation, marks update notifications, and system alerts.

Interface: REST API or message queue consumer (e.g., receives events from Admin Panel or Student Portal); internal access to email provider.

Audit Log Service

Responsibility: Record important system events (mark updates, enrollments, admin actions) for compliance and debugging.

Interface: REST API or message queue consumer; internal access to audit log storage.

Shared Databases (or per-service DBs)

Responsibility: Persist data for students, courses, faculty, enrollments, marks, audit logs.

Interface: Database query interface (SQL/NoSQL) accessed by respective services.

You can choose per-service databases or a shared DB; in microservices, per-service DBs are common to enforce loose coupling.

b. Layered Architecture for Student Portal
Layers:

Presentation Layer

What it does: Handles HTTP requests from the web frontend (e.g., React app), parses input, and returns responses (JSON).

Data flow:

Receives: HTTP request (e.g., GET /students/marks?semester=3).

Passes on: Extracted parameters (student_id, semester) to the Business Layer via method calls or internal API.

Receives back: Domain objects (marks list) from Business Layer.

Returns: HTTP response with JSON.

Business Layer

What it does: Implements business logic: eligibility checks, enrollment rules, marks aggregation, validation.

Data flow:

Receives: Parameters from Presentation Layer.

Calls: Data Access Layer to fetch student records, course info, current enrollments.

Processes: Applies rules (e.g., max courses, prerequisite checks).

Passes on: Result objects (e.g., list of marks, enrollment status) back to Presentation Layer.

Data Access Layer

What it does: Encapsulates all database interactions; provides repository-style methods.

Data flow:

Receives: Queries from Business Layer (e.g., get_marks(student_id, semester)).

Executes: SQL queries or ORM calls against the database.

Returns: Raw or mapped data objects (e.g., MarksRecord, EnrollmentRecord) to Business Layer.

This layered design keeps concerns separated: HTTP handling, business rules, and data access are independent.

c. Scaling Strategy and Load Balancing
Scaling approach:

Use horizontal scaling for web servers rather than vertical scaling.

Reason: Horizontal scaling (adding more server instances) better supports 50,000 concurrent users, allows incremental capacity increases, and improves fault tolerance. Vertical scaling (upgrading a single server) has limits, is more expensive, and creates a single point of failure.

Load balancing:

A load balancer sits between clients and web servers, distributing incoming HTTP requests.

Algorithm: Round-robin is suitable here because:

Requests are generally similar in cost.

It provides even distribution without needing per-request state.

It’s simple and effective when servers are homogeneous.

The load balancer sends each new request to the next server in a circular order, ensuring all three servers get roughly equal traffic.

d. Elasticity for Cost Optimization
Elasticity means the system can automatically add or remove resources based on demand.

During off-peak periods (e.g., semester breaks):

The cloud orchestrator detects low traffic and reduces the number of web server instances (e.g., from 10 to 2).

This reduces compute costs while still maintaining minimal availability.

During peak periods (result publication):

The system detects high concurrency and automatically adds more instances (e.g., up to 20).

This ensures capacity without manual intervention.

Elasticity ensures SARS uses only as much infrastructure as needed, optimizing cost while maintaining performance.

e. Session Routing Problem and Resolution Strategies
Problem name:

This is the session consistency / distributed session problem caused by stateless load balancing with server-local sessions. More specifically, it’s a session routing inconsistency problem: subsequent requests for the same user may hit different servers that don’t share session state.

Strategy 1 – Routing-based (sticky sessions):

Modify the load balancer to use sticky sessions (also called session-affinity).

Once a user’s first request is routed to Server A, all subsequent requests for that user are always routed to Server A.

Trade-off:

Reduces fault tolerance: if Server A crashes, that user’s session is lost until they re-login.

Also can lead to uneven load if some users are much more active than others.

Strategy 2 – Storage-based (centralized session store):

Move session storage from in-memory per-server to a shared session store (e.g., Redis, database).

All web servers read/write sessions to this central store.

Trade-off:

Introduces a dependency on the session store; if it fails, authentication may break.

Adds network latency and cost for session access, but improves fault tolerance and allows any server to handle any request.
