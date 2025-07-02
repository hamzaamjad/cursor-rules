# 80-20 Data Analytics Framework

## Core Prioritization Metrics

### Revenue Impact
- **Definition**: Potential to directly affect revenue streams through increased conversion, retention, or expansion
- **Measurement**: Estimated revenue change (absolute $ and %)
- **Example high-impact**: Customer churn prediction model that could recover $1.2M in annual recurring revenue (5% of ARR)
- **Example low-impact**: Report formatting enhancement with no direct revenue connection

### Process Efficiency
- **Definition**: Time saved in recurring processes through automation or optimization
- **Measurement**: Hours saved per week/month × affected user count × hourly cost
- **Example high-impact**: Dashboard automation saving finance team (8 people) 5 hours each per week (2,000 hours/year)
- **Example low-impact**: One-time analysis with no recurring time savings

### Data Quality
- **Definition**: Improvement in data accuracy, completeness, or timeliness
- **Measurement**: Error rate reduction × business impact of errors
- **Example high-impact**: Customer address validation that reduces failed deliveries by 8% ($350K annual savings)
- **Example low-impact**: Fixing historical data inconsistencies in rarely-used fields

### Scalability
- **Definition**: Capacity to handle increasing data volumes or user loads without degradation
- **Measurement**: Headroom created for growth × expected growth rate
- **Example high-impact**: Query optimization reducing database load by 40% (enabling 2 years of projected growth)
- **Example low-impact**: Optimizing a process with stable, low volume

## Decision Framework

### Step 1: Impact Assessment
For each potential project or task, score on the four metrics above on a scale of 1-5:
1. Minimal/no impact
2. Minor impact
3. Moderate impact
4. Significant impact
5. Transformational impact

### Step 2: Effort Estimation
Estimate effort required on a scale of 1-5:
1. Hours (trivial)
2. Days (simple)
3. Weeks (moderate)
4. Months (complex)
5. Quarters (major)

### Step 3: ROI Calculation
Calculate impact-to-effort ratio:
```
ROI Score = (Revenue Impact * 0.4 + Process Efficiency * 0.3 + Data Quality * 0.2 + Scalability * 0.1) / Effort
```

### Step 4: Decision Matrix
Plot initiatives on a 2×2 matrix:
- High Impact, Low Effort: Immediate Wins (Do First)
- High Impact, High Effort: Strategic Projects (Plan Carefully)
- Low Impact, Low Effort: Quick Wins (Do When Convenient)
- Low Impact, High Effort: Avoid or Delegate

## Research Prioritization Integration

### Research Question Formulation
Apply 80-20 principle to focus on highest-impact questions:

```
# Weak Research Approach
"Research data visualization libraries"

# Strong 80-20 Research Approach
"Identify the top 2 Python visualization libraries that would reduce dashboard development time by >40% while maintaining compatibility with our existing Pandas/SQL data pipeline"
```

### Research Depth Calibration
Match research depth to expected impact:

| Expected Impact | Appropriate Research Depth |
|----------------|----------------------------|
| Transformational (5) | Deep research with multiple sources, expert consultation, and comprehensive analysis |
| Significant (4) | Thorough research with multiple high-quality sources and structured analysis |
| Moderate (3) | Focused research with 2-3 authoritative sources |
| Minor (2) | Quick verification from single authoritative source |
| Minimal (1) | Brief fact-checking only if critical |

### Source Prioritization
Apply 80-20 to source selection:

1. **Identify the vital few**: What 20% of potential sources will provide 80% of needed insights?
2. **Credential filtering**: Prioritize sources with highest expertise/authority
3. **Recency weighting**: For fast-evolving topics, prioritize most recent sources
4. **Implementation focus**: Prioritize sources with actionable implementation guidance

### Finding Synthesis
Organize research findings using 80-20 principle:

```
# Research Summary Structure

## Top 20% Findings (80% of Value)
[3-5 key insights that directly answer the core question]

## Implementation Guidance (Practical 80/20)
[The 20% of implementation steps that will deliver 80% of value]

## Limitations & Risks
[The 20% of potential issues that represent 80% of the risk]
```

## Case Studies

### Case 1: Customer Churn Analysis

**Initial Scope**: Analyze all customer data to identify churn factors

**80-20 Application**:
1. Focused on top 20% of customers representing 80% of revenue
2. Identified that 3 specific behaviors predicted 75% of churn
3. Developed targeted intervention for high-risk high-value customers

**Result**: Reduced churn by 12% for high-value segment with 65% less analysis time than full-scope approach

### Case 2: Sales Performance Dashboard

**Initial Scope**: Comprehensive dashboard with dozens of metrics

**80-20 Application**:
1. Interviewed sales leaders to identify 5 key metrics driving 80% of decisions
2. Designed simplified dashboard focused on these metrics
3. Added drill-down only for the critical dimensions

**Result**: 90% adoption rate (vs. 30% for previous complex dashboard) and 4 hours/week saved per sales manager

### Case 3: Data Pipeline Optimization

**Initial Scope**: Rewrite entire ETL pipeline for performance

**80-20 Application**:
1. Profiled pipeline to identify 3 bottleneck queries causing 85% of execution time
2. Optimized only these critical queries
3. Implemented selective materialization for high-impact tables

**Result**: Achieved 72% performance improvement with only 25% of the effort of full rewrite

## Reference Files
@80-20-prioritization.mdc
@perplexity-research-guidelines.mdc
@perplexity-deep-research.mdc
