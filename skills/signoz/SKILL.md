---
name: signoz
description: Query SigNoz observability platform for logs, metrics, and traces. Use when user asks to check logs, query metrics, analyze traces, monitor services, or investigate issues in SigNoz. Supports filtering by service, time range, and custom queries. Triggers include 'check logs in signoz', 'query metrics', 'look at traces', 'what's happening with service X', 'show me errors', 'monitoring dashboard'.
---

# SigNoz Observability

Query logs, metrics, and traces from SigNoz API.

## Quick Start

```bash
# Set environment variables
export SIGNOZ_API_KEY=your-key
export SIGNOZ_URL=https://logs.s4l.link

# Query recent logs
signoz logs --service=magento --last=1h

# Check metrics
signoz metrics cpu_usage --start=24h

# View traces
signoz traces --service=api --limit=20

# List all services
signoz services
```

## CLI Tool

Use `scripts/signoz-cli.py` for all queries:

```bash
python3 scripts/signoz-cli.py logs --service=<name> [options]
python3 scripts/signoz-cli.py metrics <metric_name> [options]
python3 scripts/signoz-cli.py traces [options]
python3 scripts/signoz-cli.py services
```

### Logs Command

```bash
signoz logs --service=magento --query="error" --start=1h --limit=50
```

Options:
- `--service, -s` — Filter by service name
- `--query, -q` — Search query string
- `--start` — Start time (e.g., `1h`, `30m`, `1d`, or timestamp)
- `--end` — End time (timestamp)
- `--limit, -l` — Max results (default: 100)

### Metrics Command

```bash
signoz metrics cpu_usage --start=24h --step=300 --aggregation=avg
```

Options:
- `metric` — Metric name (required)
- `--start` — Start time (e.g., `1h`, `24h`, `7d`)
- `--end` — End time
- `--step` — Step interval in seconds (default: 60)
- `--aggregation, -a` — Aggregation type: avg, sum, min, max, count

### Traces Command

```bash
signoz traces --service=api --operation=GET /orders --start=30m
```

Options:
- `--service, -s` — Filter by service
- `--operation, -o` — Filter by operation name
- `--start` — Start time
- `--end` — End time
- `--limit, -l` — Max results (default: 50)

### Services Command

```bash
signoz services
```

Lists all services reporting to SigNoz.

## Common Use Cases

### Debug Production Issues

```bash
# Check recent errors
signoz logs --service=magento --query="error" --start=15m

# Look at slow traces
signoz traces --service=api --start=1h | head -20

# Check resource usage during incident
signoz metrics memory_usage --start=2h --step=60
```

### Monitor Service Health

```bash
# What's running?
signoz services

# Recent activity by service
signoz logs --service=payment-gateway --start=1h --limit=10

# Error rate
signoz metrics http_requests_total --start=24h --aggregation=count
```

### Performance Analysis

```bash
# Trace latency distribution
signoz traces --service=api --start=1h

# Resource trends
signoz metrics cpu_usage --start=7d --step=3600
```

## Time Ranges

Use relative time for convenience:
- `5m` — 5 minutes ago
- `30m` — 30 minutes ago
- `1h` — 1 hour ago
- `6h` — 6 hours ago
- `24h` / `1d` — 1 day ago
- `7d` — 7 days ago

Or use millisecond timestamps for precise ranges.

## Environment Setup

Required environment variables:

```bash
export SIGNOZ_API_KEY=FS3pXDYQsAbBUAvJeOMxiPbXcVJSRafe8rpKjb12cx8=
export SIGNOZ_URL=https://logs.s4l.link
```

Add to `~/.bashrc` or `~/.zshrc` for persistence.

## API Reference

For detailed API documentation, see [references/api-reference.md](references/api-reference.md).

## Tips

- Start with broad time ranges, then narrow down
- Use `--limit` to avoid overwhelming output
- Filter by service first to reduce noise
- Combine with `grep`, `jq`, or `head` for further processing
- For dashboards, use the SigNoz web UI; use CLI for quick checks

## Troubleshooting

**"API key required" error**
→ Set `SIGNOZ_API_KEY` environment variable

**Empty results**
→ Check time range (might be too narrow)
→ Verify service name spelling
→ Try without filters first

**Connection errors**
→ Check `SIGNOZ_URL` is correct
→ Verify network access to SigNoz instance
