# Mirror Project Rules Index

<!-- Version: 2.0.0 — 2025-06-19 -->
<!-- Refactored from flat structure to hierarchical categorization -->

This index provides a comprehensive overview of all rules in the Mirror project, organized by category according to best practices for AI/LLM agent rule management.

## Directory Structure

```
.cursor/rules/
├── 000-core/           # Core foundational rules (always load first)
├── 100-cognitive/      # Thinking and reasoning rules
├── 200-domain/         # Domain-specific rules (analytics, dbt, etc.)
├── 300-integration/    # Tool and service integration rules
├── 400-patterns/       # Development patterns and best practices
├── 500-deprecated/     # Rules being phased out
└── README.md          # This file
```

## Rule Categories

### 000-core: Core Foundational Rules
These rules establish the fundamental operating principles for all agents.

- **001-philosophers-stone.mdc**: Strategic execution protocol combining effort-impact analysis with systemic leverage
- **002-pareto-prioritization.mdc**: 80/20 principle for focusing on high-impact work
- **003-stepwise-autonomy.mdc**: Chain-of-thought reasoning and progressive task execution
- **004-risk-checkpoint.mdc**: Mandatory safety gates for all potentially harmful operations

### 100-cognitive: Thinking and Reasoning Rules
Rules that enhance cognitive capabilities and problem-solving approaches.

- **101-ultrathink-prompting.mdc**: Divergent thinking with concise, high-density communication
- **102-wildcard-brainstorm.mdc**: Controlled randomness for breaking cognitive patterns
- **103-divergence-convergence.mdc**: Structured two-phase creative problem-solving
- **104-analogy-transfer.mdc**: Cross-domain knowledge transfer through structural mapping
- **105-context-trim.mdc**: Intelligent compression for optimal context utilization
- **106-concise-comms.mdc**: Information density optimization in user communications

### 200-domain: Domain-Specific Rules
Specialized rules for particular technical domains and tools.

#### Analytics & Data Science
- **analytics-engineering.mdc**: Best practices for analytics engineering workflows
- **analytics-storytelling.mdc**: Narrative construction from data insights
- **datascience-repro.mdc**: Reproducibility standards for data science

#### dbt (Data Build Tool)
- **dbt-analytics-engineering.mdc**: dbt-specific analytics patterns
- **dbt-incremental-loading-patterns.mdc**: Incremental model strategies
- **dbt-mcp-server.mdc**: MCP server integration for dbt
- **dbt-model-quality.mdc**: Quality standards for dbt models
- **dbt-semantic-modeling.mdc**: Semantic layer construction

#### SQL & Database
- **sql-correctness.mdc**: SQL query validation and best practices
- **sql-performance.mdc**: Query optimization techniques

#### Python
- **python-clean-code.mdc**: Pythonic code standards and patterns

### 300-integration: Tool and Service Integration Rules
Rules for integrating with external tools and services.

- **cursor-agent-integration.mdc**: Cursor AI agent configuration
- **perplexity-research-framework.mdc**: Research workflow using Perplexity
- **multi-model-tool-integration.mdc**: Coordinating multiple AI models
- **available_tooling_guide.mdc**: Comprehensive tool selection guide

### 400-patterns: Development Patterns and Best Practices
General software development patterns and methodologies.

#### Testing & Quality
- **test-driven-development.mdc**: TDD methodology and practices
- **ci-cd-testing-gatekeeper.mdc**: CI/CD pipeline quality gates

#### Code & Architecture
- **code-generation-patterns.mdc**: Patterns for AI-assisted code generation
- **api-design-guidelines.mdc**: RESTful API design standards
- **backend-security.mdc**: Security best practices for backend systems
- **sdk-development-checklist.mdc**: SDK development standards

#### Operations & Monitoring
- **logging-monitoring.mdc**: Observability standards
- **deployment-config.mdc**: Deployment configuration patterns
- **dependency-management.mdc**: Package and dependency management

#### Documentation & Research
- **document-analysis.mdc**: Document processing patterns
- **research-prompt-guidelines.mdc**: Effective research prompting
- **notebook-best-practices.mdc**: Jupyter notebook standards
- **notepad-best-practices.mdc**: Note-taking and documentation

#### Specialized Patterns
- **bash-safety.mdc**: Safe shell scripting practices
- **prompt-eval.mdc**: Prompt evaluation frameworks
- **structured-data-embedding-best-practices.mdc**: Embedding strategies

### 500-deprecated: Deprecated Rules
Rules scheduled for removal in future versions. Currently empty.

## Rule Naming Conventions

1. **Prefix System**: 
   - 000-099: Core rules (load order matters)
   - 100-199: Cognitive/reasoning rules
   - 200-299: Domain-specific rules
   - 300-399: Integration rules
   - 400-499: Pattern rules
   - 500-599: Deprecated rules

2. **File Naming**:
   - Use kebab-case (e.g., `risk-checkpoint.mdc`)
   - Maximum 32 characters
   - Descriptive but concise
   - Include version in metadata, not filename

## Rule Dependencies

### Dependency Graph
```
000-core (foundation)
    ├── 100-cognitive (builds on core principles)
    │   ├── 200-domain (applies cognitive patterns to domains)
    │   └── 300-integration (cognitive rules inform tool use)
    └── 400-patterns (patterns implement core principles)
```

### Load Order
1. Always load 000-core rules first
2. Load 100-cognitive rules for enhanced reasoning
3. Load domain/integration/pattern rules as needed for specific tasks
4. Never load deprecated rules

## Version History

- **v2.0.0** (2025-06-19): Major refactor from flat to hierarchical structure
- **v1.0.0** (Previous): Original flat structure with all rules in root directory

## Usage Guidelines

1. **For New Rules**: 
   - Determine appropriate category
   - Use next available number in category
   - Follow naming conventions
   - Update this index

2. **For Updates**:
   - Increment version in rule metadata
   - Document changes in rule file
   - Consider if category is still appropriate

3. **For Deprecation**:
   - Move to 500-deprecated with sunset date
   - Update dependent rules
   - Provide migration guide

## Maintenance Schedule

- **Quarterly Review**: Evaluate rule effectiveness and usage
- **Semi-Annual Cleanup**: Remove deprecated rules past sunset date
- **Annual Restructure**: Consider category reorganization based on growth