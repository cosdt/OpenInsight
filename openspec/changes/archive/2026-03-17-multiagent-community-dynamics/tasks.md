## 1. 项目基础设施

- [x] 1.1 创建`.opencode/agents/`目录结构
- [x] 1.2 创建`.opencode/skills/openinsight-briefing-style/`目录结构（含assets/、references/子目录）
- [x] 1.3 创建user-prompt.md模板文件，包含角色、关注领域、价值判断标准、输出偏好的结构化模板
- [x] 1.4 更新`opencode.json`，启用GitHub MCP并确认token配置路径正确

## 2. 核心Agent定义

- [x] 2.1 编写`openinsight-orchestrator.md`（mode: primary）：定义用户输入解析、项目配置加载、工作流编排指令、错误处理逻辑；description声明orchestration intent
- [x] 2.2 编写`project-coordinator.md`（mode: subagent）：定义三阶段调度流程（并行采集 → 融合验证 → 深度分析）、evidence fusion逻辑（URL去重 + 语义关联标记）、数据质量校验规则、价值评估与排序、item-analyst分配逻辑、wisdom notepad维护策略；description声明deep-reasoning intent
- [x] 2.3 编写`github-scout.md`（mode: subagent）：定义GitHub MCP工具调用策略、PR/Issue/Discussion/Release采集规则、bot过滤逻辑、Token预算压缩协议（Layer 1+2+3）、降级链（GitHub MCP → gh CLI → WebFetch）；description声明mechanical-extraction intent
- [x] 2.4 编写`external-source-scout-web.md`（mode: subagent）：定义WebFetch工具调用策略、Discourse论坛和博客采集规则、Token预算压缩协议、降级链（主URL → 备用URL → 标记不可用）；description声明mechanical-extraction intent
- [x] 2.5 编写`external-source-scout-slack.md`（mode: subagent）：定义Slack MCP工具调用策略、频道消息采集和线程聚合规则、Token预算压缩协议、降级提示（无替代路径）；description声明mechanical-extraction intent
- [x] 2.6 编写`item-analyst.md`（mode: subagent）：定义深度分析维度（变更概要、影响评估、技术细节、建议行动）、代码静态分析流程、local_analysis_enabled开关逻辑、wisdom notepad消费与贡献机制（读取先验 + 输出wisdom_contribution）、evidence_sources记录、结构化输出格式；description声明deep-reasoning intent
- [x] 2.7 编写`briefing-composer.md`（mode: subagent）：定义报告内容组织结构（含跨动态洞察和数据源覆盖状态）、个性化适配逻辑、降级数据源标注、skill调用方式；description声明creative-composition intent

## 3. Skill定义

- [x] 3.1 编写`openinsight-briefing-style/SKILL.md`：定义skill的frontmatter（name, description, allowed-tools）和报告生成指令
- [x] 3.2 创建HTML报告模板（`assets/report-template.html`），包含Executive Summary、高价值动态详情（含evidence引用）、跨动态洞察、分类动态列表、数据源覆盖状态（含降级标注）的HTML结构和CSS样式
- [x] 3.3 编写报告样式指导文档（`references/style-guide.md`），定义配色方案、排版规则、折叠/锚点导航、降级标注视觉样式等交互规范

## 4. 集成与验证

- [x] 4.1 验证agent拓扑完整性：确认7个agent文件均存在、frontmatter格式正确、description声明了正确的工作性质intent
- [x] 4.2 端到端流程测试：以pytorch项目、最近1天为输入，执行完整工作流，确认报告生成
- [x] 4.3 降级链测试：禁用GitHub MCP，验证github-scout能通过gh CLI降级采集；禁用Slack MCP，验证报告中标注Slack源不可用
- [x] 4.4 验证user-prompt.md个性化效果：使用不同角色配置，确认报告侧重点有差异
- [x] 4.5 验证wisdom accumulation：分析3+个高价值项，确认后续item-analyst接收到前序分析的wisdom，且分析结果引用了先验知识
- [x] 4.6 验证evidence fusion：构造跨源重复动态场景，确认coordinator正确合并、evidence_count反映在价值排序中
- [x] 4.7 验证Token预算压缩：确认每个scout的Layer 1+2输出不超过2000 tokens
