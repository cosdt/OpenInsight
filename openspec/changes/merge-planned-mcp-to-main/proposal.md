## Why

`planned` 分支承载了多轮迭代的 multi-agent 工作流（agents v2、openspec changes、评审文档、报告产出），`mcp` 分支独立开发了 Python MCP server（pytorch-community-mcp）及完整测试套件。两者从共同祖先 `65630c0` 分叉后各自演进了 ~120 个文件、~10k 行变更，当前 `main` 仍停留在祖先提交。需要将两条线合并为新的 `main`，使项目同时具备 agent 工作流和 MCP 数据层能力。

## What Changes

- 将 `planned` 分支的全部内容（multi-agent runtime、openspec 变更历史、评审/测试文档、报告）作为合并基础
- 将 `mcp` 分支的新增内容（`src/pytorch_community_mcp/`、`tests/test_*.py`、`pyproject.toml`、`uv.lock`、`docs/mcp.md`、`docs/setup.md`）合入
- 解决 20 个双方都修改的文件的冲突，主要类别：
  - `.gitignore`：两侧各添加了不同忽略规则 → 合并
  - `README.md`：planned 删除、mcp 重写 → 需决策
  - `.opencode/agents/*`、`.opencode/skills/*`：planned 大幅演进、mcp 删除 → 保留 planned 版本
  - `projects/pytorch.md`：planned 新增字段、mcp 删除 → 保留 planned 版本
  - `docs/multiagent.md`：planned 重写为需求文档、mcp 删除 → 保留 planned 版本
- **BREAKING**：合并后 `main` 将从纯文档仓库变为包含 Python 包的混合仓库

## Capabilities

### New Capabilities
- `merge-strategy`: 定义两分支合并的冲突解决策略和操作步骤
- `post-merge-validation`: 合并后的验证清单（文件完整性、测试通过、agent 配置可用）

### Modified Capabilities

（无现有 spec 需要修改）

## Impact

- **Git 历史**：main 分支将重置到合并结果，包含两条分支的完整历史
- **项目结构**：新增 `src/`、`tests/`、`pyproject.toml` 等 Python 项目文件
- **CI/依赖**：引入 `uv.lock`，需要 Python 环境支持
- **OpenCode 配置**：`.opencode/` 目录保留 planned 分支的演进版本，`opencode.json` 保留（mcp 分支已删除）
