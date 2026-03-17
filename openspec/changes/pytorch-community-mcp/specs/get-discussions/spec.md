## ADDED Requirements

### Requirement: Retrieve Discourse discussions by time range
The tool SHALL accept optional `start_date` and `end_date` parameters (ISO 8601, defaulting to past 7 days) and return topics from discuss.pytorch.org within that range.

#### Scenario: Query discussions for a week
- **WHEN** user calls `get-discussions` with `start_date="2024-01-01"` and `end_date="2024-01-07"`
- **THEN** the tool returns Discourse topics created or with activity within that date range

#### Scenario: Default time range
- **WHEN** user calls `get-discussions` without date parameters
- **THEN** the tool returns discussions from the past 7 days

### Requirement: Search discussions by keyword
The tool SHALL accept an optional `query` parameter to search topics and posts.

#### Scenario: Keyword search
- **WHEN** user calls `get-discussions` with `query="quantization"`
- **THEN** the tool returns topics matching "quantization"

### Requirement: Filter discussions by category
The tool SHALL accept an optional `category` parameter to filter by Discourse category (e.g., "dev-discuss", "announcements").

#### Scenario: Filter by category
- **WHEN** user calls `get-discussions` with `category="dev-discuss"`
- **THEN** the tool returns only topics in the dev-discuss category

### Requirement: Return unified format
The tool SHALL return a JSON object containing `summary`, `items` (list of discussion objects with title, url, author, category, created_at, last_activity_at, reply_count, views), and `metadata`.

#### Scenario: Verify response structure
- **WHEN** the tool returns results
- **THEN** each item contains `title`, `url`, `author`, `category`, `created_at`, `last_activity_at`, `reply_count`, and `views`

### Requirement: Limit results
The tool SHALL accept an optional `limit` parameter (default 30, max 100).

#### Scenario: Apply limit
- **WHEN** user calls `get-discussions` with `limit=15`
- **THEN** the tool returns at most 15 discussions
