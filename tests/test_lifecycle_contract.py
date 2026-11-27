import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "lemanon"
REFERENCES = SKILL / "references"
TEMPLATES = SKILL / "assets" / "scaffold" / "templates"


class LifecycleContractTests(unittest.TestCase):
    def test_onboard_read_order_starts_with_rules_then_hot_state(self):
        text = (REFERENCES / "onboard.md").read_text(encoding="utf-8")
        ordered = (
            "repository-root `AGENTS.md`",
            "`knowledge/AGENTS.md`",
            "`knowledge/PROJECT.md`",
            "`knowledge/STATUS.md`",
            "`knowledge/ROADMAP.md`",
            "handoff index",
        )
        positions = [text.index(item) for item in ordered]
        self.assertEqual(positions, sorted(positions))

    def test_handoff_template_requires_producer_commit_evidence_and_authority(self):
        text = (TEMPLATES / "HANDOFF.md").read_text(encoding="utf-8")
        required = (
            "Status:",
            "Producer:",
            "Receiver:",
            "Branch:",
            "Commit:",
            "Verified evidence and locations",
            "Pending and blocked",
            "Authorization and prohibited actions",
        )
        for field in required:
            with self.subTest(field=field):
                self.assertIn(field, text)

    def test_receive_preserves_producer_ownership_and_verifies_before_shared(self):
        text = (REFERENCES / "receive.md").read_text(encoding="utf-8")
        self.assertIn("Never rewrite the producer record", text)
        self.assertIn("exact branch and commit", text)
        self.assertIn("independently accepted", text)
        self.assertIn("`handoffs/shared/`", text)
        self.assertIn("authorization", text.lower())

    def test_close_synchronizes_authoritative_targets(self):
        text = (REFERENCES / "close.md").read_text(encoding="utf-8")
        targets = (
            "`STATUS.md`",
            "`decisions/`",
            "`evidence/`",
            "`HISTORY.md`",
            "handoff index",
        )
        for target in targets:
            with self.subTest(target=target):
                self.assertIn(target, text)
        self.assertIn("does not authorize", text)

    def test_skill_routes_every_mode_to_its_own_resource(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        expected = {
            "init": "scripts/lemanon.py",
            "audit": "references/audit-policy.md",
            "onboard": "references/onboard.md",
            "handoff": "references/handoff.md",
            "receive": "references/receive.md",
            "close": "references/close.md",
        }
        for mode, resource in expected.items():
            with self.subTest(mode=mode):
                self.assertIn(f"`$lemanon {mode}`", text)
                self.assertIn(resource, text)

    def test_record_templates_exist_for_lifecycle_outputs(self):
        expected = {"HANDOFF.md", "DECISION.md", "EVIDENCE.md", "WORK.md"}
        self.assertEqual(expected, {path.name for path in TEMPLATES.glob("*.md")})


if __name__ == "__main__":
    unittest.main()
