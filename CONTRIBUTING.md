# Contributing

Thanks for helping make this skill useful for real thesis work.

## What Belongs Here

- Improve the core skill in `skills/fdu-final-paper-skill/`.
- Add examples that show concrete inputs and outputs.
- Add eval prompts for realistic Fudan thesis workflows.
- Keep compliance claims tied to official Fudan Graduate School pages.
- Keep third-party code out unless its license clearly allows redistribution.

## Development Checks

Run these before opening a pull request:

```bash
python scripts/quick_validate.py skills/fdu-final-paper-skill
python scripts/check_markdown_links.py --root .
python scripts/smoke_test.py
```

For high-stakes compliance changes, also run:

```bash
python skills/fdu-final-paper-skill/scripts/check_fudan_spec_update.py \
  --reference skills/fdu-final-paper-skill/references/fudan-2026-format-checklist.md
```

## Writing Style

- Keep `SKILL.md` concise and procedural.
- Move detailed rules into `references/` and link them from `SKILL.md`.
- Prefer examples over broad claims.
- Do not invent thesis requirements, citations, results, approvals, signatures,
  publication records, or department-specific rules.

## Third-Party Material

Before adding external code, templates, screenshots, or official documents,
confirm the license and add attribution to `NOTICE`.
