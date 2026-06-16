# Example: Upload Thesis -> Compliance Report

## Prompt

```text
Use $fdu-final-paper-skill to audit my thesis outline and front matter for Fudan 2026 compliance.
Degree: professional master's
Submission batch: 2026-09
Files available: thesis-outline.md, front-matter.pdf, references.bib
```

## Compliance Summary

Status: Needs revision before submission.

The outline is academically usable, but several front-matter and evidence-alignment items should be fixed before generating the final PDF.

## High-Risk Items

| Area | Finding | Action |
| --- | --- | --- |
| Title page | CLC and UDC fields are not shown in the supplied front matter. | Download the current official 2026.06 template and compare field by field. |
| Abstracts | Chinese abstract lists application value, but the English abstract emphasizes model accuracy. | Align both abstracts to the same problem -> method -> findings -> contribution order. |
| Figure/table lists | The thesis contains figures and tables, but no separate lists are shown. | Confirm the current rule and department template; add lists if required. |
| Main text | The outline has "总结" but no clearly named "结论" chapter or section. | Rename or restructure the final chapter so conclusions are explicit. |
| References | `references.bib` uses mixed English capitalization and incomplete journal fields. | Run BibTeX cleanup and confirm GB/T 7714 version for the submission batch. |

## Medium-Risk Items

- Innovation claims should be reduced to claims supported by Chapters 3-5.
- Terms for "spatial heterogeneity" should use one stable Chinese translation.
- The acknowledgements and research-output section should follow department rules.

## Unknowns For Department Confirmation

- Whether professional master's theses in the department require additional practice-report materials.
- Whether the department has a stricter cover/title-page template than the Graduate School version.
- Which GB/T 7714 rule the library or department expects after 2026-07-01.
