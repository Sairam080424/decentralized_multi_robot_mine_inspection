# Git Workflow & Release Process

## 1. Branch Strategy
The repository adheres to a strict, direct Git workflow:
- `main`: Stable reviewed integration branch representing verified project milestones and production-ready code.
- `feature/<module>-<name>`: Scoped feature branches for individual development, branched directly from `main`.
- `fix/<issue>-<name>`: Scoped defect corrections, branched directly from `main`.
- Pull Requests: All feature and fix branches target `main` directly via Pull Request. Direct pushes to `main` are strictly prohibited.
- Note: No intermediate `develop` branch is utilized unless explicitly justified by clear architectural necessity and approved by the Technical Founder.

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
