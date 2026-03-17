## 1. 项目脚手架与配置

- [ ] 1.1 初始化 Python 项目结构（pyproject.toml / setup.py），添加 fastmcp、httpx、feedparser 依赖
- [ ] 1.2 创建 PyTorch 专属知识配置模块 `pytorch_knowledge.py`（REPOS、MODULES、KEY_CONTRIBUTORS 映射表）
- [ ] 1.3 创建环境变量配置模块，支持 GITHUB_TOKEN、SLACK_BOT_TOKEN、DISCOURSE_API_KEY 等凭证
- [ ] 1.4 创建 FastMCP Server 入口文件 `server.py`，初始化 `FastMCP("pytorch-community-mcp")`

## 2. 底层 MCP Client 连接层

- [ ] 2.1 实现 GitHub MCP Client 连接与工具调用封装
- [ ] 2.2 实现 Slack MCP Client 连接与工具调用封装
- [ ] 2.3 实现 Discourse MCP Client 连接与工具调用封装
- [ ] 2.4 实现统一错误处理：底层 MCP 不可用时返回部分结果 + 错误说明

## 3. 统一返回格式层

- [ ] 3.1 实现 `UnifiedResponse` 数据类（summary、items、metadata），提供 `to_json()` 和 `to_markdown()` 方法
- [ ] 3.2 实现各数据源的响应格式化器（GitHub JSON → UnifiedResponse、Slack Markdown → UnifiedResponse 等）

## 4. 核心工具实现 — GitHub 类

- [ ] 4.1 实现 `get-prs` 工具：时间范围过滤、模块过滤、分页、统一格式返回
- [ ] 4.2 实现 `get-issues` 工具：时间范围过滤、模块过滤、状态过滤、统一格式返回
- [ ] 4.3 实现 `get-rfcs` 工具：聚合 pytorch/pytorch 和 pytorch/rfcs 两个仓库的 RFC，分类过滤

## 5. 核心工具实现 — Slack 类

- [ ] 5.1 实现 `get-slack-threads` 工具：频道过滤、时间范围、关键词搜索、统一格式返回

## 6. 核心工具实现 — Discourse 类

- [ ] 6.1 实现 `get-discussions` 工具：时间范围、关键词搜索、分类过滤、统一格式返回

## 7. 核心工具实现 — 聚合类

- [ ] 7.1 实现 `get-key-contributors-activity` 工具：跨 GitHub/Slack/Discourse 聚合关键人物动态，处理部分平台不可用
- [ ] 7.2 实现 `get-gov` 工具：从 GitHub governance 文件和 Discourse 获取治理信息
- [ ] 7.3 实现 `get-foundation` 工具：从 pytorch-fdn GitHub 和 Events API 获取基金会信息

## 8. 核心工具实现 — 事件与活动

- [ ] 8.1 实现 Events API HTTP 调用层（pytorch.org/wp-json/tec/v1/events）
- [ ] 8.2 实现 RSS Feed 解析层（pytorch.org/feed/）
- [ ] 8.3 实现 `get-event` 工具：聚合 Events API 和 RSS，时间范围过滤、活动类型过滤

## 9. 渐进式披露工具

- [ ] 9.1 实现 `get-specific-mcp-tool` 工具：MCP 名称验证、工具路由、参数透传
- [ ] 9.2 实现 `tool_name="list"` 模式：列出指定 MCP 的可用工具

## 10. 测试

- [ ] 10.1 为每个工具编写单元测试，mock 底层 MCP 调用
- [ ] 10.2 编写集成测试，验证实际 MCP 连接和数据格式
- [ ] 10.3 验证统一返回格式在所有工具中的一致性

## 11. 文档与部署配置

- [ ] 11.1 编写 README：项目说明、安装步骤、环境变量配置、使用示例
- [ ] 11.2 提供 Claude Desktop / Claude Code 的 MCP 配置示例（mcpServers JSON）
