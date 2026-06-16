# Compliance Source Policy

Use this reference when a thesis compliance task may rely on rules beyond the
default Fudan 2026.06 specification.

## Default Baseline

Use `references/fudan-2026-format-checklist.md` as the default compliance and
template baseline when the user does not provide another source. Keep the
default visible in the final report so the user knows which rule set was used.

## Accepted User-Supplied Sources

Accept any of the following as compliance or template references:

- Official Fudan Graduate School links.
- Official department, school, program, or supervisor-provided notices.
- PDF, DOCX, Markdown, text, LaTeX, BibTeX, or template files.
- Folders or glob patterns containing multiple specification, template, or
  submission-instruction files.
- User-provided extracted text from a rule document when the original file is
  not available.

For local files and folders, use `scripts/read_reference_file.py` before making
compliance claims. For folders, prefer `--glob` or `--list-env` so the source
set is explicit.

## Priority Order

When sources conflict, use this priority order unless the user gives a clearer
instruction:

1. Current official Fudan Graduate School requirements for the target batch.
2. Current official department or program requirements for the same target
   batch, when they are stricter or more specific.
3. User-supplied supervisor or administrative instructions, marked as
   user-provided if not publicly verifiable.
4. The bundled Fudan 2026.06 checklist as the default baseline.
5. Older public samples, old templates, or unverified examples only as
   historical context, not as authority.

If the user supplies an alternative source but it is incomplete, combine it with
the Fudan 2026.06 default only for missing items and label those fallback checks.

## Audit Trail

Every compliance report should include:

- Sources used, including file names, links, or folder/glob patterns.
- Whether Fudan 2026.06 was the default baseline, a fallback for missing items,
  or superseded by a newer or stricter source.
- Conflicts between sources and the rule used to resolve them.
- Unknowns that must be confirmed with the department or Graduate School.

Do not invent rules from memory. If a linked source cannot be opened because
network access is unavailable, ask the user to upload or extract the document,
or mark the linked rule as unverified.
