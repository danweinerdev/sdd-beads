import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISPATCH_CONTRACTS = (
    ROOT / "skills/sdd-beads-execute/SKILL.md",
    ROOT / "shared/agent-runtime.md",
    ROOT / "README.md",
)


class RuntimeNeutralityTests(unittest.TestCase):
    def test_implement_task_identifier_is_preserved_in_dispatch_contracts(self):
        for contract in DISPATCH_CONTRACTS:
            with self.subTest(contract=contract):
                self.assertIn("implement_task", contract.read_text())

    def test_dispatch_contracts_do_not_name_runtime_specific_agents_or_models(self):
        forbidden_identifiers = ("subagent_type", "gpt-", "claude-", "anthropic")
        for contract in DISPATCH_CONTRACTS:
            with self.subTest(contract=contract):
                content = contract.read_text().lower()
                for identifier in forbidden_identifiers:
                    self.assertNotIn(identifier, content)

    def test_beads_closure_preserves_commit_first_sdd_execution(self):
        execute = " ".join(
            (ROOT / "skills/sdd-beads-execute/SKILL.md").read_text().lower().split()
        )
        contract = " ".join((ROOT / "shared/contract.md").read_text().lower().split())
        for required in ("clean", "complete", "bisectable", "implementation commit"):
            self.assertIn(required, execute)
        self.assertIn("lifecycle/evidence commit", execute)
        self.assertIn("never substitutes for clean task commits", contract)
        self.assertNotIn(
            "do not commit, git-push, or dolt-push without explicit authority",
            execute,
        )


if __name__ == "__main__":
    unittest.main()
