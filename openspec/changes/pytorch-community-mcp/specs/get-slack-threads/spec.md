## ADDED Requirements

### Requirement: Retrieve Slack threads by channel and time range
The tool SHALL accept a required `channel` parameter (channel name or ID) and optional `start_date`/`end_date` parameters (ISO 8601, defaulting to past 7 days), and return message threads from that channel.

#### Scenario: Query specific channel
- **WHEN** user calls `get-slack-threads` with `channel="dev-discuss"` and `start_date="2024-01-01"` and `end_date="2024-01-07"`
- **THEN** the tool returns threads from the dev-discuss channel within that date range

#### Scenario: Default time range
- **WHEN** user calls `get-slack-threads` with `channel="general"` and no date parameters
- **THEN** the tool returns threads from the past 7 days

### Requirement: Search Slack messages by keyword
The tool SHALL accept an optional `query` parameter to search messages within the specified channel.

#### Scenario: Keyword search
- **WHEN** user calls `get-slack-threads` with `channel="dev-discuss"` and `query="distributed training"`
- **THEN** the tool returns threads matching "distributed training" in the dev-discuss channel

### Requirement: Return unified format
The tool SHALL return a JSON object containing `summary`, `items` (list of thread objects with text, author, timestamp, reply_count, channel, thread_url), and `metadata`.

#### Scenario: Verify response structure
- **WHEN** the tool returns results
- **THEN** each item contains `text`, `author`, `timestamp`, `reply_count`, `channel`, and `thread_url`

### Requirement: Limit results
The tool SHALL accept an optional `limit` parameter (default 30, max 100).

#### Scenario: Apply limit
- **WHEN** user calls `get-slack-threads` with `limit=10`
- **THEN** the tool returns at most 10 threads
