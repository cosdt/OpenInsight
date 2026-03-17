## ADDED Requirements

### Requirement: Aggregate activity across platforms for key contributors
The tool SHALL accept an optional `contributors` parameter (list of usernames) and an optional time range (`start_date`/`end_date`, defaulting to past 7 days), and return aggregated activity from GitHub (PRs, issues, reviews), Slack (messages), and Discourse (posts, topics) for those contributors.

#### Scenario: Query specific contributor
- **WHEN** user calls `get-key-contributors-activity` with `contributors=["ezyang"]` and `start_date="2024-01-01"` and `end_date="2024-01-07"`
- **THEN** the tool returns ezyang's GitHub PRs/reviews, Slack messages, and Discourse posts from that period

#### Scenario: Query all key contributors with defaults
- **WHEN** user calls `get-key-contributors-activity` without parameters
- **THEN** the tool uses the built-in key contributor list and returns activity from the past 7 days

### Requirement: Use built-in key contributor list as default
The tool SHALL maintain a configurable list of PyTorch key contributors. When `contributors` parameter is not provided, this list MUST be used.

#### Scenario: Default contributor list
- **WHEN** user calls `get-key-contributors-activity` without `contributors` parameter
- **THEN** the tool queries activity for all contributors in the built-in list

### Requirement: Return per-contributor activity breakdown
The tool SHALL return a JSON object containing `summary`, `items` (list of contributor objects, each with `username`, `github_activity`, `slack_activity`, `discourse_activity`), and `metadata`.

#### Scenario: Verify response structure
- **WHEN** the tool returns results
- **THEN** each item contains `username` and activity breakdown per platform, with each platform section listing relevant items (PRs, messages, posts) with title/text, url, and timestamp

### Requirement: Handle partial platform availability
The tool SHALL return available data even if one platform is unreachable, with the `metadata` field indicating which platforms had errors.

#### Scenario: Slack unavailable
- **WHEN** Slack MCP is unreachable during a query
- **THEN** the tool returns GitHub and Discourse data, and `metadata.errors` includes `{"slack": "connection timeout"}`
