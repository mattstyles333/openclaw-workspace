---
name: qa-tester
description: "Comprehensive QA testing framework for frontend features using OpenClaw browser tool. Tests desktop and mobile flows, finds bugs and CRO issues through systematic testing. Use when user says 'QA test', 'test this feature', 'run QA on', or requests thorough frontend testing. Executes from main session using browser tool for reliability."
---

# QA Tester Framework (Browser Tool)

Systematic frontend testing using **OpenClaw browser tool** directly from main session. Sequential testing for maximum reliability.

## Core Philosophy

- **Test like a customer** — follow real user flows, not just functionality
- **Find CRO killers** — anything that hurts conversion is a bug
- **Desktop + Mobile** — responsive issues are revenue issues
- **Screenshots as evidence** — every bug gets a screenshot
- **Sequential execution** — use browser tool directly from main session (most reliable)
- **DeepSeek model** — uses `openrouter/deepseek/deepseek-v3.2` for analysis when needed

## Trigger Patterns

- "QA test [feature/page]"
- "Test this feature"
- "Run QA on [URL/feature]"
- "Find bugs in [area]"

## Testing Approach

**No subagents.** Use browser tool directly from main session for:
- Direct control over browser state
- Immediate screenshot capture
- Reliable element interaction
- No subagent timeout issues

## Test Types

### 1. Happy Path (Core Flow)
Browse → Product → Cart → Checkout → Confirmation

### 2. Mobile Experience
Mobile viewport, touch interactions, responsive issues

### 3. CRO Audit
Conversion killers, friction points, trust signals

### 4. Edge Cases
Errors, validation, race conditions

## Execution Workflow

### Phase 1: Setup (2 min)

1. Confirm URL and scope
2. auth credentials if needed
3. Define test sequence

### Phase 2: Sequential Testing (15-20 min)

Run tests one by one using browser tool:

```python
# Test 1: Happy Path Desktop
browser: {
  "action": "open",
  "targetUrl": "https://example.com"
}
browser: {
  "action": "screenshot"
}
# ... more steps ...

# Test 2: Mobile Viewport  
browser: {
  "action": "open",
  "targetUrl": "https://example.com",
  "viewport": {"width": 390, "height": 844}
}
# ... more steps ...

# Test 3: CRO Audit
# Analyze current page for conversion issues

# Test 4: Edge Cases
# Test form validation, errors, etc.
```

### Phase 3: Synthesize Report (5 min)

Compile findings into structured QA report.

## Test Scripts

### Test 1: Happy Path Desktop

```python
# Step 1: Navigate to homepage
browser: {
  "action": "open",
  "targetUrl": "[URL]"
}
browser: {
  "action": "screenshot",
  "fullPage": true
}

# Step 2: Navigate to category
browser: {
  "action": "act",
  "request": {"kind": "click", "ref": "[Category Name]"}
}
browser: {
  "action": "wait",
  "timeMs": 2000
}
browser: {
  "action": "screenshot",
  "fullPage": true
}

# Step 3: Click first product
browser: {
  "action": "act",
  "request": {"kind": "click", "selector": ".product-item:first-child a"}
}
browser: {
  "action": "wait",
  "timeMs": 2000
}
browser: {
  "action": "screenshot",
  "fullPage": true
}

# Step 4: Add to cart
browser: {
  "action": "act",
  "request": {"kind": "click", "ref": "Add to Cart"}
}
browser: {
  "action": "wait",
  "timeMs": 2000
}
browser: {
  "action": "screenshot"
}

# Step 5: Go to cart
browser: {
  "action": "act",
  "request": {"kind": "click", "ref": "Cart"}
}
browser: {
  "action": "screenshot",
  "fullPage": true
}

# Step 6: Checkout flow
browser: {
  "action": "act",
  "request": {"kind": "click", "ref": "Checkout"}
}
browser: {
  "action": "wait",
  "timeMs": 3000
}
browser: {
  "action": "screenshot",
  "fullPage": true
}

# Fill shipping info if needed...

# Step 7: Order confirmation
browser: {
  "action": "wait",
  "timeMs": 2000
}
browser: {
  "action": "screenshot",
  "fullPage": true
}
```

### Test 2: Mobile Viewport

```python
# Navigate with mobile viewport
browser: {
  "action": "open",
  "targetUrl": "[URL]",
  "viewport": {"width": 390, "height": 844}
}
browser: {
  "action": "screenshot",
  "fullPage": true
}

# Test hamburger menu
browser: {
  "action": "act",
  "request": {"kind": "click", "ref": "☰"}
}
browser: {
  "action": "wait",
  "timeMs": 1000
}
browser: {
  "action": "screenshot"
}

# Test touch targets...
# Test mobile checkout...
```

### Test 3: CRO Audit

While on checkout page, analyze:

| Check | What to Look For |
|-------|------------------|
| Load Speed | Page load time |
| Form Fields | Count input fields |
| Trust Signals | Security badges visible? |
| Progress Indicator | Shows checkout steps? |
| Error Messages | Clear and helpful? |
| Hidden Fees | Any surprise costs? |
| Exit Links | Links away from checkout? |

```python
# Screenshot for analysis
browser: {
  "action": "screenshot",
  "fullPage": true
}

# Get page state
browser: {
  "action": "snapshot",
  "compact": false
}
```

### Test 4: Edge Cases

```python
# Test 1: Empty form submission
browser: {
  "action": "act",
  "request": {"kind": "click", "ref": "Submit"}
}
browser: {
  "action": "screenshot"
}

# Test 2: Invalid email
browser: {
  "action": "act",
  "request": {"kind": "fill", "fields": [{"name": "email", "value": "invalid-email"}]}
}
browser: {
  "action": "act",
  "request": {"kind": "click", "ref": "Submit"}
}
browser: {
  "action": "screenshot"
}

# Test 3: Back navigation during checkout
browser: {
  "action": "act",
  "request": {"kind": "press", "key": "Alt+Left"}
}
browser: {
  "action": "screenshot"
}
```

## CRO-Focused Checks

Every test validates:

| Check | Target | Impact |
|-------|--------|--------|
| Load Speed | < 3s | Critical |
| Mobile Friction | No zoom required | High |
| Form Abandonment | < 10 fields | High |
| Trust Signals | Security badges visible | Critical |
| CTA Clarity | One clear primary action | High |
| Price Shock | No hidden fees | Critical |
| Error Handling | Helpful messages | High |
| Exit Opportunities | No distracting links | Medium |

## Output Format: QA Report

```markdown
# QA Test Report: [Feature/Page]

**Date:** [Date]
**URL:** [Tested URL]
**Test Type:** [Happy Path / Mobile / CRO / Edge Cases]

## Executive Summary
| Metric | Result |
|--------|--------|
| Tests Passed | X/Y |
| Critical Bugs | X |
| CRO Issues | X |
| Mobile Issues | X |
| **Verdict** | 🟢 Ship / 🟡 Fix / 🔴 Block |

## Critical Issues
| # | Issue | Impact | Screenshot |
|---|-------|--------|------------|
| 1 | [Description] | [Crash/Bug] | [link] |

## CRO Issues
| # | Issue | Impact | Recommendation |
|---|-------|--------|----------------|
| 1 | [Description] | [High/Med/Low] | [Fix suggestion] |

## Mobile Issues
| # | Issue | Viewport | Screenshot |
|---|-------|----------|------------|
| 1 | [Description] | 390x844 | [link] |

## Screenshots
[All screenshots with descriptions]

## Recommendations
1. [Priority action]
2. [Secondary action]
```

## Cost & Time

| Test Type | Est. Time | Notes |
|-----------|-----------|-------|
| Happy Path | 5-8 min | 7-10 screenshots |
| Mobile | 5-8 min | 5-8 screenshots |
| CRO Audit | 3-5 min | Analysis + screenshots |
| Edge Cases | 5-10 min | Multiple scenarios |
| **Full Suite** | **20-30 min** | Sequential execution |

## Alternative: Quick QA Check

For rapid feedback:

```
Quick QA: Check [URL] for:
- Page loads correctly
- No console errors
- Mobile responsive
- Forms work
```

5-minute