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
`planning-config.json` as `sdd-beads-publish`. Read the target plan and all
phase frontmatter in scope, and run `bd list --all --limit 0 --json` from the
target repository.

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

Run `bd dep cycles` and preserve its actual output.

## Repair rules

Safe projection repairs may proceed when requested: create missing issues,
refresh mutable link/title/acceptance/metadata fields, synchronize
blocked/deferred status, add missing SDD-owned blocking edges, and remove stale
edges proven SDD-owned by prior projection metadata. Do not delete issues,
remove operational dependencies, reopen closed issues, clear assignment, or
change SDD completion status from Beads state.

Never close a task from SDD status or checked subtasks alone. Close an open task
bead only when durable verification output is available and matches the SDD
verification, or after rerunning the exact verification successfully. If the
verification cannot safely be run or its evidence is unavailable, report the
task for evidence review and leave it open.
Close a phase epic only when the SDD phase is `complete` and every projected
task child is closed. Close a plan epic only when the SDD plan is `complete`
and every projected phase child is closed. Never use aggregate closure as proof
that source code was merged, deployed, or pushed.

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
