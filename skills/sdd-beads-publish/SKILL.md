---
name: sdd-beads-publish
description: Publish or refresh an approved SDD implementation plan in Beads. Use after an SDD plan is approved or revised, or when asked to create Beads issues from a plan.
---

# Publish an SDD Plan to Beads

Before opening `shared/...`, canonicalize this loaded `SKILL.md` path and derive
`<plugin-root>` from `<plugin-root>/skills/sdd-beads-publish/SKILL.md`. If the
runtime does not expose the path, search repository/user `.agents` roots,
installed plugin roots, runtime-configured skill roots, and Codex plugin
caches; accept only a root with this skill, both named shared files, and an
`sdd-beads` manifest. Missing or ambiguous roots are a stop. Then read
`shared/agent-runtime.md` and `shared/contract.md`. Never resolve plugin
resources relative to the target repository.

## Preconditions

1. Resolve the planning root from `planning-config.json` in the current
   directory or its parents. A relative `planningRoot` is relative to that
   config file; absent configuration means the repository root. Then resolve
   the target repository: when `planMapping["<PlanName>"]` names a repository
   key, resolve that key through the same `planning-config.json` file's
   `repositories.<key>.path` and verify the path exists. Stop and ask for the
   target path if any mapping component is missing; never guess or clone.
2. Read the complete target plan `README.md` and every phase document named in
   its `phases[]` frontmatter. Do not publish from remembered plan content.
3. Require plan status `approved` or `active`. A draft plan is not executable.
   A complete or archived plan is historical and is not newly imported.
4. Ground the installed CLI with `bd version`, then run `bd where --json` from
   the resolved target repository. Run every subsequent `bd` command from that
   repository. If either check fails, report that publication was skipped.
   Never install or initialize Beads implicitly.

## Existing-state index

Run:

```bash
bd list --all --limit 0 --json
```

Index the result by `external_ref`. Stop if any target reference is duplicated.
The canonical references are:

```text
sdd-plan:<PlanName>
sdd-phase:<PlanName>:<phase-id>
sdd-task:<PlanName>:<task-id>
```

Use the plan directory name as `<PlanName>`, not the display title. Preserve
phase and task IDs exactly as serialized in frontmatter.

## Publication

1. Create or update one plan epic. Link it to the plan `README.md`; label it
   `sdd,sdd-plan`; set metadata `sdd_plan` and `sdd_status`. Keep the open
   aggregate epic `in_progress` so it is not claimable work.
2. Create or update one child epic for each non-complete phase. Link it to its
   phase document; label it `sdd,sdd-phase`; set `sdd_plan`, `sdd_phase`, and
   `sdd_status`.
3. Create or update one child task for each non-complete SDD task. Its title
   starts with the stable task ID, its `acceptance` is the SDD `verification`
   text, and its description is a short pointer to the phase task section. Set
   `sdd_plan`, `sdd_task`, and `sdd_status`; label it `sdd,sdd-task`.
4. Set `spec_id` according to planning-root location. For an in-repository
   planning root, use the repository-relative artifact path. For an external
   planning root, use the stable planning-root-relative SDD path and set the
   issue description plus `sdd_planning_root` metadata to the resolved absolute
   planning root so an executor can locate it.
5. If a matching issue exists, update only mutable projection fields: title,
   parent, description, acceptance, `spec_id`, external-planning-root metadata,
   and SDD-owned labels/metadata. Add or update the named SDD labels and
   metadata keys without deleting unrelated project labels or metadata. Never
   replace comments, assignment, or handoff notes.
6. Do not create historical issues for already-complete phases or tasks. If an
   existing projected issue now corresponds to verified SDD completion, leave
   closure to `sdd-beads-reconcile` or the execution workflow.
7. Synchronize task status for non-closed issues without overriding Beads
   operational state. New tasks map `planned` to `open`, `in-progress` to
   `in_progress`, `blocked` to `blocked`, and `deferred` to `deferred`. Existing
   `open` tasks may move to the SDD-required blocked/deferred state. Never clear
   an existing blocked/deferred state, downgrade a claimed `in_progress` issue,
   or reopen a closed issue; report those transitions for reconciliation.
   Keep non-blocked phase epics `in_progress` as aggregate containers; a wholly
   blocked/deferred phase epic may mirror that state.
8. After all target issues exist, synchronize explicit blocking dependencies
   matching SDD `depends_on`. The canonical add command is:

   ```bash
   bd dep add <blocked-issue> <blocker-issue>
   ```

   Read the previous `sdd_blockers_json` value, which is a string containing a
   compact, lexicographically sorted JSON array of canonical blocker external
   references. Inspect
   existing dependency objects first and add only missing `blocks`
   relationships. When an approved revision removes a dependency, remove it
   with `bd dep remove <blocked-issue> <blocker-issue>` only if the previous
   metadata proves it was SDD-owned. Preserve every unrecorded operational
   blocker. Write the new `sdd_blockers_json` only after every edge operation
   succeeds. Hierarchy is organization, not execution ordering.
9. Run `bd dep cycles`. A cycle is a failed publication; report it verbatim and
   do not weaken SDD dependencies to make the graph pass.

Use `bd create`/`bd update` flags verified by the installed CLI. On updates,
prefer `--add-label` and `--set-metadata key=value` so unrelated issue state is
preserved. Pass creation metadata as JSON and quote all paths and user-authored
text. Prefer stdin/body files for multiline text rather than constructing shell
fragments.

## Safety and result

- Publication is idempotent by `external_ref`, not by title.
- Never delete issues. Report removed/deferred SDD elements as drift.
- Never reopen closed issues automatically.
- Never mark SDD artifacts complete from Beads state.
- Do not commit, Git-push, or Dolt-push unless repository policy or the user
  explicitly authorizes it.

Report the plan path, created/updated/unchanged issue IDs, dependency changes,
cycle-check output, and any conflicts. A publication failure does not roll back
an already-approved SDD plan; state clearly that the plan is approved but its
Beads projection is incomplete.
