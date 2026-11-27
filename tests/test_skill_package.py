import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "lemanon"
MODES = ("init", "onboard", "handoff", "receive", "close", "audit")


class SkillPackageContractTests(unittest.TestCase):
    def test_repository_and_skill_entrypoints_exist(self):
        expected = (
            ROOT / "README.md",
            ROOT / "LICENSE",
            SKILL_DIR / "SKILL.md",
            SKILL_DIR / "agents" / "openai.yaml",
        )
        self.assertEqual([], [str(path.relative_to(ROOT)) for path in expected if not path.is_file()])

    def test_skill_frontmatter_is_discoverable_without_summarizing_workflow(self):
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"\A---\n(?P<header>.*?)\n---\n", text, flags=re.DOTALL)
        self.assertIsNotNone(match)
        header = match.group("header")
        self.assertRegex(header, r"(?m)^name:\s*lemanon\s*$")
        self.assertRegex(header, r"(?m)^description:\s*Use when\b")
        self.assertNotIn("init →", header)
        self.assertNotIn("onboard →", header)

    def test_skill_declares_the_six_public_modes(self):
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        for mode in MODES:
            with self.subTest(mode=mode):
                self.assertIn(f"`$lemanon {mode}`", text)

    def test_openai_metadata_uses_explicit_lemanon_invocation(self):
        text = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^\s*display_name:\s*[\"']?Lemanon[\"']?\s*$")
        self.assertRegex(text, r"(?m)^\s*allow_implicit_invocation:\s*false\s*$")
        self.assertIn("$lemanon", text)


if __name__ == "__main__":
    unittest.main()
