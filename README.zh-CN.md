# 复旦研究生学位论文写作 Skill

[English](README.md) | 简体中文

当前 skill 版本：`v0.1.1`。更新记录见 [`CHANGELOG.md`](CHANGELOG.md)。

上传论文 -> 得到合规报告。给出选题 -> 得到章节规划。贴入草稿 -> 得到 claim-evidence 审查。

这是一个面向复旦大学硕士、博士学位论文的 Codex skill，用于目录规划、摘要/绪论/结论修改、证据链检查、答辩前自查、LaTeX/BibTeX 工作流和论文规范合规检查。默认以复旦 2026.06 版规范作为合规审查和模板参考，也支持使用更新的研究生院链接、院系规则、导师/教务说明、模板文件或规则文件夹覆盖或补充默认基线。

![合规报告截图](assets/product-screenshot.svg)

## 一分钟安装

先准备一个支持 skills 的 agent，例如 Codex、Claude Code 等。

然后二选一安装：

1. 如果 agent 自带 skill installer，直接把这个 GitHub 仓库交给它，让它安装 `fdu-final-paper-skill`。
2. 如果想手动安装，先 `git clone` 到本地，再把 `skills/fdu-final-paper-skill` 这个文件夹复制到 agent 的本地 `skills` 文件夹。

Bash/macOS/Linux：

```bash
git clone https://github.com/XuTianle0101/fDu-Paper-Skill.git
cd fDu-Paper-Skill
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/fdu-final-paper-skill "${CODEX_HOME:-$HOME/.codex}/skills/"
```

PowerShell/Windows：

```powershell
git clone https://github.com/XuTianle0101/fDu-Paper-Skill.git
cd fDu-Paper-Skill
$target = if ($env:CODEX_HOME) { "$env:CODEX_HOME\skills" } else { "$HOME\.codex\skills" }
New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item -Recurse -Force .\skills\fdu-final-paper-skill $target
```

安装后重启 agent，然后可以直接这样试用：

```text
Use $fdu-final-paper-skill to audit my thesis outline for Fudan 2026 compliance.
```

## 更新已安装的 skill

Codex skill 安装后会被复制到本地 skills 目录。已经安装过早期版本的用户，需要先更新仓库，再覆盖本地已安装的 skill 文件夹。

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

重新安装后请重启 Codex，让新版 skill 生效。

如果用户是从 GitHub 安装并已经有本地仓库副本，可以使用：

```bash
cd path/to/fdu-final-paper-skill
git pull
rm -rf "${CODEX_HOME:-$HOME/.codex}/skills/fdu-final-paper-skill"
cp -R skills/fdu-final-paper-skill "${CODEX_HOME:-$HOME/.codex}/skills/"
```

## 发布与更新通知

重要更新会记录在 [`CHANGELOG.md`](CHANGELOG.md)。维护者发布面向用户的更新时，建议同步创建 GitHub tag 和 Release，例如 `v0.1.0`、`v0.1.1`、`v0.2.0`。

用户如果希望收到更新通知，可以在 GitHub 仓库页面选择 **Watch -> Custom -> Releases**，之后每次发布新 release 时会收到 GitHub 通知。

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
- 论文到合规报告：默认按复旦 2026.06 基线检查封面/题名页、摘要、图表清单、参考文献、注释、结论和答辩前风险；也可按用户提供的院系规则、链接、模板或文件夹进行审查。
- LaTeX/BibTeX：内置 `fduthesis` 友好的编译诊断脚本，可处理常见包冲突、输出目录和 PDF 产物校验；更完整的论文写作流程可复用仓库内 MIT 许可的可选 LaTeX helper bundle。
- DOCX：不再内嵌授权不明的 DOCX 代码；如需 Word 修订，请使用当前 Codex 环境中已安装的文档/DOCX 能力。

## 自定义合规来源

复旦 2026.06 仍是默认合规审查和模板参考。你也可以提供更新的研究生院链接、院系通知、导师或教务要求、模板文件，或包含多份规则文件的文件夹。Skill 会读取这些来源，说明最终采用了哪些规则，并只在信息缺失时把复旦 2026.06 作为默认基线或补充检查项。

示例 prompt：

```text
Use $fdu-final-paper-skill to audit my thesis.
Default baseline: Fudan 2026.06.
Additional compliance sources:
- Department notice: docs/department-2026-defense-rules.pdf
- Template folder: templates/fudan-school-template/
- Official link: https://example.edu/department/thesis-rules
```

如果本地规则文件放在一个文件夹里，可先抽取为 Markdown：

```bash
python skills/fdu-final-paper-skill/scripts/read_reference_file.py \
  --glob "docs/compliance/**/*.pdf" \
  --glob "docs/compliance/**/*.docx" \
  --glob "docs/compliance/**/*.md" \
  -o extracted-compliance-sources.md
```

## 更顺畅的 LaTeX 编译

对 `fduthesis` 项目，优先用内置辅助脚本跑第一轮诊断：

```bash
python skills/fdu-final-paper-skill/scripts/compile_latex_project.py \
  --project-dir path/to/thesis --main main.tex --engine auto
```

如果项目使用 build 输出目录：

```bash
python skills/fdu-final-paper-skill/scripts/compile_latex_project.py \
  --project-dir path/to/thesis --main main.tex --engine auto --output-dir build
```

脚本会提示 `fduthesis`/`unicode-math` 与 `amssymb`、`amsfonts` 等包冲突，提前创建 `\include` 在输出目录下需要的 aux 子目录，并按实际新生成的 PDF 路径判断编译结果，减少“PDF 已生成但 wrapper 判失败”的情况。

## 维护

```bash
python scripts/quick_validate.py skills/fdu-final-paper-skill
python scripts/smoke_test.py
python skills/fdu-final-paper-skill/scripts/check_fudan_spec_update.py \
  --reference skills/fdu-final-paper-skill/references/fudan-2026-format-checklist.md
```

许可证和第三方说明见 [`LICENSE`](LICENSE) 与 [`NOTICE`](NOTICE)。

![GitHub 手绘 stars](assets/github-stars.svg)

## Star History

<a href="https://www.star-history.com/#XuTianle0101/fDu-Paper-Skill&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=XuTianle0101/fDu-Paper-Skill&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=XuTianle0101/fDu-Paper-Skill&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=XuTianle0101/fDu-Paper-Skill&type=Date" />
  </picture>
</a>
