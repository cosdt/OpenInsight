## Context

PyTorch 社区信息分布在 5 个独立平台：GitHub（pytorch/pytorch、pytorch/rfcs 等）、Slack（pytorch.slack.com）、Discourse（discuss.pytorch.org）、官网 Events API、RSS 订阅。当前 Agent 需加载 120+ 个通用工具才能覆盖全部数据源，导致上下文膨胀、误选工具和格式混乱。

本设计基于 FastMCP 框架构建一个聚合层 MCP Server，将底层 MCP 和 API 封装为 10 个面向 PyTorch 社区的高级工具。

## Goals / Non-Goals

**Goals:**

- 将 120+ 通用工具精简为 10 个面向 PyTorch 社区信息获取的高级工具
- 内置 PyTorch 专属知识（仓库→模块映射、关键人物列表、RFC 仓库路径），消除 Agent 误选
- 统一返回格式为 Markdown + 结构化 JSON，降低 Agent 解析负担
- 支持时间范围过滤，适配日报/周报等定期信息获取场景
- 提供渐进式披露机制，按需暴露底层 MCP 能力

**Non-Goals:**

- 不做数据写入（不创建 issue、不发 Slack 消息、不发帖）
- 不做数据缓存或持久化存储
- 不做用户认证和权限管理（依赖底层 MCP 的 token 配置）
- 不处理非 PyTorch 社区的信息

## Decisions

### 1. 使用 FastMCP 框架（Python）

**选择**: FastMCP (Python)
**理由**: FastMCP 提供 `@mcp.tool` 装饰器实现零样板工具定义，支持 `mount()` 组合多个子服务器，支持 `create_proxy()` 代理底层 MCP Server。Python 生态对 GitHub API、RSS 解析、HTTP 请求等有成熟库支持。
**备选**: TypeScript MCP SDK — 性能略优但 Python 在数据处理和 API 集成方面生态更丰富。

### 2. 底层 MCP 调用方式：Client 直连

**选择**: 使用 FastMCP Client 在工具函数内部直接调用底层 MCP Server
**理由**: 每个高级工具内部组合调用多个底层 MCP 工具，需要灵活控制调用逻辑（如 get-rfcs 需要同时查 pytorch/pytorch 和 pytorch/rfcs）。Client 直连比 Proxy 模式更灵活，便于组合和转换。
**备选**: Proxy/Mount 模式 — 适合简单转发，但无法实现跨 MCP 的数据聚合和格式统一。

### 3. 统一返回格式

**选择**: 每个工具返回包含 `summary`（Markdown 摘要）、`items`（结构化数据列表）、`metadata`（来源、时间范围、总数）的 JSON
**理由**: Agent 可直接使用 summary 做自然语言回答，用 items 做结构化分析，用 metadata 判断数据完整性。

```python
{
    "summary": "## PR 概览\n在过去 7 天...",
    "items": [{"title": "...", "url": "...", "author": "...", ...}],
    "metadata": {"source": "github", "time_range": "2024-01-01..2024-01-07", "total_count": 42}
}
```

### 4. PyTorch 专属知识内置为配置

**选择**: 将仓库映射、模块分类、关键人物等 PyTorch 专属知识维护为 Python 配置模块
**理由**: 这些知识相对稳定，内置配置比动态发现更可靠。后续可通过配置文件外置实现可扩展性。

```python
# pytorch_knowledge.py
REPOS = {
    "main": "pytorch/pytorch",
    "rfcs": "pytorch/rfcs",
    "website": "pytorch/pytorch.github.io",
    "foundation": "pytorch-fdn",
}

MODULES = ["distributed", "compiler", "autograd", "nn", "cuda", ...]

KEY_CONTRIBUTORS = ["ezyang", "albanD", "malfet", ...]
```

### 5. 渐进式披露通过工具名路由

**选择**: `get-specific-mcp-tool` 接受 `mcp_name`（github/slack/discourse）和 `tool_name` 参数，动态路由到底层 MCP
**理由**: 覆盖高级工具未封装的长尾需求，同时避免一次性暴露全部 120+ 工具。Agent 仅在高级工具不满足时才使用此工具。

### 6. 传输协议：stdio

**选择**: 默认使用 stdio 传输
**理由**: 与 Claude Desktop、Claude Code 等本地 Agent 客户端兼容，配置最简单。后续可通过 FastMCP 的 `run(transport="http")` 扩展为 HTTP 传输。

## Risks / Trade-offs

- **底层 MCP 可用性依赖** → 每个工具内部添加错误处理，底层 MCP 不可用时返回部分结果和错误说明
- **API Rate Limit** → GitHub API 有速率限制，组合调用可能加速耗尽配额 → 在文档中明确建议使用 PAT 而非 OAuth App token
- **PyTorch 专属知识过时** → 模块分类、关键人物可能变动 → 配置文件集中管理，易于更新
- **Slack/Discourse 凭证管理** → 需用户自行配置多个 token → 提供清晰的配置文档和环境变量模板
- **返回数据量过大** → 大时间范围查询可能返回过多结果 → 每个工具设默认 limit 和分页支持
