# SDD/Beads Contract

## Authority

1. SDD specs, designs, decisions, and plans are authoritative for intent,
   scope, dependencies, verification, and durable completion.
2. Beads is authoritative for live ownership, assignment, claims, handoffs,
   and ready-queue operations.
3. A Beads issue never amends an SDD artifact. When discovered work changes
   approved scope, revise and approve the SDD artifact before implementing it.
4. A task bead closes only after its SDD task is complete with verification
   evidence. Closing a bead does not prove source code was merged or deployed.

## Mapping

- Plan epic external reference: `sdd-plan:<PlanName>`
- Phase epic external reference: `sdd-phase:<PlanName>:<phase-id>`
- Task external reference: `sdd-task:<PlanName>:<task-id>`
- `spec_id`: path to the governing phase document for a phase or task, and to
  the plan `README.md` for the plan epic. Use a repository-relative path when
  the planning root is inside the target repository; for an external planning
  root, use the stable planning-root-relative SDD path and record the resolved
  absolute planning root in the SDD-owned `sdd_planning_root` metadata key and
  issue description.
- Metadata keys: every projected issue has `sdd_plan`; phase and task issues
  additionally have exactly one of `sdd_phase` or `sdd_task`. Projected issues
  also record `sdd_status`. The exact dependency-provenance key is
  `sdd_blockers_json`, stored as a string containing a compact, lexicographically
  sorted JSON array of canonical blocker external references. This distinguishes
  plan dependencies from operational Beads blockers.
- Labels: `sdd`, `sdd-plan`, `sdd-phase`, or `sdd-task` as applicable.

External references are stable identities. Titles and descriptions may change;
external references must not. Duplicate external references are a hard stop.

## Status rules

- SDD `planned` normally corresponds to Beads `open`.
- Claiming a bead produces Beads `in_progress`; the SDD implement workflow then
  marks the task `in-progress` as it begins.
- SDD `blocked` corresponds to Beads `blocked`, with the reason recorded in a
  comment or notes. It must not appear in `bd ready`.
- SDD `deferred` corresponds to Beads `deferred`. A future `defer_until` is
  optional; the stored status alone keeps the issue out of `bd ready`.
- SDD `complete` corresponds to Beads `closed`, but only after verification.

Plan and non-blocked phase epics are aggregate containers. Keep them
`in_progress` while open so they do not pollute the claimable ready queue; their
actual SDD lifecycle state remains in `sdd_status`. Agents select executable
work with `bd ready --type task --label sdd-task`.

Do not automatically reopen a closed bead, downgrade a complete SDD task, or
infer verification from status alone. Report those conflicts for resolution.

Beads owns operational blockers. Publication may move an `open` projected task
to `blocked` or `deferred` when SDD requires it, but it never clears an existing
Beads `blocked`/`deferred` state merely because SDD returns to `planned`.
Clearing that state requires explicit reconciliation after confirming there is
no operational blocker.

## Dependency ownership

SDD `depends_on` edges and operational Beads blockers may coexist. Projected
issues record the canonical references of SDD-owned blockers in
`sdd_blockers_json`. A publication refresh reads the previous value before any
mutation, adds missing SDD-owned edges, removes an obsolete edge only when that
previous value proves ownership, and writes the new sorted array only after all
edge operations succeed. Unrecorded blockers are operational and are never
removed automatically.

## Git and Dolt

Git source history and Beads Dolt history are independent. Skills may inspect
both, but commit, Git push, `bd dolt pull`, and `bd dolt push` remain explicit
policy-controlled operations.
