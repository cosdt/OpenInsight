## ADDED Requirements

### Requirement: Analyst 触发条件

Analyst subagent SHALL 由 orchestrator 在融合阶段标记 high-value items 后启动。

触发的启发式条件（非硬规则，orchestrator 可自主调整）：
- 涉及 breaking API change 的 PR 或 RFC
- 影响用户关注模块的重大改动（由 user-prompt.md 定义）
- 跨多个子项目的关联变更
- 新的 RFC 提案

每个 high-value item 启动一个 Analyst 实例，最多 3 个并行。

#### Scenario: Breaking API change 触发分析

- **WHEN** fusion.md 中标记了一个 PR 包含 `[BC-breaking]` 标签
- **THEN** orchestrator SHALL 启动 Analyst 对该 PR 进行深度分析

#### Scenario: 无 high-value items

- **WHEN** fusion.md 中没有 item 被标记为 high-value
- **THEN** orchestrator SHALL 跳过深度分析阶段

#### Scenario: 超过并行上限

- **WHEN** fusion.md 中有 5 个 high-value items
- **THEN** orchestrator SHALL 分两批执行（3 + 2），等第一批完成后启动第二批

### Requirement: 影响面分析

Analyst SHALL 对分配的 item 执行影响面分析，包含：

1. **变更范围**：识别受影响的模块、API、组件
2. **影响链**：追踪变更对下游项目（如 torch-npu）的传导路径
3. **兼容性**：评估对现有代码的兼容性影响
4. **紧急程度**：判断该变更是否需要团队立即响应

#### Scenario: PR 影响面分析

- **WHEN** Analyst 收到一个修改 `torch.distributed` 模块的 PR
- **THEN** Analyst SHALL 分析该 PR 对分布式训练工作流的影响，评估是否影响下游 NPU 适配

### Requirement: 源码级分析

Analyst SHALL 自主判断是否需要源码级分析。当 Analyst 判断以下条件满足时，SHALL 使用本地仓库进行代码级分析：

- PR 修改了用户关注模块的核心 API
- 需要版本对比来理解变更的完整影响
- 变更涉及复杂的跨模块依赖

源码级分析使用 `repo-management` 规范定义的 bare clone 和 worktree 机制。

#### Scenario: 需要源码级分析

- **WHEN** Analyst 分析一个修改 `torch.compile` 内部实现的 PR，且用户关注 compiler backends
- **THEN** Analyst SHALL 创建 worktree，检出相关代码，分析具体的代码变更和影响范围

#### Scenario: 不需要源码级分析

- **WHEN** Analyst 分析一个新增教程文档的 PR
- **THEN** Analyst SHALL 仅基于 PR 描述和评论进行分析，不创建 worktree

### Requirement: 行动建议

Analyst SHALL 为每个分析的 item 提供具体的行动建议：

- **建议类型**：关注/跟进/适配/忽略
- **建议内容**：具体说明团队应采取什么行动
- **优先级**：P0（立即行动）/ P1（本周内）/ P2（关注即可）
- **依据**：说明建议的推理过程

#### Scenario: 需要适配的变更

- **WHEN** Analyst 分析发现一个 PR 将移除 torch-npu 依赖的内部 API
- **THEN** Analyst SHALL 建议类型为"适配"，优先级 P0，具体说明哪个 API 被移除及建议的替代方案

### Requirement: Analyst 输出格式

Analyst SHALL 将分析结果写入 staging 文件 `analysis_{n}.md`，格式如下：

```markdown
# 深度分析: {item_title}

## 基本信息
- URL: {source_url}
- 类型: {PR/Issue/RFC}
- 分析深度: {overview/code-level/version-comparison}

## 影响面分析
{impact_analysis}

## 源码分析（如有）
{code_analysis}

## 行动建议
- 类型: {关注/跟进/适配/忽略}
- 优先级: {P0/P1/P2}
- 建议: {具体行动}
- 依据: {推理过程}
```

#### Scenario: 完整深度分析输出

- **WHEN** Analyst 完成一个 code-level 深度分析
- **THEN** Analyst SHALL 按上述格式写入 staging 文件，所有字段均填充完整
