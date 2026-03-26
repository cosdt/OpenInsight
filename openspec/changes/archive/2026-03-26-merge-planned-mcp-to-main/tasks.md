## 1. 准备工作

- [x] 1.1 确认当前 planned 分支无未提交变更（stash 或 commit working changes）
- [x] 1.2 确认 mcp worktree（`/Users/chu/project/openinsight_mcp`）状态干净

## 2. Fast-forward main to planned

- [x] 2.1 切换到 main 分支：`git checkout main`
- [x] 2.2 Fast-forward merge planned：`git merge planned`（应为 fast-forward，无冲突）
- [x] 2.3 验证 main HEAD 等于 planned HEAD（`8907f2d`）

## 3. Merge mcp into main

- [x] 3.1 执行 `git merge mcp`，触发冲突
- [x] 3.2 解决 `.gitignore` 冲突：合并双方新增的忽略规则
- [x] 3.3 解决 `README.md` 冲突：写新的综合 README
- [x] 3.4 解决 `.opencode/agents/*` 冲突：全部保留 planned 版本（`git checkout --ours`）
- [x] 3.5 解决 `.opencode/skills/*` 冲突：全部保留 planned 版本
- [x] 3.6 解决 `.opencode/instructions.md` 冲突：无冲突（planned 已删除，mcp 也删除）
- [x] 3.7 解决 `projects/pytorch.md`、`projects/torch-npu.md` 冲突：保留 planned 版本
- [x] 3.8 解决 `docs/multiagent.md` 冲突：保留 planned 版本
- [x] 3.9 解决其余冲突文件：无额外冲突
- [x] 3.10 `git add` 所有已解决的文件，创建 merge commit

## 4. 合并后验证

- [x] 4.1 检查 `src/pytorch_community_mcp/` 目录完整性（与 mcp 分支对比文件列表）
- [x] 4.2 检查 `.opencode/agents/` 目录完整性（与 planned 分支对比）
- [x] 4.3 检查 `openspec/` 目录完整性（main 是 planned + mcp 的超集）
- [x] 4.4 检查 `pyproject.toml` 和 `uv.lock` 存在
- [x] 4.5 运行 `uv sync --all-extras` 确认依赖可安装
- [x] 4.6 运行 `uv run pytest` — 161 passed, 0 failures
- [x] 4.7 对比文件数量：216 ≥ max(117, 103) ✓

## 5. 清理

- [x] 5.1 删除 mcp worktree：`git worktree remove --force`（仅含临时文件）
- [x] 5.2 删除 mcp 本地分支：`git branch -d mcp`
- [x] 5.3 确认 main 分支状态正确：merge commit 8b090f0，两条分支历史完整保留
