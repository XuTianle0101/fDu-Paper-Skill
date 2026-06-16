# LaTeX Compile Debugging for Fudan Theses

Use this reference when a Fudan thesis task involves LaTeX compilation, `fduthesis`, XeLaTeX/LuaLaTeX, BibTeX/Biber, wrapper scripts, output directories, `aux` files, or a reported failure despite a generated PDF.

## Preferred First Pass

1. Identify the root file, engine, template/class, bibliography tool, and output directory policy.
2. Run the bundled helper from the installed skill folder when available:

```bash
python scripts/compile_latex_project.py --project-dir . --main main.tex --engine auto
```

For a separate build directory:

```bash
python scripts/compile_latex_project.py --project-dir . --main main.tex --engine auto --output-dir build
```

Use `--preflight-only` before editing if the user only wants diagnosis. Use `--strict-exit-code` only for CI-style checks where the compiler's nonzero exit code must remain authoritative.

## fduthesis and unicode-math Package Rules

- Treat `fduthesis`, `ctex`, `fontspec`, and `unicode-math` as the owners of Chinese/font/math setup unless the template documentation says otherwise.
- Do not add `amssymb` or `amsfonts` to an `fduthesis` or `unicode-math` project. They commonly re-define symbols already managed by `unicode-math` and can trigger errors such as `Command \Bbbk already defined`.
- Keep `amsmath` and usually `mathtools` when needed; they are not the same conflict as `amssymb`.
- Avoid legacy math font packages with `unicode-math`, including `mathptmx`, `newtxmath`, `txfonts`, `pxfonts`, and `mathspec`.
- Prefer removing the conflicting package line over adding defensive redefinitions. Do not "fix" duplicate symbol errors by redefining symbols from the template or package internals.

Minimal fix pattern:

```latex
% Keep:
\usepackage{amsmath}
\usepackage{mathtools}

% Remove in fduthesis/unicode-math projects:
% \usepackage{amssymb}
% \usepackage{amsfonts}
```

## Output Directory and include Aux Files

`\include{chapters/intro}` writes an auxiliary file for that included unit. When the compiler is run with `-output-directory=build` or `latexmk -outdir=build`, some TeX distributions do not reliably create nested directories such as `build/chapters/` before writing `intro.aux`.

Use this order:

1. During diagnosis, compile in the project root unless a clean build directory is required.
2. If using an output directory, pre-create output subdirectories that mirror every `\include{...}` parent path. The bundled helper does this automatically.
3. Keep `\include` paths relative to the project root and do not point them outside the project.
4. Do not rewrite chapter-level `\include` commands to `\input` just to avoid the build directory issue unless the user accepts the semantic change.

Typical symptom and fix:

| Symptom | Likely Cause | First Fix |
| --- | --- | --- |
| `I can't write on file 'chapters/intro.aux'` | Missing mirrored output subdirectory | Run the bundled helper with `--output-dir build` or create `build/chapters/` |
| Root compile works but build directory fails | `\include` aux path issue | Confirm included parent directories exist under the output dir |
| BibTeX cannot find aux | Wrapper expects aux in root while compiler wrote to build | Run BibTeX/Biber against the output directory or use `latexmk` |

## Avoid False Failures from Wrapper Scripts

For thesis compile tasks, determine success from both the compiler result and the actual artifact:

1. Record compile start time.
2. Read the log for `Output written on ...pdf`.
3. Check the PDF path reported by the log first, then the configured output directory, then the project root.
4. Require a non-empty PDF whose modification time is newer than the compile start.
5. If the compiler returned nonzero but the log reports a fresh PDF and no fatal error, report a successful PDF build with a wrapper warning instead of saying the compile failed.
6. If the log contains fatal errors, report failure even if a partial PDF exists.

Common wrapper mismatch:

```text
latexmk -outdir=build main.tex
wrapper expects: main.pdf
actual artifact: build/main.pdf
```

The correct report is: PDF generated at `build/main.pdf`; wrapper expectation is wrong or stale.

## Debugging Loop

Use a tight loop and make one minimal change at a time:

1. Run preflight.
2. Fix package ownership conflicts first.
3. Run compile with the actual engine and output policy.
4. Read the first fatal log error, not the last repeated error.
5. Verify the PDF artifact path and freshness.
6. Report the exact command, PDF path, whether the PDF is fresh, and remaining warnings.
