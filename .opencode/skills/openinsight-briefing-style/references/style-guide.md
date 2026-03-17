# OpenInsight Briefing Style Guide

## 配色方案

| 用途 | 颜色 | 色值 |
|------|------|------|
| 主色 | 蓝色 | `#1a73e8` |
| 主色浅 | 浅蓝 | `#e8f0fe` |
| 危险/高影响 | 红色 | `#d93025` |
| 危险浅 | 浅红 | `#fce8e6` |
| 警告/中影响 | 黄色 | `#f9ab00` |
| 警告浅 | 浅黄 | `#fef7e0` |
| 成功/低影响 | 绿色 | `#1e8e3e` |
| 成功浅 | 浅绿 | `#e6f4ea` |
| 正文 | 深灰 | `#202124` |
| 辅助文字 | 灰色 | `#5f6368` |
| 边框 | 浅灰 | `#dadce0` |
| 背景 | 白色 | `#ffffff` |
| 次背景 | 浅灰 | `#f8f9fa` |

## 排版规则

### 字体

- 主字体栈：`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`
- 代码字体：`"SF Mono", "Fira Code", "Consolas", monospace`

### 字号

| 元素 | 字号 | 字重 |
|------|------|------|
| 报告标题 | 24px | 600 |
| 章节标题 | 18px | 600 |
| 动态标题 | 16px | 500 |
| 正文 | 14px | 400 |
| 辅助信息 | 13px | 400 |
| 标签/badge | 12px | 600 |

### 行高

- 正文：1.6
- 标题：1.3
- 列表项：1.5

## 影响等级视觉标识

| 等级 | 标识 | Badge 样式 |
|------|------|-----------|
| High | 🔴 | 红底白字 `badge-high` |
| Medium | 🟡 | 黄底深黄字 `badge-medium` |
| Low | 🟢 | 绿底绿字 `badge-low` |

## 折叠/展开交互

- 使用 HTML `<details>` + `<summary>` 原生折叠
- 分类动态列表默认展开第一个分类，其余折叠
- Executive Summary 和高价值动态始终展开
- 折叠区域的 summary 文字使用主色 hover 效果

## 锚点导航

- 报告顶部提供锚点导航栏，链接到各章节
- 导航栏固定在容器顶部，使用白色背景 + shadow
- 链接使用主色，无下划线，hover 时显示下划线

## 降级标注视觉样式

### 正常数据源

```html
<div class="source-status source-ok">
  <span class="source-icon">✅</span>
  数据源名称: 正常采集，获取 N 条动态
</div>
```
- 浅绿背景 `#e6f4ea`

### 降级数据源

```html
<div class="source-status source-degraded">
  <span class="source-icon">⚠️</span>
  数据源名称: 降级模式（降级方式），数据可能不完整
</div>
```
- 浅黄背景 `#fef7e0`

### 失败数据源

```html
<div class="source-status source-failed">
  <span class="source-icon">❌</span>
  数据源名称: 不可用（失败原因），相关数据缺失
</div>
```
- 浅红背景 `#fce8e6`

## 卡片样式

- 高价值动态使用卡片布局（`item-card`）
- 卡片有 1px 边框，hover 时边框变为主色
- 卡片内包含：标题（含链接和影响等级badge）、元信息、分析摘要、建议行动、信息来源

## 洞察框样式

- 跨动态洞察使用左侧边框强调框（`insight-box`）
- 浅蓝背景 + 4px 主色左边框
- 圆角仅右侧

## 高价值标记

- 在分类动态列表中，被选为高价值的条目用 ⭐ 标记
- 星标使用黄色 `#f9ab00`

## 响应式设计

- 最大宽度 960px，居中显示
- 移动端 padding 减小为 16px
- 导航栏在窄屏下自动换行
