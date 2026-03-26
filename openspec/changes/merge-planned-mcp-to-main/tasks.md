## 1. 准备工作

- [ ] 1.1 确认当前 planned 分支无未提交变更（stash 或 commit working changes）
- [ ] 1.2 确认 mcp worktree（`/Users/chu/project/openinsight_mcp`）状态干净

## 2. Fast-forward main to planned

- [ ] 2.1 切换到 main 分支：`git checkout main`
- [ ] 2.2 Fast-forward merge planned：`git merge planned`（应为 fast-forward，无冲突）
- [ ] 2.3 验证 main HEAD 等于 planned HEAD（`8907f2d`）

## 3. Merge mcp into main

- [ ] 3.1 执行 `git merge mcp`，触发冲突
- [ ] 3.2 解决 `.gitignore` 冲突：合并双方新增的忽略规则
- [ ] 3.3 解决 `README.md` 冲突：向用户展示选项并等待决策
- [ ] 3.4 解决 `.opencode/agents/*` 冲突：全部保留 planned 版本（`git checkout --ours`）
- [ ] 3.5 解决 `.opencode/skills/*` 冲突：全部保留 planned 版本
- [ ] 3.6 解决 `.opencode/instructions.md` 冲突：保留 planned 版本（若存在）
- [ ] 3.7 解决 `projects/pytorch.md`、`projects/torch-npu.md` 冲突：保留 planned 版本
- [ ] 3.8 解决 `docs/multiagent.md` 冲突：保留 planned 版本
- [ ] 3.9 解决其余冲突文件（`docs/prd.md`、`docs/opencode-local-setup.md` 等）：逐一检查
- [ ] 3.10 `git add` 所有已解决的文件，创建 merge commit

## 4. 合并后验证

- [ ] 4.1 检查 `src/pytorch_community_mcp/` 目录完整性（与 mcp 分支对比文件列表）
- [ ] 4.2 检查 `.opencode/agents/` 目录完整性（与 planned 分支对比）
- [ ] 4.3 检查 `openspec/` 目录完整性
- [ ] 4.4 检查 `pyproject.toml` 和 `uv.lock` 存在
- [ ] 4.5 运行 `uv sync` 确认依赖可安装
- [ ] 4.6 运行 `uv run pytest` 确认测试通过
- [ ] 4.7 对比文件数量：合并结果 ≥ max(planned, mcp) 的独有文件数

## 5. 清理

- [ ] 5.1 删除 mcp worktree：`git worktree remove /Users/chu/project/openinsight_mcp`
- [ ] 5.2 删除 mcp 本地分支（可选）：`git branch -d mcp`
- [ ] 5.3 确认 main 分支状态正确，考虑是否 push
