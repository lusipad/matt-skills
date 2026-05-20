Skills are organized into bucket folders under `skills/`:

- `engineering/` — daily code work
- `productivity/` — daily non-code workflow tools
- `misc/` — kept around but rarely used
- `personal/` — tied to my own setup, not promoted
- `in-progress/` — drafts not yet ready to ship
- `deprecated/` — no longer used

Every skill in `engineering/`, `productivity/`, or `misc/` must have a reference in the top-level `README.md`, an entry in `.claude-plugin/plugin.json`, and a Codex adapter under `.agents/skills/`. Skills in `personal/`, `in-progress/`, and `deprecated/` must not appear in any public plugin surface.

`.codex-plugin/plugin.json` must point at the Codex adapter directory, not directly at the bucketed `skills/` tree, so draft/personal/deprecated skills are not accidentally exposed.

Each skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.

Each bucket folder has a `README.md` that lists every skill in the bucket with a one-line description, with the skill name linked to its `SKILL.md`.
