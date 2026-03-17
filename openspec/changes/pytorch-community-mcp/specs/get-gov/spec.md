## ADDED Requirements

### Requirement: Retrieve PyTorch governance information
The tool SHALL return current PyTorch governance structure by querying GitHub (pytorch/pytorch governance files) and Discourse (governance-related topics).

#### Scenario: Query governance info
- **WHEN** user calls `get-gov`
- **THEN** the tool returns governance structure including maintainers, module owners, and governance documents

### Requirement: Filter by governance area
The tool SHALL accept an optional `area` parameter (e.g., "maintainers", "module-owners", "policies") to narrow results.

#### Scenario: Query maintainers only
- **WHEN** user calls `get-gov` with `area="maintainers"`
- **THEN** the tool returns the current maintainer list

#### Scenario: Query all governance info
- **WHEN** user calls `get-gov` without `area` parameter
- **THEN** the tool returns comprehensive governance information

### Requirement: Return unified format
The tool SHALL return a JSON object containing `summary` (Markdown overview of governance), `items` (structured governance data), and `metadata` (sources, last_updated).

#### Scenario: Verify response structure
- **WHEN** the tool returns results
- **THEN** the response contains `summary`, `items`, and `metadata` with `source_urls` listing the governance documents consulted
