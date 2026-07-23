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


if __name__ == "__main__":
    unittest.main()
