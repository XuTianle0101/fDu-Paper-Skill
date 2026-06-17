# Embedded latex-paper-skills Snapshot

English | [简体中文](README.zh-CN.md)

This directory is a partial, vendored snapshot of `latex-paper-skills`, kept only as an optional helper bundle for the Fudan thesis skill. It is not a full upstream checkout.

## What Is Included

- Reusable Codex skills under [.codex/skills/](.codex/skills/).
- Shared helper scripts and references used by those skills.
- The upstream [MIT License](LICENSE).

## What Is Not Included

- Showcase projects, generated papers, datasets, screenshots, and diagram assets.
- The upstream beginner workflow guide.
- Any promise that this embedded snapshot is current with upstream.

## Skill Entry Points

- [paper-from-zero](.codex/skills/paper-from-zero/SKILL.md): route a topic into the appropriate paper-writing workflow.
- [arxiv-paper-writer](.codex/skills/arxiv-paper-writer/SKILL.md): write review or survey papers with gated LaTeX and citation workflow.
- [empirical-paper-writer](.codex/skills/empirical-paper-writer/SKILL.md): plan and write evidence-bearing experimental papers.
- [results-backfill](.codex/skills/results-backfill/SKILL.md): replace placeholders after real results are available.
- [latex-rhythm-refiner](.codex/skills/latex-rhythm-refiner/SKILL.md): refine LaTeX prose while preserving citations.
- [check-collaborators](.codex/skills/check-collaborators/SKILL.md): check optional collaborator CLI availability.
- [collaborating-with-gemini](.codex/skills/collaborating-with-gemini/SKILL.md): use Gemini as an optional breadth collaborator.
- [collaborating-with-claude](.codex/skills/collaborating-with-claude/SKILL.md): use Claude as an optional depth collaborator.

## Use From This Repository

For Fudan thesis work, start with the main skill at [../../skills/fdu-final-paper-skill/SKILL.md](../../skills/fdu-final-paper-skill/SKILL.md). Load these embedded skills only when a task needs their LaTeX, BibTeX, citation-audit, planning, or results-backfill mechanics.

Do not inherit arXiv, IEEEtran, ML/AI, page-limit, or two-column assumptions for a Fudan degree thesis unless the user explicitly asks for them.
