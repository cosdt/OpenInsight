## ADDED Requirements

### Requirement: URL-Based跨源去重

project-coordinator SHALL在收到所有scout结果后，对动态条目执行URL-based去重：
- 提取每条动态的`url`字段
- 相同URL的条目合并为一条，保留各源的互补信息（如GitHub提供PR diff摘要，Slack提供开发者讨论观点）
- 合并后条目的`evidence_count`字段记录原始出现次数，作为重要性信号

#### Scenario: 同一PR出现在GitHub和Slack

- **WHEN** github-scout返回PR#12345的条目，slack-scout也返回包含PR#12345链接的讨论
- **THEN** coordinator SHALL将两条合并为一条，`evidence_count=2`，摘要整合GitHub的技术变更描述和Slack的开发者讨论要点

#### Scenario: 无重复时正常通过

- **WHEN** 三个scout返回的所有条目URL均不重复
- **THEN** 所有条目SHALL直接进入价值评估阶段，`evidence_count=1`

### Requirement: 语义关联标记

对于URL不同但可能相关的动态（如Discourse RFC和对应的GitHub Issue），coordinator SHALL进行语义关联标记：
- 基于标题关键词相似度识别潜在关联
- 关联条目标记为`related_items`列表，而非强制合并
- 关联关系在报告中展示，帮助用户看到事件的完整图景

#### Scenario: RFC与对应Issue关联

- **WHEN** web-scout返回一条标题为"RFC: New Tensor Subclass API"的Discourse帖子，github-scout返回一条标题为"[RFC] Implement Tensor Subclass API"的Issue
- **THEN** coordinator SHALL将两条标记为related_items，但保持为独立条目，各自参与价值评估

#### Scenario: 无明显关联

- **WHEN** 动态条目的标题之间无关键词重叠
- **THEN** 不进行关联标记，条目保持独立

### Requirement: 数据质量校验

coordinator SHALL在融合后对数据执行质量校验：
- **格式完整性**: 每条动态的6个必填字段均存在且非空
- **时间窗口校验**: 动态日期在请求的时间窗口内
- **异常检测**: 标记明显异常的条目（如summary为空或过短、URL格式无效）
- 校验失败的条目标记为`quality_flag: warning`，不直接丢弃，由coordinator在价值评估时降权

#### Scenario: 缺失字段的条目

- **WHEN** 某条动态缺少`author`字段
- **THEN** coordinator SHALL标记`quality_flag: warning`并在价值评估时对该条目降权，而非丢弃

#### Scenario: 超出时间窗口的条目

- **WHEN** 请求的时间窗口为最近7天，但某条动态的date为30天前
- **THEN** coordinator SHALL将该条目标记为`quality_flag: out_of_range`并从价值评估中排除

### Requirement: 多源佐证作为价值信号

在价值评估阶段，`evidence_count > 1`的条目SHALL获得价值加分：
- 一条动态在多个数据源出现，表明其在社区中引起了跨平台关注
- 加分幅度应使原本处于筛选边界的条目更可能被选为高价值项

#### Scenario: 多源佐证提升价值排名

- **WHEN** 条目A（evidence_count=3）和条目B（evidence_count=1）的初始价值评分接近
- **THEN** 融合后条目A的最终价值评分SHALL高于条目B，因为多源佐证表明更广泛的社区关注
