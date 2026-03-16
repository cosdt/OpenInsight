# Product Requirements Document

## 1. 产品定位

OpenInsight 是一套面向开源项目跟踪场景的 AI Native 社区情报 `delivery` runtime。它运行在 OpenCode 内，通过多 agent 协作从 GitHub、Web、Slack 等来源提炼高浓度事件摘要、风险判断与建议动作，并产出 `mail_html + trace`。

当前版本的核心设计目标不是“长期记住每个用户是谁”，而是把**一次运行的上下文边界**设计清楚：

- 用户想要的个性化视角，全部通过本次 `openinsight-orchestrator` 的输入 prompt 给出
- 项目级配置与扩展事实，全部通过 `projects/*.md` 给出
- 下游 agent 只处理上游消化后的结构化 brief

## 2. 设计原则

### 2.1 唯一个性化入口

只有 `openinsight-orchestrator` 能读取原始用户 prompt。

这意味着：

- 不维护 `users/*`
- 不维护 `department_strategy.md`
- 不把原始用户 prompt 一路透传给所有 subagent
- 不把“角色化”做成持久化画像

PL、开发骨干、架构师、维护者这些视角，都是**本次运行的 prompt lens**，不是仓库里的长期 profile。

### 2.2 项目配置与个性化解耦

项目级信息继续维护在 `projects/*.md`，包括：

- 数据源配置
- repo 关系
- 版本映射
- 本地分析增强策略

个性化 prompt 只能：

- 选择本次跑哪些已配置项目
- 规定本次关注什么主题
- 规定时间窗口、排序偏好、输出偏好

个性化 prompt 不能：

- 临时改写 `projects/*.md`
- 临时添加 source
- 临时更改 repo / ref / mapping 规则

### 2.3 逐级消化上下文

父 agent 必须先把上下文翻译成更小的结构化对象，再交给子 agent。

关键规则：

- orchestrator 把原始用户 prompt 翻译成 `session_directives`
- orchestrator 为每个项目生成 `project_run_brief`
- `project-coordinator` 读取项目配置后，继续生成 `source_discovery_brief` 和 `item_analysis_brief`
- scout / analyst / fuser / composer 都不直接依赖原始用户 prompt

## 3. 用户价值

### 3.1 按次定制，而不是长期画像

用户可以直接输入：

- “PL lens, only cover pytorch and torch-npu, focus on ecosystem impact”
- “Core maintainer lens, all configured projects, focus on API churn and release blockers”
- “只看本周 breaking changes，输出更短、更偏决策摘要”

系统需要在本次 run 内正确消费这些指令，但不会把它们沉淀成长期 profile。

### 3.2 项目级可扩展

接入新项目时，只需要新增或维护 `projects/<project>.md`，而不需要修改所有 agent prompt。

### 3.3 证据可追溯

最终输出必须包含 `trace`，便于追踪：

- 用了哪些工具
- 查了哪些来源
- 引用了哪些链接
- 哪些结论存在 coverage gap

## 4. 运行时模型

### 4.1 拓扑

- `openinsight-orchestrator`：唯一主入口
- `project-coordinator`：唯一项目级 dispatcher
- `github-scout` / `external-source-scout-web` / `external-source-scout-slack`：候选发现层
- `item-analyst`：单条候选深读层
- `evidence-fuser`：跨项目排序层
- `briefing-composer`：最终成稿层

### 4.2 Artifact Contract

运行时内部需要稳定的结构化 artifact：

- `session_directives`
- `session_delivery_plan`
- `project_run_brief`
- `source_discovery_brief`
- `candidate_card`
- `selected_candidate`
- `item_analysis_brief`
- `item_brief`
- `project_evidence_pack`
- `ranked_event`
- `trace`

这些对象是 OpenInsight runtime 的内部契约，不是 OpenCode 内置 schema。

### 4.3 默认行为

- 如果 prompt 没指定项目，默认跑所有已配置 `projects/*.md`
- 如果 prompt 指定了未知项目，记录 gap，并继续处理已知项目
- 如果缺失 `repo@ref/sha`，任何 `code-aware-*` 分析都必须退化为 coverage gap，而不是猜测

## 5. 配置面

### 5.1 用户输入 prompt

职责：

- 定义本次运行的分析视角
- 定义本次运行的目标项目范围
- 定义时间窗口、排序偏好、输出偏好

推荐支持的最小结构化字段：

- `audience_lens`
- `focus_topics[]`
- `deprioritized_topics[]`
- `time_window`
- `ranking_bias[]`
- `output_preferences`
- `target_projects[]`
- `assumptions[]`

### 5.2 项目配置 `projects/*.md`

职责：

- 定义项目事实
- 定义 source 和 fetcher
- 定义 repo 关系和版本映射
- 定义本地增强策略

### 5.3 Agent Prompt

`.opencode/agents/*.md` 的目标是保证：

- 流程是通的
- 上下文边界是清楚的
- 每个 agent 的职责单一
- prompt 不承载持久化个性化配置

## 6. 当前仓库范围

当前仓库只覆盖 OpenCode 内部 `delivery` runtime，不覆盖外部投递系统。

当前明确不做：

- `users/*`
- `department_strategy.md`
- reply-feedback 闭环
- SMTP / IMAP / HTTP server / 队列 / 数据库
- PII 映射
- 非 `delivery` 的 UI 或 dashboard

如果未来要做这些能力，应当以独立目录和独立设计进入，而不是重新混入当前 runtime prompt。

## 7. 验收标准

当以下条件同时满足时，认为当前设计达标：

1. 只有 `openinsight-orchestrator` 读取原始用户 prompt。
2. 只有 `project-coordinator` 直接读取 `projects/*.md`。
3. 所有下游 agent 只消费结构化 brief。
4. prompt 可以缩小本次项目范围，但不能覆盖项目配置。
5. 仓库文档与 prompt 中不再依赖 `users/*`、`department_strategy.md`、reply-feedback personalization。
