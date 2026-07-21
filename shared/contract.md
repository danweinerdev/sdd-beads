# SDD/Beads Contract

## Authority

1. SDD specs, designs, decisions, and plans are authoritative for intent,
   scope, dependencies, verification, and durable completion.
2. Beads is authoritative for live ownership, assignment, claims, handoffs,
   and ready-queue operations.
3. A Beads issue never amends an SDD artifact. When discovered work changes
   approved scope, revise and approve the SDD artifact before implementing it.
4. A task, phase, or plan bead closes only after its matching SDD entity is
   complete with a populated, conforming completion-evidence section under the
   sdd-planner `shared/completion-evidence.md` contract. Prospective
   `verification`, status, checked subtasks, and closed children are not
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

The SDD completion-evidence section is the durable proof of what ran. Every
task, phase, and plan closure carries its own canonical Beads proof comment.

For an issue with canonical external reference `<external-ref>`, construct the
proof as follows:

1. Require the SDD artifact and evidence section to be UTF-8 with LF line
   endings. The exact evidence-section bytes include its Markdown heading and
   continue through the byte before the next heading of equal or higher level;
   retain its final LF. `spec_id` and `external_ref` may not contain LF.
2. Construct `body` as the exact bytes
   `spec_id: <spec_id>\nexternal_ref: <external-ref>\n` followed immediately by
   those evidence-section bytes.
3. Compute lowercase hexadecimal SHA-256 over `body` only. The marker is
   `completion-evidence:<external-ref>:<sha256(body)>`.
4. The exact comment bytes are `<marker>\n<body>`. Submit them through stdin so
   shell quoting cannot alter the bytes, then read the stored comment back and
   recompute its hash.
5. Before posting, inspect all issue comments. Reuse one byte-identical valid
   proof idempotently. More than one marker for the same external reference, or
   a marker with a different body/hash, is a hard conflict; do not append
   another proof or close the issue.
6. Close with a reason citing the exact marker. Re-read the closed issue with
   comments, verify the stored reason cites that marker, and verify exactly one
   valid proof remains. If the installed Beads version cannot expose the close
   reason and full comment bytes for verification, closure cannot be validated
   and must stop for manual resolution.

Immediately before proof construction, recompute the complete canonical
identity: VCS/base, clean revision or source snapshot, exclusions,
ignored/environment/directory inputs, exact governing-input reference set, and
governing-intent projection digest. A source or intent mismatch makes the
evidence stale and forbids comment creation or closure.

Closure validation depends on the installed `sdd-planner` contract (D-0005).
Locate `sdd-implement` through the runtime's exposed skill inventory or its
active repository/user `.agents` roots, installed plugin roots,
runtime-configured skill roots, and Codex plugin caches. Canonicalize every
candidate, require exactly one root with the skill, shared contract, and
`codex-sdd-planner` manifest, then read that installation's
`shared/completion-evidence.md`. If the peer skill or contract is unavailable
or ambiguous, auditing may continue but no task, phase, or plan bead may close.

Plan and non-blocked phase epics are aggregate containers. Keep them
`in_progress` while open so they do not pollute the claimable ready queue; their
actual SDD lifecycle state remains in `sdd_status`. Agents select executable
work with `bd ready --type task --label sdd-task`.

A phase closes only after its own proof validates and every task child has a
valid task proof and close-reason citation. A plan closes only after its own
proof validates and every phase and descendant task has a valid proof and
close-reason citation. Closed children without valid proofs are hard conflicts,
not aggregate evidence.

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
