# SDD Beads

`sdd-beads` is a runtime-neutral Agent Skills plugin that connects structured
SDD plans to [Beads](https://github.com/gastownhall/beads) execution queues.

The boundary is deliberate:

- SDD artifacts own requirements, design, task scope, dependencies,
  verification, and durable completion status.
- Beads owns the live ready queue, claims, assignment, handoffs, and discovered
  work.
- Beads issues link to SDD artifacts; they do not copy or replace them.

## Skills

- `sdd-beads-publish` — idempotently project an approved or active SDD plan
  into Beads.
- `sdd-beads-execute` — claim a projected task, run the SDD implementation
  workflow, and close the bead only after verified SDD completion.
- `sdd-beads-reconcile` — detect and repair drift under the authority rules.

## Installation

Expose each skill through an Agent Skills discovery directory. For the
`~/.agents` convention:

```bash
ln -s ../plugins/sdd-beads/skills/sdd-beads-publish ~/.agents/skills/sdd-beads-publish
ln -s ../plugins/sdd-beads/skills/sdd-beads-execute ~/.agents/skills/sdd-beads-execute
ln -s ../plugins/sdd-beads/skills/sdd-beads-reconcile ~/.agents/skills/sdd-beads-reconcile
```

The target repository must already have an initialized Beads workspace.
This plugin never initializes Beads implicitly and never pushes Git or Dolt
state without authorization.

Restart the agent runtime or begin a new session after installation; skill
inventories are commonly loaded only at startup.

## Stable mapping

| SDD element | Beads element | `external_ref` |
|---|---|---|
| Plan | Epic | `sdd-plan:<PlanName>` |
| Phase | Child epic | `sdd-phase:<PlanName>:<phase-id>` |
| Task | Child task | `sdd-task:<PlanName>:<task-id>` |

One SDD task maps to one claimable Beads task. If a task needs multiple owners,
split the SDD task first rather than inventing a second decomposition in Beads.
