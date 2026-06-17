# 内嵌 latex-paper-skills 快照

[English](README.md) | 简体中文

这个目录是 `latex-paper-skills` 的部分内嵌快照，只作为复旦学位论文 skill 的可选辅助工具包保留。它不是完整上游仓库。

## 已包含内容

- [.codex/skills/](.codex/skills/) 下的可复用 Codex skills。
- 这些 skills 使用的共享脚本和 references。
- 上游 [MIT License](LICENSE)。

## 未包含内容

- showcase 项目、生成论文、数据集、截图和流程图资产。
- 上游新手工作流指南。
- 与上游仓库实时同步的承诺。

## Skill 入口

- [paper-from-zero](.codex/skills/paper-from-zero/SKILL.md)：将选题路由到合适的论文写作流程。
- [arxiv-paper-writer](.codex/skills/arxiv-paper-writer/SKILL.md)：用门禁 LaTeX 和引用流程撰写综述/调研论文。
- [empirical-paper-writer](.codex/skills/empirical-paper-writer/SKILL.md)：规划并撰写有实验证据支撑的论文。
- [results-backfill](.codex/skills/results-backfill/SKILL.md)：真实结果就绪后替换草稿中的占位内容。
- [latex-rhythm-refiner](.codex/skills/latex-rhythm-refiner/SKILL.md)：在保留引用位置的前提下润色 LaTeX 文本。
- [check-collaborators](.codex/skills/check-collaborators/SKILL.md)：检查可选协作 CLI 是否可用。
- [collaborating-with-gemini](.codex/skills/collaborating-with-gemini/SKILL.md)：把 Gemini 作为可选的广度协作者。
- [collaborating-with-claude](.codex/skills/collaborating-with-claude/SKILL.md)：把 Claude 作为可选的深度协作者。

## 在本仓库中的使用方式

复旦学位论文任务应从主 skill [../../skills/fdu-final-paper-skill/SKILL.md](../../skills/fdu-final-paper-skill/SKILL.md) 开始。仅当任务需要 LaTeX、BibTeX、引用审计、规划或结果回填机制时，再加载这些内嵌 skills。

除非用户明确要求，不要把 arXiv、IEEEtran、ML/AI、页数限制或双栏排版假设继承到复旦学位论文任务中。
