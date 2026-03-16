# OpenInsight

OpenInsight 是一套运行在 OpenCode 内的开源社区情报 `delivery` runtime。它从 GitHub、Web、Slack 等多源信号中提炼高浓度摘要与行动建议，并产出可直接投递的 `mail_html + trace`。

## 当前模型

- **唯一入口**：`openinsight-orchestrator` 是唯一主 agent，也是唯一允许读取原始用户 prompt 的个性化入口。
- **项目解耦**：`projects/*.md` 只维护项目级事实与扩展配置，例如数据源、仓库关系、版本映射、本地分析策略。
- **逐级消化**：下游 agent 只消费上游缩减后的结构化 brief，不直接读取原始用户 prompt，也不直接读取项目配置。
- **可追溯**：最终结果带有 `trace`，可追溯到工具、来源和链接。

## 它能做什么

- **按次定制简报**：通过 orchestrator prompt 指定本次关注视角、时间窗口、重点主题和目标项目。
- **多源情报汇聚**：聚合 GitHub（issue/PR/release）、论坛、官网/博客、Slack 等信号，形成统一事件视图。
- **深度研判**：对少量高价值候选做深读，输出影响范围、风险判断与建议动作。
- **运行结果落盘**：每次成功运行后，结果持久化到 `daily_report/<YYYYMMDD-HHMM>/`。

## 仓库范围

当前仓库只包含 OpenCode 内部 `delivery` runtime：

- `.opencode/agents/*.md`：多 agent prompt
- `.opencode/skills/*/SKILL.md`：运行契约和输出风格
- `projects/*.md`：项目级运行时配置
- `daily_report/`：已生成结果

当前 **不包含**：

- `users/*`、`department_strategy.md` 或任何持久化个性化配置
- SMTP / IMAP / HTTP server / 队列 / 数据库
- reply-feedback 闭环
- UI 或 dashboard

## 参考文档

- [docs/multiagent.md](/Users/chu/project/openinsight/docs/multiagent.md)
- [docs/prd.md](/Users/chu/project/openinsight/docs/prd.md)
- [docs/opencode-local-setup.md](/Users/chu/project/openinsight/docs/opencode-local-setup.md)
