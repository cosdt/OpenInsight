## Context

OpenInsight项目需要在OpenCode平台上构建一个multi-agent系统，自动化PyTorch等开源社区的动态采集与分析。当前已有：

- `projects/pytorch.md` 和 `projects/torch-npu.md` 定义了数据源配置
- `opencode.json` 配置了GitHub MCP（remote）和Slack MCP（docker），但均处于disabled状态
- OpenCode支持agent定义（`.opencode/agents/*.md`，YAML frontmatter + markdown指令）和skill定义（`.opencode/skills/*/SKILL.md`）
- OpenCode Sessions插件提供agent间协作能力：`message`模式（turn-based协作）、`new`模式（干净上下文）、`fork`模式（并行探索）

参考框架：oh-my-opencode的multi-agent架构提供了多项可借鉴的设计范式，包括wisdom accumulation、category-based delegation、三层编排（Planning→Execution→Verification）、graceful degradation chains等。

约束：技术栈为markdown + OpenCode server，不引入额外后端服务。

## Goals / Non-Goals

**Goals:**

- 构建完整的7-agent拓扑，支持从用户输入到报告输出的端到端工作流
- 各agent职责清晰、输入输出契约明确，支持独立调试和替换
- 通过OpenCode Sessions插件实现agent间协作，无需自定义通信层
- 支持多项目配置（pytorch、torch-npu等），通过`projects/*.md`驱动数据源发现
- 报告格式可扩展（HTML、Slack通知等），通过skill管理输出样式
- **跨item分析过程中积累wisdom，后续分析质量递增**
- **scout输出有token预算控制，防止上下文溢出**
- **MCP不可用时有实际fallback策略，非简单报错**

**Non-Goals:**

- 不构建自定义MCP server（复用已有GitHub MCP、Slack MCP、WebFetch）
- 不实现实时流式处理或持续监控（按需触发，非daemon）
- 不处理需要登录认证的私有数据源（仅公开信息）
- 不实现自然语言到结构化查询的通用转换层
- 暂不开发pytorch-community-dynamics-mcp（后续迭代）
- 不实现oh-my-opencode的hook系统或plugin框架（超出纯markdown agent范畴）

## Decisions

### D1: Agent定义格式采用OpenCode标准agent markdown

**决策**: 每个agent用`.opencode/agents/<name>.md`定义，包含YAML frontmatter（description, mode, model, temperature）和markdown指令体。

**理由**: 这是OpenCode原生支持的agent定义方式，无需额外插件，`mode: primary`标识主agent，`mode: subagent`标识子agent。

**替代方案**: 用JSON/YAML配置文件定义agent → 不符合OpenCode惯例，丧失markdown指令的表达力。

### D2: Agent间协作使用OpenCode Sessions的message模式

**决策**: orchestrator通过`session({ mode: "message", agent: "<target>", text: "..." })`将任务分派给subagent，subagent完成后结果通过session返回。

**理由**: message模式实现turn-based协作，agent共享同一conversation上下文，适合线性流水线。scouts并行采集可通过orchestrator在project-coordinator指令中要求并行调用实现。

**替代方案**:
- `fork`模式 → 适合探索性并行，但不便于结果汇总回主流程
- 直接工具调用 → OpenCode subagent不是工具，需通过session通信

### D3: Scouts并行采集策略

**决策**: project-coordinator在其指令中要求并行调用三个scout（github-scout, external-source-scout-web, external-source-scout-slack），利用OpenCode的并行tool call能力。每个scout独立返回结构化结果。

**理由**: scouts之间无依赖关系，并行执行可显著缩短采集耗时。OpenCode支持在单个response中发起多个独立tool call。

**替代方案**: 串行调用 → 耗时是并行的3倍，无额外收益。

### D4: 价值筛选在project-coordinator中集中执行

**决策**: scouts返回初步过滤的动态列表后，由project-coordinator统一进行价值判断和排序，挑选高价值项交给item-analyst。

**理由**: 集中筛选可跨数据源去重、综合评估，避免各scout独立评估导致标准不一。project-coordinator拥有用户偏好上下文，更适合做价值判断。

**替代方案**: 各scout自行深度过滤 → scout缺乏用户偏好上下文，评估标准碎片化。

### D5: item-analyst采用per-item独立session

**决策**: 对每个高价值动态项，project-coordinator通过`session({ mode: "new", agent: "item-analyst" })`为其创建独立session，传入动态项详情和分析要求。

**理由**: `new`模式为每次分析提供干净上下文，避免多个动态项的分析互相干扰。每个item-analyst session聚焦单一动态，上下文利用率最高。

**替代方案**: 复用同一session分析多个item → 上下文膨胀，后分析的item质量下降。

### D6: 报告生成通过skill + subagent分离

**决策**: `briefing-composer` subagent负责内容组织和个性化适配，调用`openinsight-briefing-style` skill控制输出格式。skill中包含HTML模板、Slack消息格式等资源。

**理由**: 将内容逻辑（agent）与展示逻辑（skill）分离，新增输出格式只需扩展skill，不影响agent逻辑。

**替代方案**: agent内直接硬编码输出格式 → 每新增一种格式都需修改agent指令。

### D7: 项目配置驱动数据源发现

**决策**: agents读取`projects/<project>.md`获取数据源列表、仓库上下文、版本映射等信息。orchestrator根据用户指定的项目名加载对应配置。

**理由**: 复用已有配置格式，新增项目只需添加配置文件，无需修改agent逻辑。

**替代方案**: 将数据源信息硬编码在agent指令中 → 每新增项目都需修改多个agent。

### D8: Wisdom Accumulation — 跨item分析的智慧传递

**决策**: project-coordinator维护一个session内的wisdom notepad（结构化文本），每个item-analyst完成分析后，coordinator从结果中提取可复用的发现（模块依赖关系、关键人物活跃模式、跨PR关联性等），追加到notepad中。后续item-analyst session启动时携带当前notepad作为先验知识。

**理由**: 借鉴oh-my-opencode的wisdom accumulation模式。多个高价值动态之间存在隐性关联（如同一开发者的多个PR、同一模块的Issue和RFC）。如果每个item-analyst从零开始分析，会重复探索相同的代码路径，且无法发现跨item模式。通过wisdom传递，后续分析不仅更快，质量也更高。

**实现**: notepad不是独立文件，而是coordinator在session内维护的结构化文本块，包含：
- `discoveries`: 已发现的关键模式/关联
- `key_people`: 识别到的活跃核心人物及其关注领域
- `module_map`: 已探索过的模块和它们的依赖关系

**替代方案**: 每个item-analyst完全独立分析 → 重复劳动，无法发现跨item模式；共享同一session分析所有item → 上下文爆炸。

### D9: Intent-Based Agent Delegation

**决策**: agent定义中通过description声明其工作性质（如"mechanical data extraction"、"deep analytical reasoning"、"creative report composition"），而非在frontmatter中绑定具体model名称。model选择由运行时环境决定。

**理由**: 借鉴oh-my-opencode的category-based delegation。不同工作性质对model能力的要求不同——scouts需要精确的工具调用能力（mechanical），item-analyst需要深度推理（deep reasoning），briefing-composer需要优质文字表达（creative writing）。声明intent而非绑定model，使得：
1. 用户可根据自己的model配额灵活调整
2. 新model上线时无需修改agent定义
3. agent指令聚焦于任务而非实现

**实现**: frontmatter中使用`description`字段描述intent，可选的`model`字段作为默认建议而非硬约束。

**替代方案**: 每个agent硬编码model → 换model需改所有agent文件。

### D10: Scout输出Token预算压缩协议

**决策**: 每个scout的输出须遵循分层压缩协议：
- **Layer 1 — 统计摘要**（必须）: 采集总数、过滤后数量、数据源状态，约50 tokens
- **Layer 2 — 条目列表**（必须）: 每条动态的6字段结构化摘要（type/title/url/author/date/summary），每条约30-50 tokens，上限30条
- **Layer 3 — 补充详情**（可选，按coordinator请求）: 特定条目的完整描述、评论摘要等

coordinator首先接收Layer 1+2，基于此做价值筛选，仅对需要深入的条目请求Layer 3。

**理由**: 借鉴oh-my-opencode对token成本的管理哲学。三个scout并行返回时，如果每个都返回大量原始文本，coordinator上下文将迅速饱和。分层协议确保coordinator在做决策时拥有足够信息但不过载。Layer 3按需获取避免浪费。

**替代方案**: scout返回完整原始数据 → coordinator上下文溢出；scout过度压缩 → coordinator信息不足无法正确评估。

### D11: 跨源证据融合（Evidence Fusion）

**决策**: project-coordinator在收到所有scout结果后、价值评估前，执行跨源证据融合：
1. **URL-based去重**: 同一GitHub PR/Issue可能同时出现在github-scout（PR本身）和slack-scout（PR讨论链接）中，通过URL匹配合并
2. **语义关联**: 同一主题在不同源的讨论（如Discourse RFC + GitHub Issue + Slack thread），通过标题/关键词相似度关联
3. **信息互补**: 合并后的条目整合各源的独特信息（如GitHub提供代码diff，Slack提供开发者讨论意见）

**理由**: 同一动态在多个源的存在恰恰表明其重要性。不合并会导致：1）重复展示浪费报告篇幅；2）每条都作为独立项评估，低估其真实影响。合并后的"多源佐证"本身是价值判断的强信号。

**替代方案**: 简单去重（删除重复） → 丢失不同源的互补信息；完全不处理 → 报告中同一事件出现多次。

### D12: Graceful Degradation Chains

**决策**: 每个依赖外部数据源的agent须定义degradation chain：

- **github-scout**: GitHub MCP → gh CLI工具 → GitHub WebFetch（最后手段）
- **external-source-scout-web**: WebFetch主URL → WebFetch备用URL → 标记该源不可用
- **external-source-scout-slack**: Slack MCP → 标记Slack源不可用（无替代路径）

降级时agent须在输出中标注：实际使用的获取方式、降级原因、数据完整性影响。

**理由**: 借鉴oh-my-opencode的provider fallback chain模式。在生产使用中，MCP不可用是常态而非异常——token过期、API限流、Docker未启动等都是高频场景。仅返回错误提示会导致整个报告缺失关键数据源。降级链确保"有总比没有好"，同时通过标注让用户知道数据质量。

**替代方案**: 单一路径+错误提示 → 用户看到"Slack不可用"但无法获得任何替代信息，体验差。

## Risks / Trade-offs

- **[上下文窗口压力]** scouts并行返回的数据量可能超出project-coordinator的上下文容量 → **缓解**: D10分层压缩协议，Layer 1+2控制在~2000 tokens/scout，三个scout共~6000 tokens
- **[Session通信开销]** 多层agent嵌套（orchestrator → coordinator → scouts/analyst）增加session切换次数 → **缓解**: 扁平化高频通信路径，scouts直接由coordinator调度而非再经orchestrator
- **[MCP可用性]** GitHub MCP和Slack MCP目前disabled，需要正确的token配置才能工作 → **缓解**: D12 graceful degradation chains，确保fallback路径
- **[数据源覆盖不全]** 初期仅覆盖GitHub/Web/Slack三类源，可能遗漏邮件列表、LinkedIn等渠道 → **接受**: 作为V1限制，架构设计支持扩展新scout
- **[静态分析深度有限]** item-analyst的代码分析依赖LLM理解，非传统AST工具 → **缓解**: agent指令中引导使用grep/read工具进行结构化代码搜索，而非纯靠推理
- **[Wisdom传递噪声]** wisdom notepad可能积累错误发现，污染后续分析 → **缓解**: coordinator在追加wisdom前做简单校验，notepad条目标注置信度；单次session结束后notepad不持久化
- **[Evidence Fusion误合并]** URL-based去重简单可靠，但语义关联可能产生false positive → **缓解**: V1仅实现URL-based去重，语义关联标记为"可能相关"而非确定合并
