import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "lemanon" / "scripts" / "lemanon.py"


def load_lemanon():
    spec = importlib.util.spec_from_file_location("lemanon_audit_cli", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AuditProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lemanon = load_lemanon()

    def make_project(self, root: Path) -> Path:
        self.lemanon.init_project(root)
        return root

    def findings(self, report, severity: str, code: str):
        return [item for item in getattr(report, severity) if item.code == code]

    def test_missing_core_files_are_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = self.lemanon.audit_project(Path(tmp))

            paths = {item.path for item in self.findings(report, "error", "missing-core")}
            self.assertIn("knowledge/STATUS.md", paths)
            self.assertIn("knowledge/PROJECT.md", paths)

    def test_broken_relative_markdown_link_is_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.make_project(Path(tmp))
            (project / "knowledge" / "PROJECT.md").write_text(
                "# Project\n\nSee [missing](decisions/no-record.md).\n",
                encoding="utf-8",
            )

            report = self.lemanon.audit_project(project)

            findings = self.findings(report, "warning", "broken-link")
            self.assertEqual(["knowledge/PROJECT.md"], [item.path for item in findings])

    def test_secret_is_error_and_value_is_redacted(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.make_project(Path(tmp))
            secret = "AK" + "IA" + "A" * 16
            (project / "credential.txt").write_text(secret, encoding="utf-8")

            report = self.lemanon.audit_project(project)
            payload = json.dumps(report.to_dict())

            self.assertEqual(1, len(self.findings(report, "error", "suspected-secret")))
            self.assertNotIn(secret, payload)

    def test_personal_absolute_path_is_warning_and_username_is_redacted(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.make_project(Path(tmp))
            username = "private-person"
            (project / "knowledge" / "SOURCES.md").write_text(
                f"Source: /{'Users'}/{username}/private/project\n",
                encoding="utf-8",
            )

            report = self.lemanon.audit_project(project)
            payload = json.dumps(report.to_dict())

            self.assertEqual(1, len(self.findings(report, "warning", "personal-path")))
            self.assertNotIn(username, payload)

    def test_large_file_can_be_allowlisted_but_secret_cannot(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.make_project(Path(tmp))
            large = project / "reference.bin"
            secret = "AK" + "IA" + "B" * 16
            large.write_bytes((b"x" * (1024 * 1024 + 1)) + secret.encode("ascii"))

            first = self.lemanon.audit_project(project)
            self.assertEqual(1, len(self.findings(first, "warning", "large-file")))
            self.assertEqual(1, len(self.findings(first, "error", "suspected-secret")))

            (project / ".lemanon-audit.json").write_text(
                json.dumps({"large_files": ["reference.bin"]}), encoding="utf-8"
            )
            second = self.lemanon.audit_project(project)

            self.assertEqual([], self.findings(second, "warning", "large-file"))
            self.assertEqual(1, len(self.findings(second, "error", "suspected-secret")))

    def test_old_last_verified_date_is_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.make_project(Path(tmp))
            (project / "knowledge" / "STATUS.md").write_text(
                "# Current status\n\n- Last verified: 2000-01-01\n",
                encoding="utf-8",
            )

            report = self.lemanon.audit_project(project)

            self.assertEqual(1, len(self.findings(report, "warning", "stale-status")))

    def test_freshly_initialized_project_has_no_errors_or_warnings(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.make_project(Path(tmp))

            report = self.lemanon.audit_project(project)

            self.assertEqual([], report.error)
            self.assertEqual([], report.warning)

    def test_audit_does_not_modify_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = self.make_project(Path(tmp))
            before = {
                path.relative_to(project): path.read_bytes()
                for path in project.rglob("*")
                if path.is_file()
            }

            self.lemanon.audit_project(project)

            after = {
                path.relative_to(project): path.read_bytes()
                for path in project.rglob("*")
                if path.is_file()
            }
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
