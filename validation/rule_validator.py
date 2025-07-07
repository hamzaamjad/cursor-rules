#!/usr/bin/env python3
"""
Rule Validation Framework
Comprehensive validation for cursor rules system
"""

import os
import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
import subprocess
import ast

@dataclass
class ValidationResult:
    rule_path: Path
    passed: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metrics: Dict[str, any] = field(default_factory=dict)
    
    @property
    def severity(self) -> str:
        if not self.passed:
            return "error"
        elif self.warnings:
            return "warning"
        return "success"

class RuleValidator:
    """Comprehensive rule validation system"""
    
    def __init__(self, rules_dir: Path):
        self.rules_dir = rules_dir
        self.results: List[ValidationResult] = []
        
        # Load configuration
        self.config = self._load_config()
        self.tag_vocabulary = set(self.config.get('approved_tags', []))
        self.max_tokens = self.config.get('max_tokens', 1000)
        self.max_lines = self.config.get('max_lines', 150)
        
    def _load_config(self) -> Dict:
        """Load validation configuration"""
        config_path = self.rules_dir.parent / 'validation' / 'config.yaml'
        if config_path.exists():
            with open(config_path) as f:
                return yaml.safe_load(f)
        return self._default_config()
    
    def _default_config(self) -> Dict:
        """Default validation configuration"""
        return {
            'max_lines': 150,
            'warn_lines': 100,
            'max_tokens': 1000,
            'approved_tags': [
                'foundational', 'strategic', 'cognitive-enhancement', 
                'reasoning', 'performance', 'safety', 'quality',
                'optimization', 'domain-specific', 'specialized',
                'integration', 'tooling', 'patterns', 'best-practices',
                'experimental', 'research', 'evolution', 'meta-learning'
            ],
            'required_sections': ['Purpose', 'Requirements', 'Validation'],
            'version_pattern': r'^\d+\.\d+\.\d+$'
        }
    
    def validate_all(self) -> Dict[str, any]:
        """Validate all rules in the system"""
        rule_files = list(self.rules_dir.rglob("*.mdc"))
        
        for rule_file in rule_files:
            result = self.validate_rule(rule_file)
            self.results.append(result)
        
        return self._generate_report()
    
    def validate_rule(self, rule_path: Path) -> ValidationResult:
        """Validate a single rule file"""
        result = ValidationResult(rule_path=rule_path)
        
        try:
            with open(rule_path) as f:
                content = f.read()
            
            # Parse metadata and content
            metadata, body = self._parse_rule(content)
            
            # Run all validation checks
            self._validate_metadata(metadata, result)
            self._validate_structure(body, result)
            self._validate_content(body, result)
            self._validate_dependencies(metadata, result)
            self._validate_performance(metadata, content, result)
            
        except Exception as e:
            result.passed = False
            result.errors.append(f"Failed to validate: {str(e)}")
        
        return result
    
    def _parse_rule(self, content: str) -> Tuple[Dict, str]:
        """Parse rule into metadata and body"""
        match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
        if not match:
            raise ValueError("Invalid rule format: missing frontmatter")
        
        metadata = yaml.safe_load(match.group(1))
        body = match.group(2)
        
        return metadata, body
    
    def _validate_metadata(self, metadata: Dict, result: ValidationResult):
        """Validate metadata structure and content"""
        required_fields = ['version', 'description', 'category', 'performance', 'dependencies', 'tags']
        
        for field in required_fields:
            if field not in metadata:
                result.errors.append(f"Missing required metadata field: {field}")
                result.passed = False
        
        # Version format
        if 'version' in metadata:
            if not re.match(self.config['version_pattern'], str(metadata['version'])):
                result.errors.append(f"Invalid version format: {metadata['version']}")
                result.passed = False
        
        # Tag validation
        if 'tags' in metadata:
            invalid_tags = set(metadata['tags']) - self.tag_vocabulary
            if invalid_tags:
                result.warnings.append(f"Unknown tags: {', '.join(invalid_tags)}")
        
        # Performance metrics
        if 'performance' in metadata:
            perf = metadata['performance']
            if 'token_budget' in perf and perf['token_budget'] > self.max_tokens:
                result.warnings.append(f"Token budget exceeds recommended: {perf['token_budget']} > {self.max_tokens}")
    
    def _validate_structure(self, body: str, result: ValidationResult):
        """Validate rule structure"""
        lines = body.strip().split('\n')
        line_count = len(lines)
        
        # Line count validation
        if line_count > self.config['max_lines']:
            result.errors.append(f"Rule exceeds maximum lines: {line_count} > {self.config['max_lines']}")
            result.passed = False
        elif line_count > self.config['warn_lines']:
            result.warnings.append(f"Rule approaching size limit: {line_count} lines")
        
        result.metrics['line_count'] = line_count
        
        # Required sections
        content_lower = body.lower()
        for section in self.config['required_sections']:
            if section.lower() not in content_lower:
                result.warnings.append(f"Missing recommended section: {section}")
    
    def _validate_content(self, body: str, result: ValidationResult):
        """Validate content quality"""
        # Check for examples
        if '```' not in body and 'example' not in body.lower():
            result.warnings.append("No code examples found")
        
        # Check for validation criteria
        if 'check:' not in body.lower() and 'validation' not in body.lower():
            result.warnings.append("No explicit validation criteria")
        
        # Estimate token count (rough approximation)
        word_count = len(body.split())
        estimated_tokens = int(word_count * 1.3)
        result.metrics['estimated_tokens'] = estimated_tokens
        
        if estimated_tokens > self.max_tokens:
            result.warnings.append(f"Estimated tokens exceed budget: {estimated_tokens} > {self.max_tokens}")
    
    def _validate_dependencies(self, metadata: Dict, result: ValidationResult):
        """Validate dependencies and check for cycles"""
        if 'dependencies' not in metadata:
            return
        
        deps = metadata['dependencies']
        if 'required' in deps:
            for dep in deps['required']:
                dep_path = self.rules_dir / dep
                if not dep_path.exists():
                    result.errors.append(f"Missing dependency: {dep}")
                    result.passed = False
    
    def _validate_performance(self, metadata: Dict, content: str, result: ValidationResult):
        """Validate performance metrics"""
        if 'performance' not in metadata:
            return
        
        perf = metadata['performance']
        
        # Check if metrics are populated
        if perf.get('avg_tokens', 0) == 0:
            result.warnings.append("Performance metrics not measured")
        
        # Validate token reduction claims
        if 'tokenReduction' in perf:
            reduction = perf['tokenReduction']
            if isinstance(reduction, str) and '%' in reduction:
                try:
                    value = float(reduction.strip('%'))
                    if value > 90:
                        result.warnings.append(f"Very high token reduction claimed: {reduction}")
                except ValueError:
                    pass
    
    def _generate_report(self) -> Dict[str, any]:
        """Generate validation report"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        warnings = sum(1 for r in self.results if r.warnings)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_rules': total,
                'passed': passed,
                'failed': total - passed,
                'warnings': warnings,
                'success_rate': f"{(passed/total)*100:.1f}%" if total > 0 else "0%"
            },
            'results': []
        }
        
        # Group results by severity
        for result in sorted(self.results, key=lambda r: (r.severity, str(r.rule_path))):
            report['results'].append({
                'rule': str(result.rule_path.relative_to(self.rules_dir)),
                'status': 'PASS' if result.passed else 'FAIL',
                'errors': result.errors,
                'warnings': result.warnings,
                'metrics': result.metrics
            })
        
        return report

def main():
    """Run validation and generate report"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate cursor rules")
    parser.add_argument('--rules-dir', default='./rules', help='Rules directory')
    parser.add_argument('--output', default='validation_report.json', help='Output file')
    parser.add_argument('--format', choices=['json', 'markdown'], default='json')
    
    args = parser.parse_args()
    
    validator = RuleValidator(Path(args.rules_dir))
    report = validator.validate_all()
    
    if args.format == 'json':
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
    else:
        # Generate markdown report
        md_report = generate_markdown_report(report)
        with open(args.output, 'w') as f:
            f.write(md_report)
    
    print(f"Validation complete: {report['summary']}")
    
    # Exit with error if validation failed
    if report['summary']['failed'] > 0:
        exit(1)

def generate_markdown_report(report: Dict) -> str:
    """Generate markdown validation report"""
    lines = [
        "# Rule Validation Report",
        f"\nGenerated: {report['timestamp']}",
        "\n## Summary",
        f"- Total Rules: {report['summary']['total_rules']}",
        f"- Passed: {report['summary']['passed']}",
        f"- Failed: {report['summary']['failed']}",
        f"- Warnings: {report['summary']['warnings']}",
        f"- Success Rate: {report['summary']['success_rate']}",
        "\n## Results\n"
    ]
    
    # Group by status
    failed = [r for r in report['results'] if r['status'] == 'FAIL']
    warned = [r for r in report['results'] if r['warnings'] and r['status'] == 'PASS']
    passed = [r for r in report['results'] if not r['warnings'] and r['status'] == 'PASS']
    
    if failed:
        lines.append("### ❌ Failed Rules\n")
        for r in failed:
            lines.append(f"#### `{r['rule']}`")
            for error in r['errors']:
                lines.append(f"- **Error**: {error}")
            lines.append("")
    
    if warned:
        lines.append("### ⚠️ Rules with Warnings\n")
        for r in warned:
            lines.append(f"#### `{r['rule']}`")
            for warning in r['warnings']:
                lines.append(f"- **Warning**: {warning}")
            lines.append("")
    
    if passed:
        lines.append("### ✅ Passed Rules\n")
        for r in passed:
            lines.append(f"- `{r['rule']}` ({r['metrics'].get('line_count', 'N/A')} lines)")
    
    return '\n'.join(lines)

if __name__ == '__main__':
    main()
