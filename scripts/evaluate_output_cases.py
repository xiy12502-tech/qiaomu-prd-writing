#!/usr/bin/env python3
"""Evaluate recorded PRD fixtures; this is not a provider-backed model eval."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def check(output: str, assertions: dict[str, list[str]]) -> dict[str, object]:
    required = assertions.get("required_patterns", [])
    forbidden = assertions.get("forbidden_patterns", [])
    missing = [pattern for pattern in required if not re.search(pattern, output, flags=re.I | re.M)]
    present_forbidden = [pattern for pattern in forbidden if re.search(pattern, output, flags=re.I | re.M)]
    return {"ok": not missing and not present_forbidden, "missing": missing, "forbidden_hits": present_forbidden}


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate recorded output fixtures and label the evidence boundary.")
    parser.add_argument("--cases", default="evals/output_cases.json")
    parser.add_argument("--output", "-o")
    args = parser.parse_args()

    payload = json.loads(Path(args.cases).read_text(encoding="utf-8"))
    results = []
    for case in payload.get("cases", []):
        baseline = check(case.get("baseline_output", ""), case.get("assertions", {}))
        with_skill = check(case.get("with_skill_output", ""), case.get("assertions", {}))
        results.append({"id": case.get("id"), "baseline": baseline, "with_skill": with_skill})

    passed = sum(1 for item in results if item["with_skill"]["ok"])
    result = {
        "ok": passed == len(results) and bool(results),
        "evidence_type": "recorded_fixture",
        "provider_run": "missing evidence",
        "human_blind_review": "missing evidence",
        "summary": {"total": len(results), "with_skill_passed": passed},
        "results": results
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    if not result["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
