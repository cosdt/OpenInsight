## ADDED Requirements

### Requirement: Agent 拓扑定义

系统 SHALL 由 4 个 agent 类型组成：

| Agent | Mode | 职责 |
|-------|------|------|
| Orchestrator | primary | 工作流编排、数据融合、质量门禁 |
| GitHub Collector | subagent | GitHub 数据源采集 |
| Community Collector | subagent | 社区数据源采集（Discourse/Blog/Events/Slack） |
| Analyst | subagent | 高价值 item 深度分析 |
| Composer | subagent | 个性化报告生成 |

Orchestrator SHALL 作为唯一的 primary agent，所有其他 agent 均为 subagent。

#### Scenario: 用户触发标准工作流

- **WHEN** 用户向 orchestrator 提交 `{project} 最近{window} 执行完整工作流生成报告`
- **THEN** orchestrator SHALL 按顺序执行：解析输入 → 加载配置 → 并行采集 → 融合筛选 → 深度分析 → 报告生成 → 质量检查

### Requirement: Orchestrator 工作流阶段

Orchestrator SHALL 按以下阶段执行工作流：

1. **解析与配置**：从用户输入解析 project name 和 time window，加载 `projects/{project}.md` 和 `user-prompt.md`
2. **Staging 初始化**：创建 `reports/.staging/{project}_{date}_{window}/` 目录
3. **并行采集**：同时启动 GitHub Collector 和 Community Collector
4. **数据融合**：读取 collector 输出，执行 URL 去重、关联分析、优先级排序，写入 `fusion.md`
5. **深度分析**（可选）：对标记的 high-value items 启动 Analyst subagent
6. **报告生成**：启动 Composer subagent 生成最终报告
7. **质量门禁**：检查报告质量，不通过则给 Composer 一次修正机会

#### Scenario: 完整工作流正常执行

- **WHEN** orchestrator 收到 `pytorch 最近1周 执行完整工作流生成报告`
- **THEN** orchestrator SHALL 创建 staging 目录，并行启动两个 collector，等待两者完成后执行融合，选择 high-value items 进行深度分析，启动 composer 生成报告，执行质量检查

#### Scenario: 无 high-value items 需要深度分析

- **WHEN** orchestrator 完成融合后判断没有 item 需要深度分析
- **THEN** orchestrator SHALL 跳过深度分析阶段，直接启动 composer

### Requirement: 数据融合职责

Orchestrator SHALL 在收到两个 collector 的完成信号后，读取 staging 文件执行数据融合：

1. **URL 去重**：相同 URL 的 item 合并为一条，保留信息最丰富的版本
2. **语义关联**：识别跨数据源引用同一变更的 items（如 PR 和对应的 Discourse 讨论）
3. **角色筛选**：基于 `user-prompt.md` 中定义的关注领域过滤低相关度 items
4. **优先级排序**：按影响面和紧急程度排序，标记 high-value items
5. **输出**：写入 `fusion.md`，包含排序后的 item 列表和 high-value 标记

#### Scenario: 跨数据源关联

- **WHEN** GitHub Collector 报告了一个 PR `#12345`，Community Collector 报告了一个 Discourse 帖子讨论同一 PR
- **THEN** orchestrator SHALL 在 fusion.md 中将两者关联为同一事项，合并信息

#### Scenario: 基于角色的筛选

- **WHEN** user-prompt.md 定义用户关注 "operator compatibility, compiler backends"，fusion 数据中包含一个纯文档修复的 PR
- **THEN** orchestrator SHALL 将该 PR 标记为低优先级或过滤掉

### Requirement: 质量门禁

Orchestrator SHALL 在 Composer 生成报告后执行 5 维度质量检查：

1. **事实准确性**：报告中的声明 MUST 能在 staging 文件中找到对应数据支撑
2. **源链接完整性**：每条动态 MUST 包含指向原始数据源的 URL
3. **覆盖度**：报告 MUST 覆盖 fusion.md 中所有 high-priority items
4. **个性化匹配度**：报告内容 MUST 与 user-prompt.md 定义的角色关注点一致
5. **可解释性**：每条动态 MUST 说明被选入简报的原因

不通过 SHALL 触发一次且仅一次修正循环。

#### Scenario: 质量检查通过

- **WHEN** 报告满足全部 5 个维度
- **THEN** orchestrator SHALL 将报告从 staging 移动到 `reports/` 目录

#### Scenario: 质量检查不通过

- **WHEN** 报告缺少 2 条 high-priority item 的源链接
- **THEN** orchestrator SHALL 向 composer 发送修正指令，附带具体的缺陷描述，等待修正后的报告

#### Scenario: 修正后仍不通过

- **WHEN** 修正后的报告仍未通过质量检查
- **THEN** orchestrator SHALL 接受当前报告并在报告末尾附加质量警告标记，不再循环

### Requirement: Subagent 通信协议

Orchestrator 与 subagent 之间 SHALL 通过以下方式通信：

- **下发**：conversation message 中传递任务描述 + staging 目录路径 + 配置参数（≤500 tokens）
- **上报**：subagent 将完整输出写入 staging 文件，conversation message 中仅返回完成状态 + 摘要（≤200 tokens）

MUST NOT 在 conversation message 中传递完整数据内容。

#### Scenario: Orchestrator 启动 Collector

- **WHEN** orchestrator 启动 GitHub Collector
- **THEN** orchestrator SHALL 传递：项目配置（repo、数据源列表）、时间窗口、staging 目录路径、输出文件名

#### Scenario: Collector 返回结果

- **WHEN** GitHub Collector 完成数据采集
- **THEN** collector SHALL 将完整数据写入 `staging/github.md`，向 orchestrator 返回 `已完成，共采集 N 条 items，覆盖 PR/Issue/RFC/Commits`
