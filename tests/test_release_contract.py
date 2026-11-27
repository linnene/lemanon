import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "lemanon" / "scripts" / "lemanon.py"


def load_lemanon():
    spec = importlib.util.spec_from_file_location("lemanon_release", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ReleaseContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lemanon = load_lemanon()

    def test_repository_audits_without_errors_or_warnings(self):
        report = self.lemanon.audit_project(ROOT)
        self.assertEqual([], report.error)
        self.assertEqual([], report.warning)

    def test_public_repository_guidance_exists(self):
        security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("privately", security.lower())
        self.assertIn("synthetic", contributing.lower())
        self.assertIn("remote", contributing.lower())

    def test_ci_runs_the_same_suite_and_repository_audit(self):
        workflow = (ROOT / ".github" / "workflows" / "checks.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("python -m unittest discover -s tests -v", workflow)
        self.assertIn("python skills/lemanon/scripts/lemanon.py audit . --json", workflow)
        self.assertIn("ubuntu-latest", workflow)


if __name__ == "__main__":
    unittest.main()
