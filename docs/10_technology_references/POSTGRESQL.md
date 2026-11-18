# Technology Evaluation: PostgreSQL 14+ with PostGIS & TimescaleDB

## 1. Purpose
ACID-compliant relational, spatial, and time-series database management system.

## 2. Relevant Modules
Module 3.5 Data and Reporting, Module 3.3 Inspection Management.

## 3. Installation Requirements
- **Prerequisites**: Standard Ubuntu repository (`postgresql-14`, `postgresql-14-postgis-3`).

## 4. ROS 2 Compatibility
- **Compatibility Status**: `External integration via Python asyncpg / psycopg3.`

## 5. Advantages
Unmatched reliability, spatial PostGIS indexing for mine assets, TimescaleDB hypertables for telemetry.

## 6. Limitations
Requires server infrastructure; not suitable for running directly on ultra-low-power microcontrollers.

## 7. Adoption Decision
- **Status**: `ADOPTED`
- **Architectural Rationale**: Adopted as the primary operations and inspection database on surface stations and gateway nodes.
