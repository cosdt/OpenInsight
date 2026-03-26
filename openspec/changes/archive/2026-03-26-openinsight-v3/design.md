## Context

OpenInsight 是运行在 OpenCode (opencode.ai) 上的 multi-agent 系统，自动采集 PyTorch 社区动态并生成个性化简报。当前 v2 架构有 8 个 agent 类型，通过 coordinator 中间层管理 3 个 scout → evidence-fusion → item-analyst → composer → evaluator 的 pipeline。实际运行中，coordinator 仅做简单委派，3 个 scout 共用同一 MCP server，evidence-fusion 仅做 URL 去重——复杂度远超需要。

技术栈约束：
- 运行时：OpenCode server（`opencode run` / `opencode serve`）
- Agent 定义：`.opencode/agents/*.md`（YAML frontmatter + markdown prompt）
- 数据采集：`pytorch-community` MCP server（独立维护于 `openinsight_mcp`）
- 可用模型：`alibaba-cn/qwen3.5-plus`、`alibaba-cn/glm-5`、`alibaba-cn/kimi-k2.5`
- 输出格式：Markdown 报告，通过 GitHub Pages 静态展示

## Goals / Non-Goals

**Goals:**

- 将 agent 数量从 8 减至 4，消除不必要的中间层
- 保持核心数据采集能力（6 种数据源类型，不含 Release）
- 保持 artifact-based 数据流（staging 文件 + 轻量引用）
- 提高可调试性：更少的 agent 意味着更短的调用链和更清晰的日志
- 遵循 Anthropic multi-agent 范式：simplicity first、heuristics over rules、tool design as ACI
- 满足 docs/requirement.md 的全部功能和质量需求

**Non-Goals:**

- 不修改 `openinsight_mcp` MCP server（独立维护）
- 不引入新的运行时或框架（继续使用 OpenCode）
- 不实现定时触发或 webhook（仅手动触发，通过 `opencode run` 执行）
- 不做 GitHub Pages 部署自动化（保持手动部署）
- 不支持 PyTorch 以外的项目（torch-npu 配置保留但非优先）

## Decisions

### D1: Agent 拓扑——4 个 agent，无 coordinator

```
Orchestrator (primary)
  ├── GitHub Collector (subagent, parallel)
  ├── Community Collector (subagent, parallel)
  ├── Analyst (subagent, per item, max 3 parallel)
  └── Composer (subagent)
```

**选择理由：** Anthropic 范式要求 "simplicity first"——只在有证据时升级复杂度。Coordinator 在 v2 中仅做委派和简单去重，这些职责可以由 orchestrator 直接承担。评审数据流后发现 orchestrator→coordinator→scout 链路中 coordinator 不增加智能决策，只增加延迟和 token 消耗。

**被否决的方案：**
- 保留 coordinator（v2 方案）：复杂度高、调试困难、无智能增益
- 单 collector（无并行）：数据采集串行化，运行时间增加 40-60%
- 无 analyst（orchestrator 自行分析）：orchestrator context window 膨胀，源码分析质量下降

### D2: 数据采集——2 个 Collector 并行，MCP-first

| Collector | 数据源 | MCP 工具 |
|-----------|--------|----------|
| GitHub Collector | PR, Issue, RFC, Commits, Key Contributors | `get_prs`, `get_issues`, `get_rfcs`, `get_commits`, `get_key_contributors_activity` |
| Community Collector | Discourse, Blog, Events, Slack | `get_discussions`, `get_blog_news`, `get_events`, `get_slack_threads` |

**选择理由：** v2 的 3 个 scout 中 Slack scout 使用频率最低（Slack MCP 经常 disabled），合并到 Community Collector。GitHub 和 Community 数据源有天然分界，适合并行。两个 collector 以 `pytorch-community` MCP server 为主要数据源，GitHub Collector 保留 `gh` CLI 作为降级通道（MCP server 有已知可靠性问题）。不采集 Release 信息。

**被否决的方案：**
- 3 个 scout（v2 方案）：Slack 独立 scout 利用率低，增加管理开销
- 1 个 collector：失去并行优势，总采集时间更长

### D3: Orchestrator 承担 fusion 和质量门禁

Orchestrator 在收到两个 collector 的输出后，直接执行：
1. **读取** staging 文件 `github.md` 和 `community.md`
2. **去重**：按 URL 去重
3. **筛选**：基于用户角色（user-prompt.md）筛选相关动态
4. **排序**：按影响面和紧急程度排序
5. **选择**：标记需要深度分析的 high-value items
6. **写入** `fusion.md`

质量门禁也由 orchestrator 在 composer 输出后执行，检查 5 个维度：事实准确性、源链接完整性、覆盖度、个性化匹配度、可解释性。不通过则给 composer 一次修正机会。

**选择理由：** Fusion 是读两个文件→去重→写一个文件的简单操作，不需要独立 agent。Quality gate 是 5 条 checklist，orchestrator 有足够 context 执行。将两者集成到 orchestrator 减少了 2 个 agent 和 2 次 LLM 调用。

### D4: Staging 目录结构简化

```
reports/.staging/{project}_{date}_{window}/
  github.md          # GitHub Collector 输出
  community.md       # Community Collector 输出
  fusion.md          # Orchestrator 融合结果
  analysis_{n}.md    # Analyst 深度分析（每个 item 一个文件）
```

去掉 v2 的 `phase1_`/`phase2_`/`phase3_` 前缀。文件名语义化，直接反映内容来源。

### D5: Heuristics-driven prompt 设计

所有 agent prompt 遵循 "heuristics over rigid rules" 原则：

- **不要**：`步骤1: 调用 get_prs。步骤2: 调用 get_issues。步骤3: ...`
- **要**：`像一个经验丰富的开源社区研究员一样工作。先用 wide queries 探索数据全景，评估各数据源的覆盖情况，然后逐步聚焦到高价值信号。`

每个 prompt 包含：
1. **角色定义**（intent-based，非 step-by-step）
2. **可用工具列表**（带明确的选择启发式）
3. **输出格式**（staging 文件的 schema）
4. **边界**（明确不做什么）
5. **Gotchas**（基于 v2 运行经验积累的易错点）

### D6: Analyst 触发条件由 Orchestrator 自主判断

Orchestrator 在 fusion 阶段根据以下 heuristics 判断是否需要深度分析：
- 涉及 breaking API change 的 PR/RFC
- 影响用户关注模块（由 user-prompt.md 定义）的重大改动
- 跨多个子项目的关联变更

这些不是硬规则，是启发式——orchestrator 可以根据具体情况调整。源码级分析的触发完全由 analyst agent 自主判断。

### D7: GitHub Collector 保留 gh CLI 降级通道

`pytorch-community` MCP server 有已知可靠性问题（Connection closed、无分页等）。GitHub Collector 在 MCP 工具失败时，SHALL 降级到 `gh` CLI 采集 PR 和 Issue 数据。

降级映射：
| MCP 工具 | gh CLI 降级 |
|----------|------------|
| `get_prs` | `gh pr list --json ...` |
| `get_issues` | `gh issue list --json ...` |
| `get_rfcs` | 无降级（跳过并记录警告） |
| `get_commits` | `gh api repos/{owner}/{repo}/commits` |
| `get_key_contributors_activity` | 无降级（跳过并记录警告） |

Community Collector 无降级通道——MCP 失败则跳过该数据源。

**选择理由：** GitHub 数据（PR/Issue）是报告价值的核心来源，不能因 MCP 故障全部丢失。gh CLI 已在环境中可用且经过 v2 验证。Community 数据（Discourse/Blog/Events/Slack）价值密度较低，丢失可接受。

### D8: 不采集 Release，仅手动触发

- **Release**：从数据源中移除。Release 信息变化频率低，用户可通过 GitHub 直接查看。
- **触发方式**：仅支持手动触发（`opencode run`），不实现周期执行。

## Risks / Trade-offs

**[Orchestrator context 膨胀]** → Orchestrator 承担 fusion + quality gate，context window 使用量增加。**缓解**：staging 文件只在需要时读取，conversation 中传递轻量引用（≤200 tokens）。如果未来运行中 orchestrator 频繁触及 context limit，再考虑拆分。

**[2 个 collector 覆盖不均]** → GitHub Collector 处理 5 种数据源，Community Collector 处理 4 种，工作量可能不均衡导致一方成为瓶颈。**缓解**：两个 collector 并行执行，总时间取决于最慢的那个。实测后如果不均衡严重再调整分配。

**[Heuristics 的不可预测性]** → Heuristics-driven prompt 可能导致不同运行产生不同的分析深度和覆盖范围。**缓解**：通过 quality gate 确保底线质量。通过 20+ 测试用例建立 baseline。接受一定的变异性——这是 heuristics 的设计意图。

**[Analyst 并行限制]** → 多个 analyst 同时运行可能触及 API rate limit。**缓解**：batch size 限制为 max 3，与 v2 的 batch-of-2 相比仅微增。

**[v2 → v3 迁移]** → 全量替换所有 agent 定义，无渐进迁移路径。**缓解**：v3 是 prompt-only 变更（agent .md 文件），不涉及运行时代码修改。旧文件可通过 git 恢复。staging 目录结构向后兼容（新文件名不会与旧文件冲突）。
