#!/bin/bash
# Daily Plane.so In-Progress Tasks Report Generator

WORKSPACE="spex4less"
PROJECTS=(
  "d43cf042-98e5-42a6-81aa-2c876bb2a8bd:spex4less"
  "d79f2fb1-4904-4115-95b4-5578defd8dfd:Showroom Marketing"
)

echo "**📋 Good morning! Here's today's in-progress tasks by assignee:**"
echo ""

TOTAL=0

# For each project, fetch in-progress tasks
for proj in "${PROJECTS[@]}"; do
  IFS=':' read -r proj_id proj_name <<< "$proj"
  
  # Get states for this project
  STATES=$(curl -s -H "X-API-Key: $PLANE_API_KEY" \
    "https://api.plane.so/api/v1/workspaces/$WORKSPACE/projects/$proj_id/states/" | jq -r '.results[] | select(.name=="In Progress") | .id')
  
  for state_id in $STATES; do
    # Get issues in this state
    curl -s -H "X-API-Key: $PLANE_API_KEY" \
      "https://api.plane.so/api/v1/workspaces/$WORKSPACE/projects/$proj_id/issues/?state=$state_id" | \
      jq -r --arg proj "$proj_name" '.results[] | select(.completed_at==null) | "\(.id)|\(.name)|\(.priority)|\(.assignees | join(","))|\($proj)"'
  done
done | sort -t'|' -k4
