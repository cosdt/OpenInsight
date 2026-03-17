## ADDED Requirements

### Requirement: 深度分析能力

`item-analyst` SHALL对单条高价值动态执行深度分析，分析维度包括：
- **变更概要**: 该动态的核心内容和目标
- **影响评估**: 对用户（基于角色）的潜在影响程度和方式
- **技术细节**: 涉及的模块、API、代码路径
- **建议行动**: 用户应该采取的响应行动（关注、参与讨论、代码审查等）

#### Scenario: 分析一个破坏性API变更的PR

- **WHEN** item-analyst接收到一个标题含"deprecate"或"breaking change"的PR进行分析
- **THEN** analyst SHALL识别出受影响的API，分析影响范围，并在建议行动中标注需要关注的紧急程度

#### Scenario: 分析一个新特性RFC

- **WHEN** item-analyst接收到一个RFC类型的动态
- **THEN** analyst SHALL总结RFC的目标、设计方案、社区讨论态度，并评估对用户的参与价值

### Requirement: 代码静态分析

对于涉及代码变更的动态（PR、Issue），item-analyst SHALL具备通过代码搜索和文件读取进行静态分析的能力：
- 使用grep/search工具查找受影响的代码路径
- 使用read工具检查具体文件内容
- 结合项目配置中的related_repos分析跨仓库影响

#### Scenario: 分析PR对torch-npu的影响

- **WHEN** item-analyst分析一个pytorch/pytorch的PR，且项目配置中torch-npu标记为related/upstream
- **THEN** analyst SHALL评估该PR的变更是否可能影响torch-npu的兼容性，通过代码搜索相关模块和API使用情况

#### Scenario: 本地代码分析开关

- **WHEN** 项目配置中`local_analysis_enabled: false`
- **THEN** item-analyst SHALL跳过需要本地仓库的深度代码分析，仅基于PR/Issue描述和diff进行分析

### Requirement: Wisdom Notepad消费与贡献

每个item-analyst session SHALL：
1. **消费wisdom**: 在分析开始时读取coordinator传入的wisdom notepad，将其作为先验知识指导分析方向
2. **贡献wisdom**: 在分析结束时，在结果中附带`wisdom_contribution`字段，包含本次分析中发现的可复用知识

wisdom_contribution的类型包括：
- `module_insight`: 模块级发现（如"torch.distributed正在大规模重构"）
- `person_pattern`: 人物活动模式（如"@pytorchbot 近期主要在autograd模块活跃"）
- `cross_reference`: 跨动态关联（如"此PR与Issue #12345直接相关"）
- `codebase_pattern`: 代码模式发现（如"该仓库的breaking change通常在utils/目录先出现"）

#### Scenario: 利用wisdom发现跨item关联

- **WHEN** item-analyst收到wisdom notepad中包含"开发者X正在推进distributed training重构"，且当前分析的PR作者也是开发者X
- **THEN** analyst SHALL在分析中引用此先验知识，将本PR置于更大的重构叙事中评估其影响

#### Scenario: 贡献新wisdom

- **WHEN** item-analyst在分析中发现一个全新的模块依赖关系（如torch.compile依赖torch._dynamo的内部API）
- **THEN** analyst SHALL在wisdom_contribution中记录此发现，类型为module_insight，供后续analyst使用

#### Scenario: 空wisdom notepad

- **WHEN** 这是coordinator分配的第一个item-analyst（wisdom notepad为空）
- **THEN** analyst SHALL正常执行分析，不依赖先验知识，并在完成后贡献wisdom

### Requirement: 分析结果结构化输出

item-analyst SHALL以结构化格式返回分析结果，包含：
- `item_type`: 动态类型（PR/Issue/RFC/Discussion等）
- `item_title`: 原始标题
- `item_url`: 来源链接
- `summary`: 深度分析摘要（200-500字）
- `impact_level`: 影响等级（high/medium/low）
- `impact_areas`: 受影响的模块或领域列表
- `recommended_action`: 建议行动
- `analysis_depth`: 分析深度标记（surface/code-level）
- `evidence_sources`: 本次分析引用的信息源列表（如"PR diff", "torch-npu source grep", "Discourse discussion"）
- `wisdom_contribution`: 本次分析贡献的可复用发现列表

#### Scenario: 输出结构完整性

- **WHEN** item-analyst完成对任意动态项的分析
- **THEN** 返回结果SHALL包含上述所有字段，不允许缺失必填字段
