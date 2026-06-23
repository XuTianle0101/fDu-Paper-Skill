# Evals

`prompts.json` contains 13 realistic prompts that should keep working as the skill evolves. `expected/` contains minimal golden sketches for those prompts, and `fixtures/` contains longer task inputs used by behavior-oriented evals.

Use them for manual forward tests or automated agent evaluations. A good answer should satisfy each prompt's `expected_checks`, declared `behavior_checks`, and global safety behaviors without inventing data, citations, Fudan rules, supervisor approvals, or publication records.

Prompt objects may include:

- `fixture_path`: a long Markdown input file under `evals/` that the model output should be based on.
- `behavior_checks`: required behaviors such as declaring sources, listing unknowns, bounding claims to evidence, avoiding unverified official conclusions, and avoiding fabricated data.
- `forbidden_patterns`: prompt-specific regular expressions that must not appear in the output.

Run the rubric checker with:

```bash
python3 scripts/check_eval_outputs.py
```

To check model outputs, write one Markdown file per prompt ID in another directory and run:

```bash
python3 scripts/check_eval_outputs.py --outputs-dir path/to/model-outputs
```
