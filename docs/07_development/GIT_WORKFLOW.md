# Git Workflow & Release Process

## 1. Branch Strategy
- `main`: Release-ready code corresponding to verified project milestones.
- `develop`: Nightly active development and feature integration.
- `feature/<module>-<name>`: Scoped feature development branched from `develop`.

## 2. Commit Format (Conventional Commits)
```text
<type>(<scope>): <summary in imperative mood>

[optional detailed description]

Refs: #<issue_number>
```
Example: `feat(layer2_alloc): implement Contract Net Protocol bid comparator`

## 3. Remote Synchronization
Target GitHub Remote:
`https://github.com/Sairam080424/decentralized_multi_robot_mine_inspection`
