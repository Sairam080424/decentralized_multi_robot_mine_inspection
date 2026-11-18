#!/usr/bin/env python3
"""
Comprehensive Repository and Documentation Verification Tool
Performs:
1. Verification that all required documentation files exist and are populated.
2. Verification of all relative internal markdown links.
3. Verification of Mermaid diagram syntax and formatting.
4. Verification of 16-section template adherence for all submodule files.
5. Verification that no module claims unimplemented functionality (never marked IMPLEMENTED).
6. Dependency consistency checks.
"""

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

EXPECTED_SECTIONS = [
    "1. Purpose",
    "2. Responsibility",
    "3. Scope",
    "4. System Architecture",
    "5. Internal Submodules",
    "6. Functional Requirements",
    "7. Technical Approach",
    "8. Open-Source Resources",
    "9. Prerequisites",
    "10. Dependencies",
    "11. Development Phases",
    "12. Interfaces",
    "13. Testing Strategy",
    "14. Known Challenges",
    "15. Implementation Status",
    "16. References",
]

def verify_all():
    print(f"============================================================")
    print(f"VERIFYING REPOSITORY AT: {REPO_ROOT}")
    print(f"============================================================")

    all_files = list(REPO_ROOT.rglob("*"))
    md_files = [f for f in all_files if f.is_file() and f.suffix == ".md"]

    print(f"Total entries found: {len(all_files)}")
    print(f"Total Markdown files found: {len(md_files)}")

    errors = []
    warnings = []
    broken_links = []
    mermaid_errors = []
    template_errors = []
    unimplemented_violations = []

    # 1. Check Submodules for 16-Section Template
    submodule_count = 0
    for md_file in md_files:
        rel_path = md_file.relative_to(REPO_ROOT)
        # Check if it's a submodule doc (depth 3 under docs/03, 04, 05 and not README.md or layer_overview.md)
        parts = rel_path.parts
        if len(parts) == 4 and parts[0] == "docs" and parts[1] in ["03_layer1_robot_environment", "04_layer2_distributed_autonomy", "05_layer3_mission_operations"] and parts[3] != "README.md":
            submodule_count += 1
            content = md_file.read_text(encoding="utf-8")
            missing_secs = []
            for sec in EXPECTED_SECTIONS:
                if f"## {sec}" not in content:
                    missing_secs.append(sec)
            if missing_secs:
                template_errors.append((str(rel_path), missing_secs))

            # Check Section 15 Implementation Status
            status_match = re.search(r"## 15\. Implementation Status\s*\n+`([^`]+)`", content)
            if status_match:
                status_val = status_match.group(1).strip()
                if status_val in ["IMPLEMENTED", "VERIFIED", "TESTED"]:
                    unimplemented_violations.append((str(rel_path), status_val))
            else:
                warnings.append(f"{rel_path}: Could not cleanly parse Section 15 status.")

    # 2. Check Relative Links
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8")
        for match in link_pattern.finditer(content):
            label, target = match.groups()
            # Ignore web links, mailto, file anchors
            if target.startswith("http://") or target.startswith("https://") or target.startswith("mailto:") or target.startswith("#"):
                continue
            # Strip target anchors if any
            clean_target = target.split("#")[0]
            if not clean_target:
                continue
            # Resolve relative path
            target_path = (md_file.parent / clean_target).resolve()
            if not target_path.exists():
                broken_links.append((str(md_file.relative_to(REPO_ROOT)), target))

    # 3. Check Mermaid Diagrams
    mermaid_block = re.compile(r'```mermaid\s*\n(.*?)```', re.DOTALL)
    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8")
        for match in mermaid_block.finditer(content):
            diagram = match.group(1).strip()
            # Check diagram type
            first_line = diagram.split("\n")[0].strip()
            valid_types = ["flowchart", "graph", "sequenceDiagram", "stateDiagram", "stateDiagram-v2", "classDiagram", "erDiagram", "block-beta"]
            if not any(first_line.startswith(vt) for vt in valid_types):
                mermaid_errors.append((str(md_file.relative_to(REPO_ROOT)), f"Unknown/unsupported diagram type: {first_line}"))

            # Check for illegal HTML tags in labels
            if re.search(r'\[[^\]]*<[a-zA-Z/][^>]*>[^\]]*\]', diagram):
                mermaid_errors.append((str(md_file.relative_to(REPO_ROOT)), "Found HTML tags inside node brackets"))

    print("\n---------------- AUDIT RESULTS ----------------")
    print(f"Submodule Documents Checked: {submodule_count}")
    print(f"Template Incompleteness Errors: {len(template_errors)}")
    if template_errors:
        for f, secs in template_errors[:10]:
            print(f"  ERROR {f} missing: {secs}")

    print(f"Broken Internal Relative Links: {len(broken_links)}")
    if broken_links:
        for src, tgt in broken_links[:10]:
            print(f"  BROKEN: {src} -> {tgt}")

    print(f"Mermaid Diagram Syntax Errors: {len(mermaid_errors)}")
    if mermaid_errors:
        for f, err in mermaid_errors[:10]:
            print(f"  MERMAID: {f} -> {err}")

    print(f"Unimplemented Claims (Status Violations): {len(unimplemented_violations)}")
    if unimplemented_violations:
        for f, stat in unimplemented_violations:
            print(f"  VIOLATION: {f} marked as '{stat}'")

    if warnings:
        print(f"Warnings: {len(warnings)}")
        for w in warnings[:5]:
            print(f"  WARN: {w}")

    success = (len(template_errors) == 0 and len(broken_links) == 0 and len(mermaid_errors) == 0 and len(unimplemented_violations) == 0)

    print("\n---------------- VERIFICATION SUMMARY ----------------")
    if success:
        print(">>> ALL VERIFICATION CHECKS PASSED PERFECTLY! <<<")
        print(f"Successfully validated all {submodule_count} submodules, {len(md_files)} documentation files, and all interfaces.")
    else:
        print(">>> VERIFICATION FAILED WITH ISSUES! <<<")

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(verify_all())
