# Contributing to Cursor Rules

First off, thank you for considering contributing to Cursor Rules! It's people like you that make this framework a powerful tool for the AI development community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Rule Contribution Guidelines](#rule-contribution-guidelines)
- [Style Guidelines](#style-guidelines)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/cursor-rules.git
   cd cursor-rules
   ```
3. Create a new branch for your contribution:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible using our issue template.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. Use the feature request template and provide:
- A clear and descriptive title
- A detailed description of the proposed enhancement
- Rationale for why this would be useful
- Examples of how it would be used

### Contributing Rules

New rules are the heart of this project! When proposing a new rule:

1. Use the rule proposal issue template first to discuss the rule
2. Ensure the rule follows our philosophical framework
3. Provide empirical evidence or research backing when possible
4. Include concrete examples and validation criteria

## Rule Contribution Guidelines

### Rule Structure

All rules must follow this structure:

```markdown
---
description: Brief description of what the rule does
globs: ["**/*.py", "**/*.js"]  # File patterns this rule applies to
alwaysApply: false  # Whether this rule always applies
dependencies: ["rule-1", "rule-2"]  # Other rules this depends on
---

# Rule Name

## Purpose
Clear explanation of why this rule exists and what problem it solves.

## Requirements
- Specific requirement 1
- Specific requirement 2
- Specific requirement 3

## Validation
- Check: How to verify requirement 1
- Check: How to verify requirement 2
- Check: How to verify requirement 3

## Examples

### Scenario: [Describe scenario]
**Without rule**:
```language
# Example of code/prompt without the rule
```

**With rule**:
```language
# Example of code/prompt following the rule
```

## Scientific Basis (optional)
References to research, studies, or empirical evidence supporting this rule.

## Dependencies
Explanation of how this rule interacts with other rules.
```

### Rule Categories

Place your rule in the appropriate category:
- **000-core**: Foundational philosophical principles
- **100-cognitive**: Thinking and reasoning patterns
- **200-domain**: Domain-specific technical guidelines
- **200-engineering**: Software engineering practices
- **300-integration**: Tool and platform integration
- **300-techniques**: Technical approaches and methods
- **400-patterns**: Development patterns and best practices
- **600-experimental**: Experimental features (require extensive testing)

### Naming Conventions

- Use kebab-case for all file names (e.g., `my-new-rule.mdc`)
- Include a 3-digit prefix for rules within numbered categories
- Be descriptive but concise in naming

## Style Guidelines

### Markdown

- Use ATX-style headers (`#` not underlining)
- Include a blank line before and after headers
- Use fenced code blocks with language specification
- Keep line length under 120 characters when possible

### YAML Frontmatter

- Always include `description`, `globs`, and `alwaysApply`
- Keep descriptions under 100 characters
- Use empty arrays `[]` rather than omitting array fields

### Writing Style

- Be clear and concise
- Use active voice
- Provide concrete examples
- Avoid jargon without explanation
- Include metrics and measurements when claiming improvements

## Testing

### Rule Validation

Before submitting, run the validation script:

```bash
python rules/validate_rules.py
```

This checks for:
- Correct YAML frontmatter
- No circular dependencies
- Proper file naming
- Required sections present

### Manual Testing

1. Test your rule with multiple AI models if possible
2. Verify the examples work as documented
3. Check that validation criteria actually catch violations
4. Ensure no negative interactions with existing rules

## Pull Request Process

1. Update the README.md with details of significant changes
2. Update the CHANGELOG.md following the Keep a Changelog format
3. Ensure all tests pass and no validation errors occur
4. Follow the PR template (to be added)
5. Request review from maintainers

### PR Title Format

Use conventional commits format:
- `feat: Add new rule for X`
- `fix: Correct validation in Y rule`
- `docs: Update README with Z`
- `refactor: Reorganize pattern rules`

### Review Process

PRs will be reviewed for:
1. Alignment with project philosophy
2. Code/rule quality and clarity
3. Proper documentation
4. Testing evidence
5. No breaking changes without discussion

## Questions?

Feel free to open an issue for any questions about contributing. We're here to help!

## Recognition

Contributors will be recognized in our README.md and significant contributions may be highlighted in our CHANGELOG.md.

Thank you for contributing to making AI development more effective and thoughtful!