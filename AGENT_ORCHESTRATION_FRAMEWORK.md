# Report Orchestration Framework (ROF)
## OpenClaw Agent Process for High-Quality Reports

### Overview
This framework ensures every report request follows a systematic, thorough process that maximizes insight quality and actionable value.

---

## Phase 1: Goal Identification & Context Gathering (5-10 min)

### 1.1 Clarify the Request
**Ask clarifying questions until you understand:**
- What decision will this report inform?
- Who is the audience? (You, team, investors, customers?)
- What's the time horizon? (Historical analysis, current state, future prediction?)
- What format do you prefer? (Bullet points, narrative, tables, visualizations?)

**Questions to ask:**
- "What problem are you trying to solve with this report?"
- "What would make this report a 'success' for you?"
- "Do you have any existing data/benchmarks to compare against?"
- "What's your gut feeling on this - are you looking to validate or challenge it?"

### 1.2 Constraint Identification
**Understand limitations:**
- Budget/time constraints
- Data availability
- Scope boundaries
- Confidentiality requirements

---

## Phase 2: Research & Discovery (10-20 min)

### 2.1 Multi-Source Intelligence Gathering
**Use multiple tools to gather context:**

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `web_search` | Current trends, benchmarks, industry standards | Always start here |
| `web_fetch` | Deep dive into specific sources | For authoritative content |
| `memory_search` | Your historical context/preferences | Check MEMORY.md first |
| `sessions_history` | Previous related work | Avoid duplication |
| Database queries | Your specific data (PostHog, email_metrics, etc.) | For personalized insights |
| API calls (Cloudflare, PostHog, etc.) | Real-time data from your systems | When fresh data matters |

### 2.2 Information Triangulation
**Cross-reference findings:**
- Compare 3+ sources before stating a fact
- Note conflicting information (present both sides)
- Identify consensus vs. speculation

### 2.3 Stakeholder Perspective Mapping
**Consider multiple viewpoints:**
- What would your competitors say?
- What would a skeptic say?
- What would an expert in this field say?

---

## Phase 3: Sequential Thinking & Framework Development (10-15 min)

### 3.1 Problem Decomposition
**Break down the request:**
```
Main Question
├── Sub-question 1
│   ├── Data needed: ___
│   └── Analysis method: ___
├── Sub-question 2
│   ├── Data needed: ___
│   └── Analysis method: ___
└── Sub-question 3
    ├── Data needed: ___
    └── Analysis method: ___
```

### 3.2 KPI & Metric Identification
**Define what success looks like:**
- What metrics actually matter for this goal?
- What's the benchmark/good/bad range?
- Leading vs. lagging indicators?

**Create a measurement framework:**
| Metric | Why It Matters | Target | Current | Source |
|--------|----------------|--------|---------|--------|
| | | | | |

### 3.3 Insight Hierarchy
**Structure findings by importance:**
1. **Critical Insights** (must-know, decision-driving)
2. **Supporting Evidence** (context, validation)
3. **Interesting but Non-Essential** (nice-to-know)
4. **Assumptions & Caveats** (limitations, risks)

---

## Phase 4: Devil's Advocate & Stress Testing (5-10 min)

### 4.1 Challenge Your Own Findings
**Ask the contrarian questions:**
- "What if I'm wrong about...?"
- "What data would disprove this conclusion?"
- "What's the strongest argument against this recommendation?"
- "Where are the gaps in my knowledge?"

### 4.2 Bias Check
**Identify potential blind spots:**
- Confirmation bias (did I only search for supporting evidence?)
- Recency bias (am I over-weighting recent events?)
- Availability bias (am I over-weighting easily accessible data?)
- Sunk cost bias (am I defending previous recommendations?)

### 4.3 Alternative Scenarios
**Present multiple futures:**
- Best case scenario
- Most likely scenario
- Worst case scenario
- "Black swan" scenario (low probability, high impact)

---

## Phase 5: Report Construction (10-15 min)

### 5.1 Executive Summary (TL;DR)
**Lead with the answer:**
- 2-3 sentence summary of key findings
- Clear recommendation/action item
- Confidence level (High/Medium/Low)

### 5.2 Structured Body
**Use consistent formatting:**

```markdown
## 🎯 Executive Summary
[2-3 sentences + recommendation]

## 📊 Key Findings
| Finding | Evidence | Impact |
|---------|----------|--------|
| | | |

## 📈 Metrics That Matter
[Tables/charts with benchmarks]

## 🔍 Deep Dive
[Detailed analysis by section]

## ⚠️ Risks & Caveats
[What could go wrong]

## 💡 Recommendations
[Prioritized action items]

## 📚 Sources & Methodology
[How we got here]
```

### 5.3 Actionable Outputs
**Every report should include:**
- ✅ Specific, actionable recommendations
- ✅ Clear next steps (who does what by when)
- ✅ Metrics to track going forward
- ✅ Red flags to watch for

---

## Phase 6: Review & Validation (5 min)

### 6.1 Quality Checklist
Before delivering, verify:
- [ ] Did I answer the original question?
- [ ] Is every claim supported by evidence?
- [ ] Did I include both pros and cons?
- [ ] Are the recommendations actionable?
- [ ] Would a skeptic find this convincing?
- [ ] Is the formatting clear and scannable?

### 6.2 Confidence Calibration
**Label your certainty:**
- **High Confidence:** Multiple reliable sources, clear data
- **Medium Confidence:** Some assumptions, limited data
- **Low Confidence:** Mostly speculation, need more research

---

## Implementation in OpenClaw

### Option 1: Automated Checklist
I can create a `sessions_spawn` sub-agent that follows this framework:

```bash
# Spawn a dedicated report-writing agent
sessions_spawn(
  task="Generate report following ROF framework",
  context={
    "phase": "research",
    "goal": "[your request]",
    "constraints": "[time/budget/scope]"
  }
)
```

### Option 2: Interactive Process
We work through each phase together, with me asking questions at each step.

### Option 3: Hybrid Approach
Quick clarification → I spawn sub-agents for research → We review together → Final report

---

## Example Workflow

**Your Request:** "Should we expand into European markets?"

**Phase 1:**
- Which countries? (UK, Germany, France - got it)
- What's your current US performance? (Need to check)
- Timeline? (Q3 2026 - noted)

**Phase 2:**
- Search: "European e-commerce market 2026"
- Search: "UK eyewear market size"
- Query: Your PostHog data for international traffic
- Check: Cloudflare data on EU visitors

**Phase 3:**
- Decompose: Market size, competition, logistics, regulations
- KPIs: TAM, CAC vs US, shipping costs, conversion rates

**Phase 4:**
- Devil's advocate: "What if Brexit regulations change?"
- Bias check: "Am I over-optimistic about EU demand?"

**Phase 5:**
- Construct report with data tables, risk matrix, recommendations

**Phase 6:**
- Quality check: Did I answer the expansion question? Yes.

---

## Your Preferences

Let's customize this for you:

1. **Speed vs. Depth:** Do you prefer quick insights (15 min) or comprehensive analysis (1 hour)?

2. **Format:** Do you like bullet points, narrative, or data-heavy tables?

3. **Tone:** Formal business report or casual conversation?

4. **Follow-up:** Should reports include "next steps" or just information?

5. **Devil's Advocate:** Always include contrarian view, or only when confidence is low?

Let me know and I'll implement this framework starting with your next request!
