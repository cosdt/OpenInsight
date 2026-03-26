# OpenInsight Agent 拓扑 (v3)

## 架构概览

```
Orchestrator (primary)
  ├── GitHub Collector (subagent, parallel)
  ├── Community Collector (subagent, parallel)
  ├── Analyst (subagent, per high-value item, max 3 parallel)
  └── Composer (subagent)
```

## Agent 定义

| Agent | 文件 | Mode | 职责 |
|-------|------|------|------|
| Orchestrator | `openinsight-orchestrator.md` | primary | 工作流编排、数据融合、质量门禁 |
| GitHub Collector | `github-collector.md` | subagent | GitHub 数据源采集（PR/Issue/RFC/Commits/Key Contributors） |
| Community Collector | `community-collector.md` | subagent | 社区数据源采集（Discourse/Blog/Events/Slack） |
| Analyst | `analyst.md` | subagent | 高价值 item 深度分析与行动建议 |
| Composer | `composer.md` | subagent | 个性化 Markdown 报告生成 |

## 工作流

1. **解析与配置** — Orchestrator 解析用户输入，加载项目配置和用户角色
2. **Staging 初始化** — 创建 `reports/.staging/{project}_{date}_{window}/`
3. **并行采集** — 同时启动 GitHub Collector 和 Community Collector
4. **数据融合** — Orchestrator 读取 staging 文件，执行去重、筛选、排序
5. **深度分析**（可选） — 对 high-value items 启动 Analyst（最多 3 并行）
6. **报告生成** — 启动 Composer 生成最终报告
7. **质量门禁** — Orchestrator 检查报告质量（5 维度），不通过则一次修正

## 数据流

- Subagent 将完整数据写入 staging 文件
- 对话消息仅传递轻量引用（≤200 tokens）
- Composer 从 `fusion.md` 读取数据，不直接读取 collector 原始输出

## MCP 数据源

| MCP Server | 用途 |
|------------|------|
| `pytorch-community` | PR/Issue/RFC/Commits/Contributors/Discourse/Blog/Events/Slack |
| `github` | GitHub Copilot MCP（备用） |

## 降级策略

- GitHub Collector：MCP 失败 → gh CLI（PR/Issue/Commits）
- Community Collector：MCP 失败 → 跳过该数据源（无降级通道）
