## ADDED Requirements

### Requirement: User Prompt配置格式

系统SHALL定义user-prompt.md的标准结构，用户通过此文件描述个性化需求：
- **角色**: 用户在开源社区中的角色（核心开发者/模块维护者/普通贡献者等）
- **关注领域**: 用户关注的模块、技术方向或议题
- **价值判断标准**: 用户定义的"高价值"信息标准
- **输出偏好**: 报告格式、语言、详细程度

#### Scenario: 用户配置示例

- **WHEN** 一个torch-npu团队的开发者配置user-prompt.md
- **THEN** 文件SHALL支持描述角色为"torch-npu开发者"、关注领域为"算子兼容性、编译器后端"、价值标准为"影响npu适配的上游变更"

#### Scenario: 配置文件缺失

- **WHEN** 用户未提供user-prompt.md或文件为空
- **THEN** orchestrator SHALL使用合理的默认值（通用开发者角色、全领域关注、中等详细程度），并提示用户可通过创建user-prompt.md进行个性化配置

### Requirement: 用户配置在工作流中的传递

用户的个性化配置SHALL在multi-agent工作流中完整传递：
- orchestrator读取配置后，将角色和关注领域传递给project-coordinator
- project-coordinator使用这些信息进行价值评估和排序
- briefing-composer使用输出偏好和角色信息进行报告个性化

#### Scenario: 配置信息完整传递

- **WHEN** 用户配置了关注领域为"distributed training"
- **THEN** project-coordinator在价值评估时SHALL优先标记与distributed training相关的动态，briefing-composer在报告中SHALL将这些动态放在显著位置

### Requirement: 时间窗口参数

用户SHALL能够在调用时指定时间窗口参数，支持以下格式：
- 天数：`最近7天`、`last 7 days`
- 日期范围：`2026-03-01 到 2026-03-15`
- 默认值：如未指定，默认为最近1天

#### Scenario: 指定天数

- **WHEN** 用户输入`@user-prompt.md pytorch 最近7天`
- **THEN** orchestrator SHALL解析时间窗口为最近7天，并将对应的起止日期传递给各scout

#### Scenario: 未指定时间窗口

- **WHEN** 用户输入`@user-prompt.md pytorch`但未指定时间
- **THEN** orchestrator SHALL使用默认值（最近1天），并在输出中说明使用的时间范围
