## ADDED Requirements

### Requirement: Retrieve PyTorch events from official API
The tool SHALL query the PyTorch Events API (pytorch.org/wp-json/tec/v1/events) and return community events. It SHALL also check the RSS feed (pytorch.org/feed/) for event announcements in blog posts.

#### Scenario: Query upcoming events
- **WHEN** user calls `get-event` with `start_date` set to today
- **THEN** the tool returns upcoming events from the Events API and any event-related blog posts from RSS

### Requirement: Filter events by time range
The tool SHALL accept optional `start_date` and `end_date` parameters (ISO 8601). When not provided, `start_date` defaults to today and `end_date` defaults to 90 days from today.

#### Scenario: Query events for next 3 months
- **WHEN** user calls `get-event` without date parameters
- **THEN** the tool returns events in the next 90 days

#### Scenario: Query events for a specific period
- **WHEN** user calls `get-event` with `start_date="2024-06-01"` and `end_date="2024-12-31"`
- **THEN** the tool returns events within that date range

### Requirement: Filter events by type
The tool SHALL accept an optional `event_type` parameter ("virtual", "in-person", "all", defaulting to "all").

#### Scenario: Query virtual events only
- **WHEN** user calls `get-event` with `event_type="virtual"`
- **THEN** the tool returns only virtual events

### Requirement: Return unified format
The tool SHALL return a JSON object containing `summary`, `items` (list of event objects with title, url, start_date, end_date, location, event_type, description, registration_url), and `metadata`.

#### Scenario: Verify response structure
- **WHEN** the tool returns results
- **THEN** each item contains `title`, `url`, `start_date`, `end_date`, `location`, `event_type`, `description`, and `registration_url`
