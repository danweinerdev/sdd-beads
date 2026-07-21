---
name: sdd-beads-reconcile
description: Audit and reconcile drift between SDD plans and their Beads projections. Use when plan and Beads statuses, dependencies, links, or issue structure may disagree.
---

# Reconcile SDD and Beads

Before opening `shared/...`, canonicalize this loaded `SKILL.md` path and derive
`<plugin-root>` from `<plugin-root>/skills/sdd-beads-reconcile/SKILL.md`. If the
runtime does not expose the path, search repository/user `.agents` roots,
installed plugin roots, runtime-configured skill roots, and Codex plugin
caches; accept only a root with this skill, both named shared files, and an
`sdd-beads` manifest. Missing or ambiguous roots are a stop. Then read
`shared/agent-runtime.md` and `shared/contract.md`, and resolve the planning root
and target repository using the same `planMapping`/`repositories` fields in
`planning-config.json` as `sdd-beads-publish`. Read the complete target plan
README and every phase document in scope, including task, phase, and plan
evidence bodies, and run `bd list --all --limit 0 --json` from the target
repository.

Before validating or repairing any closure, locate `sdd-implement` through the
runtime inventory or active skill/plugin search roots defined in
`shared/contract.md`; canonicalize candidates, require exactly one valid
`codex-sdd-planner` root, and read its `shared/completion-evidence.md`. If the
skill or contract is missing or ambiguous, continue the audit but do not close
any issue.

## Audit

Compare by canonical `external_ref`, never by title:

- Missing or duplicate plan, phase, and task issues.
- Wrong `spec_id`, parent, labels, or SDD metadata.
- Missing or extra blocking dependencies relative to SDD `depends_on`.
- Beads `closed` while SDD is not `complete`.
- SDD `complete` while Beads remains open or in progress.
- SDD `blocked`/`deferred` while Beads is ready or in progress, and stale
  Beads blocked/deferred state after the SDD status changes.
- Beads ownership conflicts or multiple in-progress tasks assigned to the same
  task identity.
- Beads issues for SDD elements that were removed, deferred, or renumbered.
- Open plan/phase epics that appear in the ready queue instead of using the
  aggregate-container `in_progress` convention.
- For every projected issue, inspect full comments with `bd show <id> --json
  --include-comments` or `bd comments <id> --json`. Validate the canonical proof
  in `shared/contract.md` byte-for-byte against current `spec_id`,
  `external_ref`, and SDD evidence; recompute its proof hash and validate the
  recorded revision, durable source snapshot objects, and durable governing-
  intent projection. For an open issue being closed, also recompute current
  source identity and intent; do not compare an already closed issue's
  historical source/intent to a worktree or artifacts changed by later tasks.
  Verify a closed issue's close reason cites the exact unique marker. Missing,
  duplicate, conflicting, stale, malformed, or cross-issue proof is a hard
  conflict.
- For every closed phase, validate every task-child proof. For every closed
  plan, validate every phase and descendant-task proof. A closed aggregate with
  any invalid descendant proof is a hard conflict.

Run `bd dep cycles` and preserve its actual output.

## Repair rules

Safe projection repairs may proceed when requested: create missing issues,
refresh mutable link/title/acceptance/metadata fields, synchronize
blocked/deferred status, add missing SDD-owned blocking edges, and remove stale
edges proven SDD-owned by prior projection metadata. Do not delete issues,
remove operational dependencies, reopen closed issues, clear assignment, or
change SDD completion status from Beads state.

Never close an issue from SDD status, prospective `verification`, checked
subtasks, or child status alone. Close an open issue only when its matching SDD
evidence conforms, its source identity matches an immediate recomputation, and
the canonical proof protocol in `shared/contract.md` succeeds. Task, phase, and
plan markers respectively use their canonical `sdd-task:...`, `sdd-phase:...`,
and `sdd-plan:...` external references. If evidence is absent, pending, stale,
failing, or cannot be corroborated, report it and leave the issue open;
rerunning verification must first update SDD evidence.

Close a phase only when all task-child proofs and closure citations validate,
then post and validate the phase's own proof before closing it. Close a plan
only when all phase and descendant-task proofs and closure citations validate,
then post and validate the plan's own proof before closing it. Existing closed
issues with any proof fault are hard conflicts: report them without appending a
replacement proof, reopening, or changing SDD status. Never use aggregate
closure as proof that source code was merged, deployed, or pushed.

Clearing Beads `blocked` or `deferred` state requires explicit reconciliation:
confirm the state came only from a prior SDD projection and that no operational
blocker or defer reason remains. Otherwise preserve it even when SDD says
`planned`.

To adopt discovered work after an approved plan revision, require the user or
maintainer to identify the existing discovered bead and exact new SDD task.
Then update that bead with `bd update <id> --external-ref
"sdd-task:<PlanName>:<task-id>"`, parent, `spec_id`, acceptance, SDD labels,
and SDD metadata. Preserve its `discovered-from` edge and comments. Never select
an adoption candidate by title, and never create a second projected bead after
adoption.

When status conflicts:

- Scope, dependency intent, verification, and completion: SDD wins.
- Current assignment, claim, and handoff state: Beads wins.
- Closed Beads plus incomplete SDD: report as a hard conflict requiring
  evidence review; do not choose a side automatically.

Output a table of SDD identity, Beads ID, discrepancy, authority, and action.
Separate repaired items from conflicts requiring user or maintainer action.
Do not commit, Git-push, or Dolt-push without explicit authority.
