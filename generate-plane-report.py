#!/usr/bin/env python3
"""Generate daily in-progress tasks report from Plane.so"""

import json
import os
from collections import defaultdict
import urllib.request
import urllib.error

# Member ID to name mapping (from Plane API)
MEMBERS = {
    "5df73cf4-4f4c-467b-b3b3-541988acb939": "Carlo",
    "09c51bd5-11b3-4b75-be5a-3d57274b07c5": "Jake",
    "3227af64-8ea1-4d82-977c-34775096191b": "Alex",
    "22a16ca5-471f-4e28-b47c-defc606700ea": "Matt",
}

PROJECTS = [
    ("d43cf042-98e5-42a6-81aa-2c876bb2a8bd", "spex4less"),
    ("d79f2fb1-4904-4115-95b4-5578defd8dfd", "Showroom Marketing"),
]

PRIORITY_EMOJI = {
    "urgent": "🔴",
    "high": "🟠",
    "medium": "🟡",
    "low": "🟢",
    "none": "⚪",
}

def api_call(url):
    """Make authenticated API request"""
    api_key = os.environ.get("PLANE_API_KEY")
    req = urllib.request.Request(
        url,
        headers={"X-API-Key": api_key}
    )
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"API Error: {e}", file=os.sys.stderr)
        return None

def get_in_progress_state(proj_id):
    """Get In Progress state ID for project"""
    url = f"https://api.plane.so/api/v1/workspaces/spex4less/projects/{proj_id}/states/"
    data = api_call(url)
    if data and "results" in data:
        for state in data["results"]:
            if state["name"] == "In Progress":
                return state["id"]
    return None

def get_in_progress_issues(proj_id, state_id):
    """Get all in-progress (not completed) issues"""
    url = f"https://api.plane.so/api/v1/workspaces/spex4less/projects/{proj_id}/issues/?state={state_id}"
    data = api_call(url)
    if data and "results" in data:
        return [t for t in data["results"] if t.get("completed_at") is None]
    return []

def generate_report():
    all_tasks = []
    
    for proj_id, proj_name in PROJECTS:
        state_id = get_in_progress_state(proj_id)
        if state_id:
            tasks = get_in_progress_issues(proj_id, state_id)
            for task in tasks:
                task["project_name"] = proj_name
                all_tasks.append(task)
    
    # Group by assignee
    by_assignee = defaultdict(list)
    unassigned = []
    
    for task in all_tasks:
        assignees = task.get("assignees", [])
        if assignees:
            for aid in assignees:
                by_assignee[aid].append(task)
        else:
            unassigned.append(task)
    
    # Format report
    lines = []
    lines.append("**📋 Good morning! Here's today's in-progress tasks by assignee:**")
    lines.append("")
    lines.append(f"**Total: {len(all_tasks)} in-progress task{'s' if len(all_tasks) != 1 else ''}**")
    lines.append("")
    
    # Sort assignees by name
    sorted_assignees = sorted(by_assignee.keys(), key=lambda x: MEMBERS.get(x, x).lower())
    
    for aid in sorted_assignees:
        name = MEMBERS.get(aid, aid[:8])
        tasks = by_assignee[aid]
        lines.append(f"**👤 {name}** — {len(tasks)} task{'s' if len(tasks) > 1 else ''}")
        for t in sorted(tasks, key=lambda x: x["name"]):
            prio = PRIORITY_EMOJI.get(t.get("priority", "none"), "⚪")
            lines.append(f"  {prio} **{t['project_name']}** — {t['name']}")
        lines.append("")
    
    if unassigned:
        lines.append(f"**👤 Unassigned** — {len(unassigned)} task{'s' if len(unassigned) > 1 else ''}")
        for t in sorted(unassigned, key=lambda x: x["name"]):
            prio = PRIORITY_EMOJI.get(t.get("priority", "none"), "⚪")
            lines.append(f"  {prio} **{t['project_name']}** — {t['name']}")
        lines.append("")
    
    lines.append("---")
    lines.append("*Priority: 🔴 Urgent | 🟠 High | 🟡 Medium | 🟢 Low | ⚪ None*")
    
    return "\n".join(lines)

if __name__ == "__main__":
    print(generate_report())
