import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "lemanon" / "scripts" / "lemanon.py"
TEMPLATE = ROOT / "skills" / "lemanon" / "assets" / "scaffold" / "templates" / "HANDOFF.md"
ADAPTER = ROOT / "adapters" / "claude-code"
EXAMPLE = ROOT / "examples" / "sample-project" / "README.md"


def load_lemanon():
    spec = importlib.util.spec_from_file_location("lemanon_e2e", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class EndToEndTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lemanon = load_lemanon()

    def test_synthetic_project_preserves_rules_audits_cleanly_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "signal-garden"
            project.mkdir()
            agents = project / "AGENTS.md"
            original = "# Project rules\n\nRead `knowledge/AGENTS.md` before acting.\n"
            agents.write_text(original, encoding="utf-8")

            first = self.lemanon.init_project(project)
            self.assertEqual(original, agents.read_text(encoding="utf-8"))
            self.assertIn("AGENTS.md", first.existing)
            self.assertNotIn("AGENTS.md", first.proposals)

            handoff = project / "knowledge" / "handoffs" / "codex" / "sample.md"
            handoff.parent.mkdir(parents=True)
            shutil.copyfile(TEMPLATE, handoff)

            audit = self.lemanon.audit_project(project)
            self.assertEqual([], audit.error)
            self.assertEqual([], audit.warning)

            second = self.lemanon.init_project(project)
            self.assertEqual([], second.created)
            self.assertEqual([], second.proposals)

    def test_cross_host_resources_are_thin_and_canonical(self):
        adapter_readme = (ADAPTER / "README.md").read_text(encoding="utf-8")
        command = (ADAPTER / "commands" / "lemanon.md").read_text(encoding="utf-8")
        example = EXAMPLE.read_text(encoding="utf-8")

        self.assertIn("skills/lemanon/SKILL.md", adapter_readme)
        self.assertIn("Do not fork", adapter_readme)
        self.assertIn("$ARGUMENTS", command)
        self.assertIn("canonical", command.lower())
        for mode in ("init", "onboard", "handoff", "receive", "close", "audit"):
            with self.subTest(mode=mode):
                self.assertIn(f"$lemanon {mode}", example)

    def test_repository_readme_documents_install_walkthrough_and_uninstall(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for heading in ("## Install", "## Lifecycle", "## Uninstall"):
            with self.subTest(heading=heading):
                self.assertIn(heading, text)
        self.assertIn("$lemanon init", text)
        self.assertIn("$lemanon receive", text)
        self.assertIn("remains ordinary Markdown", text)


if __name__ == "__main__":
    unittest.main()
