import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "lemanon" / "scripts" / "lemanon.py"
CORE_PATHS = {
    "AGENTS.md",
    "knowledge/AGENTS.md",
    "knowledge/README.md",
    "knowledge/PROJECT.md",
    "knowledge/STATUS.md",
    "knowledge/ROADMAP.md",
    "knowledge/SOURCES.md",
    "knowledge/HISTORY.md",
    "knowledge/LESSONS.md",
    "knowledge/handoffs/README.md",
}


def load_lemanon():
    spec = importlib.util.spec_from_file_location("lemanon_cli", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class InitProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lemanon = load_lemanon()

    def test_empty_project_gets_minimum_usable_structure(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            report = self.lemanon.init_project(project)

            self.assertEqual(CORE_PATHS, set(report.created))
            self.assertEqual([], report.existing)
            self.assertEqual([], report.proposals)
            for relative in CORE_PATHS:
                self.assertTrue((project / relative).is_file(), relative)

    def test_existing_agents_file_is_preserved_and_reported_as_proposal(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            agents = project / "AGENTS.md"
            original = b"# Existing rules\n\nDo not replace me.\n"
            agents.write_bytes(original)

            report = self.lemanon.init_project(project)

            self.assertEqual(original, agents.read_bytes())
            self.assertIn("AGENTS.md", report.existing)
            self.assertIn("AGENTS.md", report.proposals)
            self.assertNotIn("AGENTS.md", report.created)

    def test_partial_tree_keeps_custom_files_and_adds_only_missing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            status = project / "knowledge" / "STATUS.md"
            status.parent.mkdir()
            status.write_text("# Custom status\n", encoding="utf-8")

            report = self.lemanon.init_project(project)

            self.assertEqual("# Custom status\n", status.read_text(encoding="utf-8"))
            self.assertIn("knowledge/STATUS.md", report.existing)
            self.assertNotIn("knowledge/STATUS.md", report.created)
            self.assertTrue((project / "knowledge" / "PROJECT.md").is_file())

    def test_dry_run_reports_changes_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)

            report = self.lemanon.init_project(project, dry_run=True)

            self.assertEqual(CORE_PATHS, set(report.created))
            self.assertEqual([], list(project.iterdir()))

    def test_second_run_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.lemanon.init_project(project)

            report = self.lemanon.init_project(project)

            self.assertEqual([], report.created)
            self.assertEqual(CORE_PATHS, set(report.existing))
            self.assertEqual([], report.proposals)

    def test_project_path_with_spaces_works_through_cli_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project with spaces"
            project.mkdir()

            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "init", str(project), "--json"],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(0, completed.returncode, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(CORE_PATHS, set(payload["created"]))
            self.assertTrue((project / "knowledge" / "STATUS.md").is_file())


if __name__ == "__main__":
    unittest.main()
