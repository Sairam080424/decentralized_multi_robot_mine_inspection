# Security Policy

## 1. Supported Versions
Security patches and updates are currently provided for:

| Version | Supported |
|---|---|
| 0.1.x (Milestone M0) | Yes |

---

## 2. Reporting a Vulnerability
We prioritize the physical safety of autonomous robotics and data confidentiality in industrial mining. If you discover a security vulnerability or safety-critical defect, please report it responsibly:

1. **Verified Reporting Channel**:
   - Report security vulnerabilities privately through **GitHub Security Advisories**:
     Navigate to [Security Advisories](https://github.com/Sairam080424/decentralized_multi_robot_mine_inspection/security/advisories/new) and select **"Report a vulnerability"**.
   - Alternatively, use GitHub's **Private Vulnerability Reporting** feature directly on the repository's `Security` tab.
   - **Do NOT** submit public GitHub issues, pull requests, or forum discussions for sensitive vulnerabilities.

2. **Required Report Details**:
   - Description of the vulnerability and affected subsystem (e.g., Layer 1 Safety Manager, Layer 2 Zenoh Mesh, Layer 3 Ingestion API).
   - Clear reproduction steps, proof-of-concept scripts, or simulation scenarios.
   - Assessment of safety impact (e.g., potential for remote motor override, denial-of-service, or sensor spoofing).

3. **Response & Disclosure Timeline**:
   - **Initial Acknowledgement**: Within 48 hours of submission.
   - **Triage & Assessment**: Within 5 business days.
   - **Patch & Advisory Release**: Coordinated fix deployed within 14 business days before any public disclosure.

---

## 3. Robotics & Safety Critical Invariants
- The **Local Safety Manager** (Layer 1) must never be bypassed by remote network messages.
- Any vulnerability that allows remote execution or actuator override without local safety arbitrations is classified as **CRITICAL P0**.
