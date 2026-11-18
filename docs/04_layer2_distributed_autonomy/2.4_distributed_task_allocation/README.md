# Module 2.4: Distributed Task Allocation

## 1. Module Overview
Module 2.4 implements a decentralized Contract Net Protocol (CNP) task allocation engine, multi-criteria cost evaluation, distributed auction clearance, two-phase task assignment confirmation, and duplicate assignment prevention without a centralized server.

## 2. Submodule Index
- [2.4.1 Task Bidding](task_bidding.md): Contract Net Protocol auction announcement, bid generation, and bid transmission.
- [2.4.2 Cost Evaluation](cost_evaluation.md): Multi-factor cost function formulation (travel distance, battery, risk, capability match).
- [2.4.3 Task Negotiation](task_negotiation.md): Ephemeral auctioneer clearance, bid comparison, tie-breaking, and winner selection.
- [2.4.4 Assignment Confirmation](assignment_confirmation.md): Two-phase commit protocol (Award -> Ack -> Lease Issued).
- [2.4.5 Duplicate Assignment Prevention](duplicate_assignment_prevention.md): Time-bounded lease locks, idempotent task claims, and mutual exclusion.
