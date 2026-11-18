# Mission Schema Specification

## 1. Schema Definition
Defines complex multi-task missions structured as Directed Acyclic Graphs (DAGs).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "MissionSpecification",
  "type": "object",
  "required": ["mission_id", "mission_name", "tasks"],
  "properties": {
    "mission_id": { "type": "string", "format": "uuid" },
    "mission_name": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" },
    "max_duration_sec": { "type": "number" },
    "tasks": {
      "type": "array",
      "items": { "$ref": "task_schema.json" }
    }
  }
}
```
