# Capability Schema Specification

## 1. Schema Definition
The capability schema defines the declarative format used by robots to advertise their mobility, sensor payloads, and resources.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "RobotCapability",
  "type": "object",
  "required": ["robot_id", "archetype", "locomotion", "sensors", "actions", "resources"],
  "properties": {
    "robot_id": { "type": "string", "format": "uuid" },
    "archetype": { "type": "string", "enum": ["EXPLORATION_SCOUT", "INSPECTION_SPECIALIST"] },
    "locomotion": {
      "type": "object",
      "required": ["type", "max_linear_speed", "max_incline_deg"],
      "properties": {
        "type": { "type": "string", "enum": ["DIFFERENTIAL_DRIVE", "TRACKED_SKID_STEER"] },
        "max_linear_speed": { "type": "number", "minimum": 0.1 },
        "max_incline_deg": { "type": "number", "minimum": 0.0, "maximum": 45.0 }
      }
    },
    "sensors": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["LIDAR_3D", "RGB_OPTICAL", "RADIOMETRIC_THERMAL", "IMU_6DOF", "GAS_DETECTOR"]
      }
    },
    "actions": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["EXPLORE_FRONTIER", "NAVIGATE_WAYPOINT", "INSPECT_THERMAL", "INSPECT_VISUAL", "RENDEZVOUS"]
      }
    },
    "resources": {
      "type": "object",
      "required": ["battery_soc_percent", "disk_free_gb"],
      "properties": {
        "battery_soc_percent": { "type": "number", "minimum": 0.0, "maximum": 100.0 },
        "disk_free_gb": { "type": "number", "minimum": 0.0 }
      }
    }
  }
}
```
