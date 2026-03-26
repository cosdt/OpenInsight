## ADDED Requirements

### Requirement: Composer 输入协议

Composer SHALL 从 staging 目录读取以下文件作为输入：

- `fusion.md`：经过融合排序的全量 items
- `analysis_*.md`：深度分析结果（0 个或多个）
- `user-prompt.md`：用户角色定义（通过 orchestrator 传递路径）

Composer MUST NOT 直接读取 `github.md` 或 `community.md`——融合后的数据是唯一的事实来源。

#### Scenario: 有深度分析的报告

- **WHEN** staging 目录包含 fusion.md 和 3 个 analysis_*.md 文件
- **THEN** Composer SHALL 读取全部文件，将深度分析内容整合到报告的相应章节

#### Scenario: 无深度分析的报告

- **WHEN** staging 目录仅包含 fusion.md，无 analysis_*.md
- **THEN** Composer SHALL 基于 fusion.md 生成报告，报告中不包含深度分析章节

### Requirement: 报告结构

Composer SHALL 生成包含以下章节的 Markdown 报告：

1. **概览**：时间窗口内社区动态的总体摘要（3-5 句）
2. **重点关注**：high-priority items 的详细介绍，包含深度分析结果和行动建议
3. **社区动态**：按数据源分类的完整动态列表（PR、Issue、RFC、Discourse、Blog、Events）
4. **关键人物动态**：社区关键人物的活动摘要
5. **附录**：数据采集统计、数据源覆盖情况

#### Scenario: 标准报告结构

- **WHEN** Composer 收到包含 PR/Issue/RFC/Discourse 数据的 fusion.md
- **THEN** 生成的报告 SHALL 包含上述 5 个章节，每个章节有明确的标题

### Requirement: 个性化内容

Composer SHALL 根据 user-prompt.md 定义的用户角色定制报告内容：

- 用户关注领域的 items 放在"重点关注"章节
- 报告语言和详细程度匹配用户偏好
- 行动建议针对用户的具体角色

#### Scenario: NPU 开发者视角

- **WHEN** user-prompt.md 定义用户关注 "operator compatibility, NPU adaptation"
- **THEN** 报告 SHALL 将涉及 operator 和 NPU 的变更突出展示，行动建议聚焦适配工作

### Requirement: 源链接完整性

报告中的每条动态 MUST 包含指向原始数据源的 URL 链接。

- PR/Issue：链接到 GitHub PR/Issue 页面
- Discourse：链接到论坛帖子
- Blog：链接到官网博客页面
- RFC：链接到 RFC 文档

#### Scenario: 所有 items 有源链接

- **WHEN** Composer 生成报告
- **THEN** 报告中每条动态 MUST 以 Markdown 链接格式 `[标题](URL)` 引用源数据

#### Scenario: 源链接缺失

- **WHEN** fusion.md 中某 item 缺少 URL 字段
- **THEN** Composer SHALL 在该 item 旁标注 `[源链接缺失]`，不伪造 URL

### Requirement: 可解释性

报告中每条被选入"重点关注"的动态 MUST 说明入选原因。

格式：`> 入选原因: {reason}`

#### Scenario: 解释入选原因

- **WHEN** 一个 `torch.compile` 相关的 PR 被放入"重点关注"
- **THEN** 该 PR 条目下 MUST 包含 `> 入选原因: 涉及用户关注的 compiler backends 模块，包含 API 变更`

### Requirement: 报告输出路径

Composer SHALL 将报告写入 staging 目录。Orchestrator 通过质量检查后将报告移动到最终位置。

最终路径：`reports/{project}_community_briefing_{date}.md`

- 如果同名文件已存在，SHALL 追加序号：`{project}_community_briefing_{date}_v2.md`
- MUST NOT 覆盖已有报告

#### Scenario: 首次生成报告

- **WHEN** `reports/pytorch_community_briefing_2026-03-26.md` 不存在
- **THEN** orchestrator SHALL 将报告保存为该路径

#### Scenario: 同名报告已存在

- **WHEN** `reports/pytorch_community_briefing_2026-03-26.md` 已存在
- **THEN** orchestrator SHALL 将报告保存为 `reports/pytorch_community_briefing_2026-03-26_v2.md`

### Requirement: 报告语言

报告 SHALL 使用中文撰写。技术术语（如 API 名、模块名、PR 标题）保持英文原文。

#### Scenario: 中英混合

- **WHEN** Composer 描述一个修改 `torch.nn.Module` 的 PR
- **THEN** 报告 SHALL 用中文描述变更内容，`torch.nn.Module` 保持英文
