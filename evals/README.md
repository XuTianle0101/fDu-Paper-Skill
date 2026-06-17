# Evals

`prompts.json` contains 10 realistic prompts that should keep working as the skill evolves. `expected/` contains minimal golden sketches for those prompts.

Use them for manual forward tests or automated agent evaluations. A good answer should satisfy each prompt's `expected_checks` without inventing data, citations, Fudan rules, supervisor approvals, or publication records.

Run the rubric checker with:

```bash
python3 scripts/check_eval_outputs.py
```

To check model outputs, write one Markdown file per prompt ID in another directory and run:

```bash
python3 scripts/check_eval_outputs.py --outputs-dir path/to/model-outputs
```
