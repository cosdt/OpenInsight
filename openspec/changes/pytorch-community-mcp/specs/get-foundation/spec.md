## ADDED Requirements

### Requirement: Retrieve PyTorch Foundation information
The tool SHALL return PyTorch Foundation information by querying the pytorch-fdn GitHub organization and official channels.

#### Scenario: Query foundation info
- **WHEN** user calls `get-foundation`
- **THEN** the tool returns foundation membership, board information, and recent announcements

### Requirement: Filter by information type
The tool SHALL accept an optional `type` parameter ("members", "board", "announcements", "all", defaulting to "all").

#### Scenario: Query board info only
- **WHEN** user calls `get-foundation` with `type="board"`
- **THEN** the tool returns board member information

#### Scenario: Query all foundation info
- **WHEN** user calls `get-foundation` without `type` parameter
- **THEN** the tool returns comprehensive foundation information

### Requirement: Return unified format
The tool SHALL return a JSON object containing `summary`, `items`, and `metadata`.

#### Scenario: Verify response structure
- **WHEN** the tool returns results
- **THEN** the response contains `summary`, `items`, and `metadata` with `source_urls`
