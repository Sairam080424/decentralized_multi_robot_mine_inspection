# Submodule 3.6.2: Mission APIs (OpenAPI / WebSockets)

## 1. Purpose
Defines the formal REST and WebSocket API specifications for enterprise integration, surface dispatch, and operator consoles.

## 2. Responsibility
Expose OpenAPI 3.0 documented REST endpoints for CRUD operations and WebSockets for real-time telemetry streaming; enforce authentication and rate limiting.

## 3. Scope
### In-Scope
OpenAPI 3.0 specification (`openapi.yaml`), FastAPI route definitions, JWT bearer token authentication, and WebSocket session management.

### Out-of-Scope
Internal inter-robot Zenoh gossip protocols.

## 4. System Architecture
```mermaid
flowchart TD
    Client["External Client / Web UI"] --> Gateway["FastAPI API Gateway (Port 8000)"]
    Gateway --> Auth["JWT Bearer Authentication & Rate Limiter"]
    Auth --> Routes{"API Route Dispatcher"}
    Routes -->|POST /api/v1/missions| M_Submit["Mission Submission Route"]
    Routes -->|GET /api/v1/fleet| F_Status["Fleet Status Route"]
    Routes -->|GET /api/v1/evidence/{id}| E_Fetch["Evidence Fetch Route"]
    Routes -->|WS /ws/telemetry| WS_Stream["WebSocket Live Telemetry Stream"]
    M_Submit --> L3_Core["Layer 3 Core Services"]
    F_Status --> L3_Core
    E_Fetch --> L3_Core
    WS_Stream --> L3_Core
```

## 5. Internal Submodules
- **FastAPI Route Controller**: Implements typed request/response handlers with automated Pydantic serialization.
- **WebSocket Connection Hub**: Broadcasts 5 Hz telemetry and event frames to active browser sessions.

## 6. Functional Requirements
- **REQ-3.6-003**: All REST endpoints shall be documented with interactive OpenAPI 3.0 Swagger UI documentation.
- **REQ-3.6-004**: REST endpoints shall respond with mean latency `[PROPOSED TARGET: < 30 ms]` under 100 concurrent requests.

## 7. Technical Approach
Deploy FastAPI in Python 3.10 with Uvicorn ASGI server. Secure endpoints with OAuth2 / JWT bearer tokens. Generate interactive documentation at `/docs`.

## 8. Open-Source Resources
### FastAPI
- **What it provides**: Modern, fast web framework for building APIs with Python.
- **Why it is relevant**: High-performance async web framework with automatic OpenAPI documentation.
- **What we can reuse**: FastAPI routing and dependency injection.
- **What we must develop ourselves**: Robotics API routes.


## 9. Prerequisites
Python 3.10+, FastAPI, Uvicorn.

## 10. Dependencies
- **Upstream Dependencies**: Submodule 3.5.1 Mission Database.
- **Downstream Dependencies**: Submodule 3.6.1 Public SDK, Submodule 3.4.1 Map Visualization.
- **Interfaces with Other Modules**: HTTP Port 8000.

## 11. Development Phases
### Phase 1: API Gateway Implementation
- **Objective**: Implement FastAPI routes and OpenAPI documentation.
- **Activities**: Code route handlers, integrate database queries, test Swagger UI.
- **Required resources**: FastAPI, Uvicorn.
- **Input**: Route specifications.
- **Output**: Running REST API server.
- **Dependencies**: None.
- **Validation**: Execute curl test on `/api/v1/fleet`; verify JSON response.
- **Completion criteria**: Swagger UI accessible at `/docs` with all endpoints.


## 12. Interfaces
### OpenAPI
- `docs/06_interfaces_protocols/openapi.yaml`: Formal OpenAPI 3.0 specification.


## 13. Testing Strategy
Execute automated Locust load test simulating 50 concurrent operators querying fleet telemetry; verify zero errors and 99th percentile latency < 50 ms.

## 14. Known Challenges
- **WebSocket Connection Drops**: Operators moving tablets between surface Wi-Fi APs experience drops; client must implement exponential backoff reconnects without missing critical events.

## 15. Implementation Status
`PLANNED`

## 16. References
- [FastAPI Documentation](https://fastapi.tiangolo.com)
