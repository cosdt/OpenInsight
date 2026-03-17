## ADDED Requirements

### Requirement: Aggregate RFCs from multiple repositories
The tool SHALL query both pytorch/pytorch (issues/PRs labeled "RFC" or "rfc") and pytorch/rfcs repository, and return a unified list of RFCs.

#### Scenario: RFCs from both repos
- **WHEN** user calls `get-rfcs`
- **THEN** the tool returns RFCs from both pytorch/pytorch and pytorch/rfcs, with each item's `source_repo` field indicating its origin

### Requirement: Filter RFCs by time range
The tool SHALL accept optional `start_date` and `end_date` parameters (ISO 8601), defaulting to the past 30 days.

#### Scenario: Query recent RFCs
- **WHEN** user calls `get-rfcs` without date parameters
- **THEN** the tool returns RFCs from the past 30 days

#### Scenario: Query RFCs for a specific period
- **WHEN** user calls `get-rfcs` with `start_date="2024-01-01"` and `end_date="2024-03-31"`
- **THEN** the tool returns all RFCs created or updated in Q1 2024

### Requirement: Filter RFCs by category
The tool SHALL accept an optional `category` parameter (e.g., "distributed", "compiler", "autograd") to filter RFCs by topic area.

#### Scenario: Filter by category
- **WHEN** user calls `get-rfcs` with `category="distributed"`
- **THEN** the tool returns only RFCs related to distributed training

### Requirement: Return unified format with source attribution
The tool SHALL return a JSON object containing `summary`, `items` (with title, url, author, state, source_repo, created_at, updated_at, abstract), and `metadata`.

#### Scenario: Verify response structure
- **WHEN** the tool returns results
- **THEN** each item contains `title`, `url`, `author`, `state`, `source_repo`, `created_at`, `updated_at`, and `abstract` (first 200 chars of body)
