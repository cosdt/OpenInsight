# OpenInsight

OpenInsight 为参与 PyTorch 开源项目的团队提供**自动化社区动态简报**。它从 GitHub、Discourse、PyTorch 官网等多个数据源采集社区动态，经过筛选、分析后生成个性化报告，帮助开发者快速掌握高价值信号。

## 快速开始

### 1. 安装依赖

```bash
# 需要 Python >= 3.11 和 uv
uv sync
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，至少配置 GITHUB_TOKEN
```

| 变量 | 用途 | 必需 |
|------|------|------|
| `GITHUB_TOKEN` | GitHub API 访问 | 是 |
| `DISCOURSE_API_KEY` | Discourse 论坛 API | 否 |
| `DISCOURSE_API_USERNAME` | Discourse 用户名 | 否（与 API Key 配对） |

### 3. 配置你的角色

编辑 `user-prompt.md`，描述你的角色和关注领域。已提供两个模板：

- `user-prompt.md` — 团队开发者（关注具体模块、代码级分析）
- `user-prompt-core-dev.md` — 核心开发者（关注架构变更、社区治理）

### 4. 生成报告

```bash
opencode run \
  --agent openinsight-orchestrator \
  --model alibaba-cn/qwen3.5-plus \
  -- "@user-prompt.md pytorch 最近1天 执行完整工作流生成报告。"
```

报告输出到 `reports/` 目录。

## 架构

OpenInsight 由两部分组成：

### MCP Server（数据层）

`pytorch-community-mcp` 是一个 domain-specific [MCP](https://modelcontextprotocol.io/) server，提供 10 个 PyTorch 社区数据工具：

| 工具 | 数据源 | 说明 |
|------|--------|------|
| `get_prs` | GitHub | 按时间范围和模块获取 PR |
| `get_issues` | GitHub | 按时间范围、模块和状态获取 Issue |
| `get_commits` | GitHub | 按时间范围和作者获取 Commit |
| `get_rfcs` | GitHub | 获取 pytorch/pytorch 和 pytorch/rfcs 的 RFC |
| `get_pr_detail` | GitHub | 获取单个 PR 详情 |
| `get_issue_detail` | GitHub | 获取单个 Issue 详情 |
| `get_discussions` | Discourse | 搜索论坛话题 |
| `get_events` | pytorch.org | 获取社区活动 |
| `get_blog_news` | pytorch.org | 获取博客 RSS |
| `get_key_contributors_activity` | GitHub + Discourse | 关键贡献者跨平台活动 |

单独启动 MCP server：

```bash
uv run pytorch-community-mcp
```

### Multi-Agent 工作流（分析层）

运行在 [OpenCode](https://opencode.ai) 上的多 agent 协作系统：

```
Orchestrator (编排)
  ├── GitHub Collector (并行采集)
  ├── Community Collector (并行采集)
  ├── Analyst (深度分析, max 3 并行)
  └── Composer (个性化报告)
```

Agent 定义在 `.opencode/agents/`，工作流详情见 `docs/multiagent.md`。

## MCP 客户端配置

### Claude Code

```json
{
  "mcpServers": {
    "pytorch-community": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/openinsight", "pytorch-community-mcp"],
      "env": { "GITHUB_TOKEN": "ghp_..." }
    }
  }
}
```

### OpenCode

在 `opencode.json` 中配置（已包含在仓库中）。

## 开发

```bash
# 安装依赖
uv sync

# 运行测试
uv run pytest

# 启动 MCP server（开发模式）
uv run pytorch-community-mcp
```

## 文档

- [MCP Server 详细文档](docs/mcp.md)
- [Multi-Agent 工作流](docs/multiagent.md)
- [环境搭建](docs/setup.md)
- [需求规格](docs/requirement.md)

## License

Apache-2.0
