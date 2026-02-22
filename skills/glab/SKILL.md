---
name: glab
description: GitLab CLI skill for interacting with GitLab repositories, merge requests, issues, pipelines, and more using the glab command-line tool.
allowed-tools: Bash(glab:*)
---

# GitLab CLI (glab) Skill

This skill provides access to the GitLab CLI (`glab`) for managing GitLab repositories, merge requests, issues, pipelines, and more.

## Prerequisites

- `glab` must be installed (`/usr/local/bin/glab`)
- `GITLAB_TOKEN` environment variable must be set for gitlab.s4l.link

## Authentication

The token is configured via environment variable (already set in `~/.bashrc` and `~/.profile`):

```bash
export GITLAB_TOKEN="glpat-j0lt9f64v3Fk5F7tCgxLOG86MQp1OjIH.01.0w1cczmtr"
```

To use glab, always include the hostname flag for gitlab.s4l.link:
```bash
glab <command> --hostname gitlab.s4l.link
```

To check authentication status:
```bash
glab auth status
```

## Common Commands

### Repository Operations

```bash
# List all projects
glab api /projects --hostname gitlab.s4l.link

# Clone a repository
glab repo clone owner/repo

# View repository details
glab repo view --hostname gitlab.s4l.link
```

### Merge Requests

```bash
# List merge requests for a project
glab mr list --hostname gitlab.s4l.link -R matt/gtin-scanner

# View a specific MR
glab mr view 123 --hostname gitlab.s4l.link

# Create a merge request
glab mr create --title "My MR" --description "Description" --hostname gitlab.s4l.link
```

### Issues

```bash
# List issues
glab issue list --hostname gitlab.s4l.link

# View an issue
glab issue view 123 --hostname gitlab.s4l.link

# Create an issue
glab issue create --title "Bug report" --description "Description" --hostname gitlab.s4l.link
```

### Pipelines & CI

```bash
# List pipelines
glab pipeline list --hostname gitlab.s4l.link

# View CI jobs
glab ci list --hostname gitlab.s4l.link

# View CI job logs
glab ci trace --hostname gitlab.s4l.link
```

### API Commands

```bash
# Make raw API calls
glab api /user --hostname gitlab.s4l.link
glab api /projects --hostname gitlab.s4l.link
```

## Tips

- **Always use `--hostname gitlab.s4l.link`** for commands targeting your self-hosted GitLab
- Use `--output=json` for programmatic output
- The CLI respects the current git repository context by default (when run from within a repo)

## Self-Hosted GitLab Note

For self-hosted GitLab instances like gitlab.s4l.link, glab requires:
1. The `GITLAB_TOKEN` environment variable set
2. The `--hostname gitlab.s4l.link` flag on each command (unless run from within a git repo cloned from that host)
