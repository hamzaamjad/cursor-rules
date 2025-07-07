#!/usr/bin/env python3
"""
Enhanced Rule Validation Framework v2.0
Production-ready validation with performance profiling and auto-fix suggestions
"""

import os
import re
import yaml
import json
import time
import ast
import networkx as nx
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from collections import defaultdict
import traceback
import psutil
import subprocess
from enum import Enum

# Performance profiling imports
import cProfile
import pstats
from io import StringIO


class FixType(Enum):
    """Types of automatic fixes available"""
    ADD_MISSING_FIELD = "add_missing_field"
    UPDATE_VERSION = "update_version"
    REDUCE_TOKENS = "reduce_tokens"
    FIX_DEPENDENCY = "fix_dependency"
    NORMALIZE_TAGS = "normalize_tags"


@dataclass
class PerformanceMetrics:
    """Performance measurement results"""
    rule_path: Path
    load_time_ms: float
    parse_time_ms: float
    validation_time_ms: float
    token_count: int
    line_count: int
    file_size_bytes: int
    memory_usage_mb: float
    
    def to_dict(self) -> Dict:
        return {
            'rule': str(self.rule_path.name),
            'load_time_ms': round(self.load_time_ms, 2),
            'parse_time_ms': round(self.parse_time_ms, 2),
            'validation_time_ms': round(self.validation_time_ms, 2),
            'token_count': self.token_count,
            'line_count': self.line_count,
            'file_size_bytes': self.file_size_bytes,
            'memory_usage_mb': round(self.memory_usage_mb, 2)
        }


@dataclass 
class Fix:
    """Suggested fix for validation issues"""
    type: FixType
    description: str
    old_value: Any
    new_value: Any
    line_number: Optional[int] = None
    
    def to_dict(self) -> Dict:
        return {
            'type': self.type.value,  # Convert enum to string
            'description': self.description,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'line_number': self.line_number
        }
@dataclass
class ValidationResult:
    """Enhanced validation result with performance metrics"""
    rule_path: Path
    passed: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    suggested_fixes: List[Fix] = field(default_factory=list)
    performance: Optional[PerformanceMetrics] = None
    
    @property
    def severity(self) -> str:
        if not self.passed:
            return "error"
        elif self.warnings:
            return "warning"
        return "success"
    
    def to_dict(self) -> Dict:
        return {
            'rule': str(self.rule_path.name),
            'status': 'PASS' if self.passed else 'FAIL',
            'severity': self.severity,
            'errors': self.errors,
            'warnings': self.warnings,
            'metrics': self.metrics,
            'fixes': [fix.to_dict() for fix in self.suggested_fixes],
            'performance': self.performance.to_dict() if self.performance else None
        }


class DependencyGraph:
    """Analyze rule dependencies and detect cycles"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.metadata_cache: Dict[Path, Dict] = {}
    
    def build_from_directory(self, rules_dir: Path) -> None:
        """Build dependency graph from all rules"""
        yaml_files = list(rules_dir.rglob("*.yaml"))
        
        for yaml_file in yaml_files:
            if yaml_file.name == '_category.yaml':
                continue
                
            with open(yaml_file) as f:
                metadata = yaml.safe_load(f)
                self.metadata_cache[yaml_file] = metadata
                
                rule_name = yaml_file.stem
                self.graph.add_node(rule_name, path=yaml_file)
                
                if 'dependencies' in metadata:
                    for dep in metadata['dependencies']:
                        dep_name = Path(dep).stem
                        self.graph.add_edge(rule_name, dep_name)
    
    def find_cycles(self) -> List[List[str]]:
        """Find all cycles in dependency graph"""
        try:
            cycles = list(nx.simple_cycles(self.graph))
            return cycles
        except nx.NetworkXNoCycle:
            return []
    
    def get_dependency_depth(self, rule: str) -> int:
        """Get maximum dependency depth for a rule"""
        if rule not in self.graph:
            return 0
        
        try:
            paths = nx.single_source_shortest_path_length(self.graph, rule)
            return max(paths.values()) if paths else 0
        except nx.NetworkXError:
            # This can happen if the rule is not in the graph, which is a valid case
            return 0
    
    def get_dependency_tree(self, rule: str) -> Dict:
        """Get full dependency tree for a rule"""
        if rule not in self.graph:
            return {}
        
        tree = {}
        for successor in self.graph.successors(rule):
            tree[successor] = self.get_dependency_tree(successor)
        return tree

class EnhancedRuleValidator:
    """Production-ready rule validation with profiling and fixes"""
    
    def __init__(self, rules_dir: Path):
        self.rules_dir = rules_dir
        self.results: List[ValidationResult] = []
        self.dependency_graph = DependencyGraph()
        self.config = self._load_config()
        self.process = psutil.Process()
        
        # Performance tracking
        self.profiler = cProfile.Profile()
        self.performance_baselines: Dict[str, PerformanceMetrics] = {}
        self._load_baselines()
    
    def _load_config(self) -> Dict:
        """Load validation configuration"""
        config_path = self.rules_dir.parent / 'validation' / 'config.yaml'
        defaults = {
            'max_lines': 150,
            'warn_lines': 100,
            'max_tokens': 1000,
            'max_dependency_depth': 3,
            'approved_tags': [
                'foundational', 'strategic', 'cognitive-enhancement',
                'reasoning', 'performance', 'safety', 'quality',
                'optimization', 'domain-specific', 'specialized',
                'integration', 'tooling', 'patterns', 'best-practices',
                'experimental', 'research', 'evolution', 'meta-learning',
                'security', 'validation', 'prompt-safety', 'analytics',
                'metacognition', 'self-improvement', 'feedback-loop'
            ],
            'required_metadata': [
                'version', 'description', 'author', 'created',
                'performance', 'tags'
            ]
        }
        
        if config_path.exists():
            with open(config_path) as f:
                loaded = yaml.safe_load(f)
                defaults.update(loaded)
        
        return defaults
    
    def _load_baselines(self) -> None:
        """Load performance baselines"""
        baseline_path = self.rules_dir.parent / 'baseline_metrics.json'
        if baseline_path.exists():
            with open(baseline_path) as f:
                data = json.load(f)
                for rule, metrics in data.items():
                    self.performance_baselines[rule] = PerformanceMetrics(
                        rule_path=Path(rule),
                        **metrics
                    )
    def benchmark_rule(self, rule_path: Path) -> PerformanceMetrics:
        """Benchmark rule loading and parsing performance"""
        start_time = time.perf_counter()
        initial_memory = self.process.memory_info().rss / 1024 / 1024
        
        # Load MDC file
        load_start = time.perf_counter()
        with open(rule_path) as f:
            content = f.read()
        load_time = (time.perf_counter() - load_start) * 1000
        
        # Parse metadata from corresponding YAML file
        parse_start = time.perf_counter()
        yaml_path = rule_path.with_suffix('.yaml')
        metadata = {}
        if yaml_path.exists():
            try:
                with open(yaml_path) as f:
                    metadata = yaml.safe_load(f)
            except yaml.YAMLError:
                metadata = {}
        parse_time = (time.perf_counter() - parse_start) * 1000
        
        # Validation timing
        val_start = time.perf_counter()
        result = ValidationResult(rule_path=rule_path)
        self._validate_metadata(metadata, result)
        val_time = (time.perf_counter() - val_start) * 1000
        
        # Calculate metrics
        file_stats = rule_path.stat()
        lines = content.count('\n') + 1
        tokens = self._estimate_tokens(content)
        final_memory = self.process.memory_info().rss / 1024 / 1024
        
        return PerformanceMetrics(
            rule_path=rule_path,
            load_time_ms=load_time,
            parse_time_ms=parse_time,
            validation_time_ms=val_time,
            token_count=tokens,
            line_count=lines,
            file_size_bytes=file_stats.st_size,
            memory_usage_mb=final_memory - initial_memory
        )
    
    def analyze_dependencies(self) -> DependencyGraph:
        """Build and analyze complete dependency graph"""
        self.dependency_graph.build_from_directory(self.rules_dir)
        return self.dependency_graph
    
    def suggest_fixes(self, errors: List[str], metadata: Dict, content: str) -> List[Fix]:
        """Generate automatic fix suggestions"""
        fixes = []
        
        for error in errors:
            if "Missing required metadata field" in error:
                field = error.split(": ")[1]
                fixes.append(Fix(
                    type=FixType.ADD_MISSING_FIELD,
                    description=f"Add missing {field} field",
                    old_value=None,
                    new_value=self._default_value_for_field(field)
                ))
            
            elif "Invalid version format" in error:
                fixes.append(Fix(
                    type=FixType.UPDATE_VERSION,
                    description="Fix version to semantic format",
                    old_value=metadata.get('version'),
                    new_value="1.0.0"
                ))
            
            elif "exceeds maximum lines" in error:
                fixes.append(Fix(
                    type=FixType.REDUCE_TOKENS,
                    description="Move to notepad system",
                    old_value=len(content.splitlines()),
                    new_value=100
                ))
        
        return fixes
    def validate_all(self, report_format: str = "json") -> Dict[str, Any]:
        """Complete validation with dependency analysis"""
        self.profiler.enable()
        
        # Build dependency graph first
        self.analyze_dependencies()
        cycles = self.dependency_graph.find_cycles()
        
        # Validate all rules
        rule_files = list(self.rules_dir.rglob("*.mdc"))
        yaml_files = list(self.rules_dir.rglob("*.yaml"))
        
        # Match MDC files with their YAML metadata
        rule_pairs = []
        for mdc in rule_files:
            yaml_path = mdc.with_suffix('.yaml')
            if yaml_path.exists():
                rule_pairs.append((mdc, yaml_path))
            else:
                self.results.append(ValidationResult(
                    rule_path=mdc,
                    passed=False,
                    errors=[f"Missing metadata file: {yaml_path.name}"]
                ))
        
        # Validate each rule
        for mdc_path, yaml_path in rule_pairs:
            result = self._validate_rule_pair(mdc_path, yaml_path)
            self.results.append(result)
        
        self.profiler.disable()
        
        # Generate report
        return self.generate_report(report_format, cycles)
    
    def _validate_rule_pair(self, mdc_path: Path, yaml_path: Path) -> ValidationResult:
        """Validate MDC rule with YAML metadata"""
        result = ValidationResult(rule_path=mdc_path)
        
        try:
            # Benchmark performance
            result.performance = self.benchmark_rule(mdc_path)
            
            # Load files
            with open(mdc_path) as f:
                mdc_content = f.read()
            with open(yaml_path) as f:
                metadata = yaml.safe_load(f)
            
            # Validation checks
            self._validate_metadata(metadata, result)
            self._validate_content(mdc_content, result)
            self._validate_performance_against_baseline(result)
            self._validate_dependencies_exist(metadata, result)
            self._validate_no_conflicts(metadata, result)
            
            # Generate fixes if needed
            if result.errors:
                result.suggested_fixes = self.suggest_fixes(
                    result.errors, metadata, mdc_content
                )
            
        except Exception as e:
            result.passed = False
            result.errors.append(f"Validation failed: {str(e)}")
        
        return result    
    def _parse_rule(self, content: str) -> Tuple[Dict, str]:
        """Parse rule content into metadata and body"""
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    metadata = yaml.safe_load(parts[1])
                    body = parts[2].strip()
                    return metadata, body
                except yaml.YAMLError:
                    # Failed to parse YAML, treat as if no frontmatter exists
                    pass
        return {}, content
    
    def _validate_metadata(self, metadata: Dict, result: ValidationResult) -> None:
        """Validate metadata fields"""
        # Check required fields
        for field in self.config['required_metadata']:
            if field not in metadata:
                result.passed = False
                result.errors.append(f"Missing required metadata field: {field}")
        
        # Validate version format
        if 'version' in metadata:
            version = metadata['version']
            if not re.match(r'^\d+\.\d+\.\d+$', str(version)):
                result.passed = False
                result.errors.append(f"Invalid version format: {version}")
        
        # Validate tags
        if 'tags' in metadata:
            invalid_tags = set(metadata['tags']) - set(self.config['approved_tags'])
            if invalid_tags:
                result.warnings.append(f"Unknown tags: {invalid_tags}")
    
    def _estimate_tokens(self, content: str) -> int:
        """Estimate token count for content"""
        # Rough estimation: 1 token ≈ 4 characters
        return len(content) // 4
    
    def _default_value_for_field(self, field: str) -> Any:
        """Provide default value for missing field"""
        defaults = {
            'version': '1.0.0',
            'author': 'Unknown',
            'created': datetime.now().strftime('%Y-%m-%d'),
            'last_modified': datetime.now().strftime('%Y-%m-%d'),
            'last_reviewed': datetime.now().strftime('%Y-%m-%d'),
            'tags': [],
            'performance': {
                'avg_tokens': 0,
                'p95_latency': 0,
                'success_rate': 0,
                'token_budget': 1000
            }
        }
        return defaults.get(field, '')    
    def _validate_content(self, content: str, result: ValidationResult) -> None:
        """Validate rule content"""
        lines = content.splitlines()
        line_count = len(lines)
        
        # Check line count
        if line_count > self.config['max_lines']:
            result.passed = False
            result.errors.append(f"Rule exceeds maximum lines: {line_count} > {self.config['max_lines']}")
        elif line_count > self.config['warn_lines']:
            result.warnings.append(f"Rule approaching size limit: {line_count} lines")
        
        # Check token estimate
        tokens = self._estimate_tokens(content)
        if tokens > self.config['max_tokens']:
            result.warnings.append(f"High token count: ~{tokens} tokens")
        
        result.metrics['line_count'] = line_count
        result.metrics['estimated_tokens'] = tokens
    
    def _validate_performance_against_baseline(self, result: ValidationResult) -> None:
        """Compare performance against baseline"""
        if not result.performance:
            return
        
        rule_name = result.rule_path.stem
        if rule_name in self.performance_baselines:
            baseline = self.performance_baselines[rule_name]
            perf = result.performance
            
            # Check for performance regression
            if perf.validation_time_ms > baseline.validation_time_ms * 1.5:
                result.warnings.append(
                    f"Performance regression: {perf.validation_time_ms:.1f}ms vs baseline {baseline.validation_time_ms:.1f}ms"
                )            
            if perf.token_count > baseline.token_count * 1.2:
                result.warnings.append(
                    f"Token increase: {perf.token_count} vs baseline {baseline.token_count}"
                )
    
    def _validate_dependencies_exist(self, metadata: Dict, result: ValidationResult) -> None:
        """Verify all dependencies exist"""
        if 'dependencies' not in metadata:
            return
        
        for dep in metadata['dependencies']:
            dep_path = self.rules_dir / dep
            if not dep_path.exists():
                result.passed = False
                result.errors.append(f"Dependency not found: {dep}")
    
    def _validate_no_conflicts(self, metadata: Dict, result: ValidationResult) -> None:
        """Check for unresolved conflicts"""
        if 'conflicts' not in metadata:
            return
        
        for conflict in metadata['conflicts']:
            if isinstance(conflict, dict) and 'resolution' not in conflict:
                result.warnings.append(f"Conflict without resolution strategy: {conflict.get('rule', conflict)}")
    
    def generate_report(self, format: str, cycles: List[List[str]] = None) -> Dict[str, Any]:
        """Generate validation report in specified format"""
        total_rules = len(self.results)
        passed_rules = sum(1 for r in self.results if r.passed)
        errors = sum(len(r.errors) for r in self.results)
        warnings = sum(len(r.warnings) for r in self.results)        
        report = {
            'timestamp': datetime.now().isoformat(),
            'success': errors == 0,
            'total_rules': total_rules,
            'valid_rules': passed_rules,
            'error_count': errors,
            'warning_count': warnings,
            'dependency_cycles': cycles or [],
            'results': [r.to_dict() for r in self.results]
        }
        
        # Add performance summary
        if any(r.performance for r in self.results):
            perf_data = [r.performance.to_dict() for r in self.results if r.performance]
            report['performance_summary'] = {
                'avg_validation_time_ms': sum(p['validation_time_ms'] for p in perf_data) / len(perf_data),
                'total_tokens': sum(p['token_count'] for p in perf_data),
                'largest_rule': max(perf_data, key=lambda p: p['line_count'])
            }
        
        # Add suggested fixes summary
        all_fixes = []
        for r in self.results:
            if r.suggested_fixes:
                all_fixes.extend([{
                    'rule': str(r.rule_path.name),
                    'fix': fix.to_dict()
                } for fix in r.suggested_fixes])
        
        if all_fixes:
            report['suggested_fixes'] = all_fixes        
        if format == 'json':
            return report
        elif format == 'html':
            return self._generate_html_report(report)
        else:
            return report
    
    def _generate_html_report(self, report: Dict) -> str:
        """Generate HTML report"""
        html = f"""
        <html>
        <head>
            <title>Rule Validation Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .success {{ color: green; }}
                .error {{ color: red; }}
                .warning {{ color: orange; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>Rule Validation Report</h1>
            <p>Generated: {report['timestamp']}</p>
            
            <h2>Summary</h2>
            <ul>
                <li>Total Rules: {report['total_rules']}</li>
                <li>Valid Rules: {report['valid_rules']}</li>
                <li>Errors: {report['error_count']}</li>
                <li>Warnings: {report['warning_count']}</li>
            </ul>            
            <h2>Results</h2>
            <table>
                <tr>
                    <th>Rule</th>
                    <th>Status</th>
                    <th>Issues</th>
                    <th>Performance</th>
                </tr>
        """
        
        for result in report['results']:
            status_class = 'success' if result['status'] == 'PASS' else 'error'
            issues = '<br>'.join(result['errors'] + result['warnings'])
            perf = result.get('performance', {})
            perf_text = f"{perf.get('validation_time_ms', 'N/A')}ms" if perf else 'N/A'
            
            html += f"""
                <tr>
                    <td>{result['rule']}</td>
                    <td class="{status_class}">{result['status']}</td>
                    <td>{issues}</td>
                    <td>{perf_text}</td>
                </tr>
            """
        
        html += """
            </table>
        </body>
        </html>
        """
        
        return html

def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate Cursor Rules")
    parser.add_argument('--all', action='store_true', help='Validate all rules')
    parser.add_argument('--rule', help='Validate specific rule')
    parser.add_argument('--report-format', choices=['json', 'html'], default='json')
    parser.add_argument('--output', help='Output file for report')
    
    args = parser.parse_args()
    
    rules_dir = Path(__file__).parent.parent / 'rules'
    validator = EnhancedRuleValidator(rules_dir)
    
    if args.all:
        report = validator.validate_all(args.report_format)
    elif args.rule:
        # Single rule validation
        rule_path = rules_dir / args.rule
        yaml_path = rule_path.with_suffix('.yaml')
        result = validator._validate_rule_pair(rule_path, yaml_path)
        report = {
            'success': result.passed,
            'results': [result.to_dict()]
        }
    else:
        parser.print_help()
        return
    
    # Output report
    if args.output:
        with open(args.output, 'w') as f:
            if args.report_format == 'json':
                json.dump(report, f, indent=2)
            else:
                f.write(report)
    else:
        if args.report_format == 'json':
            print(json.dumps(report, indent=2))
        else:
            print(report)


if __name__ == '__main__':
    main()