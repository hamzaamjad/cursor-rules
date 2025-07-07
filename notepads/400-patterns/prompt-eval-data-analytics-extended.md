# Extended content for prompt-eval-data-analytics

    
    3. **Market Sizing Analysis Pattern**: See the template in the Notepads directory

*   **Research-Oriented Validation Rules**:

    When evaluating data analytics research prompts, apply these additional validation criteria:

    1. **Business Alignment**:
       - [ ] Clear connection to specific business metrics or KPIs
       - [ ] Scope appropriately calibrated to business impact (following 80-20 principle)
       - [ ] Output format designed for decision-maker consumption

    2. **Data Understanding**:
       - [ ] Required data structure and quality clearly specified
       - [ ] Assumptions about the data explicitly stated
       - [ ] Handling of data limitations and edge cases addressed

    3. **Statistical Validity**:
       - [ ] Appropriate statistical methods specified for the analysis
       - [ ] Clear threshold for significance defined
       - [ ] Validation approach for analytical conclusions included

    4. **Insight Actionability**:
       - [ ] Clear path from findings to decisions
       - [ ] Prioritization framework for multiple insights
       - [ ] Explicit connection to next steps or business processes

*   **Edge Case Handling Examples**:

    1. **Data Quality Issues**:
       ```
       Error scenario: Analysis based on data with significant quality issues
       Handling approach: 
       1. Establish data quality thresholds upfront (e.g., max % missing values)
       2. Include pre-analysis data quality assessment step
       3. Document data quality limitations in final output
       4. Qualify conclusions based on data reliability
       ```

    2. **Conflicting Signals**:
       ```
       Error scenario: Analysis yields contradictory trends or indicators
       Handling approach:
       1. Present multiple interpretations with confidence levels
       2. Segment analysis to identify contextual factors
       3. Recommend additional data collection to resolve contradictions
       4. Provide decision framework that accounts for uncertainty
       ```

    3. **Inconclusive Results**:
       ```
       Error scenario: Analysis fails to detect clear patterns or explanations
       Handling approach:
       1. Document what was ruled out and what remains uncertain
       2. Suggest alternative analytical approaches
       3. Recommend experimental design to generate more conclusive data
       4. Provide best interpretation given current limitations
       ```

*   **Validation**:
    *   Check: Does the prompt follow the core structure from `prompt-eval.mdc`?
    *   Check: Are business context and metrics clearly defined?
    *   Check: Is data structure and quality addressed?
    *   Check: Are insights prioritized according to business impact?
    *   Check: Is there guidance for handling data quality issues and edge cases?
    *   Check: Does the output format support business decision-making?
    *   Check: Are validation steps included to verify analytical accuracy?

*   **Source References**: `.cursor/rules/prompt-eval.mdc`; `.cursor/notepads/data-analytics-prompt-patterns.md`; `.cursor/rules/80-20-prioritization.mdc`