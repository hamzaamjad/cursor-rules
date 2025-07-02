#!/usr/bin/env python3
"""
Enhanced Rule Validation Script
Validates rule structure, dependencies, and interactions
"""

import os
import yaml
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
import networkx as nx
from collections import defaultdict

class RuleValidator:
    def __init__(self, rules_dir: str):
        self.rules_dir = Path(rules_dir)
        self.rules: Dict[str, Dict] = {}
        self.dependency_graph = nx.DiGraph()
        self.conflicts: List[Tuple[str, str, str]] = []
        self.warnings: List[str] = []
        self.errors: List[str] = []
        
    def load_rules(self):
        """Load all .mdc rule files"""
        for rule_file in self.rules_dir.rglob("*.mdc"):
            if "deprecated" in str(rule_file):
                continue
                
            try:
                with open(rule_file, 'r') as f:
                    content = f.read()
                    
                # Extract YAML frontmatter
                if content.startswith('---'):
                    yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
                    if yaml_match:
                        metadata = yaml.safe_load(yaml_match.group(1))
                    else:
                        metadata = {}
                else:
                    metadata = {}
                
                # Extract rule name from path
                relative_path = rule_file.relative_to(self.rules_dir)
                rule_name = str(relative_path).replace('.mdc', '')
                
                self.rules[rule_name] = {
                    'path': rule_file,
                    'metadata': metadata,
                    'content': content,
                    'category': relative_path.parts[0] if len(relative_path.parts) > 1 else 'root'
                }
                
            except Exception as e:
                self.errors.append(f"Failed to load {rule_file}: {e}")
    
    def extract_dependencies(self):
        """Extract dependencies from rule content and metadata"""
        for rule_name, rule_data in self.rules.items():
            # Check metadata dependencies
            metadata = rule_data['metadata']
            if 'dependencies' in metadata:
                for dep in metadata['dependencies']:
                    self.dependency_graph.add_edge(dep, rule_name)
            
            # Check content references
            content = rule_data['content']
            
            # Look for rule references in content
            rule_refs = re.findall(r'@Rule:([a-zA-Z0-9\-_.]+)', content)
            for ref in rule_refs:
                if ref in self.rules:
                    self.dependency_graph.add_edge(ref, rule_name)
            
            # Look for implicit dependencies
            if 'divergence-convergence' in content:
                self.dependency_graph.add_edge('103-divergence-convergence', rule_name)
            
            if 'internal_thought' in content and 'user_facing_response' in content:
                # Rule uses phase separation
                self.dependency_graph.add_edge('103-divergence-convergence', rule_name)
    
    def check_conflicts(self):
        """Identify potential rule conflicts"""
        conflict_patterns = [
            (['wildcard-brainstorm', 'concise-comms'], 'phase_separation'),
            (['ultrathink-prompting', 'sql-correctness'], 'context_based'),
            (['risk-checkpoint', 'wildcard-brainstorm'], 'risk_context'),
        ]
        
        for rules, resolution in conflict_patterns:
            present_rules = [r for r in rules if any(r in rn for rn in self.rules)]
            if len(present_rules) > 1:
                self.conflicts.append((present_rules[0], present_rules[1], resolution))
    
    def check_dependencies(self):
        """Validate dependency graph"""
        # Check for cycles
        try:
            cycles = list(nx.simple_cycles(self.dependency_graph))
            if cycles:
                for cycle in cycles:
                    self.errors.append(f"Circular dependency detected: {' -> '.join(cycle)}")
        except:
            pass
        
        # Check for missing dependencies
        for node in self.dependency_graph.nodes():
            if node not in self.rules and not node.startswith('@'):
                self.warnings.append(f"Missing dependency: {node}")
        
        # Check load order violations
        core_rules = [r for r in self.rules if r.startswith('000-core/')]
        cognitive_rules = [r for r in self.rules if r.startswith('100-cognitive/')]
        
        for cog_rule in cognitive_rules:
            for core_rule in core_rules:
                if self.dependency_graph.has_edge(cog_rule, core_rule):
                    self.errors.append(
                        f"Load order violation: cognitive rule {cog_rule} "
                        f"depends on core rule {core_rule}"
                    )
    
    def check_phase_consistency(self):
        """Ensure phase-based rules are consistent"""
        divergence_rules = []
        convergence_rules = []
        
        for rule_name, rule_data in self.rules.items():
            content = rule_data['content'].lower()
            
            if 'divergence phase' in content or 'divergent' in content:
                divergence_rules.append(rule_name)
            if 'convergence phase' in content or 'convergent' in content:
                convergence_rules.append(rule_name)
        
        # Check that divergence-convergence orchestrator exists if phases are used
        if (divergence_rules or convergence_rules) and \
           '103-divergence-convergence' not in self.rules:
            self.errors.append(
                "Phase-based rules found but divergence-convergence orchestrator missing"
            )
    
    def check_naming_conventions(self):
        """Validate rule naming conventions"""
        for rule_name, rule_data in self.rules.items():
            filename = Path(rule_name).name
            
            # Check kebab-case
            if not re.match(r'^[0-9]{3}-[a-z0-9\-]+$', filename):
                self.warnings.append(
                    f"Non-standard naming: {filename} "
                    "(expected: NNN-kebab-case)"
                )
            
            # Check category alignment
            category = rule_data['category']
            if category != 'root' and not filename.startswith(category[:3]):
                self.warnings.append(
                    f"Category mismatch: {filename} in {category}"
                )
    
    def generate_report(self) -> str:
        """Generate validation report"""
        report = []
        report.append("# Mirror Rules Validation Report\n")
        
        report.append(f"## Summary")
        report.append(f"- Total rules: {len(self.rules)}")
        report.append(f"- Dependencies: {self.dependency_graph.number_of_edges()}")
        report.append(f"- Conflicts: {len(self.conflicts)}")
        report.append(f"- Errors: {len(self.errors)}")
        report.append(f"- Warnings: {len(self.warnings)}\n")
        
        if self.errors:
            report.append("## ❌ Errors")
            for error in self.errors:
                report.append(f"- {error}")
            report.append("")
        
        if self.warnings:
            report.append("## ⚠️ Warnings")
            for warning in self.warnings:
                report.append(f"- {warning}")
            report.append("")
        
        if self.conflicts:
            report.append("## 🔄 Detected Conflicts")
            for rule1, rule2, resolution in self.conflicts:
                report.append(f"- {rule1} ↔ {rule2} (resolution: {resolution})")
            report.append("")
        
        # Dependency visualization
        report.append("## 📊 Dependency Graph")
        report.append("```mermaid")
        report.append("graph TD")
        
        # Group by category
        categories = defaultdict(list)
        for rule in self.rules:
            cat = self.rules[rule]['category']
            categories[cat].append(rule)
        
        for cat, rules in sorted(categories.items()):
            if rules:
                report.append(f"    subgraph {cat}")
                for rule in sorted(rules):
                    short_name = Path(rule).name
                    report.append(f"        {rule.replace('/', '_')}[\"{short_name}\"]")
                report.append("    end")
        
        # Add edges
        for source, target in self.dependency_graph.edges():
            src_safe = source.replace('/', '_').replace('-', '_')
            tgt_safe = target.replace('/', '_').replace('-', '_')
            report.append(f"    {src_safe} --> {tgt_safe}")
        
        report.append("```\n")
        
        # Token efficiency analysis
        report.append("## 📈 Token Efficiency Analysis")
        token_rules = ['105-context-trim', '106-concise-comms']
        for rule in token_rules:
            matching = [r for r in self.rules if rule in r]
            if matching:
                report.append(f"- {rule}: ✅ Present")
            else:
                report.append(f"- {rule}: ❌ Missing (performance impact)")
        
        return "\n".join(report)
    
    def validate(self):
        """Run all validations"""
        self.load_rules()
        self.extract_dependencies()
        self.check_conflicts()
        self.check_dependencies()
        self.check_phase_consistency()
        self.check_naming_conventions()
        
        return self.generate_report()

def main():
    """Main validation entry point"""
    rules_dir = "/Users/hamzaamjad/mirror/.cursor/rules"
    validator = RuleValidator(rules_dir)
    report = validator.validate()
    
    # Write report
    report_path = Path(rules_dir) / "VALIDATION_REPORT.md"
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"Validation complete. Report written to: {report_path}")
    
    # Exit with error code if errors found
    if validator.errors:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()
