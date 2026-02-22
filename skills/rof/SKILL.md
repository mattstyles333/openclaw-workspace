---
name: rof
description: "Report Orchestration Framework (ROF) - A structured 6-phase process for producing high-quality, multi-perspective research reports with parallel model processing. Use when the user triggers with 'ROF:' prefix or asks for a detailed report/analysis requiring research, synthesis, and actionable recommendations. Triggers include 'ROF: [topic]', 'run ROF on [topic]', or requests for comprehensive analysis with devil's advocate review and multiple strategic options."
---

# Report Orchestration Framework (ROF)

A hybrid, parallel-processing research framework for producing truth-first, actionable reports.

## Core Values

- **Truth > Comfort** - Never sugarcoat; say what the data shows
- **Distilled Knowledge > Data Dumps** - Separate signal from noise
- **Wisdom > Information** - Focus on what to do, not just what happened

## Trigger Pattern

When user says: `ROF: [topic]` or `run ROF on [topic]`
→ Activate full 6-phase framework immediately

## The 6-Phase Process

### Phase 1: Goal & Context (2-3 min)

**Purpose:** Lock in success criteria before research begins.

**Actions:**
1. Acknowledge ROF activation
2. Ask clarifying questions:
   - What decision are you trying to make?
   - What would make this report a success?
   - Any constraints (budget, timeline, must-haves)?
   - Speed vs depth preference (15-min quick vs 1-hour deep)?
   - Output format preference (data-heavy tables / narrative / bullets)?
3. Confirm understanding with concise summary

**Update Format:**
```
🎯 Goal: [1-line summary]
❓ Need: [what you're trying to decide]
⏱️ 2 min
```

### Phase 2: Parallel Research (10-20 min)

**Purpose:** Multi-source intelligence gathering with dual-model validation.

**Models:**
- **Primary:** Kimi-k2.5 (synthesis, structure, actionable insights)
- **Secondary:** openrouter/deepseek/deepseek-v3.2 (deep analysis, blind spots)

**Actions:**
1. Spawn sub-agents for parallel research:
   ```
   sessions_spawn with:
   - agentId: default or reasoning
   - model: openrouter/deepseek/deepseek-v3.2
   - task: [specific research query]
   ```
2. Run web searches (multiple angles)
3. Query internal data sources if available (PostHog, DB, APIs)
4. Cross-reference 3+ sources before stating facts
5. Map stakeholder perspectives (competitor view, skeptic view, expert view)

**Update Format (every 2-3 min):**
```
🔍 Spawned 3 agents | 📊 Querying [source]
📊 Consensus: X | ⚠️ Conflicts: Y | 💡 Emerging: Z
```

### Phase 3: Sequential Thinking (10-15 min)

**Purpose:** Structure insights into actionable intelligence.

**Actions:**
1. Break topic into sub-questions
2. Identify KPIs and benchmarks
3. Categorize findings:
   - **Critical** - Must know for decision
   - **Supporting** - Adds context
   - **Interesting** - Nice to know
   - **Assumptions** - Flag for validation

**Update Format:**
```
🔍 Key Findings: [number]
📊 Metrics Identified: [list]
⏱️ 5 min
```

### Phase 4: Devil's Advocate (5-10 min)

**Purpose:** Challenge findings to surface blind spots.

**Actions:**
1. Ask: "What if I'm wrong about each major finding?"
2. Run bias check:
   - Confirmation bias (seeking confirming evidence)
   - Recency bias (overweighting latest info)
   - Availability bias (overweighting memorable info)
3. Present multiple scenarios: best case / most likely / worst case
4. Flag disagreements between models for deeper investigation

**Update Format:**
```
⚠️ Devil's Advocate: [key challenge]
🎯 Scenario Analysis: best/most likely/worst
⏱️ 3 min
```

### Phase 5: Report Construction (10-15 min)

**Purpose:** Produce clear, actionable output.

**Structure:**
```markdown
# 🎯 [Topic] - ROF Report

## TL;DR
[2-3 sentence summary + clear recommendation]

## Executive Summary
| Option | Best For | [Key Metric] | Verdict |
|--------|----------|--------------|---------|
| [A]    | [use case]| [value]     | [emoji] |
| [B]    | [use case]| [value]     | [emoji] |
| [C]    | [use case]| [value]     | [emoji] |

## Key Metrics That Matter
| Criteria | Priority | Option A | Option B | Option C |
|----------|----------|----------|----------|----------|
| [metric] | ⭐⭐⭐⭐⭐ | [rating] | [rating] | [rating] |

## Deep Dive
### [Option A] (Confidence: [HIGH/MEDIUM/LOW])
**Why it works:**
- [point 1]
- [point 2]

**The catch:**
- [risk/limitation]

### [Option B]...

## ⚠️ Devil's Advocate: What Could Go Wrong
1. [Challenge to finding 1]
2. [Challenge to finding 2]

## 💡 Recommendations
**Option [X]:** [Name]
- **Do this if:** [conditions]
- **Cost/Impact:** [summary]
- **Action:** [next step]

**Option [Y]:** [Name]
- ...

## 📚 Sources & Confidence
| Claim | Confidence | Source |
|-------|------------|--------|
| [claim] | ✅ High / ⚠️ Medium / ❓ Low | [source] |
```

**Confidence Labels (on every claim):**
- ✅ **High** - Both models agree + 3+ independent sources
- ⚠️ **Medium** - Some gaps or single-source
- ❓ **Low** - Disagreement between models or speculation

### Phase 6: Review & Validation (2-3 min)

**Purpose:** Quality assurance before delivery.

**Checklist:**
- [ ] Did I answer the original question?
- [ ] Is it actionable (not just informational)?
- [ ] Are all major claims backed by evidence?
- [ ] Did I include multiple options (not cut-and-dry)?
- [ ] Are confidence labels applied?

**Final Prompt to User:**
```
Your call: [specific decision options]
Need deeper analysis on any section?
```

## Multi-Option Decision Framework

**Never present a single recommendation.** Always offer 3-4 strategic options:

| Option Type | Description |
|-------------|-------------|
| **Conservative** | Safe choice, proven, lower risk/return |
| **Balanced** | Middle ground, best expected value |
| **Aggressive** | Higher risk, higher potential payoff |
| **Alternative** | Outside-the-box option most people miss |

## Progress Updates

Keep user informed with **super concise updates** every 2-3 minutes:

```
🎯 Goal: X | ❓ Need: Y | ⏱️ 2 min
🔍 Spawned 3 agents | 📊 Querying PostHog
📊 Consensus: X | ⚠️ Conflicts: Y | 💡 Emerging: Z
```

## Sub-Agent Spawn Pattern

When spawning parallel research agents:

```
sessions_spawn:
  task: "Research [specific angle]. Focus on: [metrics/sources]. Return: [format]."
  model: "openrouter/deepseek/deepseek-v3.2"
  runTimeoutSeconds: 300
```

## Reference Materials

For detailed examples and templates, see [references/examples.md](references/examples.md).
