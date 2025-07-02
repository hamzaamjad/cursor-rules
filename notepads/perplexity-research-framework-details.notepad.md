# Perplexity Research Framework - Detailed Guidance & Examples

## Research Depth Decision Tree
- **Standard Research**: For routine information needs with clear parameters
  - When to use: Single-domain questions, factual verification, basic exploration
  - Example: "What are the most common Python libraries for data visualization?"
  
- **Deep Research**: For complex topics requiring synthesis across sources
  - When to use: Multi-domain questions, emerging topics, comparative analysis
  - Example: "How do different cloud providers handle data lineage tracking for analytics workloads?"

## Common Components

### 1. Justification
- Clearly articulate why research is necessary
- Connect to business impact using 80-20 principle
- Example: "Research needed to identify optimal data processing approach that will impact 80% of pipeline performance"

### 2. Scoping
- Define overall research questions and sub-questions
- Use MECE principle (Mutually Exclusive, Collectively Exhaustive)
- Example:
  ```
  Overall: What ML model works best for customer churn prediction?
  Sub-questions:
  - What algorithms perform best on imbalanced classification tasks?
  - What feature engineering techniques improve churn prediction?
  - How do different models compare on interpretability vs accuracy?
  ```

### 3. Question Formulation
- Craft specific, unambiguous questions
- Use domain-specific terminology
- Avoid bias in phrasing
- Example: "What are the tradeoffs between data warehouse solutions (Snowflake, BigQuery, Redshift) for real-time analytics workloads with emphasis on query performance and cost efficiency?"

### 3.1. Achieving Research Breadth (e.g., Domain Coverage)
- If specific breadth is required (e.g., covering N+ domains, comparing X technologies), explicitly state this in the scope.
- **Strategy 1 (Targeted Queries)**: Formulate separate, specific questions for each required area/domain.
    - Example: If needing info on 3 domains (A, B, C), ask "Research topic X specifically for domain A", then "Research topic X specifically for domain B", etc.
- **Strategy 2 (Broad Query + Filtering)**: Use a broader query initially requesting coverage across multiple areas, then filter/analyze the results to ensure targets are met.
    - Example: "Research topic X across domains A, B, C, D, and E. Summarize findings for each."
- **Refinement**: If initial queries don't yield sufficient breadth, refine questions to be more targeted or explore adjacent concepts/domains.

### 4. Output Specification
- Specify desired output format and structure
- Define level of technical detail
- Example: "Provide a comparison table with solutions as rows, and: setup complexity, maintenance overhead, query performance, and cost factors as columns. Include quantitative metrics where available."

### 5. Citation Review
- Assess relevance and credibility of sources
- Prioritize peer-reviewed or authoritative sources
- Check for recency (especially for rapidly evolving topics)
- Example evaluation: "Source is a 2024 industry benchmark report with transparent methodology, making it highly relevant and credible"

### 6. Actionable Summary
- Synthesize key findings into actionable insights
- Highlight decision points using 80-20 principle
- Example: "Research indicates that time-series forecasting for this use case performs best with Prophet for faster implementation or LSTM for higher accuracy, with Prophet requiring 75% less implementation time while sacrificing 10% accuracy"

### 7. Integration
- Apply findings to task execution
- Update project plans based on research
- Example: "Based on research, we'll implement data validation using Great Expectations library before pipeline deployment, focusing on completeness and timeliness checks which address 85% of historical data quality issues"

## RevOps/FinOps-Specific Research Examples

### Example 1: Revenue Optimization Research
```
Research Question: What are best practices for detecting and addressing revenue leakage in SaaS subscription businesses?

Sub-questions:
- Which metrics most effectively surface potential revenue leakage?
- What data integration patterns enable timely detection?
- How can reconciliation processes be automated?

Output Specification: 
- Key metrics with calculation methods
- Data pipeline architecture diagram
- Implementation priority matrix
```

### Example 2: Cost Efficiency Analysis
```
Research Question: How can we optimize cloud data warehouse spending while maintaining query performance?

Sub-questions:
- Which warehouse sizing and scaling strategies provide optimal cost/performance balance?
- What query patterns contribute most to current costs?
- Which optimization techniques provide highest ROI?

Output Specification:
- Quantified comparison of scaling approaches
- Top 3 optimization techniques with effort/impact assessment
- Implementation roadmap
```
