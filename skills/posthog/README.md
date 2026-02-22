# PostHog Analytics Skill

A comprehensive OpenClaw skill for querying and analyzing data from PostHog product analytics platform.

## Features

- **Events**: Query latest events with filtering by date and event type
- **Insights**: List all saved insights and dashboards
- **Dashboards**: Browse dashboard collections
- **Funnels**: Retrieve funnel statistics and conversion data
- **Persons**: Query user data with search capabilities
- **Cohorts**: List user cohorts and segments
- **Feature Flags**: View active feature flags
- **Session Recordings**: Browse session recordings

## Installation

1. Copy the skill to your OpenClaw skills directory:
```bash
cp -r skills/posthog /root/.openclaw/workspace/skills/
```

2. Set your environment variables (optional - defaults are pre-configured):
```bash
export POSTHOG_API_KEY="your_api_key"
export POSTHOG_PROJECT_ID="43640"
export POSTHOG_HOST="https://eu.posthog.com"
```

## Usage

### Events

Query the latest events captured by PostHog:

```bash
# Get 10 most recent events
!posthog events

# Get 50 events
!posthog events --limit=50

# Get events after a specific date
!posthog events --after=2024-01-01

# Filter by event type
!posthog events --event=\$pageview

# Combined filters
!posthog events --limit=20 --after=2024-01-01 --event=\$autocapture
```

### Insights & Dashboards

List all saved insights and dashboards:

```bash
# List all insights
!posthog insights

# List all dashboards
!posthog dashboards
```

### Funnels

Get funnel statistics by ID:

```bash
# Get funnel data
!posthog funnel 683977

# The funnel ID can be found from the insights list
```

### Persons/Users

Query person/user data:

```bash
# Get 20 most recent persons
!posthog persons

# Get more persons
!posthog persons --limit=50

# Search by email or property
!posthog persons --search=user@example.com
```

### Cohorts

List user cohorts:

```bash
!posthog cohorts
```

### Feature Flags

List all feature flags:

```bash
!posthog flags
```

### Session Recordings

Browse session recordings:

```bash
# Get 10 most recent recordings
!posthog recordings

# Get more recordings
!posthog recordings --limit=20
```

## Output Formats

All commands output both:
1. **Human-readable tables** with color-coded columns
2. **Raw JSON** for programmatic use and piping

## Examples

### Daily Active Users Report

```bash
# Get today's pageview events
!posthog events --after=$(date +%Y-%m-%d) --event=\$pageview --limit=100
```

### User Journey Analysis

```bash
# Find a specific user
!posthog persons --search=specific@email.com

# Get their events
!posthog events --after=2024-01-01 --limit=50
```

### Conversion Funnel Check

```bash
# List all insights to find funnel ID
!posthog insights

# Get funnel details
!posthog funnel 683977
```

## Troubleshooting

### API Key Issues

If you see authentication errors:
1. Verify your API key is correct
2. Check that the key has access to the project
3. Ensure you're using the correct PostHog host (EU vs US)

### Rate Limiting

If you hit rate limits:
1. Reduce the `--limit` parameter
2. Add more specific filters like `--after`
3. Cache results locally if running repeatedly

### Empty Results

If commands return no results:
1. Check your project ID is correct
2. Verify data exists in the PostHog UI
3. Try broadening your filters (remove `--event` or date filters)

## API Reference

This skill uses the PostHog REST API:
- **Base URL**: `https://eu.posthog.com/api/projects/{project_id}`
- **Authentication**: Bearer token in Authorization header
- **Documentation**: https://posthog.com/docs/api

## License

MIT License - Part of the OpenClaw skill ecosystem.
