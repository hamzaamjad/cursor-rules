# Stepwise Autonomy Complexity Assessment Guide

This notepad provides detailed guidance for assessing task complexity and applying the appropriate protocol level. The examples and expanded criteria support consistent implementation of the stepwise autonomy pattern across diverse task scenarios.

## Complexity Classification Detailed Examples

### Simple Tasks (Streamlined Protocol)

Simple tasks represent operations that can be completed with minimal planning and verification. These tasks typically involve predictable outcomes and isolated changes that do not impact other system components.

Example scenarios include formatting a single file according to established style guidelines, renaming variables within a confined scope, or updating configuration values that have no downstream dependencies. For instance, changing a timeout value from 30 to 60 seconds in a configuration file represents a simple task when that value is only referenced in one location.

The streamlined protocol for simple tasks involves direct execution with basic result confirmation. Verification focuses on syntax correctness and immediate output validation rather than comprehensive system impact analysis.

### Moderate Tasks (Standard Protocol)

Moderate tasks require structured planning and systematic verification but remain within well-understood boundaries. These operations typically span multiple files or components while maintaining predictable interaction patterns.

A representative moderate task might involve adding a new API endpoint to an existing service. This requires creating the endpoint handler, updating routing configuration, and potentially modifying documentation. While spanning multiple files, the changes follow established patterns and have limited cascading effects.

The standard protocol applies full planning and verification steps but optimizes for efficiency. Each step receives appropriate verification without excessive overhead, and tool usage remains focused on essential operations rather than exhaustive system analysis.

### Complex Tasks (Enhanced Protocol)

Complex tasks demand comprehensive planning, extensive tool utilization, and rigorous verification at each stage. These operations often involve significant architectural changes, cross-system dependencies, or high-risk modifications that could impact system stability.

Examples of complex tasks include refactoring core authentication systems, implementing new data processing pipelines that span multiple services, or debugging intermittent production issues that manifest across distributed components. These tasks require deep system understanding and careful coordination of changes.

The enhanced protocol mandates detailed planning documentation, exploration of multiple solution approaches using Tree of Thoughts methodology, and comprehensive verification including integration testing and rollback planning. Tool usage extends to specialized services for documentation lookup, dependency analysis, and automated testing frameworks.

## Complexity Reassessment Guidelines

Task complexity assessment remains dynamic throughout execution. Initial classifications may require adjustment based on discoveries during implementation. The protocol includes specific triggers for reassessing complexity to ensure appropriate rigor applies at each stage.

Escalation triggers indicate when a task exceeds its initial complexity assessment. Repeated verification failures suggest hidden dependencies or system interactions not apparent during initial planning. Discovery of additional affected components or unexpected tool operation results similarly warrant complexity escalation.

De-escalation occurs less frequently but remains important for efficiency. When initial investigation reveals simpler implementation paths than anticipated, or when user clarification reduces scope, the protocol adjusts to avoid unnecessary overhead while maintaining appropriate safety margins.

## Scope Confirmation Best Practices

Effective scope confirmation prevents misaligned expectations and ensures efficient execution. The protocol emphasizes explicit confirmation of performance targets, output format preferences, and constraint specifications before implementation begins.

Performance targets require quantitative definition whenever possible. Rather than optimizing for "better performance," the protocol seeks specific metrics such as "reduce processing time below 100ms" or "limit memory usage to 512MB." These concrete targets enable objective verification and prevent over-engineering.

Output format preferences significantly impact implementation approaches. Minimal output focusing on essential results differs substantially from detailed reporting including intermediate steps and diagnostic information. Early clarification prevents unnecessary rework and ensures deliverables meet stakeholder expectations.

Constraint specifications encompass both technical and business limitations. Technical constraints include API rate limits, processing timeouts, and resource quotas. Business constraints involve regulatory requirements, data handling policies, and operational windows. Explicit acknowledgment of these constraints shapes implementation decisions from the outset.