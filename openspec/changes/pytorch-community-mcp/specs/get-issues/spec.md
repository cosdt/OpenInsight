## ADDED Requirements

### Requirement: Retrieve PyTorch issues by time range
The tool SHALL accept `start_date` and `end_date` (ISO 8601) parameters and return issues from pytorch/pytorch created or updated within that range. Both parameters MUST be optional, defaulting to the past 7 days.

#### Scenario: Query issues for a specific date range
- **WHEN** user calls `get-issues` with `start_date="2024-01-01"` and `end_date="2024-01-07"`
- **THEN** the tool returns all issues from pytorch/pytorch created or updated in that range

#### Scenario: Default time range
- **WHEN** user calls `get-issues` without date parameters
- **THEN** the tool returns issues from the past 7 days

### Requirement: Filter issues by module
The tool SHALL accept an optional `module` parameter and filter issues by matching labels (e.g., "module: distributed") in the pytorch/pytorch repository.

#### Scenario: Filter by module label
- **WHEN** user calls `get-issues` with `module="compiler"`
- **THEN** the tool returns only issues labeled with "module: compiler"

### Requirement: Filter issues by state
The tool SHALL accept an optional `state` parameter ("open", "closed", or "all", defaulting to "all") to filter issues by their current state.

#### Scenario: Query only open issues
- **WHEN** user calls `get-issues` with `state="open"`
- **THEN** the tool returns only open issues

### Requirement: Return unified format
The tool SHALL return a JSON object containing `summary` (Markdown overview), `items` (list of issue objects with title, url, author, state, labels, created_at, updated_at, comments_count), and `metadata`.

#### Scenario: Verify response structure
- **WHEN** the tool returns results
- **THEN** each item contains `title`, `url`, `author`, `state`, `labels`, `created_at`, `updated_at`, and `comments_count`

### Requirement: Limit results
The tool SHALL accept an optional `limit` parameter (default 50, max 200).

#### Scenario: Apply limit
- **WHEN** user calls `get-issues` with `limit=20`
- **THEN** the tool returns at most 20 issues
