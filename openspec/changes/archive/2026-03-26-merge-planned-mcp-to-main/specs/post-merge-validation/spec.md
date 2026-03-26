## ADDED Requirements

### Requirement: MCP server 文件完整性
合并后 `src/pytorch_community_mcp/` 目录 SHALL 包含 mcp 分支的全部源文件，无遗漏。

#### Scenario: All MCP source files present
- **WHEN** 合并完成后列出 `src/pytorch_community_mcp/` 目录
- **THEN** 包含 server.py、config.py、formatter.py、clients/*.py、tools/*.py 等全部文件

### Requirement: Python 测试套件通过
合并后 SHALL 能通过 `uv run pytest` 运行全部测试且无失败。

#### Scenario: Pytest passes
- **WHEN** 在合并后的 main 分支执行 `uv run pytest`
- **THEN** 全部测试通过，exit code 为 0

### Requirement: Agent 配置文件完整
合并后 `.opencode/agents/` 目录 SHALL 包含 planned 分支的全部 agent 定义文件。

#### Scenario: All agent files present
- **WHEN** 合并完成后列出 `.opencode/agents/`
- **THEN** 包含 openinsight-orchestrator.md 及其他 planned 分支中的 agent 文件

### Requirement: OpenSpec 变更历史保留
合并后 `openspec/` 目录 SHALL 保留 planned 分支的全部变更记录和归档。

#### Scenario: OpenSpec archives intact
- **WHEN** 合并完成后列出 `openspec/changes/` 和 `openspec/archive/`（如存在）
- **THEN** 目录结构与 planned 分支一致

### Requirement: 无意外文件丢失
合并后的文件集合 SHALL 是两个分支独有文件的并集加上冲突解决后的文件，不存在任何一方的文件被意外丢弃。

#### Scenario: File count validation
- **WHEN** 合并完成后统计文件数
- **THEN** 文件数 ≥ max(planned 文件数, mcp 文件数)，除非有共识删除的文件
