## ADDED Requirements

### Requirement: Retrieve PyTorch PRs by time range
The tool SHALL accept `start_date` (ISO 8601) and `end_date` (ISO 8601) parameters and return all PRs from pytorch/pytorch created or updated within that range. Both parameters MUST be optional, defaulting to the past 7 days.

#### Scenario: Query PRs for a specific week
- **WHEN** user calls `get-prs` with `start_date="2024-01-01"` and `end_date="2024-01-07"`
- **THEN** the tool returns all PRs from pytorch/pytorch created or updated between 2024-01-01 and 2024-01-07

#### Scenario: Query PRs with default time range
- **WHEN** user calls `get-prs` without date parameters
- **THEN** the tool returns PRs from the past 7 days

### Requirement: Filter PRs by module
The tool SHALL accept an optional `module` parameter (e.g., "distributed", "compiler", "autograd") and filter PRs by matching labels or path prefixes in the pytorch/pytorch repository.

#### Scenario: Filter PRs by distributed module
- **WHEN** user calls `get-prs` with `module="distributed"`
- **THEN** the tool returns only PRs labeled with "module: distributed" or touching files under `torch/distributed/`

#### Scenario: No module filter
- **WHEN** user calls `get-prs` without `module` parameter
- **THEN** the tool returns PRs across all modules

### Requirement: Return unified format
The tool SHALL return a JSON object containing `summary` (Markdown overview), `items` (list of PR objects with title, url, author, state, labels, created_at, updated_at), and `metadata` (source, time_range, total_count).

#### Scenario: Verify response structure
- **WHEN** the tool returns results
- **THEN** the response contains `summary`, `items`, and `metadata` fields, where each item has `title`, `url`, `author`, `state`, `labels`, `created_at`, and `updated_at`

### Requirement: Limit results with pagination
The tool SHALL accept an optional `limit` parameter (default 50, max 200) to control the number of returned PRs.

#### Scenario: Apply result limit
- **WHEN** user calls `get-prs` with `limit=10`
- **THEN** the tool returns at most 10 PRs
