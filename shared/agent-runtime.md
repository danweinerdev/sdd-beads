# Agent Runtime Conventions

This plugin provides runtime-neutral Agent Skills, not slash commands,
runtime hooks, or named subagent types. Skills must remain usable without
collaboration agents.

## Resolve plugin resources

`shared/...` always belongs to this installed plugin; it is never relative to
the target repository or planning root.

Resolve `<plugin-root>` in this order:

1. Canonicalize the loaded `SKILL.md` path by following symlinks, then ascend
   from `<plugin-root>/skills/<skill-name>/SKILL.md`.
2. If the runtime does not expose that path, search active skill roots,
   including repository/user `.agents/skills`, user `.agents/plugins/*/skills`,
   runtime-configured skill paths, and Codex plugin caches. Canonicalize each
   candidate before deriving its root.
3. Accept a candidate only when it contains the requested skill,
   `shared/agent-runtime.md`, `shared/contract.md`, and
   `.codex-plugin/plugin.json` whose `name` is `sdd-beads`.
4. If no candidate or multiple candidates remain, stop and report the missing
   or ambiguous installation. Never select by current directory, modification
   time, or guessed version.

Read plugin resources in place. Never copy, vendor, or symlink shared resources
into the target repository. Installing the skill-directory symlinks described
by the plugin README is an installation action, not runtime resource copying.

## Optional peers

`sdd-beads` may hand work to an independently installed SDD implementation
skill. Capability-detect that skill through the current runtime. Do not search
for or install a peer plugin during execution, and do not reimplement its
workflow when it is absent.
