---
name: openinsight-briefing-style
description: "Generates beautifully formatted HTML community briefing reports with executive summaries, deep analysis details, cross-item insights, and data source coverage status."
allowed-tools:
  - Read
  - Write
  - Glob
---

# OpenInsight Briefing Style

你是报告样式生成技能，负责将结构化的社区动态分析结果渲染为美观的 HTML 报告。

## 使用方式

briefing-composer agent 在生成报告时调用此 skill。

## 资源文件

- `assets/report-template.html`: HTML 报告模板，包含完整的结构和 CSS 样式
- `references/style-guide.md`: 报告样式指导文档，定义配色、排版、交互规范

## 报告生成指令

### 1. 读取模板

从 `assets/report-template.html` 读取 HTML 模板结构。

### 2. 填充内容

将分析结果填充到模板对应区域：
- `{{executive_summary}}` → Executive Summary 内容
- `{{high_value_items}}` → 高价值动态详情
- `{{cross_insights}}` → 跨动态洞察
- `{{categorized_list}}` → 分类动态列表
- `{{data_source_status}}` → 数据源覆盖状态
- `{{report_date}}` → 报告生成日期
- `{{time_window}}` → 时间窗口描述
- `{{project_name}}` → 项目名称

### 3. 样式应用

参照 `references/style-guide.md` 中的规范：
- 使用指定的配色方案
- 应用排版规则
- 添加折叠/展开交互
- 添加锚点导航
- 降级数据源使用特殊视觉样式

### 4. 输出

生成完整的 HTML 文件，包含内联 CSS，无外部依赖。文件保存到用户指定路径或默认路径。
