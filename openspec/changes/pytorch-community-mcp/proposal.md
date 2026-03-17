## Why

PyTorch 开源社区的信息分散在 GitHub（pytorch/pytorch、pytorch/rfcs）、Slack、Discourse 开发者论坛、官网 Events API 和 RSS 等多个平台。Agent 要完整访问这些信息需同时加载 3 个通用 MCP（GitHub 80+ 工具、Slack 10 工具、Discourse 18 工具）及多个网络接口，总计超过 120 个工具。这导致上下文膨胀、工具误选（如 RFC 查询只搜主仓而漏掉 rfcs 仓库）、返回格式混乱（Markdown / JSON / 纯文本混合），严重降低 Agent 的准确性和效率。

## What Changes

- 新建 `pytorch-community-mcp` MCP Server，封装 10 个面向 PyTorch 社区信息获取的高级工具
- 聚合 GitHub MCP、Slack MCP、Discourse MCP 及官网 Events API / RSS 作为底层数据源
- 工具内置 PyTorch 专属知识（仓库映射、模块分类、关键人物列表），避免 Agent 误选数据源
- 统一所有工具的返回格式为 Markdown + 结构化摘要 JSON（含 summary、key_points、source_links）
- 提供 `get-specific-mcp-tool` 渐进式披露机制，按需暴露底层 MCP 能力

## Capabilities

### New Capabilities

- `get-prs`: 获取指定时间范围和模块的 PyTorch PR 列表，底层调用 GitHub MCP
- `get-issues`: 获取指定时间范围和模块的 PyTorch Issue 列表，底层调用 GitHub MCP
- `get-rfcs`: 获取指定时间范围的 RFC，自动聚合 pytorch/pytorch 和 pytorch/rfcs 两个仓库
- `get-slack-threads`: 获取指定频道和时间范围的 Slack 消息线程
- `get-key-contributors-activity`: 聚合关键人物在 GitHub、Slack、Discourse 的活动动态
- `get-discussions`: 获取指定时间范围的开发者论坛（Discourse）讨论
- `get-gov`: 获取 PyTorch 组织治理信息，聚合 GitHub 和 Discourse 数据
- `get-foundation`: 获取 PyTorch 基金会信息，聚合 Events API 和 GitHub 数据
- `get-event`: 获取官网事件和活动信息，聚合 Events API 和 RSS
- `get-specific-mcp-tool`: 渐进式披露底层 MCP 工具，按需暴露 GitHub / Slack / Discourse MCP 能力

### Modified Capabilities

_无，这是全新项目。_

## Impact

- **新增依赖**: GitHub MCP Server、Slack MCP Server、Discourse MCP Server、PyTorch Events API、PyTorch RSS Feed
- **部署**: 需配置各平台的访问凭证（GitHub Token、Slack Bot Token、Discourse API Key）
- **面向用户**: 开发者只需部署一个 MCP 即可获取完整的 PyTorch 社区信息，替代此前需要分别部署 3 个 MCP + 手动 prompt 的方式
- **合规**: 仅获取公开信息，仅限内部使用
