# Security Policy

## 1. Supported Versions
Security patches and updates are currently provided for:

| Version | Supported |
|---|---|
| 0.1.x (Milestone M0) | Yes |

---

## 2. Reporting a Vulnerability
We prioritize the physical safety of autonomous robotics and data confidentiality in industrial mining:
1. **Reporting Channel**: Do not submit public GitHub issues for security vulnerabilities.
2. **Contact**: Report security vulnerabilities directly to the platform founder at `sairam@example.com` with subject line `[SECURITY] Subterranean Autonomy Platform`.
3. **Disclosure Policy**: We follow responsible disclosure principles. Vulnerabilities will be addressed and patched within 7 business days before public disclosure.

---

## 3. Robotics & Safety Critical Invariants
- The **Local Safety Manager** (Layer 1) must never be bypassed by remote network messages.
- Any vulnerability that allows remote execution or actuator override without local safety arbitrations is classified as **CRITICAL P0**.
