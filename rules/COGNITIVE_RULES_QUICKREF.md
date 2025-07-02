# Cognitive Rules Quick Reference Guide

## The Six Cognitive Enhancement Rules

### 🧠 102-wildcard-brainstorm
**Purpose**: Inject controlled randomness to break cognitive patterns  
**When to Use**: Open-ended problems, creative blocks, initial ideation  
**Key Features**:
- Temperature increase (0.9)
- Domain crossing mandatory
- 5-10 diverse options minimum
- Explicit "wildcard" labeling

**Example Prompt**: "Apply wildcard-brainstorm: How might we improve user onboarding?"

---

### 📐 103-divergence-convergence  
**Purpose**: Orchestrate two-phase problem-solving (explore → synthesize)  
**When to Use**: Complex decisions, architecture design, strategy development  
**Key Features**:
- Explicit DIVERGENCE/CONVERGENCE phases
- 40/60 time split
- Invokes other rules as subroutines
- State machine implementation

**Example Prompt**: "Use divergence-convergence to design our caching strategy"

---

### 🔗 104-analogy-transfer
**Purpose**: Apply patterns from other domains to current problems  
**When to Use**: Novel challenges, system design, optimization tasks  
**Key Features**:
- Structural mapping (not surface)
- 2-3 source domains
- Confidence scoring
- Explicit non-transfers

**Example Prompt**: "Find analogies from nature for our distributed system"

---

### ✂️ 105-context-trim
**Purpose**: Compress input while preserving semantic integrity  
**When to Use**: ALWAYS (runs first automatically)  
**Key Features**:
- Multiple strategies (keep_edges, semantic_skeleton)
- 93% compression typical
- Task-aware adaptation
- Lossless reference storage

**Example Prompt**: Automatic - no explicit invocation needed

---

### 📝 106-concise-comms
**Purpose**: Optimize output information density  
**When to Use**: All user-facing communication  
**Key Features**:
- 150-300 token limits
- Tweet test validation
- Inverted pyramid structure
- Only applies to final output

**Example Prompt**: Applied automatically to responses

---

### 🛡️ 004-risk-checkpoint (Core, but integrated)
**Purpose**: Validate all operations for safety  
**When to Use**: Before ANY state-changing operation  
**Key Features**:
- CRITICAL/HIGH/MEDIUM/LOW classification
- Pattern-based detection
- Veto power over all rules
- Co-evolution mandate

**Example Prompt**: Automatic safety gate - no explicit invocation

---

## Quick Decision Tree

```
Need creative ideas?
├─ YES → wildcard-brainstorm
│   └─ Complex problem? → divergence-convergence
└─ NO → Need optimization?
    ├─ YES → pareto-prioritization
    └─ NO → Need cross-domain insight?
        └─ YES → analogy-transfer

Always Active:
- context-trim (input optimization)
- risk-checkpoint (safety validation)  
- concise-comms (output optimization)
```

## Common Stacks

### 🎨 Creative Stack
```
context-trim → divergence-convergence → [wildcard-brainstorm + analogy-transfer] → risk-checkpoint → concise-comms
```

### 📊 Analytical Stack  
```
context-trim → philosophers-stone → pareto-prioritization → stepwise-autonomy → concise-comms
```

### 🚀 Rapid Iteration Stack
```
ultrathink-prompting → wildcard-brainstorm → risk-checkpoint → concise-comms
```

### 🔒 Production Stack
```
risk-checkpoint → pareto-prioritization → stepwise-autonomy → backend-security
```

## Phase Indicators

**In DIVERGENCE Phase**:
- "Exploring all possibilities..."
- "Generating diverse options..."
- "What if we tried..."

**In CONVERGENCE Phase**:
- "Evaluating options against criteria..."
- "The optimal synthesis is..."
- "Focusing on high-impact..."

## Performance Benchmarks

| Rule | Performance Impact | Quality Impact |
|------|-------------------|----------------|
| context-trim | 10x speed boost | Improved focus |
| wildcard-brainstorm | -15% speed | +25-50% creativity |
| divergence-convergence | -20% speed | +35% solution quality |
| analogy-transfer | Neutral | +d=0.50 problem-solving |
| concise-comms | +5% speed | +40% readability |
| risk-checkpoint | -5% speed | -90% incidents |

## Integration Gotchas

1. **Never** run wildcard-brainstorm and concise-comms in same phase
2. **Always** let context-trim run first (automatic)
3. **Risk-checkpoint** can override any other rule's output
4. **Divergence-convergence** should orchestrate, not be orchestrated
5. **Internal_thought** field is exempt from concise-comms

## Monitoring Success

✅ Good Signs:
- Multiple distinct options generated
- Clear phase transitions
- Explicit risk assessments
- Token counts within limits

⚠️ Warning Signs:
- Single-track solutions
- Skipped divergence phase
- Token limit warnings
- Circular dependencies

## Emergency Overrides

```yaml
# Disable all cognitive rules
profile: minimal

# Maximum safety mode
profile: production_changes

# Skip specific rule
rules:
  exclude: [wildcard-brainstorm]
```

---

*Remember: These rules are tools, not laws. Use judgment to adapt them to specific contexts.*
