# PostHog Analytics Skill

Query and analyze data from PostHog product analytics platform.

## Configuration

Set these environment variables:
- `POSTHOG_API_KEY` - Your PostHog Personal API Key
- `POSTHOG_PROJECT_ID` - Your PostHog Project ID (default: 43640)
- `POSTHOG_HOST` - PostHog instance URL (default: https://eu.posthog.com)

## Usage

```bash
# Query latest events
!posthog events [--limit=10] [--after=2024-01-01] [--event=$pageview]

# List dashboards
!posthog insights

# Get funnel statistics
!posthog funnel <funnel_id>

# Query persons/users
!posthog persons [--search=email] [--limit=20]

# List cohorts
!posthog cohorts

# List feature flags
!posthog flags

# Get session recordings
!posthog recordings [--limit=10]
```

## Output Formats

- Events: JSON with event name, timestamp, distinct_id, and properties
- Insights: Table of dashboards with ID, name, and description
- Persons: Table of users with ID, distinct_id, and created date
- Cohorts: Table of cohorts with ID, name, and user count
- Feature Flags: Table of flags with key, name, and status

## API Reference

Uses PostHog REST API v1:
- Base URL: `https://eu.posthog.com/api/projects/{project_id}`
- Authentication: Bearer token in Authorization header
- Rate limits apply based on your PostHog plan
