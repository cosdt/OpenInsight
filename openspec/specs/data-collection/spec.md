## ADDED Requirements

### Requirement: GitHub Scout数据采集

`github-scout` SHALL通过GitHub MCP工具采集指定时间窗口内的以下类型动态：
- Pull Requests（标题、作者、标签、状态、摘要）
- Issues（标题、作者、标签、状态、摘要）
- Discussions（标题、分类、摘要）
- Releases（版本号、变更摘要）

采集范围由`projects/<project>.md`中的`scope`字段驱动。

#### Scenario: 采集pytorch最近7天的PR

- **WHEN** github-scout接收到项目pytorch、时间窗口7天、scope包含pr的任务
- **THEN** scout SHALL通过GitHub MCP的list_issues/list_pull_requests/search等工具获取pytorch/pytorch仓库最近7天的PR列表，返回结构化摘要

#### Scenario: GitHub MCP不可用时降级

- **WHEN** GitHub MCP未启用或token无效
- **THEN** github-scout SHALL按降级链尝试：1) gh CLI工具 2) WebFetch访问GitHub页面。最终返回结果中SHALL标注实际使用的获取方式和数据完整性影响

### Requirement: Web Source Scout数据采集

`external-source-scout-web` SHALL通过WebFetch工具采集以下Web源的动态：
- Discourse论坛（dev-discuss.pytorch.org）的核心讨论和RFC
- PyTorch官网博客（pytorch.org/blog）的文章和发布公告

采集范围由`projects/<project>.md`中对应数据源的`scope`字段驱动。

#### Scenario: 采集Discourse论坛RFC

- **WHEN** web-scout接收到pytorch项目、scope包含rfc的任务
- **THEN** scout SHALL通过WebFetch访问dev-discuss.pytorch.org，提取最近时间窗口内的RFC帖子标题、作者和摘要

#### Scenario: Web源不可达时降级

- **WHEN** 目标网站主URL无法访问
- **THEN** web-scout SHALL尝试备用URL（如缓存页面、镜像站），若所有路径均失败则标记该源不可用，对可达的源继续采集，最终在返回结果中标注失败项和降级原因

### Requirement: Slack Scout数据采集

`external-source-scout-slack` SHALL通过Slack MCP工具采集指定频道在时间窗口内的讨论线程，提取主题、参与者和关键内容摘要。

#### Scenario: 采集Slack讨论

- **WHEN** slack-scout接收到指定频道和时间窗口的任务
- **THEN** scout SHALL通过Slack MCP获取该频道的消息线程，按主题聚合并返回摘要

#### Scenario: Slack MCP未配置时降级

- **WHEN** Slack MCP未启用
- **THEN** slack-scout SHALL返回明确提示说明Slack数据源不可用（无替代路径），不影响其他数据源的采集

### Requirement: Scout初步过滤

每个scout SHALL在返回结果前执行初步过滤：
- 去除明显的噪声（bot自动生成的PR、CI-only变更等）
- 每个scout返回的条目数量SHALL有上限（默认不超过30条）
- 每条动态SHALL包含：类型、标题、来源URL、作者、日期、简要摘要

#### Scenario: 过滤bot生成的PR

- **WHEN** github-scout采集到的PR中包含dependabot、renovate等bot创建的自动化PR
- **THEN** scout SHALL将这些PR从结果中过滤掉

#### Scenario: 返回结果格式统一

- **WHEN** 任意scout完成数据采集
- **THEN** 返回的每条动态SHALL包含type、title、url、author、date、summary六个字段

### Requirement: Token预算压缩协议

每个scout的输出SHALL遵循分层压缩协议：

**Layer 1 — 统计摘要**（必须返回）:
- 数据源名称和状态（成功/降级/失败）
- 采集总数 vs 过滤后数量
- 实际使用的获取方式（如降级发生）
- 预算：约50 tokens

**Layer 2 — 条目列表**（必须返回）:
- 每条动态的6字段结构化摘要
- 每条约30-50 tokens，上限30条
- 预算：约900-1500 tokens

**Layer 3 — 补充详情**（按需获取）:
- 仅在coordinator请求特定条目的详情时返回
- 包含完整描述、评论摘要、标签详情等
- 不主动返回，避免上下文膨胀

#### Scenario: 正常压缩输出

- **WHEN** github-scout采集到100条PR，过滤后剩30条
- **THEN** 输出SHALL包含Layer 1（统计：100条采集/30条保留/GitHub MCP正常）和Layer 2（30条结构化摘要），总输出不超过2000 tokens

#### Scenario: Coordinator请求Layer 3

- **WHEN** coordinator对github-scout返回的第5条PR需要更详细信息
- **THEN** coordinator SHALL通过追加消息请求该条目的Layer 3详情，scout SHALL仅返回该条目的完整信息
