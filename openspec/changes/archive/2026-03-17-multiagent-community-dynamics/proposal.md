## Why

PyTorch开源社区每天在GitHub、Discourse论坛、Slack等多个信息源产生海量动态，核心开发者每天需花1-2小时手动浏览筛选，仍然容易错过高价值信号。现有工具（Copilot、Grok）受限于上下文窗口和单次对话行动步数，无法支撑跨源聚合+代码级深度分析的完整工作流。

需要基于OpenCode构建multi-agent协作系统，自动完成社区动态采集、价值筛选、深度分析和个性化报告生成。系统应当借鉴成熟multi-agent框架的核心设计哲学：**分层编排、上下文压缩、跨任务智慧积累、优雅降级**，使其在信息源不完备、上下文有限的真实环境中仍能产出高质量报告。

## What Changes

- 新增 `openinsight-orchestrator` 主agent，作为唯一用户入口，编排整个multi-agent工作流
- 新增 `project-coordinator` subagent，负责项目级信息调度：调用scouts采集、**数据质量校验与跨源证据融合**、执行价值筛选、分配item-analyst深度分析、**汇总时提取跨item wisdom**
- 新增 `github-scout` subagent，通过GitHub MCP采集PR/Issue/Discussion/RFC动态并初步过滤，**输出遵循token预算压缩协议**
- 新增 `external-source-scout-web` subagent，通过WebFetch采集Discourse论坛、PyTorch官网博客等Web源动态，**含fallback降级链**
- 新增 `external-source-scout-slack` subagent，通过Slack MCP采集Slack频道讨论动态，**含fallback降级链**
- 新增 `item-analyst` subagent，对高价值动态项进行深度分析，包括代码静态分析影响范围；**各item-analyst间传递wisdom notepad（发现的模式、关键人物、模块关联）避免重复探索**
- 新增 `briefing-composer` subagent，将分析结果组织成个性化报告
- 新增 `openinsight-briefing-style` skill，定义报告输出格式与样式
- 利用已有 `projects/*.md` 项目配置驱动数据源发现
- **新增 `evidence-fuser` 逻辑（内嵌于project-coordinator）：跨数据源同一动态的证据合并与去重**

## Capabilities

### New Capabilities

- `agent-orchestration`: 定义multi-agent拓扑结构、agent间协作流程、session管理策略；**包含分层编排模式（Planning Context → Execution → Verification）和intent-based delegation（agent声明工作性质而非绑定具体model）**
- `data-collection`: scouts群组的数据采集规范——GitHub/Web/Slack三类scout的输入输出契约、初步过滤规则、与project config的对接方式；**包含token预算压缩协议和graceful degradation chains**
- `item-deep-analysis`: item-analyst的深度分析能力规范——价值评估维度、代码静态分析流程、影响范围判定规则；**包含wisdom accumulation机制（跨item发现传递）**
- `report-generation`: briefing-composer的报告生成规范——报告结构、个性化适配（角色+偏好）、输出格式（HTML/Slack通知等）
- `user-personalization`: 用户个性化配置规范——user-prompt.md格式定义、角色/需求/价值判断标准的结构化描述
- `evidence-fusion`: 跨数据源证据融合规范——同一动态在不同源中的识别、合并、信息互补策略；**数据质量校验规则**

### Modified Capabilities

（无已有capability需要修改）

## Impact

- **新增文件**: `.opencode/agents/` 下7个agent定义文件、`.opencode/skills/` 下报告样式skill
- **配置变更**: `opencode.json` 需启用GitHub MCP和Slack MCP，可能需新增agent相关配置
- **依赖**: GitHub MCP（remote）、Slack MCP（docker）、WebFetch工具；OpenCode Sessions插件用于multi-agent协作
- **项目配置**: 复用已有 `projects/pytorch.md`、`projects/torch-npu.md` 作为数据源配置
- **设计哲学引入**: 借鉴oh-my-opencode的wisdom accumulation、context compression、graceful degradation模式，使系统在真实不完美环境中鲁棒运行
