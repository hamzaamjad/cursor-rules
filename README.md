# Cursor Rules

![Validate Rules](https://github.com/hamzaamjad/cursor-rules/workflows/Validate%20Rules/badge.svg)
![Benchmark Rules](https://github.com/hamzaamjad/cursor-rules/workflows/Benchmark%20Rules/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A collection of cognitive enhancement rules and methodologies for AI-assisted development.

## Overview

This repository contains a comprehensive system of rules and notepads designed to enhance AI-assisted software development workflows. These rules have been battle-tested in production environments and represent best practices for working with AI coding assistants.

## Structure

```
cursor-rules/
├── rules/              # Hierarchical rule system
│   ├── 000-core/       # Foundational principles
│   ├── 100-cognitive/  # Thinking and reasoning patterns
│   ├── 200-domain/     # Domain-specific rules
│   ├── 200-engineering/# Software engineering practices
│   ├── 300-integration/# Tool integration guidelines
│   ├── 300-techniques/ # Technical approaches
│   ├── 400-patterns/   # Development patterns
│   └── 600-experimental/# Experimental features
└── notepads/           # Reusable contexts and frameworks
```

## Rule Categories

### Core Rules (000-core)
Foundational principles that underpin all other rules:
- **Philosopher's Stone**: Strategic execution protocols
- **Pareto Prioritization**: 80/20 principle application
- **Stepwise Autonomy**: Progressive delegation patterns

### Cognitive Rules (100-cognitive)
Enhanced thinking and reasoning patterns:
- **Ultrathink Prompting**: Deep analysis techniques
- **Wildcard Brainstorming**: Creative exploration methods
- **Divergence-Convergence**: Problem-solving frameworks

### Domain Rules (200-domain)
Specialized rules for specific technical domains:
- Analytics engineering (dbt, SQL)
- Python development
- Data science workflows
- API design patterns

### Integration Rules (300-integration)
Guidelines for tool integration:
- Cursor IDE optimization
- Multi-model coordination
- MCP (Model Context Protocol) servers

### Pattern Rules (400-patterns)
Best practices and design patterns:
- Security guidelines
- Testing strategies
- Performance optimization
- Error handling

## Usage

### In Cursor IDE

1. **Manual Import**: Copy desired rules to your project's `.cursorrules` file
2. **Symlink Method**: Create symbolic links to rules you want to use
3. **Submodule Integration**: Add this repository as a git submodule

### Rule Format

Rules use the `.mdc` extension (Markdown with YAML frontmatter):

```yaml
---
id: rule-name
title: Rule Title
description: Brief description
dependencies: [optional-dependencies]
---

# Rule Content

Detailed rule documentation in Markdown format...
```

## Notepads

The `notepads/` directory contains reusable contexts and frameworks:
- Project initiation playbooks
- Security checklists
- Research frameworks
- Data analytics patterns
- Git workflows

## Contributing

Contributions are welcome! Please:
1. Follow the existing naming conventions
2. Include comprehensive documentation
3. Test rules in real projects before submitting
4. Open an issue for discussion before major changes

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

These rules were developed through extensive real-world usage and represent collective wisdom from the AI-assisted development community.
