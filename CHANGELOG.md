# Changelog

All notable user-facing changes to `fdu-final-paper-skill` are documented here.

This project follows version tags such as `v0.1.0`, `v0.1.1`, and `v0.1.2`. For each important release, note what changed, what was fixed, whether users should reinstall the skill, and the recommended update command.

## Unreleased

- No unreleased changes.

## v0.1.2 - 2026-06-17

### Added

- Added smoke-test coverage for PDF extraction through the `pdftotext` fallback backend.
- Added golden eval sketches and a rubric checker so eval prompts test source declarations, missing information, claim-evidence risks, and compliance unknowns.

### Fixed

- Fixed `compile_latex_project.py` on Python 3.8 by avoiding `Path.is_relative_to()`.
- Fixed `quick_validate.py` so folded YAML descriptions such as `description: >` are parsed as full trigger text instead of the literal `>`.
- Replaced the embedded `latex-paper-skills` README files with snapshot manifests that do not link to omitted upstream assets.

### Changed

- `quick_validate.py` now checks description length, trigger keyword coverage, and `agents/openai.yaml` interface freshness.
- Documented optional PDF extraction backends: `pypdf`/`PyPDF2`, `pdfplumber`, `PyMuPDF`, or Poppler `pdftotext`.
- Markdown link checking now includes `embedded/` and local HTML image/source resources.
- CI now runs validation and smoke tests on Python 3.8 and 3.11.

### Reinstall Required

- Yes. Users who want the Python 3.8 LaTeX helper fix, updated PDF backend guidance, and refreshed skill routing should reinstall by replacing the local `fdu-final-paper-skill` folder.

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

## v0.1.1 - 2026-06-16

### Added

- Added `scripts/compile_latex_project.py` for Fudan-friendly LaTeX compilation diagnostics.
- Added `references/latex-compile-debugging.md` with guidance for `fduthesis`, `unicode-math`, output directories, `\include` aux files, and wrapper/PDF artifact checks.
- Added smoke-test coverage for `fduthesis` plus `amssymb` preflight detection and verified-PDF handling when a wrapper returns a nonzero code.
- Added README instructions for the new LaTeX compile helper in English and Chinese.
- Added README instructions for updating an already installed Codex skill.
- Added release notification guidance using GitHub Releases and **Watch -> Custom -> Releases**.
- Added this changelog as the canonical place for future release notes.
- Added a custom compliance source workflow: Fudan 2026.06 remains the default baseline, while newer or department-specific links, files, folders, and templates can override or supplement compliance checks.

### Fixed

- Avoid repeated advice to add legacy math symbol packages when `fduthesis` or `unicode-math` already owns math symbol setup.
- Avoid false compile failures when the PDF is freshly generated in the configured output directory but a wrapper script expects it beside the root `.tex` file.
- Prepare output subdirectories needed by `\include{...}` aux writes when using a build directory.

### Reinstall Required

- Yes. Users who want the new LaTeX compile helper, debugging reference, and updated skill routing should reinstall by replacing the local `fdu-final-paper-skill` folder.

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
