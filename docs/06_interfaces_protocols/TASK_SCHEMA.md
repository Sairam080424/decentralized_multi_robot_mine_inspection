# Task Schema Specification

## 1. Schema Definition
Defines atomic tasks created during mission decomposition and negotiated during Contract Net Protocol auctions.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "TaskDefinition",
  "type": "object",
  "required": ["task_id", "task_type", "target_location", "required_sensors", "priority", "dwell_time_sec"],
  "properties": {
    "task_id": { "type": "string", "format": "uuid" },
    "task_type": {
      "type": "string",
      "enum": ["EXPLORE_FRONTIER", "NAVIGATE_WAYPOINT", "INSPECT_THERMAL", "INSPECT_VISUAL", "RENDEZVOUS"]
    },
    "target_location": {
      "type": "object",
      "required": ["x", "y", "z"],
      "properties": {
        "x": { "type": "number" },
        "y": { "type": "number" },
        "z": { "type": "number" },
        "yaw_deg": { "type": "number" }
      }
    },
    "required_sensors": {
      "type": "array",
      "items": { "type": "string" }
    },
    "priority": { "type": "integer", "minimum": 1, "maximum": 100 },
    "dwell_time_sec": { "type": "number", "minimum": 0.0 },
    "arrival_tolerance_m": { "type": "number", "default": 0.3 },
    "dependencies": {
      "type": "array",
      "items": { "type": "string", "format": "uuid" }
    }
  }
}
```
