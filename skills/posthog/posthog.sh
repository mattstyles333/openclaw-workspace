#!/bin/bash

# PostHog Analytics Skill for OpenClaw
# Query and analyze data from PostHog product analytics

set -e

# Configuration
POSTHOG_API_KEY="${POSTHOG_API_KEY:-phx_13fFdUuaz2FPtMGMZ2WItgMRN1zUwrGYwRodlxG91fYpFYzZ}"
POSTHOG_PROJECT_ID="${POSTHOG_PROJECT_ID:-43640}"
POSTHOG_HOST="${POSTHOG_HOST:-https://eu.posthog.com}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# API helper function
api_call() {
    local endpoint="$1"
    local params="${2:-}"
    local url="${POSTHOG_HOST}/api/projects/${POSTHOG_PROJECT_ID}${endpoint}"
    
    if [[ -n "$params" ]]; then
        url="${url}?${params}"
    fi
    
    curl -s -X GET "$url" \
        -H "Authorization: Bearer ${POSTHOG_API_KEY}" \
        -H "Content-Type: application/json" 2>/dev/null
}

# Format timestamp
format_date() {
    local ts="$1"
    if command -v date &>/dev/null; then
        date -d "$ts" '+%Y-%m-%d %H:%M' 2>/dev/null || echo "$ts"
    else
        echo "$ts"
    fi
}

# Command: events
query_events() {
    local limit="${1:-10}"
    local after="${2:-}"
    local event_type="${3:-}"
    
    local params="limit=${limit}"
    
    if [[ -n "$after" ]]; then
        params="${params}&after=${after}"
    fi
    
    if [[ -n "$event_type" ]]; then
        params="${params}&event=${event_type}"
    fi
    
    echo -e "${BLUE}Fetching events...${NC}"
    local response
    response=$(api_call "/events" "$params")
    
    if [[ -z "$response" ]] || [[ "$response" == *"error"* ]]; then
        echo -e "${RED}Error fetching events${NC}"
        echo "$response" | jq . 2>/dev/null || echo "$response"
        return 1
    fi
    
    # Output summary
    local count
    count=$(echo "$response" | jq '.results | length')
    echo -e "${GREEN}Found ${count} events${NC}\n"
    
    # Output as formatted table
    echo "$response" | jq -r '.results[] | "\u001b[36mEvent:\u001b[0m \(.event) | \u001b[33mTime:\u001b[0m \(.timestamp[0:19]) | \u001b[35mID:\u001b[0m \(.distinct_id[0:20])..."' 2>/dev/null || echo "$response" | jq .
    
    # Also output raw JSON for piping
    echo -e "\n${BLUE}--- Raw JSON ---${NC}"
    echo "$response" | jq .
}

# Command: insights
list_insights() {
    echo -e "${BLUE}Fetching insights/dashboards...${NC}"
    local response
    response=$(api_call "/insights")
    
    if [[ -z "$response" ]]; then
        echo -e "${RED}Error fetching insights${NC}"
        return 1
    fi
    
    local count
    count=$(echo "$response" | jq '.results | length')
    echo -e "${GREEN}Found ${count} insights${NC}\n"
    
    # Output as table
    echo "$response" | jq -r '.results[] | "\u001b[36mID:\u001b[0m \(.id) | \u001b[33mName:\u001b[0m \(.name) | \u001b[35mType:\u001b[0m \(.type // "N/A") | \u001b[32mCreated:\u001b[0m \(.created_at[0:10])"'
    
    echo -e "\n${BLUE}--- Raw JSON ---${NC}"
    echo "$response" | jq .
}

# Command: dashboards
list_dashboards() {
    echo -e "${BLUE}Fetching dashboards...${NC}"
    local response
    response=$(api_call "/dashboards")
    
    if [[ -z "$response" ]]; then
        echo -e "${RED}Error fetching dashboards${NC}"
        return 1
    fi
    
    local count
    count=$(echo "$response" | jq '.results | length')
    echo -e "${GREEN}Found ${count} dashboards${NC}\n"
    
    # Output as table
    echo "$response" | jq -r '.results[] | "\u001b[36mID:\u001b[0m \(.id) | \u001b[33mName:\u001b[0m \(.name) | \u001b[35mDescription:\u001b[0m \(.description // "N/A" | if length > 40 then .[0:40] + "..." else . end) | \u001b[32mCreated:\u001b[0m \(.created_at[0:10])"'
    
    echo -e "\n${BLUE}--- Raw JSON ---${NC}"
    echo "$response" | jq .
}

# Command: funnel
get_funnel() {
    local funnel_id="$1"
    
    if [[ -z "$funnel_id" ]]; then
        echo -e "${RED}Error: Funnel ID required${NC}"
        echo "Usage: !posthog funnel <funnel_id>"
        return 1
    fi
    
    echo -e "${BLUE}Fetching funnel ${funnel_id}...${NC}"
    local response
    response=$(api_call "/insights/${funnel_id}")
    
    if [[ -z "$response" ]]; then
        echo -e "${RED}Error fetching funnel${NC}"
        return 1
    fi
    
    # Check if it's actually a funnel
    local insight_type
    insight_type=$(echo "$response" | jq -r '.type // "unknown"')
    
    echo -e "${GREEN}Funnel Details:${NC}\n"
    echo "$response" | jq -r '"Name: \(.name) | ID: \(.id) | Type: \(.type // "N/A") | Created: \(.created_at[0:10])"'
    
    echo -e "\n${BLUE}--- Full JSON ---${NC}"
    echo "$response" | jq .
}

# Command: persons
query_persons() {
    local limit="${1:-20}"
    local search="${2:-}"
    
    local params="limit=${limit}"
    
    if [[ -n "$search" ]]; then
        params="${params}&search=${search}"
    fi
    
    echo -e "${BLUE}Fetching persons...${NC}"
    local response
    response=$(api_call "/persons" "$params")
    
    if [[ -z "$response" ]]; then
        echo -e "${RED}Error fetching persons${NC}"
        return 1
    fi
    
    local count
    count=$(echo "$response" | jq '.results | length')
    echo -e "${GREEN}Found ${count} persons${NC}\n"
    
    # Output as table
    echo "$response" | jq -r '.results[] | "\u001b[36mID:\u001b[0m \(.id[0:8])... | \u001b[33mDistinct ID:\u001b[0m \(.distinct_ids[0] | .[0:20])... | \u001b[35mCreated:\u001b[0m \(.created_at[0:10])"'
    
    echo -e "\n${BLUE}--- Raw JSON ---${NC}"
    echo "$response" | jq .
}

# Command: cohorts
list_cohorts() {
    echo -e "${BLUE}Fetching cohorts...${NC}"
    local response
    response=$(api_call "/cohorts")
    
    if [[ -z "$response" ]]; then
        echo -e "${RED}Error fetching cohorts${NC}"
        return 1
    fi
    
    local count
    count=$(echo "$response" | jq '.results | length')
    
    if [[ "$count" -eq 0 ]]; then
        echo -e "${YELLOW}No cohorts found in this project${NC}"
        return 0
    fi
    
    echo -e "${GREEN}Found ${count} cohorts${NC}\n"
    
    # Output as table
    echo "$response" | jq -r '.results[] | "\u001b[36mID:\u001b[0m \(.id) | \u001b[33mName:\u001b[0m \(.name) | \u001b[35mCount:\u001b[0m \(.count // "N/A") | \u001b[32mCreated:\u001b[0m \(.created_at[0:10])"'
    
    echo -e "\n${BLUE}--- Raw JSON ---${NC}"
    echo "$response" | jq .
}

# Command: flags
list_flags() {
    echo -e "${BLUE}Fetching feature flags...${NC}"
    local response
    response=$(api_call "/feature_flags")
    
    if [[ -z "$response" ]]; then
        echo -e "${RED}Error fetching feature flags${NC}"
        return 1
    fi
    
    local count
    count=$(echo "$response" | jq '.results | length')
    
    if [[ "$count" -eq 0 ]]; then
        echo -e "${YELLOW}No feature flags found in this project${NC}"
        return 0
    fi
    
    echo -e "${GREEN}Found ${count} feature flags${NC}\n"
    
    # Output as table
    echo "$response" | jq -r '.results[] | "\u001b[36mKey:\u001b[0m \(.key) | \u001b[33mName:\u001b[0m \(.name // "N/A") | \u001b[35mActive:\u001b[0m \(.active) | \u001b[32mCreated:\u001b[0m \(.created_at[0:10])"'
    
    echo -e "\n${BLUE}--- Raw JSON ---${NC}"
    echo "$response" | jq .
}

# Command: recordings
list_recordings() {
    local limit="${1:-10}"
    
    echo -e "${BLUE}Fetching session recordings...${NC}"
    local response
    response=$(api_call "/session_recordings" "limit=${limit}")
    
    if [[ -z "$response" ]]; then
        echo -e "${RED}Error fetching session recordings${NC}"
        return 1
    fi
    
    local count
    count=$(echo "$response" | jq '.results | length')
    
    if [[ "$count" -eq 0 ]]; then
        echo -e "${YELLOW}No session recordings found${NC}"
        return 0
    fi
    
    echo -e "${GREEN}Found ${count} session recordings${NC}\n"
    
    # Output as table
    echo "$response" | jq -r '.results[] | "\u001b[36mID:\u001b[0m \(.id[0:20])... | \u001b[33mDistinct ID:\u001b[0m \(.distinct_id[0:20])... | \u001b[35mStart:\u001b[0m \(.start_time[0:16]) | \u001b[32mDuration:\u001b[0m \(.duration // "N/A")"'
    
    echo -e "\n${BLUE}--- Raw JSON ---${NC}"
    echo "$response" | jq .
}

# Help
show_help() {
    cat << 'EOF'
PostHog Analytics Skill - Query your product analytics data

USAGE:
    !posthog <command> [options]

COMMANDS:
    events [options]        Query latest events
      --limit=N             Limit results (default: 10)
      --after=DATE          Filter events after date (YYYY-MM-DD)
      --event=TYPE          Filter by event type

    insights                List all insights/dashboards
    
    dashboards              List all dashboards

    funnel <id>             Get funnel statistics by ID

    persons [options]       Query persons/users
      --limit=N             Limit results (default: 20)
      --search=TERM         Search by email or property

    cohorts                 List all cohorts

    flags                   List all feature flags

    recordings [options]    List session recordings
      --limit=N             Limit results (default: 10)

    help                    Show this help message

EXAMPLES:
    !posthog events --limit=5
    !posthog events --after=2024-01-01 --event=\$pageview
    !posthog persons --search=user@example.com
    !posthog funnel 12345
    !posthog recordings --limit=5

CONFIGURATION:
    Set these environment variables:
    - POSTHOG_API_KEY       Your PostHog API key
    - POSTHOG_PROJECT_ID    Your project ID (default: 43640)
    - POSTHOG_HOST          PostHog host (default: https://eu.posthog.com)
EOF
}

# Main command dispatcher
main() {
    local cmd="${1:-help}"
    shift || true
    
    case "$cmd" in
        events)
            local limit="10"
            local after=""
            local event_type=""
            
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    --limit=*) limit="${1#*=}" ;;
                    --after=*) after="${1#*=}" ;;
                    --event=*) event_type="${1#*=}" ;;
                    *) echo "Unknown option: $1" ;;
                esac
                shift
            done
            
            query_events "$limit" "$after" "$event_type"
            ;;
            
        insights)
            list_insights
            ;;
            
        dashboards)
            list_dashboards
            ;;
            
        funnel)
            if [[ -z "$1" ]]; then
                echo -e "${RED}Error: Funnel ID required${NC}"
                echo "Usage: !posthog funnel <funnel_id>"
                exit 1
            fi
            get_funnel "$1"
            ;;
            
        persons)
            local limit="20"
            local search=""
            
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    --limit=*) limit="${1#*=}" ;;
                    --search=*) search="${1#*=}" ;;
                    *) echo "Unknown option: $1" ;;
                esac
                shift
            done
            
            query_persons "$limit" "$search"
            ;;
            
        cohorts)
            list_cohorts
            ;;
            
        flags|feature_flags)
            list_flags
            ;;
            
        recordings|sessions)
            local limit="10"
            
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    --limit=*) limit="${1#*=}" ;;
                    *) echo "Unknown option: $1" ;;
                esac
                shift
            done
            
            list_recordings "$limit"
            ;;
            
        help|--help|-h)
            show_help
            ;;
            
        *)
            echo -e "${RED}Unknown command: $cmd${NC}"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
