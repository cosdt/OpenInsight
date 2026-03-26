## ADDED Requirements

### Requirement: Fast-forward planned into main
main 分支 SHALL 先 fast-forward 到 planned 分支的 HEAD（`8907f2d`），使 main 包含 planned 的全部历史。

#### Scenario: Fast-forward merge
- **WHEN** 在 main 分支执行 `git merge planned`
- **THEN** main 的 HEAD 等于 planned 的 HEAD，无 merge commit 产生

### Requirement: Merge mcp into main with conflict resolution
main（已包含 planned）SHALL merge mcp 分支，产生一个 merge commit，所有冲突按分类策略解决。

#### Scenario: Merge mcp branch
- **WHEN** 在 main 分支执行 `git merge mcp`
- **THEN** 产生 merge commit，包含 mcp 的全部新增文件（src/、tests/test_*.py、pyproject.toml、uv.lock、docs/mcp.md、docs/setup.md）

### Requirement: .gitignore 合并双方规则
合并后的 `.gitignore` SHALL 同时包含 planned 新增的规则（`.cache`、`.codex`、`.claude`、`CLAUDE.md`、`AGENTS.md`、`reports/.staging/`）和 mcp 新增的规则（`__pycache__/`、`*.pyc`）。

#### Scenario: Both ignore rules present
- **WHEN** 合并完成后检查 `.gitignore`
- **THEN** 文件包含 `__pycache__/`、`*.pyc`、`.cache`、`.codex`、`.claude`、`CLAUDE.md`、`AGENTS.md` 等规则

### Requirement: planned 演进文件优先保留
对于 planned 分支演进但 mcp 分支删除的文件（`.opencode/agents/*`、`.opencode/skills/*`、`projects/*.md`、`docs/multiagent.md`、`user-prompt*.md`、`opencode.json` 等），合并结果 SHALL 保留 planned 版本。

#### Scenario: Agent files preserved
- **WHEN** 合并完成后检查 `.opencode/agents/openinsight-orchestrator.md`
- **THEN** 文件内容等于 planned 分支的版本（包含 v2 演进内容）

### Requirement: README.md 需用户决策
README.md 的最终内容 SHALL 由用户在冲突解决阶段决定，不自动选择任何一方。

#### Scenario: README conflict flagged
- **WHEN** merge 遇到 README.md 冲突
- **THEN** 暂停并向用户展示三个选项：采用 mcp 版本 / 合并两者 / 不保留 README
