# Cursor Notepads for Enhanced Data Analytics Workflows

This directory contains Cursor Notepads that implement the improvements recommended in our Cursor Rules Evaluation & Improvement Report. These Notepads extend and enhance the existing Cursor rules with data analytics-specific guidance, examples, and patterns.

## What Are Cursor Notepads?

Cursor Notepads are a powerful context-sharing feature that bridges the gap between composers and chat interactions. They go beyond the capabilities of .cursorrules files by providing:

- Reusable, modular contexts that can be referenced across different environments
- Rich markdown formatting for improved readability
- The ability to include file references and examples
- Easy referencing in prompts using the `@` symbol

## Available Notepads

### 1. Perplexity Research Framework
Consolidates research guidelines into a unified framework with clear differentiation between standard and deep research approaches.

**Use when**: Planning research tasks, formulating research questions, or evaluating research outputs.

**Reference with**: `@perplexity-research-framework`

### 2. Data Analytics Code Patterns
Provides concrete examples of well-structured data analytics code, including transformation patterns, validation patterns, and best practices.

**Use when**: Writing or reviewing data transformation code, setting up validation procedures, or establishing coding standards.

**Reference with**: `@data-analytics-code-patterns`

### 3. Data Pipeline Verification
Offers detailed verification procedures for data pipelines, including schema validation, transformation logic verification, and performance testing.

**Use when**: Setting up testing for data pipelines, creating validation routines, or troubleshooting data quality issues.

**Reference with**: `@data-pipeline-verification`

### 4. Data Analytics Prompt Patterns
Provides comprehensive prompt patterns for common data analytics tasks, including revenue analysis and customer cohort analysis.

**Use when**: Creating new prompts for data analysis tasks or evaluating existing prompts.

**Reference with**: `@data-analytics-prompt-patterns`

### 5. 80-20 Data Analytics Framework
Enhances the general 80-20 prioritization principle with data analytics-specific metrics, decision frameworks, and case studies.

**Use when**: Prioritizing analytics tasks, scoping projects, or allocating resources.

**Reference with**: `@80-20-data-analytics-framework`

## How to Use These Notepads

1. **In Composers**: When working in a Cursor composer, reference these Notepads by typing `@` followed by the Notepad name.

2. **In Chat**: During a chat interaction, reference relevant Notepads to provide context for your questions or tasks.

3. **For Development Guidelines**: Use these Notepads as reference material when establishing team practices or onboarding new team members.

4. **For Code Reviews**: Reference relevant patterns during code reviews to maintain consistent standards.

## Best Practices

1. **Combine Multiple Notepads**: For complex tasks, reference multiple Notepads to provide comprehensive context.

2. **Start with 80-20**: Begin by referencing the 80-20 framework to ensure focus on high-impact activities.

3. **Include Concrete Examples**: When asking for code or analysis, reference the relevant pattern Notepad and specify how you want your solution to align with it.

4. **Version Control**: These Notepads can be kept in version control alongside your project code to ensure consistency across the team.

## Example Usage

```
@perplexity-research-framework @80-20-data-analytics-framework

Research the most efficient way to implement a customer churn prediction model for our SaaS product. Focus on the highest-impact approach that balances accuracy with implementation effort, according to the 80-20 principle.
```

## Relationship to Cursor Rules

These Notepads extend and complement the existing Cursor rules in `/Users/USERNAME/.digital_twin/.cursor/rules/`. They provide more specific guidance for data analytics workflows while maintaining alignment with the core principles established in the rules.

Each Notepad references the relevant rule files to maintain this connection.
