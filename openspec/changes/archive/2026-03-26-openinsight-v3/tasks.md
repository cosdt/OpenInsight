## 1. 清理与准备

- [x] 1.1 备份当前 `.opencode/agents/` 目录到 `.opencode/agents.v2.bak/`
- [x] 1.2 清空 `.opencode/agents/` 目录，为 v3 agent 定义做准备
- [x] 1.3 更新 `opencode.json` 中的 agent 注册，移除 v2 agent 配置

## 2. Orchestrator Agent

- [x] 2.1 创建 `.opencode/agents/openinsight-orchestrator.md`：定义 primary agent，包含工作流阶段（解析配置→并行采集→融合→深度分析→报告生成→质量门禁）
- [x] 2.2 编写 orchestrator 的输入解析逻辑：从用户消息中提取 project name、time window、user-prompt 文件路径
- [x] 2.3 编写 orchestrator 的 staging 目录初始化逻辑：创建 `reports/.staging/{project}_{date}_{window}/`
- [x] 2.4 编写 orchestrator 的数据融合 prompt 段：URL 去重、语义关联、角色筛选、优先级排序、high-value 标记
- [x] 2.5 编写 orchestrator 的质量门禁 prompt 段：5 维度检查 + 修正循环
- [x] 2.6 编写 orchestrator 的 subagent 通信协议：下发格式（≤500 tokens）和上报格式（≤200 tokens）

## 3. GitHub Collector Agent

- [x] 3.1 创建 `.opencode/agents/github-collector.md`：定义 subagent，负责 GitHub 数据源采集
- [x] 3.2 编写 MCP 工具调用策略：wide-to-narrow 采集（先 list 再 detail），含 gh CLI 降级通道
- [x] 3.3 编写 bot 和噪声过滤规则
- [x] 3.4 编写输出格式定义：staging 文件 `github.md` 的结构
- [x] 3.5 编写 Gotchas section：基于 v2 运行经验的易错点

## 4. Community Collector Agent

- [x] 4.1 创建 `.opencode/agents/community-collector.md`：定义 subagent，负责 Discourse/Blog/Events/Slack 采集
- [x] 4.2 编写 MCP 工具调用策略：每个数据源的调用方式和预期输出
- [x] 4.3 编写错误处理：Slack 不可用时的优雅跳过
- [x] 4.4 编写输出格式定义：staging 文件 `community.md` 的结构
- [x] 4.5 编写 Gotchas section

## 5. Analyst Agent

- [x] 5.1 创建 `.opencode/agents/analyst.md`：定义 subagent，负责 high-value item 深度分析
- [x] 5.2 编写影响面分析 prompt：变更范围、影响链、兼容性、紧急程度
- [x] 5.3 编写源码级分析触发判断 heuristics
- [x] 5.4 编写 repo-management 集成：bare clone 检查、worktree 创建/清理
- [x] 5.5 编写行动建议生成逻辑：类型、优先级、具体建议、依据
- [x] 5.6 编写输出格式定义：staging 文件 `analysis_{n}.md` 的结构

## 6. Composer Agent

- [x] 6.1 创建 `.opencode/agents/composer.md`：定义 subagent，负责从 staging 文件生成 Markdown 报告
- [x] 6.2 编写报告 5 章节结构：概览、重点关注、社区动态（PR/Issue/RFC/Discourse/Blog/Events）、关键人物动态、附录
- [x] 6.3 编写个性化内容生成逻辑：基于 user-prompt.md 定制内容和详细程度
- [x] 6.4 编写源链接完整性保证：每条动态必须包含 URL
- [x] 6.5 编写可解释性：重点关注 items 的入选原因
- [x] 6.6 更新 `.opencode/skills/openinsight-briefing-style/` skill 模板和样式指南

## 7. 配置与集成

- [x] 7.1 更新 `opencode.json`：注册 4 个新 agent，配置工具权限
- [x] 7.2 验证 `projects/pytorch.md` 配置文件与 v3 协议兼容
- [x] 7.3 验证 `user-prompt.md` 和 `user-prompt-core-dev.md` 与 v3 协议兼容
- [x] 7.4 更新 `AGENTS.md` 说明文件

## 8. 测试与验证

- [x] 8.1 使用 `opencode run` 执行端到端测试：`pytorch 最近1天 执行完整工作流生成报告`
- [x] 8.2 验证 staging 目录结构和文件内容完整性
- [x] 8.3 验证报告质量：源链接完整性、可解释性、个性化
- [x] 8.4 验证质量门禁：故意引入缺陷，检查修正循环是否触发
- [x] 8.5 更新 `tests/evaluate.md` 评估框架以匹配 v3 agent 拓扑
- [x] 8.6 运行 3 个可用模型（qwen3.5-plus, glm-5, kimi-k2.5）的对比测试
