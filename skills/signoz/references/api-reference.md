# SigNoz API Reference

## Authentication

All API requests require the `SIGNOZ-API-KEY` header:

```
SIGNOZ-API-KEY: your-api-key-here
```

## Endpoints

### POST /api/v5/query_range

Main query endpoint for logs, metrics, and traces.

#### Query Logs

Request:
```json
{
  "start": 1708454400000,
  "end": 1708540800000,
  "requestType": "list",
  "compositeQuery": {
    "queries": [{
      "type": "builder_query",
      "spec": {
        "name": "A",
        "signal": "logs",
        "filters": [
          {"key": "service_name", "value": "magento", "operator": "="}
        ],
        "limit": 100
      }
    }]
  }
}
```

#### Query Metrics (Time Series)

Request:
```json
{
  "start": 1708454400000,
  "end": 1708540800000,
  "requestType": "time_series",
  "compositeQuery": {
    "queries": [{
      "type": "builder_query",
      "spec": {
        "name": "A",
        "signal": "metrics",
        "stepInterval": 60,
        "aggregations": [{
          "metricName": "cpu_usage",
          "timeAggregation": "avg",
          "spaceAggregation": "sum"
        }]
      }
    }]
  }
}
```

#### Query Traces

Request:
```json
{
  "start": 1708454400000,
  "end": 1708540800000,
  "requestType": "list",
  "compositeQuery": {
    "queries": [{
      "type": "builder_query",
      "spec": {
        "name": "A",
        "signal": "traces",
        "filters": [
          {"key": "service_name", "value": "api", "operator": "="}
        ],
        "limit": 50
      }
    }]
  }
}
```

## Aggregation Types

- `avg` - Average
- `sum` - Sum
- `min` - Minimum
- `max` - Maximum
- `count` - Count

## Time Formats

Timestamps should be in **milliseconds since epoch**.

Relative time shortcuts for CLI:
- `1h` - 1 hour ago
- `30m` - 30 minutes ago
- `1d` - 1 day ago
- `7d` - 7 days ago

## Common Filters

### Logs
- `service_name` - Service that emitted the log
- `severity_text` - Log level (INFO, ERROR, WARN, DEBUG)
- `body` / `message` - Log message content

### Metrics
- `metricName` - Name of the metric
- `label` - Metric labels/dimensions

### Traces
- `service_name` - Service handling the request
- `operation` - Operation/span name
- `trace_id` - Trace identifier
- `duration_nano` - Span duration in nanoseconds

## Response Format

```json
{
  "result": [
    {
      "metric": {"__name__": "metric_name", "label": "value"},
      "values": [[timestamp_ms, value], ...]
    }
  ]
}
```

For list queries (logs/traces), values contain objects with field data.

## Error Handling

Common HTTP status codes:
- `400` - Bad request (invalid query)
- `401` - Unauthorized (bad API key)
- `403` - Forbidden (insufficient permissions)
- `500` - Internal server error

## Rate Limits

SigNoz Cloud typically allows:
- 1000 requests per minute per API key
- Burst allowed for short periods

## Tips

1. Use small time ranges for faster queries
2. Add filters to reduce data volume
3. Use appropriate step intervals for metrics (don't over-sample)
4. Always set limits for list queries
5. Prefer time_series for graphs, list for details
