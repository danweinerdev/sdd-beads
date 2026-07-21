---
name: sdd-beads-execute
description: Claim and execute an SDD plan task through Beads while preserving SDD verification and status authority. Use when implementing a projected SDD task or resuming claimed plan work.
---

# Execute an SDD Task Through Beads

Before opening `shared/...`, canonicalize this loaded `SKILL.md` path and derive
`<plugin-root>` from `<plugin-root>/skills/sdd-beads-execute/SKILL.md`. If the
runtime does not expose the path, search repository/user `.agents` roots,
installed plugin roots, runtime-configured skill roots, and Codex plugin
caches; accept only a root with this skill, both named shared files, and an
`sdd-beads` manifest. Missing or ambiguous roots are a stop. Then read
`shared/agent-runtime.md` and `shared/contract.md`. This skill coordinates
execution; it does not replace the runtime's `sdd-implement` skill.

## Orient and claim

1. Run `bd prime`, then read the target SDD plan and phase task in full.
2. Run `bd list --all --limit 0 --json` and locate exactly one issue whose
   `external_ref` is `sdd-task:<PlanName>:<task-id>`. Zero or multiple matches
   are a stop; publish or reconcile before implementation.
3. Inspect the issue with `bd show <id> --json`. Confirm its `spec_id`, SDD task
   identity, parent phase, and blockers match the current plan.
4. Confirm the SDD task's dependencies are complete and the bead is ready.
5. Claim atomically:

   ```bash
   bd update <id> --claim
   ```

   If another actor owns it, stop rather than editing the same work.

## Implement

Invoke the available `sdd-implement` workflow for the exact plan task. The
SDD workflow controls code inspection, tests, verification, task status, and
scope escalation. Pass it the Beads issue ID as operational context, but do not
substitute the issue description for the plan task.

For a material handoff, record concise state with:

```bash
bd comment <id> "<completed work, remaining work, verification state>"
```

If new work is discovered, record provenance with the verified Beads syntax:

```bash
bd create "<title>" --type task --deps "discovered-from:<current-id>"
```

If the work is already inside the current SDD task's scope and verification,
the discovered bead may be implemented and closed with that verification
evidence. If it changes approved scope, leave it open, revise and approve the
SDD plan, then reconcile that existing bead to the new SDD task identity,
parent, `spec_id`, and acceptance criteria rather than creating a duplicate.
That mapping is an explicit triage decision; never infer it from similar titles.

## Complete

Close in this order:

1. Locate `sdd-implement` through the runtime inventory or active skill/plugin
   search roots defined in `shared/contract.md`; canonicalize candidates,
   require exactly one valid `codex-sdd-planner` root, and read its
   `shared/completion-evidence.md`. Stop closure if that contract is unavailable
   or ambiguous.
2. Run every SDD verification command and read the output.
3. Use `sdd-implement` to populate the task's `### Completion Evidence` under
   the sdd-planner `shared/completion-evidence.md` contract while the task is
   still non-complete, then update SDD task/subtask status only from that
   evidence.
4. Re-read the task body and frontmatter. Confirm the task is `complete`, the
    evidence section is present and non-pending, and its complete identity
    matches an immediate recomputation: VCS/base, clean revision or source
    snapshot, exclusions, ignored/environment/directory inputs, exact
    governing-input set, and governing-intent projection digest. Confirm every
    prospective verification behavior is covered and every final required check
    passed. Any source or intent mismatch forbids proof creation and closure.
5. Follow the canonical proof protocol in `shared/contract.md` for external
   reference `sdd-task:<PlanName>:<task-id>`. Inspect existing comments with
   `bd show <id> --json --include-comments` or `bd comments <id> --json`; reuse
   one byte-identical valid proof, and stop on a duplicate or conflicting
   marker. Submit a new exact comment with `bd comment <id> --stdin`, then read
   it back and recompute the body hash.
6. Close the bead with a reason that references that exact marker, then re-read
   the issue and comments and verify the reason and unique stored proof:

   ```bash
   bd close <id> --reason "SDD task <task-id> complete; evidence completion-evidence:sdd-task:<PlanName>:<task-id>:<sha256(body)>"
   ```

Do not close on partial implementation, failing verification, pending/missing
completion evidence, a stale evidence revision, or an unrecorded scope change.
On a blocker, keep the failure output verbatim, update SDD/Beads status
consistently where appropriate, and comment with the required next action.

Do not commit, Git-push, or Dolt-push without explicit authority.
