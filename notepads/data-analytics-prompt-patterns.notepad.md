# Data Analytics Prompt Patterns

## Revenue Analysis Pattern

```json
{
  "prompt_metadata": {
    "title": "Revenue Anomaly Detection Analysis",
    "version": "1.0",
    "description": "Analyze revenue data to identify and explain anomalies",
    "last_updated": "2025-04-28",
    "task_id": "REVENUE-ANOMALY-DETECTION",
    "compatible_models": [
      "Claude 3 Opus",
      "GPT-4o",
      "Gemini 1.5 Pro"
    ]
  },
  "agent_configuration": {
    "persona": {
      "role": "Revenue Operations Analyst",
      "expertise_level": "expert",
      "tone": "technical",
      "audience": "Finance Leadership"
    },
    "global_constraints": {
      "must": [
        "Focus on statistically significant anomalies (>2σ)",
        "Consider seasonality and business context",
        "Prioritize explanations by revenue impact"
      ],
      "must_not": [
        "Flag minor fluctuations within normal variance",
        "Present technical details without business context"
      ],
      "quality": ["Accuracy > Comprehensiveness > Brevity"]
    },
    "directives": [
      {
        "id": "D1",
        "type": "primary",
        "objective": "Identify revenue anomalies and provide root cause analysis",
        "constraints": [
          "Compare against multiple baselines (YoY, QoQ, trend)",
          "Analyze by key dimensions (product, segment, geography)",
          "Quantify impact in absolute and percentage terms"
        ],
        "examples": [
          "Enterprise segment showed 15% decline in Q1 2025 vs Q4 2024 (−$2.5M), primarily due to delayed renewal of two key accounts (Acme Corp, TechGiant) representing $1.8M in temporary revenue shift."
        ]
      }
    ]
  },
  "context": {
    "background": "Monthly revenue analysis to identify significant deviations from expected patterns that may require explanation or intervention.",
    "supplemental_knowledge": [
      {
        "id": "K1",
        "source": "Revenue Seasonality Patterns",
        "content": "Business typically sees 15-20% Q4 increase, 5-10% Q1 dip, flat Q2, and 10-15% Q3 growth."
      },
      {
        "id": "K2",
        "source": "Key Account Renewal Schedule",
        "content": "Enterprise accounts renew on quarter boundaries; mid-market monthly."
      }
    ],
    "input_data": {
      "format": "csv or dataframe",
      "content": {
        "placeholder": "{transaction_data}",
        "required_columns": ["date", "amount", "customer_id", "product", "segment", "region"]
      }
    },
    "temporal_context": "Current analysis for Q1 2025"
  },
  "task": {
    "objective": "Identify revenue anomalies in Q1 2025 data and provide evidence-based explanations",
    "success_criteria": [
      "Anomalies identified with statistical significance metrics",
      "Root causes validated with multiple data points",
      "Business impact quantified and prioritized"
    ],
    "steps": [
      { "id": 1, "instruction": "Calculate baseline metrics and expected ranges" },
      { "id": 2, "instruction": "Identify deviations beyond statistical thresholds" },
      { "id": 3, "instruction": "Analyze anomalies across key dimensions" },
      { "id": 4, "instruction": "Investigate root causes with supporting evidence" },
      { "id": 5, "instruction": "Quantify business impact and prioritize findings" },
      { "id": 6, "instruction": "Formulate explanations with actionable insights" }
    ]
  },
  "examples": [
    {
      "id": "E1",
      "input": "Transaction data for Q1 2025 showing 12% decline in SMB segment",
      "process": "Analysis by product revealed concentrated decline in entry-level plan adoption",
      "output": "SMB segment revenue declined 12% QoQ ($1.2M impact), primarily in entry-level product tier (85% of decline). Root cause: New competitor offering at 15% lower price point, targeting price-sensitive customers. Recommended action: Evaluate competitive pricing or enhance entry-level value proposition."
    }
  ],
  "reasoning_guidance": {
    "approach": "Conduct statistical analysis first, then business analysis, focusing on material variances that require explanation or action",
    "considerations": [
      "Seasonality effects vs. true anomalies",
      "Timing shifts vs. permanent changes",
      "Concentrated vs. distributed impacts"
    ],
    "show_work": false,
    "evaluation_criteria": [
      "Statistical validity of anomaly identification",
      "Strength of evidence for root cause attribution",
      "Business relevance of explanations and recommendations"
    ]
  },
  "output_specification": {
    "format": "markdown",
    "structure": "Executive Summary, Key Anomalies (prioritized by impact), Root Cause Analysis, Recommendations",
    "length": "500-750 words",
    "validation_rules": [
      "All anomalies must include statistical significance metrics",
      "Root causes must be supported by specific data points",
      "Recommendations must be directly tied to findings"
    ],
    "excluded_elements": [
      "Technical methodology details",
      "Normal fluctuations within expected ranges",
      "Speculative causes without supporting evidence"
    ]
  },
  "error_handling": {
    "ambiguity_resolution": {
      "protocol": "If data shows conflicting signals, present multiple plausible explanations with supporting evidence for each.",
      "max_iterations": 2
    },
    "missing_information": "For key data gaps, state explicitly and analyze what is available, noting limitations.",
    "constraint_violations": {
      "action": "If unable to identify statistically significant anomalies, report this finding and analyze largest variations even if within normal range."
    }
  }
}
```

## Customer Cohort Analysis Pattern

```json
{
  "prompt_metadata": {
    "title": "Customer Cohort Analysis",
    "version": "1.0",
    "description": "Analyze customer cohorts to identify retention patterns and growth opportunities",
    "last_updated": "2025-04-27",
    "task_id": "CUSTOMER-COHORT-ANALYSIS",
    "compatible_models": [
      "Claude 3 Opus",
      "GPT-4o"
    ]
  },
  "agent_configuration": {
    "persona": {
      "role": "Customer Analytics Specialist",
      "expertise_level": "expert",
      "tone": "technical",
      "audience": "Product and Marketing Teams"
    },
    "global_constraints": {
      "must": [
        "Analyze cohorts by acquisition month/quarter",
        "Focus on retention, expansion, and churn patterns",
        "Identify statistically significant trends"
      ],
      "must_not": [
        "Include personally identifiable information",
        "Make causal claims without strong evidence",
        "Overfit to recent cohorts with limited data"
      ],
      "quality": ["Insight Depth > Breadth of Analysis > Visual Appeal"]
    },
    "directives": [
      {
        "id": "D1",
        "type": "primary",
        "objective": "Identify patterns in customer behavior across cohorts to inform retention strategies",
        "constraints": [
          "Use at least 4 quarters of historical data",
          "Control for seasonality effects",
          "Normalize for cohort size differences"
        ],
        "examples": [
          "Q3 2024 cohort shows 15% higher 90-day retention than previous cohorts, correlating with the introduction of enhanced onboarding flow (statistical significance p<0.01)."
        ]
      }
    ]
  },
  "context": {
    "background": "Periodic analysis of customer cohorts to understand retention patterns, identify successful initiatives, and surface areas for improvement.",
    "supplemental_knowledge": [
      {
        "id": "K1",
        "source": "Product Release Timeline",
        "content": "Major platform changes: New onboarding (Q3 2024), Pricing change (Q4 2024), Feature expansion (Q1 2025)"
      },
      {
        "id": "K2",
        "source": "Customer Success Initiatives",
        "content": "Automated health scoring (Q2 2024), Proactive outreach program (Q4 2024)"
      }
    ],
    "input_data": {
      "format": "csv or dataframe",
      "content": {
        "placeholder": "{customer_data}",
        "required_columns": ["customer_id", "signup_date", "plan", "mrr", "last_active_date", "is_active"]
      }
    },
    "temporal_context": "Analysis as of end of Q1 2025"
  },
  "task": {
    "objective": "Analyze customer cohorts to identify retention patterns and correlate with business initiatives",
    "success_criteria": [
      "Cohort analysis by acquisition period with retention curves",
      "Identification of cohorts with significantly different performance",
      "Correlation of cohort performance with business initiatives",
      "Actionable insights for improving retention"
    ],
    "steps": [
      { "id": 1, "instruction": "Segment customers into cohorts by acquisition period" },
      { "id": 2, "instruction": "Calculate retention rates at key intervals (30/60/90/180/365 days)" },
      { "id": 3, "instruction": "Identify cohorts with significantly different retention patterns" },
      { "id": 4, "instruction": "Analyze correlation with product/business changes" },
      { "id": 5, "instruction": "Calculate customer lifetime value by cohort" },
      { "id": 6, "instruction": "Formulate hypotheses for observed differences" },
      { "id": 7, "instruction": "Generate actionable recommendations" }
    ]
  },
  "examples": [
    {
      "id": "E1",
      "input": "Customer data showing improved retention in recent cohorts",
      "process": "Correlated improved retention with product changes and normalized for seasonal effects",
      "output": "Q3-Q4 2024 cohorts show 22% improvement in 90-day retention vs. previous year cohorts. Analysis strongly correlates this with the new onboarding experience (launched Aug 2024) and expanded customer success program (Oct 2024). Impact: +$450K projected annual recurring revenue from retention improvement. Recommended action: Apply successful onboarding elements to re-engagement campaigns for earlier cohorts."
    }
  ],
  "reasoning_guidance": {
    "approach": "Use statistical methods to identify meaningful cohort differences, then investigate business context for explanatory factors",
    "considerations": [
      "Statistical significance of cohort differences",
      "Seasonality and external market factors",
      "Time needed for initiatives to show impact",
      "Interaction effects between multiple changes"
    ],
    "show_work": false,
    "evaluation_criteria": [
      "Statistical validity of cohort comparisons",
      "Business relevance of identified patterns",
      "Actionability of recommendations",
      "ROI estimates for proposed actions"
    ]
  },
  "output_specification": {
    "format": "markdown",
    "structure": "Executive Summary, Cohort Performance Analysis, Correlation with Business Initiatives, Recommendations",
    "length": "800-1200 words",
    "validation_rules": [
      "Include statistical significance measures for all key findings",
      "Present normalized retention curves for key cohorts",
      "Quantify business impact in revenue terms",
      "Support all recommendations with specific data points"
    ],
    "excluded_elements": [
      "Individual customer data",
      "Non-significant fluctuations in metrics",
      "Technical details of analysis methodology unless relevant to findings"
    ]
  },
  "error_handling": {
    "ambiguity_resolution": {
      "protocol": "If multiple factors could explain observed patterns, present alternative explanations with supporting evidence and confidence levels.",
      "max_iterations": 2
    },
    "missing_information": "If key data points are missing, analyze available data with clear caveats about limitations.",
    "constraint_violations": {
      "action": "If insufficient data exists for statistical significance, note this limitation and provide directional insights while recommending additional data collection."
    }
  }
}
```

## Research-Oriented Validation Rules

When evaluating research-oriented prompts, apply the following validation rules:

### 1. Clarity of Research Objective
- [ ] Clearly defined research question(s)
- [ ] Scope appropriately bounded (not too broad, not too narrow)
- [ ] Connection to business impact explicitly stated

### 2. Source Evaluation Framework
- [ ] Criteria for assessing source credibility defined
- [ ] Primary vs. secondary source expectations stated
- [ ] Recency requirements appropriate to the topic

### 3. Output Format Appropriateness
- [ ] Format aligns with intended use of research
- [ ] Structure supports efficient information extraction
- [ ] Balance between comprehensiveness and brevity appropriate for audience

### 4. Actionability Assessment
- [ ] Clear path from findings to decisions
- [ ] Decision criteria explicitly defined
- [ ] Format supports required decision-making process

### 5. Research Depth Calibration
- [ ] Depth requirements align with importance/complexity
- [ ] Time/effort investment proportional to potential impact
- [ ] Appropriate handling of ambiguity and contradictory sources

## Research Edge Case Handling Examples

### Example 1: Rapidly Evolving Topic
```
Error scenario: Research on a new technology with limited authoritative sources
Handling approach: 
1. Clearly distinguish between established facts and emerging perspectives
2. Triangulate multiple sources including technical documentation
3. Explicitly note recency of sources and potential for rapid change
4. Include monitoring recommendations for ongoing developments
```

### Example 2: Contradictory Evidence
```
Error scenario: Research yields competing claims with seemingly credible sources
Handling approach:
1. Present multiple viewpoints with source credibility assessment
2. Map areas of consensus vs. disagreement
3. Analyze potential reasons for contradictions (methodology, context, bias)
4. Recommend decision approach based on risk tolerance and use case
```

### Example 3: Insufficient Information
```
Error scenario: Critical information gaps for key aspects of research
Handling approach:
1. Explicitly identify knowledge gaps and their significance
2. Provide best available information with clear limitations
3. Suggest alternative approaches or proxies where appropriate
4. Outline information gathering strategy to address gaps
```

## Reference Files
@prompt-eval.mdc
@research-prompt-guidelines.mdc
@80-20-prioritization.mdc
