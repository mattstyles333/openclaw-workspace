# ROF v2.0 - Hybrid Parallel Processing Framework
## Multi-Model Report Orchestration for OpenClaw

### Philosophy
**Truth > Comfort. Signal > Noise. Wisdom > Information.**

Every report runs through parallel models (Kimi + DeepSeek v3.2), cross-validated and synthesized for maximum insight quality.

---

## The Hybrid Process

### Phase 0: Clarification Checkpoint (2-3 min)
**Model:** Kimi (conversational, quick context building)

**My role:** Ask targeted questions until I understand:
- What decision this informs
- What "good" looks like  
- Constraints (time/data/scope)
- Your gut hypothesis (so I can validate or challenge it)

**Concise update format:**
```
🎯 Goal: [1-sentence summary]
❓ Clarifying: [what I need to know]
⏱️  ETA: [X minutes]
```

---

### Phase 1: Parallel Research Spawning (5-10 min)
**Spawn 2-3 sub-agents simultaneously:**

| Agent | Model | Task | Output |
|-------|-------|------|--------|
| **Researcher-K** | Kimi-k2.5 | Deep web research, pattern recognition | Research memo with sources |
| **Researcher-D** | openrouter/deepseek/deepseek-v3.2 | Alternative angle research, blind spot detection | Contrarian research memo |
| **Data-Miner** | Kimi | Query your systems (PostHog, DB, Cloudflare) | Internal data insights |

**Concise update:**
```
🔍 Spawning [N] research agents...
📊 Querying: [PostHog/DB/etc.]
⏱️  Research ETA: [X min]
```

---

### Phase 2: Synthesis & Cross-Validation (5 min)
**I analyze both research outputs:**

**What I look for:**
- ✅ Agreement between models (high confidence)
- ⚠️  Disagreement (requires deeper investigation)
- 🔍 Gaps (neither model covered)
- 💡 Synthesis (insights from combining both)

**Concise update:**
```
📊 Research complete
✅ Consensus: [X points]
⚠️  Conflicts: [Y points - investigating]
💡 Emerging insight: [preview]
```

---

### Phase 3: Devil's Advocate Spawn (3-5 min)
**Spawn dedicated skeptic agent:**

| Agent | Model | Task |
|-------|-------|------|
| **Skeptic** | openrouter/deepseek/deepseek-v3.2 | Tear apart our findings, find flaws, question assumptions |

**Prompt:** "You are a ruthless skeptic. Rip apart these findings. What's wrong? What are we missing? What would make this report misleading?"

**Concise update:**
```
😈 Devil's advocate engaged...
🎯 Attacking: [key assumptions]
```

---

### Phase 4: KPI & Framework Design (3-5 min)
**I design the measurement framework:**

What metrics actually matter for this goal?
- Leading indicators (predictive)
- Lagging indicators (confirmatory)
- Benchmarks (good/bad ranges)

**Concise update:**
```
📈 KPI Framework:
   Critical: [metric 1], [metric 2]
   Benchmark: [X] = good, [Y] = bad
```

---

### Phase 5: Draft Construction (5-10 min)
**I write the report using synthesized insights:**

Structure:
```
🎯 TL;DR (situation summary — no single recommendation yet)
📊 Executive Summary (3-5 bullets)
📈 Key Metrics (table with benchmarks)
🔍 Deep Dive (synthesis of both models)
⚠️  Risks & Caveats (from devil's advocate)
🎛️ Decision Framework (3-4 strategic options with trade-offs)
📚 Sources & Confidence (High/Med/Low per claim)
```

**🎛️ Decision Framework Format:**
Present 3-4 distinct options with clear trade-offs:

| Option | Strategy | Pros | Cons | Best If... | Confidence |
|--------|----------|------|------|------------|------------|
| **A: Aggressive** | Full commitment, fast execution | Max upside, first-mover | High risk, resource drain | Market window is narrow | Medium |
| **B: Balanced** | Phased rollout, test & validate | Risk-managed, learnings | Slower, moderate upside | Uncertainty is moderate | High |
| **C: Conservative** | Minimal investment, wait & see | Low risk, preserves optionality | Missed opportunity, passive | High uncertainty, limited resources | High |
| **D: Alternative** | Different approach entirely | Unique angle, differentiation | Unproven, execution complexity | Standard paths seem wrong | Low-Medium |

**For each option include:**
- Resource requirements (time/$/people)
- Key assumptions that must hold
- Go/no-go triggers
- Estimated impact (best/realistic/worst case)

**Final section:**
```
🎯 My Suggested Path: [Option X] — but here's why the others matter...
```
(Explain which option I'd lean toward AND under what conditions you'd switch to another)

**Concise update:**
```
📝 Draft complete
✅ Confidence: [High/Med/Low]
💡 Key rec: [preview]
```

---

### Phase 6: Your Review & Decision (2-5 min)
**I present the decision framework, you choose:**

Questions I'll ask:
- "Which option resonates with your risk tolerance?"
- "What would need to be true for you to pick Option A vs B?"
- "What data would change your mind?"
- "Should I deep-dive on any specific option?"
- "Do you want me to model a hybrid approach?"

**If you want me to decide:** I'll pick one with clear conditional triggers
**If you want to decide:** I'll pressure-test your choice against the others

**Concise update:**
```
👀 Decision framework ready
🎛️ Options: A/B/C/D presented
❓ Which path feels right? Or want me to pick?
```

---

## Update Cadence

**Super concise progress updates every 2-3 minutes:**

| Phase | Update Format |
|-------|---------------|
| 0 | "🎯 Goal: X / ❓ Need: Y / ⏱️  2 min" |
| 1 | "🔍 Spawned 3 agents / ⏱️  5 min" |
| 2 | "📊 Consensus: X / ⚠️  Conflicts: Y" |
| 3 | "😈 Devil's advocate: [key challenge]" |
| 4 | "📈 KPIs: [metric 1], [metric 2]" |
| 5 | "📝 Draft ready / Confidence: High" |
| 6 | "👀 Review ready / ❓ [questions]" |

---

## Model Roles Summary

| Model | Best For | Why |
|-------|----------|-----|
| **Kimi-k2.5** (Primary) | Synthesis, structure, actionable insights | Excellent at connecting dots and presenting clearly |
| **openrouter/deepseek/deepseek-v3.2** | Deep analysis, devil's advocate, edge case detection | Better at finding what others miss, challenging assumptions |
| **Both (Parallel)** | Cross-validation, confidence building | Agreement = high confidence, disagreement = investigate |

---

## Confidence Levels

| Level | Criteria | Label |
|-------|----------|-------|
| **High** | Both models agree + 3+ sources + your data supports | "✅ High Confidence" |
| **Medium** | Models mostly agree + some gaps in data | "⚠️  Medium Confidence" |
| **Low** | Models disagree OR limited data OR mostly speculation | "❓ Low Confidence - Needs More Research" |

---

## Example: "Should We Expand to EU?"

**Phase 0 (30 sec):**
```
🎯 Goal: EU market expansion decision
❓ Clarifying: Which countries? Timeline? Budget?
⏱️  2 min
```

**Phase 1 (7 min):**
```
🔍 Spawning 3 agents...
📊 Querying: PostHog EU traffic, Cloudflare data
⏱️  7 min
```

**Phase 2 (4 min):**
```
📊 Research complete
✅ Consensus: Germany strong potential, UK saturated
⚠️  Conflicts: Shipping costs (Kimi says high, DeepSeek says manageable)
💡 Emerging: Focus on DE/FR, skip UK initially
```

**Phase 3 (3 min):**
```
😈 Devil's advocate:
   - "Brexit regulations could change"
   - "Your current US CAC is $X, EU might be $Y"
   - "What if currency fluctuates 20%?"
```

**Phase 4 (3 min):**
```
📈 KPI Framework:
   Critical: EU traffic conversion, shipping cost %, CAC
   Benchmark: Conv >2%, Ship <15% of order, CAC <$Z
```

**Phase 5 (8 min):**
```
📝 Draft complete
✅ Confidence: High (most claims), Medium (shipping costs)
🎛️ Decision Framework ready:
   Option A: Full EU launch (aggressive) — €X, 6 months
   Option B: Germany-only pilot (balanced) — €Y, 3 months
   Option C: Wait for regulatory clarity (conservative)
   Option D: UK-first via partner (alternative)
💡 My lean: Option B, but switch to A if pilot hits Z% conversion
```

**Phase 6 (ongoing):**
```
👀 Review ready
🎛️ Decision framework presented
❓ Which option fits your risk tolerance? Want me to model a hybrid?
```

---

## Next Step

**Test this framework on your next report request.** 

Just say: *"ROF this: [your question]"* and I'll activate the full process.

Or tell me to refine anything above first! 🚀
