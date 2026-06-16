# 复旦研究生学位论文写作 Skill

上传论文 -> 得到合规报告。给出选题 -> 得到章节规划。贴入草稿 -> 得到 claim-evidence 审查。

这是一个面向复旦大学硕士、博士学位论文的 Codex skill，用于目录规划、摘要/绪论/结论修改、证据链检查、答辩前自查、LaTeX/BibTeX 工作流和复旦 2026.06 版论文规范合规检查。

![合规报告截图](assets/product-screenshot.svg)

## 一分钟安装

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/fdu-final-paper-skill "${CODEX_HOME:-$HOME/.codex}/skills/"
```

PowerShell:

```powershell
$target = if ($env:CODEX_HOME) { "$env:CODEX_HOME\skills" } else { "$HOME\.codex\skills" }
New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item -Recurse -Force .\skills\fdu-final-paper-skill $target
```

## 稳定读取参考文件

已安装的 skill 内置了读取脚本，可先把中文/英文 PDF、DOCX 和常见文本参考资料抽取为 UTF-8 Markdown，再交给 agent 分析：

```bash
python skills/fdu-final-paper-skill/scripts/read_reference_file.py "path/to/reference.pdf" \
  -o extracted-reference.md
```

如果中文路径在 shell 中乱码或转义失败，用环境变量传路径：

```powershell
$env:FDU_REF_FILE = "D:\论文资料\参考文献\中文论文.docx"
python skills\fdu-final-paper-skill\scripts\read_reference_file.py --path-env FDU_REF_FILE `
  -o extracted-reference.md
```

长 PDF 可加 `--pages 1-5`，完整抽取可用 `--max-chars 0`，多个文件可用 `--list-env`。

## 三分钟试用

```text
Use $fdu-final-paper-skill to design a Fudan master's thesis outline.
Topic: 基于多源遥感数据的城市热岛效应时空演化研究
Degree: 学术型硕士
Submission batch: 2026-09
```

```text
Use $fdu-final-paper-skill to revise my Chinese abstract and check claim-evidence alignment.
```

```text
Use $fdu-final-paper-skill to audit my thesis outline for Fudan 2026 compliance.
```

示例输出见 [`examples/`](examples/)，脚本化录屏见 [`assets/demo.cast`](assets/demo.cast)。

## 能力重点

- 选题到目录：把研究问题、材料/数据、方法和学位层次转为章节树。
- 草稿到证据审查：检查创新点、结论、图表、引用和术语一致性。
- 论文到合规报告：检查封面/题名页、摘要、图表清单、参考文献、注释、结论和答辩前风险。
- LaTeX/BibTeX：可复用仓库内 MIT 许可的可选 LaTeX helper bundle。
- DOCX：不再内嵌授权不明的 DOCX 代码；如需 Word 修订，请使用当前 Codex 环境中已安装的文档/DOCX 能力。

## 维护

```bash
python scripts/quick_validate.py skills/fdu-final-paper-skill
python scripts/smoke_test.py
python skills/fdu-final-paper-skill/scripts/check_fudan_spec_update.py \
  --reference skills/fdu-final-paper-skill/references/fudan-2026-format-checklist.md
```

许可证和第三方说明见 [`LICENSE`](LICENSE) 与 [`NOTICE`](NOTICE)。
