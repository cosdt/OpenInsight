# OpenInsight OpenCode Local Setup

本仓库现在包含一套仅用于 **OpenCode 内部 `delivery` 链路** 的本地多代理骨架，并按 OpenCode 官方文档的 agents / skills / MCP 配置方式组织。

## 已落地内容

- `opencode.json`
  - 项目级 OpenCode 配置入口
  - 默认关闭真实 source MCP，按用户环境显式启用
  - 本仓库默认走 **remote-first**：优先依赖 GitHub MCP 精确读取 `repo@ref/sha`
- `.opencode/instructions.md`
  - 仓库级运行边界与 artifact 约束
- `.opencode/agents/*.md`
  - `openinsight-orchestrator`
  - `project-coordinator`
  - `github-scout`
  - `external-source-scout-web`
  - `external-source-scout-slack`
  - `item-analyst`
  - `evidence-fuser`
  - `briefing-composer`
- `.opencode/skills/*/SKILL.md`
  - `openinsight-delivery-contract`
  - `openinsight-briefing-style`
  - `openinsight-daily-report-dumper`
  - dumper script lives under `.opencode/skills/openinsight-daily-report-dumper/scripts/`
- `projects/*.md`
  - 项目级运行时配置
  - 承载数据源、仓库关系、版本映射与本地 cache 策略示例

## 本地检查

可用以下命令查看 OpenCode 是否识别到这些资产：

```bash
opencode agent list
opencode debug config
opencode debug agent openinsight-orchestrator
opencode debug skill
```

CLI 可直接使用 orchestrator 作为唯一入口：

```bash
opencode run --agent openinsight-orchestrator "run one OpenInsight daily delivery"
```

也可以带上简短上下文，例如：

```bash
opencode run --agent openinsight-orchestrator "focus on one daily rehearsal for the highest-signal OSS projects this week"
```

每次成功运行后，最终结果应被写入 `daily_report/<YYYYMMDD-HHMM>/`。

## 如何接入真实 MCP

当前 `opencode.json` 里的 source MCP 默认关闭。要启用真实 source，请手动替换对应 `mcp.<name>.command` 或 `url`，并把 `enabled` 改为 `true`。

推荐约束：

- GitHub discovery 能力只给 `github-scout`
- `item-analyst` 默认可以读取 GitHub，但只能围绕 `project-coordinator` 提供的显式 `repo@ref/sha` 做 code-aware 分析
- Web 抓取/浏览能力只给 `external-source-scout-web`
- Slack 相关工具只给 `external-source-scout-slack`
- `briefing-composer` 不开启任何检索 MCP

## Remote-first 与本地增强模式

开源默认模式是 **remote-first**：

- `project-coordinator` 从 GitHub、Web、Slack scout 收集 `candidate_card[]`
- `project-coordinator` 把少量高价值候选归一化成 `selected_candidate`
- `item-analyst` 默认依赖 GitHub MCP，按显式 `repo@ref/sha` 做 `code-aware-remote` 深读

如果用户需要本地跨文件 grep、跨仓比对或重复分析同一版本，可额外启用 **local enhancement**：

- `OPENINSIGHT_REPO_CACHE_DIR=.cache/openinsight/repos`
- `OPENINSIGHT_WORKTREE_DIR=.cache/openinsight/worktrees`

推荐目录结构：

```text
.cache/openinsight/repos/github.com/pytorch/pytorch.git
.cache/openinsight/worktrees/pytorch-pytorch/v2.7.1-<sha>
.cache/openinsight/worktrees/ascend-torch-npu/v2.7.1-<sha>
```

本地增强模式不是默认部署前置条件；没有本地 cache 时，系统仍应能在 `code-aware-remote` 下工作。

## 明确不做的内容

以下内容 **没有** 在这次实现中落地：

- `extern` 的任何组件
- SMTP / IMAP / HTTP server / 队列 / 数据库
- PII、邮箱映射、画像更新
- UI、面板或非 `delivery` 链路

如果后续需要实现这些内容，应放在独立设计与独立目录中，而不是混进这套 OpenCode 内部多代理骨架。
