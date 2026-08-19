from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_prd.py"
FIXTURES = ROOT / "tests" / "fixtures"


def run_fixture(name: str, profile: str = "auto") -> tuple[int, dict[str, object]]:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(FIXTURES / name), "--profile", profile],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, json.loads(result.stdout)


class ValidatePrdTests(unittest.TestCase):
    def test_valid_standard(self) -> None:
        code, payload = run_fixture("valid-standard.md")
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["profile"], "standard")

    def test_valid_lean(self) -> None:
        code, payload = run_fixture("valid-lean.md")
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["profile"], "lean")

    def test_invalid_document_reports_actionable_errors(self) -> None:
        code, payload = run_fixture("invalid.md")
        self.assertEqual(code, 2)
        self.assertFalse(payload["ok"])
        self.assertGreaterEqual(len(payload["errors"]), 5)
        warning_codes = {item["code"] for item in payload["warnings"]}
        self.assertIn("vague_language", warning_codes)

    def test_auto_profile_fails_safe_to_standard(self) -> None:
        code, payload = run_fixture("missing-requirement-id.md")
        self.assertEqual(payload["profile"], "standard")
        self.assertEqual(code, 2)
        error_codes = {item["code"] for item in payload["errors"]}
        self.assertIn("missing_requirement_ids", error_codes)


if __name__ == "__main__":
    unittest.main()
