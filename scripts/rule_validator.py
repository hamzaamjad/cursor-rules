#!/usr/bin/env python3
"""Rule validation system for cursor rules"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Set
import re


class ValidationError(Exception):
    pass


class CircularDependencyError(ValidationError):
    pass


class RuleValidator:
    def __init__(self, rules_dir: str):
        self.rules_dir = Path(rules_dir)
        if not self.rules_dir.exists():
            self.rules_dir.mkdir(parents=True)
        
        # Ensure .cursorrules subdirectory exists
        cursorrules_dir = self.rules_dir / '.cursorrules'
        if not cursorrules_dir.exists():
            cursorrules_dir.mkdir()
    
    def _parse_yaml_metadata(self, rule_path: str) -> Dict[str, Any]:
        """Parse YAML frontmatter from rule file"""
        try:
            with open(rule_path, 'r') as f:
                content = f.read()
            
            if not content.startswith('---'):
                return {}
            
            parts = content.split('---', 2)
            if len(parts) < 3:
                return {}
            
            return yaml.safe_load(parts[1]) or {}
        except Exception:
            return {}
    
    def _validate_structure(self, rule_path: str) -> Dict[str, Any]:
        """Validate rule structure and content"""
        result = {
            'valid': True,
            'has_metadata': False,
            'has_purpose': False,
            'has_requirements': False,
            'has_validation': False,
            'has_examples': False,
            'warnings': []
        }
        
        try:
            with open(rule_path, 'r') as f:
                content = f.read()
            
            # Check metadata
            if content.startswith('---'):
                result['has_metadata'] = True
            
            # Check sections
            result['has_purpose'] = '* **Purpose**:' in content or '**Purpose**:' in content
            result['has_requirements'] = '* **Requirements**:' in content
            result['has_validation'] = '* **Validation**:' in content
            result['has_examples'] = '<example' in content.lower()
            
            # Generate warnings
            if not result['has_purpose']:
                result['warnings'].append('Missing Purpose section')
            if not result['has_examples']:
                result['warnings'].append('Missing Examples section')
            
        except Exception as e:
            result['valid'] = False
            result['warnings'].append(f'Error reading file: {e}')
        
        return result
    
    def _count_tokens(self, text: str) -> int:
        """Approximate token count"""
        # Simple approximation: ~4 chars per token
        return len(text) // 4
    
    def _build_dependency_graph(self) -> Dict[str, List[str]]:
        """Build dependency graph from all rules"""
        graph = {}
        
        for rule_file in self.rules_dir.rglob('*.mdc'):
            metadata = self._parse_yaml_metadata(str(rule_file))
            rule_name = str(rule_file.relative_to(self.rules_dir))
            
            dependencies = metadata.get('dependencies', [])
            graph[rule_name] = dependencies
        
        return graph
    
    def _has_circular_dependencies(self, graph: Dict[str, List[str]]) -> List[List[str]]:
        """Detect circular dependencies using DFS"""
        cycles = []
        
        def dfs(node: str, stack: List[str], visited: Set[str], rec_stack: Set[str]):
            visited.add(node)
            rec_stack.add(node)
            stack.append(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor, stack[:], visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_start = stack.index(neighbor)
                    cycles.append(stack[cycle_start:] + [neighbor])
            
            rec_stack.remove(node)
            return False
        
        visited = set()
        for node in graph:
            if node not in visited:
                dfs(node, [], visited, set())
        
        return cycles
    
    def _validate_performance(self, rule_path: str, content: str, 
                            line_count: int, token_count: int) -> Dict[str, Any]:
        """Validate performance metrics"""
        result = {
            'within_limits': True,
            'line_count': line_count,
            'token_count': token_count,
            'warnings': []
        }
        
        if line_count > 150:
            result['within_limits'] = False
            result['warnings'].append(f'Exceeds line limit: {line_count} > 150')
        
        if token_count > 1500:
            result['warnings'].append(f'High token count: {token_count}')
        
        return result
    
    def validate_single(self, rule_path: str) -> Dict[str, Any]:
        """Validate a single rule file"""
        with open(rule_path, 'r') as f:
            content = f.read()
        
        lines = content.splitlines()
        line_count = len(lines)
        token_count = self._count_tokens(content)
        
        metadata = self._parse_yaml_metadata(rule_path)
        structure = self._validate_structure(rule_path)
        performance = self._validate_performance(rule_path, content, line_count, token_count)
        
        # Check dependencies exist
        dep_issues = []
        for dep in metadata.get('dependencies', []):
            dep_path = self.rules_dir / dep
            if not dep_path.exists():
                dep_issues.append(f'Missing dependency: {dep}')
        
        return {
            'valid': structure['valid'] and performance['within_limits'] and not dep_issues,
            'rule_path': rule_path,
            'metadata': metadata,
            'structure': structure,
            'performance': performance,
            'dependencies': {'issues': dep_issues}
        }
    
    def validate_all(self) -> Dict[str, Any]:
        """Validate all rules in directory"""
        results = {
            'total_rules': 0,
            'valid_rules': 0,
            'total_warnings': 0,
            'total_errors': 0,
            'rules': {}
        }
        
        for rule_file in self.rules_dir.rglob('*.mdc'):
            results['total_rules'] += 1
            
            validation = self.validate_single(str(rule_file))
            rule_name = str(rule_file.relative_to(self.rules_dir))
            results['rules'][rule_name] = validation
            
            if validation['valid']:
                results['valid_rules'] += 1
            
            # Count warnings
            warnings = validation['structure'].get('warnings', [])
            warnings += validation['performance'].get('warnings', [])
            results['total_warnings'] += len(warnings)
            
            # Count errors
            if not validation['valid']:
                results['total_errors'] += 1
        
        # Check for circular dependencies
        graph = self._build_dependency_graph()
        cycles = self._has_circular_dependencies(graph)
        if cycles:
            results['circular_dependencies'] = cycles
            results['total_errors'] += len(cycles)
        
        return results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate cursor rules")
    parser.add_argument('--rules-dir', default='.cursorrules', help='Rules directory')
    parser.add_argument('--single', help='Validate single rule file')
    
    args = parser.parse_args()
    
    validator = RuleValidator(args.rules_dir)
    
    if args.single:
        result = validator.validate_single(args.single)
        print(json.dumps(result, indent=2))
    else:
        results = validator.validate_all()
        print(f"Total rules: {results['total_rules']}")
        print(f"Valid rules: {results['valid_rules']}")
        print(f"Warnings: {results['total_warnings']}")
        print(f"Errors: {results['total_errors']}")
        
        if 'circular_dependencies' in results:
            print(f"\nCircular dependencies detected: {len(results['circular_dependencies'])}")


if __name__ == '__main__':
    main()
