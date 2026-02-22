#!/usr/bin/env python3
"""
SigNoz CLI - Query logs, metrics, and traces from SigNoz API
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime, timedelta
from urllib.parse import urljoin

class SigNozClient:
    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key or os.getenv('SIGNOZ_API_KEY')
        self.base_url = base_url or os.getenv('SIGNOZ_URL', 'https://logs.s4l.link')
        
        if not self.api_key:
            raise ValueError("API key required. Set SIGNOZ_API_KEY env var or pass --api-key")
        
        self.session = requests.Session()
        self.session.headers.update({
            'SIGNOZ-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        })
    
    def _post(self, endpoint, data):
        url = urljoin(self.base_url, f'/api/v5/{endpoint}')
        resp = self.session.post(url, json=data)
        resp.raise_for_status()
        return resp.json()
    
    def query_logs(self, service=None, query=None, start=None, end=None, limit=100):
        """Query logs with filters"""
        if not start:
            start = int((datetime.now() - timedelta(hours=1)).timestamp() * 1000)
        if not end:
            end = int(datetime.now().timestamp() * 1000)
        
        # Build filter expression
        filter_parts = []
        if service:
            filter_parts.append(f"service_name = '{service}'")
        if query:
            filter_parts.append(f"body contains '{query}'")
        
        filter_expr = " AND ".join(filter_parts) if filter_parts else ""
        
        payload = {
            "start": start,
            "end": end,
            "requestType": "raw",
            "variables": {},
            "compositeQuery": {
                "queries": [
                    {
                        "type": "builder_query",
                        "spec": {
                            "name": "A",
                            "signal": "logs",
                            "filter": {
                                "expression": filter_expr
                            } if filter_expr else {"expression": ""},
                            "selectFields": [
                                {"name": "timestamp"},
                                {"name": "body"},
                                {"name": "severity_text"},
                                {"name": "service_name"}
                            ],
                            "order": [
                                {
                                    "key": {"name": "timestamp"},
                                    "direction": "desc"
                                }
                            ],
                            "limit": limit,
                            "offset": 0,
                            "disabled": False
                        }
                    }
                ]
            }
        }
        
        return self._post('query_range', payload)
    
    def query_metrics(self, metric_name, start=None, end=None, step=60, aggregation='avg'):
        """Query time-series metrics"""
        if not start:
            start = int((datetime.now() - timedelta(hours=1)).timestamp() * 1000)
        if not end:
            end = int(datetime.now().timestamp() * 1000)
        
        payload = {
            "start": start,
            "end": end,
            "requestType": "timeseries",
            "variables": {},
            "compositeQuery": {
                "queries": [
                    {
                        "type": "builder_query",
                        "spec": {
                            "name": "A",
                            "signal": "metrics",
                            "filter": {"expression": f"__name__ = '{metric_name}'"},
                            "aggregateOperator": aggregation,
                            "stepInterval": step,
                            "disabled": False
                        }
                    }
                ]
            }
        }
        
        return self._post('query_range', payload)
    
    def query_traces(self, service=None, operation=None, start=None, end=None, limit=50):
        """Query distributed traces"""
        if not start:
            start = int((datetime.now() - timedelta(hours=1)).timestamp() * 1000)
        if not end:
            end = int(datetime.now().timestamp() * 1000)
        
        # Build filter expression
        filter_parts = []
        if service:
            filter_parts.append(f"service_name = '{service}'")
        if operation:
            filter_parts.append(f"name = '{operation}'")
        
        filter_expr = " AND ".join(filter_parts) if filter_parts else ""
        
        payload = {
            "start": start,
            "end": end,
            "requestType": "raw",
            "variables": {},
            "compositeQuery": {
                "queries": [
                    {
                        "type": "builder_query",
                        "spec": {
                            "name": "A",
                            "signal": "traces",
                            "filter": {
                                "expression": filter_expr
                            } if filter_expr else {"expression": ""},
                            "selectFields": [
                                {"name": "trace_id"},
                                {"name": "service_name"},
                                {"name": "name"},
                                {"name": "duration_nano"},
                                {"name": "timestamp"}
                            ],
                            "order": [
                                {
                                    "key": {"name": "timestamp"},
                                    "direction": "desc"
                                }
                            ],
                            "limit": limit,
                            "offset": 0,
                            "disabled": False
                        }
                    }
                ]
            }
        }
        
        return self._post('query_range', payload)
    
    def get_services(self):
        """List all services from recent traces"""
        result = self.query_traces(limit=1000)
        services = set()
        
        # Parse the response structure
        data = result.get('data', {})
        results = data.get('data', {}).get('results', [])
        
        for r in results:
            rows = r.get('rows', [])
            for row in rows:
                row_data = row.get('data', {})
                resources = row_data.get('resources_string', {})
                service = resources.get('service_name')
                if service:
                    services.add(service)
        
        return sorted(list(services))

def parse_time(time_str):
    """Parse time string like '1h', '30m', '1d' to milliseconds"""
    if not time_str:
        return None
    
    # If it's already a timestamp
    if time_str.isdigit():
        return int(time_str)
    
    unit = time_str[-1]
    value = int(time_str[:-1])
    
    now = datetime.now()
    if unit == 'h':
        dt = now - timedelta(hours=value)
    elif unit == 'm':
        dt = now - timedelta(minutes=value)
    elif unit == 'd':
        dt = now - timedelta(days=value)
    else:
        raise ValueError(f"Unknown time unit: {unit}")
    
    return int(dt.timestamp() * 1000)

def format_logs(result):
    """Pretty print log results"""
    data = result.get('data', {})
    results = data.get('data', {}).get('results', [])
    
    for r in results:
        rows = r.get('rows', [])
        for row in rows:
            row_data = row.get('data', {})
            ts = row.get('timestamp', '')
            msg = row_data.get('body', '')
            level = row_data.get('severity_text', 'INFO')
            resources = row_data.get('resources_string', {})
            service = resources.get('service_name', 'unknown')
            
            # Truncate long messages
            if len(msg) > 200:
                msg = msg[:197] + '...'
            
            print(f"[{ts}] {level:8} {service:20} {msg}")

def format_metrics(result):
    """Pretty print metric results"""
    data = result.get('data', {})
    results = data.get('data', {}).get('results', [])
    
    for r in results:
        series = r.get('series', {})
        metric_name = series.get('labels', {}).get('__name__', 'unknown')
        values = r.get('values', [])
        
        for point in values:
            ts = datetime.fromtimestamp(point[0]).strftime('%Y-%m-%d %H:%M:%S')
            value = point[1]
            print(f"[{ts}] {metric_name}: {value}")

def format_traces(result):
    """Pretty print trace results"""
    data = result.get('data', {})
    results = data.get('data', {}).get('results', [])
    
    print(f"{'Trace ID':20} {'Service':20} {'Operation':30} {'Duration':>10}")
    print("=" * 85)
    
    for r in results:
        rows = r.get('rows', [])
        for row in rows:
            row_data = row.get('data', {})
            trace_id = row_data.get('trace_id', '')[:16]
            resources = row_data.get('resources_string', {})
            service = resources.get('service_name', 'unknown')
            operation = row_data.get('name', 'unknown')
            duration = row_data.get('duration_nano', 0) / 1e6  # Convert to ms
            
            print(f"{trace_id:20} {service:20} {operation:30} {duration:>10.2f}ms")

def main():
    parser = argparse.ArgumentParser(description='SigNoz CLI')
    parser.add_argument('--api-key', help='SigNoz API key (or set SIGNOZ_API_KEY)')
    parser.add_argument('--url', default='https://logs.s4l.link', help='SigNoz URL')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Logs command
    logs_parser = subparsers.add_parser('logs', help='Query logs')
    logs_parser.add_argument('--service', '-s', help='Filter by service name')
    logs_parser.add_argument('--query', '-q', help='Search query string')
    logs_parser.add_argument('--start', help='Start time (timestamp or like "1h", "30m")')
    logs_parser.add_argument('--end', help='End time (timestamp)')
    logs_parser.add_argument('--limit', '-l', type=int, default=100, help='Max results')
    
    # Metrics command
    metrics_parser = subparsers.add_parser('metrics', help='Query metrics')
    metrics_parser.add_argument('metric', help='Metric name')
    metrics_parser.add_argument('--start', help='Start time (like "1h", "24h", "7d")')
    metrics_parser.add_argument('--end', help='End time')
    metrics_parser.add_argument('--step', type=int, default=60, help='Step interval in seconds')
    metrics_parser.add_argument('--aggregation', '-a', default='avg', choices=['avg', 'sum', 'min', 'max', 'count'])
    
    # Traces command
    traces_parser = subparsers.add_parser('traces', help='Query traces')
    traces_parser.add_argument('--service', '-s', help='Filter by service')
    traces_parser.add_argument('--operation', '-o', help='Filter by operation name')
    traces_parser.add_argument('--start', help='Start time (like "1h", "30m")')
    traces_parser.add_argument('--end', help='End time')
    traces_parser.add_argument('--limit', '-l', type=int, default=50, help='Max results')
    
    # Services command
    subparsers.add_parser('services', help='List all services')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        client = SigNozClient(api_key=args.api_key, base_url=args.url)
        
        if args.command == 'logs':
            start = parse_time(args.start) if args.start else None
            end = parse_time(args.end) if args.end else None
            result = client.query_logs(
                service=args.service,
                query=args.query,
                start=start,
                end=end,
                limit=args.limit
            )
            format_logs(result)
        
        elif args.command == 'metrics':
            start = parse_time(args.start) if args.start else None
            end = parse_time(args.end) if args.end else None
            result = client.query_metrics(
                metric_name=args.metric,
                start=start,
                end=end,
                step=args.step,
                aggregation=args.aggregation
            )
            format_metrics(result)
        
        elif args.command == 'traces':
            start = parse_time(args.start) if args.start else None
            end = parse_time(args.end) if args.end else None
            result = client.query_traces(
                service=args.service,
                operation=args.operation,
                start=start,
                end=end,
                limit=args.limit
            )
            format_traces(result)
        
        elif args.command == 'services':
            services = client.get_services()
            for svc in services:
                print(svc)
    
    except requests.exceptions.HTTPError as e:
        print(f"API Error: {e}", file=sys.stderr)
        if e.response:
            try:
                err_data = e.response.json()
                print(f"Details: {json.dumps(err_data, indent=2)}", file=sys.stderr)
            except:
                print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
