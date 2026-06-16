---
name: fdu-final-paper-skill
description: >
  Use when Codex needs to plan, outline, draft, revise, format-check, or audit
  a Fudan University master's or doctoral thesis/dissertation in Chinese,
  English, or bilingual form. Trigger for Chinese requests such as 复旦毕业论文,
  复旦学位论文, 硕士论文, 博士论文, 论文目录, 摘要润色, 绪论修改, 结论与展望, 答辩前检查,
  格式审查, 合规检查, 复旦 2026 论文规范, claim-evidence 对齐, LaTeX/BibTeX, or
  Word DOCX thesis editing. Covers graduate thesis structure, chapter logic,
  abstract/front matter, references, appendices, publication records,
  acknowledgements, defense-readiness, and Fudan 2026 thesis-spec compliance
  without assuming any particular research field.
---

# Fudan Graduate Thesis Skill

## Core Orientation

Use this skill as a general graduate thesis assistant for Fudan University. Do not assume a fixed discipline, chapter sequence, method type, or product-development pipeline. Let the user's degree type, school/department rules, research question, evidence, and target submission batch determine the structure.

Always treat official Fudan Graduate School and department documents as the final authority for cover pages, typography, binding, submission, secrecy, and fee forms. For 2026-09 and later degree batches, default to the 2026.06 revised thesis specification unless the user's department gives a newer or stricter rule.

When exact formatting or submission requirements matter, read `references/fudan-2026-format-checklist.md` and verify against:

- Fudan thesis specification page: https://gs.fudan.edu.cn/6b/9f/c2806a27551/page.htm
- Fudan Graduate School thesis-spec list: https://gs.fudan.edu.cn/2806/list.htm

## Optional External Skill Modules

This repository keeps optional implementation helpers outside the core skill so the installed skill stays lightweight and redistributable. Load them only when the task needs that format-specific workflow and the files are available in the current repository checkout.

- LaTeX paper/project workflow, when using this repository checkout: `../../embedded/latex-paper-skills/.codex/skills/`
  - Use when the user needs a LaTeX thesis or paper project, BibTeX checking, citation validation, issue-gated writing, compilation, or result back-filling.
  - Start from `paper-from-zero` when topic-to-paper routing is unclear, `arxiv-paper-writer` for review/survey papers, `empirical-paper-writer` for evidence-bearing experimental papers, `results-backfill` after verified results arrive, and `latex-rhythm-refiner` for post-draft prose rhythm.
  - For Fudan thesis tasks, reuse the LaTeX, BibTeX, citation-audit, planning, and QA mechanics only. Do not inherit ML/AI, arXiv, IEEEtran, page-limit, or two-column assumptions unless the user explicitly asks for them. Use the official Fudan or department thesis template when formatting a degree thesis.
- Word DOCX workflow:
  - Use the active document/DOCX capability already available in the current Codex environment when the user needs to create, inspect, edit, comment on, or redline `.docx` thesis files.
  - If no DOCX skill or document plugin is available, produce a Markdown or LaTeX revision package and tell the user which DOCX-capable skill/plugin should be installed or enabled. Do not assume a vendored DOCX module exists in this repository.

## Default Workflow

1. Identify the task: outline planning, section drafting, revision, compliance check, LaTeX project work, Word editing, or defense-readiness audit.
2. Capture thesis context: degree level, language, department rules, submission batch, title/topic, research object, methods, evidence, figures/tables, publication outputs, and supervisor requirements.
3. Build the thesis story before polishing sentences: problem -> gap -> objective -> method/material -> evidence -> findings -> contribution -> limitation.
4. Choose a chapter architecture that follows the evidence, not a discipline stereotype.
5. Draft or revise section by section with explicit claim-evidence checks.
6. Check Fudan-specific front matter, abstract/keywords, figure/table lists, references, notes, appendices, and required declarations.
7. Finalize with a consistency audit: abstract, introduction objectives, chapter summaries, final conclusions, innovations, and limitations must say the same thing.

## Whole-Thesis Order

Use this order as a starting point, then adapt to the current official template and department requirements:

1. Cover/title page and other required preliminary pages.
2. Originality statement, authorization statement, or other required declarations.
3. Chinese abstract and keywords.
4. English abstract and keywords.
5. Table of contents.
6. List of figures and list of tables when the thesis contains figures/tables and the current rule requires them.
7. Abbreviations, symbols, nomenclature, or glossary when useful.
8. Main text, including a conclusion chapter or conclusion section.
9. References.
10. Research outputs during the degree period if required.
11. Acknowledgements.
12. Appendices when needed.

## Chapter Architecture

### General Master's Thesis

Use this for a focused thesis with one central research question and two to four evidence chapters:

1. Introduction.
2. Literature review, theoretical basis, data/materials, or research method foundation.
3. Core study 1: model, method, data, corpus, fieldwork, experiment, design, proof, or case analysis.
4. Core study 2: result analysis, validation, comparison, mechanism explanation, or application.
5. Core study 3 when it answers a distinct question; otherwise merge with Chapter 4.
6. Conclusion and outlook.

### General Doctoral Thesis

Use this for a dissertation with multiple connected studies:

1. Introduction: broad problem, literature map, research gaps, objectives, contribution map.
2. Theory, methods, data/materials, or shared analytical framework.
3. Foundational study or model/system/corpus/data construction.
4. Study 1.
5. Study 2.
6. Study 3.
7. Integrated discussion, cross-study synthesis, or final application if warranted.
8. Conclusion and outlook.

### Article-Based or Multi-Paper Thesis

Use this when chapters map to published or publishable studies:

1. Introduction and integrated contribution map.
2. Shared background, literature synthesis, and methodology.
3. Paper/study chapter 1.
4. Paper/study chapter 2.
5. Paper/study chapter 3.
6. General discussion: cross-paper synthesis, common limitations, broader contribution.
7. Conclusion and outlook.

### Practice-, Design-, or Application-Oriented Thesis

Use this when the thesis is organized around a practical problem, artifact, system, intervention, policy, translation, or professional scenario:

1. Introduction and problem definition.
2. Related work, requirements, standards, constraints, or theoretical basis.
3. Design/method/data/system/case construction.
4. Implementation, analysis, evaluation, or field application.
5. Validation, comparison, user study, expert review, robustness test, or reflective evaluation.
6. Conclusion and outlook.

## Per-Chapter Writing Rules

### Abstract

Write the abstract as a compressed version of the whole thesis:

1. Start with the research problem and why it matters.
2. State the gap or unresolved limitation.
3. State the objective and scope.
4. Summarize methods and evidence in the same order as the thesis.
5. Report findings and contributions; include quantitative or textual evidence only when supplied.
6. End with significance, application value, theoretical value, or implications.
7. Keep Chinese and English abstracts structurally equivalent; preserve names, technical terms, standards, models, datasets, and numbers.

Do not invent results, citations, sample sizes, experimental settings, survey counts, supervisor information, or publication records.

### Introduction

Build the introduction as a funnel:

1. Research background: move from broad field to the specific problem.
2. Literature review: organize by research question, approach, school of thought, method, or evidence type rather than by one-paper-at-a-time summaries.
3. Research gap: close each review cluster with a limitation or open question.
4. Research objective and significance: connect the gap to the thesis objective.
5. Research content and structure: map each chapter to a question and evidence type.
6. Innovations or contributions: list only defensible claims supported by later chapters.

### Method, Theory, Data, or Foundation Chapter

Use this chapter to avoid repeating reusable material later. Depending on discipline, include:

- Core concepts, theory, formulas, assumptions, or definitions.
- Data/material sources, corpus/sample selection, case selection, field sites, instruments, or archives.
- Methodological workflow, preprocessing, measurement, coding, modeling, proof, interpretation, or evaluation protocol.
- Standards, benchmarks, ethical approvals, reliability/validity checks, uncertainty, or limitations.
- Reproducibility details needed for another researcher to understand what was done.

### Core Research Chapters

Use one core chapter per independent research question. A strong chapter usually follows:

1. Opening: state the local question and why it follows from earlier chapters.
2. Materials/methods/data/case/model: define evidence and procedure.
3. Results or findings: present observations in a stable order.
4. Discussion: interpret mechanism/meaning, compare with literature or standards, explain discrepancies, and state limits.
5. Chapter summary: give 3-5 conclusion-style points, not a procedural recap.

### Final Chapter

Separate these four items:

1. Main work: what the thesis did, by chapter.
2. Main conclusions: findings supported by evidence.
3. Contributions or innovations: align with the introduction and avoid inflated language.
4. Limitations and outlook: pair each limitation with a realistic future step.

Do not introduce major new literature, data, or experiments in the final chapter.

## Writing Quality Checks

Read `references/writing-quality-checklist.md` when the task is paragraph revision, chapter drafting, or reviewer-style self-check. Core checks:

- One paragraph should carry one message.
- The first sentence should orient the reader.
- Every major claim needs evidence, citation, figure/table support, or a clear marker that evidence is missing.
- Terms, abbreviations, names, variables, and translated concepts must be consistent.
- Figures and tables should be introduced before they appear and interpreted after they appear.
- Unsupported claims should be weakened, marked as pending, or removed.

## Fudan 2026 Compliance Checks

Read `references/fudan-2026-format-checklist.md` when the user asks for formatting, pre-submission checks, cover/front matter, references, notes, or a September 2026-or-later submission.

When the repository scripts are available and network access is permitted, run `python scripts/check_fudan_spec_update.py --reference references/fudan-2026-format-checklist.md` from this skill folder before high-stakes compliance work. If the script reports a newer official specification, warn the user and treat the local checklist as stale until updated.

At minimum, check:

- Cover/title page includes the current required fields, including CLC and UDC when required.
- Chinese and English names, especially for international students or foreign teachers, match official identity/passport records.
- Abstracts and keywords match language and word-count requirements in the current rule.
- Lists of figures and tables are present when applicable.
- The main text includes conclusions.
- References follow the applicable GB/T 7714 rule; GB/T 7714-2025 takes effect on 2026-07-01.
- Notes use the required placement.
- Secrecy-related theses follow Graduate School procedures; do not reuse old public cover samples.

## Handling Missing Information

If the user asks for drafting but has not supplied evidence, write a structured scaffold with `[待补充：...]` markers. For English output, use `[TBD: ...]`. Never fabricate data, citations, approvals, fee details, supervisor signatures, publication records, or compliance facts.

## Output Contract

For outline or chapter-structure tasks, return:

1. A proposed chapter tree.
2. The purpose and evidence type for each chapter.
3. Fudan compliance notes relevant to the task.
4. Missing inputs needed before final drafting.

For revision tasks, return:

1. Revised text.
2. A short explanation of structural changes.
3. Claim-evidence risks or missing information.
4. Format/compliance reminders only when relevant.

For file-producing tasks, create or edit the actual LaTeX/DOCX/Markdown files, run available validation, and report what was checked. For DOCX work, use an installed external document workflow rather than a repository-vendored DOCX module.
