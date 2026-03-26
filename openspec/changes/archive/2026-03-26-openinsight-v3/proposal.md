## Why

当前系统（v2）过度工程化：8 个 agent 类型、coordinator 中间层、3 个独立 scout 却共用同一 MCP server、evidence-fusion 作为独立阶段但实际只做去重。复杂度远超需求本身，导致调试困难、运行缓慢、质量不稳定。需要基于 Anthropic multi-agent 范式从头重建，以 "simplicity first" 为核心原则，用最少的 agent 和最清晰的数据流满足 docs/requirement.md 的全部需求。

## What Changes

- **删除 coordinator 中间层**：orchestrator 直接管理 worker agents，消除不必要的间接层
- **合并 3 个 scout 为 2 个 collector**：GitHub Collector（PR/Issue/RFC/Commits/关键人物）+ Community Collector（Discourse/Blog/Events/Slack），MCP-first + gh CLI 降级
- **Orchestrator 承担 fusion 职责**：数据融合、去重、筛选、优先级排序由 orchestrator 完成，不再需要独立的 evidence-fusion 阶段
- **简化 evaluator**：质量检查集成到 orchestrator 的最终步骤，不再作为独立 agent
- **统一 artifact 协议**：所有 agent 输出写入 staging 文件，conversation 中只传递轻量引用（≤200 tokens）
- **Heuristics-driven prompt**：所有 agent prompt 编码专家启发式而非死板规则，允许 agent 自主判断（如源码分析的触发时机）
- **Agent 数量从 8 → 4**：Orchestrator、Collector(×2 parallel)、Analyst、Composer

## Capabilities

### New Capabilities

- `orchestration`: Agent 拓扑、生命周期管理、数据融合与筛选、质量门禁——统一 orchestrator 的完整职责
- `data-pipeline`: 统一数据采集协议——Collector agent 如何使用 MCP 工具、输出格式、降级策略、去重规则
- `deep-analysis`: 影响面分析与源码级洞察——Analyst agent 的触发条件、分析深度、输出结构
- `report-composition`: 报告生成——Composer agent 如何从 staging 文件合成个性化 Markdown 报告
- `personalization`: 用户角色与项目配置系统——如何驱动个性化筛选和报告定制

### Modified Capabilities

- `repo-management`: 更新 worktree 路径约定以匹配 v3 staging 目录结构

## Impact

- **Agent 文件**：删除 `.opencode/agents/` 下全部 8 个 agent 定义，重写为 4 个
- **Skills**：更新 `openinsight-briefing-style` skill 的模板和样式指南
- **配置**：更新 `opencode.json` 的 agent 注册和工具权限
- **Staging 协议**：简化 `reports/.staging/` 目录结构（去掉 phase 编号前缀）
- **用户 Prompt**：保留 `user-prompt.md` 和 `user-prompt-core-dev.md`，但更新引用方式
- **项目配置**：保留 `projects/*.md`，更新格式以匹配 v3 协议
- **MCP Server**：不变（`openinsight_mcp` 独立维护）
- **测试**：更新 `tests/` 下的评估框架以匹配新 agent 拓扑
- **旧 Specs**：`openspec/specs/` 下现有 8 个 spec 全部由 v3 新 spec 取代
