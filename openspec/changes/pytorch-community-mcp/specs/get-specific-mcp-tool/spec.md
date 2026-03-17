## ADDED Requirements

### Requirement: Route requests to underlying MCP tools
The tool SHALL accept a required `mcp_name` parameter ("github", "slack", or "discourse") and a required `tool_name` parameter (the specific tool to invoke), plus an optional `params` parameter (JSON object of tool arguments), and route the call to the corresponding underlying MCP.

#### Scenario: Call a GitHub MCP tool
- **WHEN** user calls `get-specific-mcp-tool` with `mcp_name="github"`, `tool_name="get_file_contents"`, and `params={"owner": "pytorch", "repo": "pytorch", "path": "CONTRIBUTING.md"}`
- **THEN** the tool invokes the GitHub MCP's `get_file_contents` tool with the given parameters and returns the result

#### Scenario: Call a Discourse MCP tool
- **WHEN** user calls `get-specific-mcp-tool` with `mcp_name="discourse"`, `tool_name="discourse_read_topic"`, and `params={"topic_id": 12345}`
- **THEN** the tool invokes the Discourse MCP's `discourse_read_topic` tool and returns the result

### Requirement: Validate MCP name
The tool SHALL reject requests with unsupported `mcp_name` values and return an error listing the supported MCPs.

#### Scenario: Invalid MCP name
- **WHEN** user calls `get-specific-mcp-tool` with `mcp_name="jira"`
- **THEN** the tool returns an error: "Unsupported MCP: jira. Supported: github, slack, discourse"

### Requirement: Normalize response format
The tool SHALL wrap the underlying tool's raw response in the unified format with `summary` (brief description of what was retrieved), `items` (the raw response data), and `metadata` (source MCP, tool invoked).

#### Scenario: Verify response wrapping
- **WHEN** the underlying MCP tool returns a result
- **THEN** the response wraps it with `summary`, `items`, and `metadata` fields

### Requirement: List available tools
The tool SHALL accept a special mode where `tool_name="list"` to return available tools for the specified MCP.

#### Scenario: List GitHub MCP tools
- **WHEN** user calls `get-specific-mcp-tool` with `mcp_name="github"` and `tool_name="list"`
- **THEN** the tool returns a list of available GitHub MCP tool names with brief descriptions
