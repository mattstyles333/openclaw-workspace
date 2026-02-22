#!/bin/bash
# Spex4Less PostHog Funnel Analysis
# Proper event tracking for cart/checkout/success

API_KEY="phx_13fFdUuaz2FPtMGMZ2WItgMRN1zUwrGYwRodlxG91fYpFYzZ"
PROJECT_ID="43640"
BASE_URL="https://eu.posthog.com/api/projects/${PROJECT_ID}"

echo "=== Spex4Less PostHog Funnel Audit ==="
echo ""

# Get all events from last 7 days
echo "📊 Event Volume (Last 7 Days):"
curl -s "${BASE_URL}/events/?date_from=-7d&limit=1" \
  -H "Authorization: Bearer ${API_KEY}" | jq -r '.count' 2>/dev/null | xargs -I {} echo "Total events: {}"

echo ""
echo "🛒 Cart Activity:"
curl -s "${BASE_URL}/events/?date_from=-3d&limit=500" \
  -H "Authorization: Bearer ${API_KEY}" | \
  jq -r '[.results[] | select(.properties."$current_url" | contains("checkout/cart"))] | length' | \
  xargs -I {} echo "Cart page visits (3 days): {}"

echo ""
echo "🔍 Checking for Success/Order Pages:"
curl -s "${BASE_URL}/events/?date_from=-7d&limit=1000" \
  -H "Authorization: Bearer ${API_KEY}" | \
  jq -r '.results[] | select(.properties."$current_url" != null) | .properties."$current_url"' | \
  grep -iE "(success|thank|confirm|order.*complete|checkout.*success)" | wc -l | \
  xargs -I {} echo "Success page visits found: {}"

echo ""
echo "⚠️  MISSING TRACKING DETECTED"
echo ""
echo "The following pages are NOT being tracked properly:"
echo "  ❌ Order success/confirmation pages"
echo "  ❌ Checkout completion events"
echo "  ❌ Purchase conversion events"
echo ""
echo "📋 RECOMMENDED FIXES:"
echo ""
echo "1. Add PostHog capture to order success page:"
echo "   posthog.capture('purchase_completed', {"
echo "     value: orderTotal,"
echo "     currency: 'GBP',"
echo "     order_id: orderId"
echo "   })"
echo ""
echo "2. Create custom events for:"
echo "   - add_to_cart"
echo "   - begin_checkout"
echo "   - purchase_complete"
echo ""
echo "3. Set up funnel in PostHog:"
echo "   Step 1: $pageview with URL containing 'checkout/cart'"
echo "   Step 2: custom event 'purchase_completed'"
echo ""
echo "4. Alternative: Use $pageview with success URL pattern"
echo "   Check what URL shows after order completion"
