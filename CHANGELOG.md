# Changelog

All notable user-facing changes to `fdu-final-paper-skill` are documented here.

This project follows version tags such as `v0.1.0`, `v0.1.1`, and `v0.2.0`. For each important release, note what changed, what was fixed, whether users should reinstall the skill, and the recommended update command.

## Unreleased

### Added

- Added README instructions for updating an already installed Codex skill.
- Added release notification guidance using GitHub Releases and **Watch -> Custom -> Releases**.
- Added this changelog as the canonical place for future release notes.

### Fixed

- No code fixes in this documentation-only update.

### Reinstall Required

- Yes. Users who want the new README-distributed instructions in their installed skill should reinstall by replacing the local `fdu-final-paper-skill` folder.

### Recommended Update

```bash
git pull

rm -rf "${CODEX_HOME:-$HOME/.codex}/skills/fdu-final-paper-skill"
cp -R skills/fdu-final-paper-skill "${CODEX_HOME:-$HOME/.codex}/skills/"
```

PowerShell:

```powershell
git pull

$skills = if ($env:CODEX_HOME) { "$env:CODEX_HOME\skills" } else { "$HOME\.codex\skills" }
$dest = Join-Path $skills "fdu-final-paper-skill"

Remove-Item -Recurse -Force $dest -ErrorAction SilentlyContinue
Copy-Item -Recurse -Force .\skills\fdu-final-paper-skill $skills
```

Restart Codex after reinstalling.

## v0.1.0 - 2026-06-16

### Added

- Initial public version of the Fudan graduate thesis Codex skill.
- Thesis outline planning, abstract and chapter revision guidance, claim-evidence checks, defense-readiness audit flow, and Fudan 2026.06 thesis specification checklist.
- Reference file reader for PDFs, DOCX files, Markdown, plain text, LaTeX, and BibTeX inputs.
- Validation helpers, smoke tests, examples, and optional LaTeX helper bundle.

### Fixed

- Not applicable for the initial release.

### Reinstall Required

- Yes, for users upgrading from any pre-release copy.

### Recommended Update

Use the latest install or update command from [`README.md`](README.md).
