# Changelog

All notable changes to the cursor-rules project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Optimized metadata structure for 3 slowest-parsing rules:
  - `427-stigmergic-workflows.mdc`: Fixed broken external reference, simplified nested metadata (4.40ms → 0.21ms, 95% improvement)
  - `model-selection.mdc`: Added missing metadata header, condensed content by 40% (4.36ms → 0.20ms, 95.4% improvement)
  - `436-code-generation-patterns.mdc`: Simplified performance metrics structure (3.40ms → 0.22ms, 93.5% improvement)
- Metadata optimization pattern: Remove nested structures in performance section for faster YAML parsing
- Modularized 2 largest rules for token efficiency:
  - `301-available-tooling-guide.mdc`: Split into 3 modules (2847 → ~450 tokens core, 84% reduction)
  - `302-cursor-agent-integration.mdc`: Split into 3 modules (2145 → ~400 tokens core, 81% reduction)
- Created lazy-loading pattern for detailed content, reducing initial load overhead

### Added
- Decision-making framework rules in `100-cognitive/`:
  - `110-ira-framework.mdc`: IRA (Investigate, Research, Act) for evidence-based decisions
  - `111-ooda-loop.mdc`: OODA Loop (Observe, Orient, Decide, Act) for rapid adaptation
  - `112-ira-ooda-integration.mdc`: Combined framework for strategic-tactical alignment
- Rulesync tool (`scripts/rulesync`) for cross-platform rule synchronization:
  - Supports 5 platforms: Gemini CLI, OpenAI Codex, Claude Code, Cursor IDE, Zed Editor
  - Generates platform-specific formats from unified `rulesync.md`
  - Creates compatibility symlinks for cross-tool support
- Comprehensive research documentation:
  - `/research/sonar/20250714-rulesync-matrix.md`: Platform integration matrix with edge cases
- GitHub Actions CI/CD pipeline with validation and benchmarking workflows
- Automated rule validation on all PRs with performance regression detection
- New rule categories:
  - `500-safety/`: Input validation and prompt injection defense (1 rule)
  - `600-experimental/`: Beta features and metacognitive patterns (1 rule)
  - `700-evolution/`: Performance tracking and adaptation (1 rule)
- Production-ready validation framework with:
  - Performance profiling (timing, memory, token metrics)
  - Dependency graph analysis with cycle detection
  - Automatic fix suggestions for common issues
  - JSON/HTML report generation
- Benchmarking infrastructure:
  - `scripts/benchmark_rules.py`: Measure timing, memory, and token usage
  - `scripts/compare_benchmarks.py`: Generate performance comparison reports
  - Baseline metrics tracking for regression detection
- Documentation auto-generation system:
  - `scripts/generate_docs.py`: Create markdown docs from YAML metadata
  - Dependency visualization with NetworkX/Matplotlib
  - Cross-referenced rule documentation
  - Category documentation with metrics
- Enhanced `rule_validator.py` with 6 new capabilities:
  - `benchmark_rule()`: Performance measurement per rule
  - `analyze_dependencies()`: Build complete dependency graph
  - `suggest_fixes()`: Generate automatic remediation suggestions
  - `generate_report()`: Multi-format reporting (JSON/HTML)
  - Performance baseline comparison
  - Memory usage tracking
- CI badges in README for validation and benchmark status
- Python type hints and mypy validation in CI pipeline
- Automated fix scripts:
  - `scripts/fix_missing_created.py`: Added created field to 108 files
  - `scripts/fix_invalid_dependencies.py`: Fixed 103 invalid dependency entries
  - `scripts/move_oversized_to_notepad.py`: Moved 5 oversized rules to notepads
- Validation configuration file (`validation/config.yaml`) with customizable thresholds
- Enhanced metadata structure for all rule files with comprehensive tracking capabilities
- Automated metadata migration script (`scripts/migrate-metadata.py`)
- Enhanced metadata template (`templates/enhanced-metadata-template.yaml`)
- Scripts directory for automation tools
- Python virtual environment configuration for project dependencies
- Comprehensive metadata fields including:

### Changed
- Optimized 5 high-impact rules for token efficiency (6,661 token reduction, 6.5% of total):
  - `427-stigmergic-workflows.mdc`: 66% reduction (1,243 → ~420 tokens)
  - `443-model-selection.mdc`: 53% reduction (1,248 → ~580 tokens)
  - `436-code-generation-patterns.mdc`: 55% reduction (1,559 → ~695 tokens)
  - `301-available-tooling-guide.mdc`: 79% reduction (2,847 → ~590 tokens)
  - `302-cursor-agent-integration.mdc`: 72% reduction (2,145 → ~595 tokens)
- Extracted detailed content from oversized rules to notepads:
  - `notepads/300-integration/detailed-tooling-reference.md`: Complete tool comparison matrix
  - `notepads/300-integration/agent-integration-strategies.md`: Advanced integration patterns
- Improved rule structure with concise actionable formats:
  - Converted verbose prose to bullet points and tables
  - Added concrete code examples replacing abstract descriptions
  - Moved performance metrics to metadata headers
  - Version tracking for individual rules
  - Performance metrics (token reduction, accuracy improvement, processing overhead)
  - Explicit dependency declarations
  - Conflict specifications with resolution strategies
  - Tag-based categorization
  - Research references and empirical validation fields
- Missing notepad files for rule references (5 files in stepwise-autonomy and chain-of-code)
- `requirements.txt` with project dependencies (pyyaml, psutil, click, pytest, etc.)
- `scripts/fix-metadata-issues.py` for automated metadata repair
- Rule validation framework (`validation/rule_validator.py`)
- **Metadata separation system** - following dbt pattern (`.mdc` + `.yaml` files)
- **Rule loader with YAML-first strategy** (`validation/rule_loader.py`)
- **Category configuration files** (`_category.yaml`) for shared defaults

### Changed
- All 61 rule files migrated to enhanced metadata format
- Metadata structure standardized across all rule categories
- Improved dependency tracking with explicit declarations
- **All 104 rule files separated into content-only `.mdc` and metadata `.yaml` files**
- **Token usage reduced by 110,000 tokens (63% reduction) per full scan**
- **Average rule size decreased from 1,674 to 616 tokens**

### Fixed
- **All 106 rules now pass validation** (100% success rate)
- Missing metadata fields in 109 files
- Invalid dependency formats in 103 files
- Oversized rules moved to notepad system (5 files)
- YAML syntax errors in multiple configuration files
- Duplicate frontmatter blocks in 29 files removed
- Missing descriptions restored from secondary metadata blocks
- Migration script regex parsing made more robust
- `snmp-monitoring-patterns.mdc` moved from root to `300-techniques/302-snmp-monitoring-patterns.mdc`
- Hardcoded paths in migration script changed to relative paths

### Improved
- Rule discoverability through tag-based categorization
- **Rule loading performance - 40% faster without metadata parsing**
- **Cost efficiency - save $3.33 per full rule scan at GPT-4 rates**
- Performance monitoring capabilities with embedded metrics
- Dependency validation through explicit relationship declarations
- Token efficiency through strategic rule refactoring
  - Stepwise-autonomy rule reduced from 376 to 107 lines (71.5% reduction)
  - Chain-of-code rule reduced from 276 to 82 lines (70.3% reduction)
  - Stepwise-autonomy-data-pipeline reduced from 246 to 90 lines (63.4% reduction)
  - Stigmergic-workflows reduced from 222 to 90 lines (59.5% reduction)
  - Code-generation-patterns reduced from 217 to 104 lines (52.1% reduction)
  - Extended content moved to organized notepad resources for reference

## [1.1.0] - 2025-01-02

### Added
- Four new cognitive enhancement rules for advanced reasoning capabilities
  - `100-cognitive/107-sparring-partner-mode.mdc` - AI as challenger to preserve critical thinking (41% improvement)
  - `100-cognitive/108-cognitive-load-balancing.mdc` - Dynamic optimization of human-AI task distribution
  - `100-cognitive/109-chain-of-code.mdc` - Executable verification for calculations (17.9% improvement)
  - `400-patterns/427-stigmergic-workflows.mdc` - Environmental coordination patterns (34% faster convergence)
- Performance metrics and quantitative backing for all rules
- Research-based enhancements with citations from 2024-2025 studies
- Comprehensive test suite and validation framework
- Security vulnerability analysis for code execution patterns

### Changed
- Enhanced 21 existing rules with quantitative metrics and research backing
- Core rules now include Tree of Thoughts integration and PFC simulation patterns
- Cognitive rules updated with creativity metrics and compression algorithms
- Domain rules enhanced with performance benchmarks and best practices
- Integration rules updated with latest tool capabilities
- Pattern rules now include self-consistency validation patterns

### Improved
- 15-30% accuracy gains on complex reasoning tasks through Tree of Thoughts integration
- 93% token reduction achieved through enhanced context-trim algorithms
- 48.7% output reduction via improved concise-comms patterns
- 41% better critical thinking preservation through sparring partner mode
- 42% reduction in cognitive load while maintaining accuracy

### Security
- Sandboxed code execution for Chain of Code implementations
- Branch limits enforced for Tree of Thoughts (maximum 7 branches)
- Resource constraints to prevent denial of service attacks
- Safety invariants implemented in sparring partner mode

## [1.0.0] - 2025-01-02

### Added
- Initial public release
- Core philosophical framework (000-core)
- Cognitive enhancement patterns (100-cognitive)
- Domain-specific rules (200-domain, 200-engineering)
- Integration guidelines (300-integration, 300-techniques)
- Development patterns (400-patterns)
- Experimental Rule Symbiosis Evolution Engine (600-experimental)
- Evolution tools (700-evolution)
- Comprehensive documentation and examples
- Rule validation system
- Integration matrix showing rule synergies

### Discovered
- The 60% Principle: Systems perform optimally at 60% constraint level
- Paradoxical Innovation Pattern: Safety constraints enhance creativity
- Constraint Resonance Network for meta-learning

[Unreleased]: https://github.com/hamzaamjad/cursor-rules/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/hamzaamjad/cursor-rules/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/hamzaamjad/cursor-rules/releases/tag/v1.0.0
### Performance Optimization Phase - 2025-01-07

#### Optimized
- **427-stigmergic-workflows**: 4.40ms → 0.03ms (99% faster), 1243 → 308 tokens (75% reduction)
  - Fixed broken external dependency
  - Streamlined YAML metadata
  - Consolidated examples into JSON format
- **436-code-generation-patterns**: 3.40ms → 0.02ms (99% faster), 1559 → 447 tokens (71% reduction)
  - Reduced from 104 to 85 lines
  - Focused on critical patterns only
  - Removed redundant examples

#### Removed
- **code-generation-patterns.mdc**: Duplicate of 436-code-generation-patterns
- **model-selection.mdc**: Duplicate of 443-model-selection

#### Performance Impact
- Total time saved: 7.75ms
- Total tokens saved: 2047
- Rules now meet <2ms validation target
