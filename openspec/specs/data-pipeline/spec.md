## ADDED Requirements

### Requirement: Collector 数据源分配

系统 SHALL 配置两个 collector agent，数据源分配如下：

| Collector | 数据源 | MCP 工具 |
|-----------|--------|----------|
| GitHub Collector | PR, Issue, RFC, Commits, Key Contributors | `get_prs`, `get_issues`, `get_rfcs`, `get_commits`, `get_key_contributors_activity` |
| Community Collector | Discourse, Blog, Events, Slack | `get_discussions`, `get_blog_news`, `get_events`, `get_slack_threads` |

两个 collector SHALL 由 orchestrator 并行启动。

#### Scenario: 标准数据采集

- **WHEN** orchestrator 启动两个 collector，指定 project=pytorch, window=1周
- **THEN** GitHub Collector SHALL 调用 `get_prs`, `get_issues`, `get_rfcs`, `get_commits`, `get_key_contributors_activity`（MCP 失败时降级到 gh CLI）；Community Collector SHALL 调用 `get_discussions`, `get_blog_news`, `get_events`, `get_slack_threads`

### Requirement: MCP-first 采集策略与降级

Collector SHALL 以 `pytorch-community` MCP server 为主要数据源，GitHub Collector 保留 `gh` CLI 作为降级通道。

- 所有数据采集 MUST 首先尝试 MCP 工具
- **GitHub Collector 降级策略**：当 MCP 工具返回错误时，SHALL 降级到 `gh` CLI 采集同类数据（PR → `gh pr list`，Issue → `gh issue list`）。`gh` CLI 不支持的数据源（RFC、Key Contributors）则记录警告并跳过
- **Community Collector 无降级**：MCP 工具返回错误时，记录警告并跳过该数据源

#### Scenario: MCP 工具调用成功

- **WHEN** GitHub Collector 调用 `get_prs(repo="pytorch/pytorch", since="7d")`
- **THEN** collector SHALL 使用返回的数据，按输出格式写入 staging 文件

#### Scenario: GitHub MCP 失败降级到 gh CLI

- **WHEN** GitHub Collector 调用 `get_prs` 返回错误（如 MCP server 连接失败）
- **THEN** collector SHALL 降级到 `gh pr list --repo pytorch/pytorch --state all --limit 100 --json number,title,author,createdAt,url,labels`，解析 JSON 输出并按相同格式写入 staging 文件

#### Scenario: Community MCP 工具返回错误

- **WHEN** Community Collector 调用 `get_slack_threads` 返回错误（如 Slack 未配置）
- **THEN** collector SHALL 记录 `[WARN] get_slack_threads 不可用，跳过 Slack 数据源`，继续采集其他数据源

### Requirement: Wide-to-narrow 采集策略

Collector SHALL 采用 wide-to-narrow 搜索策略：

1. **Wide phase**：先用宽泛查询（如 `get_prs(since="7d")`）获取全量概览
2. **Evaluate phase**：评估返回数据的覆盖情况和质量
3. **Narrow phase**：对需要详细信息的 item 调用 detail 工具（如 `get_pr_detail`, `get_issue_detail`）

Collector MUST NOT 一开始就调用 detail 工具。

#### Scenario: PR 数据的 wide-to-narrow

- **WHEN** GitHub Collector 开始采集 PR 数据
- **THEN** collector SHALL 先调用 `get_prs` 获取列表，评估哪些 PR 值得获取详情，再对选中的 PR 调用 `get_pr_detail`

#### Scenario: 数据量大时的聚焦

- **WHEN** `get_prs` 返回 200+ 条 PR
- **THEN** collector SHALL 基于标题、标签、作者等信号筛选出最相关的 items（≤30 条），仅对这些调用 detail 工具

### Requirement: Collector 输出格式

Collector SHALL 将采集结果写入 staging 文件，格式如下：

```markdown
# {Collector Name} 采集结果

- 项目: {project}
- 时间窗口: {window}
- 采集时间: {timestamp}

## 采集概览

| 数据源 | 总量 | 筛选后 | 状态 |
|--------|------|--------|------|
| PR     | N    | M      | OK   |
| Issue  | N    | M      | OK   |
| ...    | ...  | ...    | ...  |

## Items

### {item_type}: {title}

- URL: {source_url}
- 时间: {date}
- 作者: {author}
- 关键信息: {summary}
- 相关性: {why_relevant}

(重复 per item)
```

每个 item MUST 包含 `URL` 字段，指向原始数据源。

#### Scenario: 正常输出

- **WHEN** GitHub Collector 完成采集，收集到 15 条 PR、8 条 Issue、2 条 RFC
- **THEN** collector SHALL 按上述格式将全部 items 写入 `staging/github.md`，每条 item 包含 URL

### Requirement: Bot 和噪声过滤

Collector SHALL 过滤以下噪声数据：

- GitHub bot 账户创建的 PR/Issue（如 `dependabot`, `pytorch-bot`, `facebook-github-bot`）
- 纯 CI/CD 相关的 commits（如 `[skip ci]`, `nightly build`）
- 重复的自动化 issue（如 nightly failure reports）

#### Scenario: Bot PR 过滤

- **WHEN** `get_prs` 返回的结果中包含 `dependabot` 创建的依赖更新 PR
- **THEN** collector SHALL 过滤该 PR，不写入 staging 文件

#### Scenario: 有意义的 bot 活动

- **WHEN** `pytorch-bot` 创建了一个 RFC tracking issue
- **THEN** collector SHALL 保留该 item（RFC 有独立数据价值）

### Requirement: 时间窗口严格遵守

Collector SHALL 仅采集指定时间窗口内的数据。

- 传递给 MCP 工具的时间参数 MUST 精确匹配 orchestrator 指定的时间窗口
- 对于不支持时间范围过滤的 MCP 工具，collector SHALL 在获取数据后客户端过滤

#### Scenario: 时间窗口过滤

- **WHEN** orchestrator 指定 window="最近1周"，`get_events` 返回了 2 周前的 event
- **THEN** collector SHALL 过滤掉超出时间窗口的 event
