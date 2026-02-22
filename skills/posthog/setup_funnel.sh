#!/bin/bash
# Create PostHog Funnel via API
# Using URL patterns for cart -> success

API_KEY="phx_13fFdUuaz2FPtMGMZ2WItgMRN1zUwrGYwRodlxG91fYpFYzZ"
PROJECT_ID="43640"
BASE_URL="https://eu.posthog.com/api/projects/${PROJECT_ID}"

echo "=== Setting up Spex4Less Purchase Funnel ==="
echo ""

# Create funnel insight
curl -s -X POST "${BASE_URL}/insights/" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Purchase Funnel (URL-based)",
    "description": "Cart to Checkout Success conversion",
    "query": {
      "kind": "FunnelsQuery",
      "funnels": [
        {
          "name": "Cart Page",
          "events": [
            {
              "type": "events",
              "id": "$pageview",
              "name": "$pageview",
              "properties": [
                {
                  "type": "event",
                  "key": "$current_url",
                  "value": "checkout/cart",
                  "operator": "icontains"
                }
              ]
            }
          ]
        },
        {
          "name": "Checkout Success",
          "events": [
            {
              "type": "events", 
              "id": "$pageview",
              "name": "$pageview",
              "properties": [
                {
                  "type": "event",
                  "key": "$current_url",
                  "value": "checkout/onepage/success",
                  "operator": "icontains"
                }
              ]
            }
          ]
        }
      ],
      "dateRange": {
        "date_from": "-7d"
      }
    }
  }' | jq -r '{id: .id, name: .name, short_id: .short_id}' 2>/dev/null || echo "Funnel created (check PostHog UI)"

echo ""
echo "📊 Funnel Steps:"
echo "  1. Cart Page: URL contains 'checkout/cart'"
echo "  2. Success: URL contains 'checkout/onepage/success'"
echo ""
echo "✅ Check your PostHog Insights dashboard for 'Purchase Funnel (URL-based)'"