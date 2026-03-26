## ADDED Requirements

### Requirement: 用户角色定义文件

系统 SHALL 通过 `user-prompt.md` 文件定义用户角色，文件 MUST 包含：

- **角色描述**：用户在团队中的职责
- **关注领域**：用户关注的技术方向和模块
- **下游项目**：用户维护的下游项目（如 torch-npu）
- **输出偏好**：报告语言、详细程度
- **关键人物列表**：用户关注的社区关键人物

#### Scenario: 加载用户角色

- **WHEN** orchestrator 启动时读取 `user-prompt.md`
- **THEN** orchestrator SHALL 解析用户角色信息，传递给 fusion 和 composer 阶段使用

#### Scenario: 用户角色文件不存在

- **WHEN** 指定的 user-prompt 文件路径不存在
- **THEN** orchestrator SHALL 使用默认角色（通用 PyTorch 开发者），不中断工作流

### Requirement: 项目配置文件

系统 SHALL 通过 `projects/{project}.md` 文件定义项目配置，文件 MUST 包含：

- **主仓库**：GitHub 仓库地址
- **关联仓库**：相关的上下游仓库列表
- **数据源启用列表**：该项目需要采集哪些数据源
- **本地分析配置**：`repo_cache_dir` 和 `worktree_dir` 路径

#### Scenario: 加载项目配置

- **WHEN** orchestrator 解析用户输入得到 project="pytorch"
- **THEN** orchestrator SHALL 读取 `projects/pytorch.md`，将仓库地址和数据源列表传递给 collector

#### Scenario: 项目配置不存在

- **WHEN** 用户指定的 project 在 `projects/` 目录下没有对应配置文件
- **THEN** orchestrator SHALL 报告错误并终止工作流

### Requirement: 个性化筛选规则

Orchestrator 在融合阶段 SHALL 基于用户角色的关注领域进行筛选：

- 与用户关注领域高度相关的 items 标记为 high-priority
- 与用户关注领域无关但影响重大的 items 标记为 medium-priority
- 与用户完全无关的 items 降为 low-priority 或过滤

筛选 SHALL 基于启发式判断，不使用硬编码的关键词匹配。

#### Scenario: NPU 开发者的筛选

- **WHEN** 用户关注 "operator compatibility, NPU adaptation"，fusion 数据中有一个修改 ATen operator 的 PR
- **THEN** orchestrator SHALL 将该 PR 标记为 high-priority

#### Scenario: 不在关注领域但影响重大

- **WHEN** 用户关注 "compiler backends"，fusion 数据中有一个 PyTorch 2.x → 3.0 的 breaking change RFC
- **THEN** orchestrator SHALL 将该 RFC 标记为 medium-priority（影响重大，即使不在直接关注领域）

### Requirement: 多角色支持

系统 SHALL 支持多个 user-prompt 文件，通过启动时指定文件路径选择角色。

- 默认使用 `user-prompt.md`
- 可通过用户输入指定替代文件（如 `@user-prompt-core-dev.md`）

#### Scenario: 指定替代角色

- **WHEN** 用户输入 `@user-prompt-core-dev.md pytorch 最近1周 执行完整工作流生成报告`
- **THEN** orchestrator SHALL 使用 `user-prompt-core-dev.md` 作为用户角色定义
