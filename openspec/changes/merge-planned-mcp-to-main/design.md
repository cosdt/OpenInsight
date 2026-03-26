## Context

项目有两条从 `65630c0` 分叉的长期分支：

| 分支 | 内容 | 文件数 | 净变更 |
|------|------|--------|--------|
| `planned` | multi-agent 工作流迭代（agents v2、openspec、评审、报告） | ~121 files | +10191/-1117 |
| `mcp` | Python MCP server + 测试套件 | ~118 files | +10350/-1219 |

`main` 停在共同祖先 `65630c0`。20 个文件在两条分支中都有修改，是潜在冲突点。

## Goals / Non-Goals

**Goals:**
- 将两条分支的全部有效工作合入一个新的 `main`
- 保留两条分支的 git 历史（merge commit，非 squash）
- 明确解决所有 20 个冲突文件
- 合并后 MCP server 测试能通过、agent 配置文件完整

**Non-Goals:**
- 不重构任何代码，纯合并操作
- 不修改 MCP server 代码以适配 agent 工作流（后续工作）
- 不处理 opencode.json 与 MCP server 的集成配置（后续工作）

## Decisions

### D1: 合并方向 — 以 planned 为基准，merge mcp 进来

**理由**：`planned` 是当前活跃开发分支（4 个 commit vs mcp 的 1 个），包含更多迭代。以 planned 为基础 merge mcp 可以最小化冲突解决工作量。

**替代方案**：以 mcp 为基准 merge planned → 冲突更多，因为 mcp 删除了大量 planned 需要的文件。

### D2: 冲突解决策略 — 按文件类别分类处理

| 冲突类别 | 文件 | 策略 | 理由 |
|----------|------|------|------|
| 双方各加不同内容 | `.gitignore` | 手动合并，保留双方新增规则 | 两侧规则互不冲突 |
| planned 删除 + mcp 重写 | `README.md` | **需与用户商议** | planned 删除了旧 README（内容移至 docs），mcp 重写为 MCP 项目介绍。两种方向都有道理 |
| planned 演进 + mcp 删除 | `.opencode/agents/*`, `.opencode/skills/*`, `projects/*.md`, `docs/multiagent.md`, `user-prompt*.md`, `tests/evaluate.md` 等 | 保留 planned 版本 | 这些是 agent 工作流核心文件，mcp 分支删除只是因为它专注 MCP 开发 |
| planned 删除 + mcp 保留原版 | `.opencode/instructions.md`, `docs/opencode-local-setup.md`, `docs/prd.md` | 检查 planned 是否有替代 | 若 planned 有新版本则用新版本，否则恢复 |
| 双方都删除 | 部分原始文件 | 不需处理 | 共识删除 |

### D3: merge 到 main 的方式

在 `main` 分支上执行：先 merge `planned`（fast-forward），再 merge `mcp`（产生 merge commit）。

**替代方案**：创建新分支 → 不必要，直接推进 main 更清晰。

### D4: README.md 处理 — 待用户决策

选项：
1. **采用 mcp 版本**：以 MCP server 为项目主介绍（适合项目重心转向 MCP）
2. **合并两者**：写一个新 README，涵盖 agent 工作流 + MCP server 两部分
3. **采用 planned 的做法**（删除 README，内容在 docs/ 中）

## Risks / Trade-offs

- **[风险] merge 后 opencode.json 引用的 MCP 配置可能不一致** → 合并后手动检查 `.mcp.json` 和 `opencode.json` 的一致性
- **[风险] uv.lock 可能与 planned 分支的 Python 环境不兼容** → 合并后运行 `uv sync` 验证
- **[权衡] 保留 planned 的所有 openspec 历史会增加仓库体积** → 可接受，这是项目演进记录

## Open Questions

1. **README.md 如何处理？** → 需要用户决策（见 D4）
2. **合并后是否需要 force-push main？** → 取决于 main 是否有其他协作者
