#!/usr/bin/env python3
"""
Rule Loader with YAML-first strategy
Supports both separated and legacy frontmatter formats
"""

import re
import yaml
from pathlib import Path
from typing import Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Rule:
    """Rule with metadata and content"""
    path: Path
    metadata: Dict
    content: str
    
    @property
    def name(self) -> str:
        return self.path.stem
    
    @property
    def category(self) -> str:
        return self.metadata.get('category', 'unknown')
    
    @property
    def version(self) -> str:
        return self.metadata.get('version', '0.0.0')
    
    @property
    def tokens(self) -> int:
        """Estimate token count"""
        return len(self.content.split()) * 1.3

class RuleLoader:
    """Load rules with YAML-first strategy"""
    
    def __init__(self, rules_dir: Path):
        self.rules_dir = Path(rules_dir)
        self._cache = {}
        
    def load_rule(self, rule_path: Path) -> Rule:
        """Load rule with metadata from YAML or frontmatter"""
        if rule_path in self._cache:
            return self._cache[rule_path]
            
        yaml_path = rule_path.with_suffix('.yaml')
        
        # YAML-first strategy
        if yaml_path.exists():
            metadata = self._load_yaml(yaml_path)
            content = rule_path.read_text()
        else:
            # Fallback to frontmatter
            full_content = rule_path.read_text()
            metadata, content = self._parse_frontmatter(full_content)
        
        rule = Rule(path=rule_path, metadata=metadata, content=content)
        self._cache[rule_path] = rule
        return rule
    
    def _load_yaml(self, yaml_path: Path) -> Dict:
        """Load metadata from YAML file"""
        with open(yaml_path) as f:
            return yaml.safe_load(f) or {}
    
    def _parse_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """Parse frontmatter from content"""
        match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
        if match:
            metadata = yaml.safe_load(match.group(1)) or {}
            body = match.group(2).strip()
            return metadata, body
        return {}, content
    
    def load_all(self) -> Dict[str, Rule]:
        """Load all rules in the system"""
        rules = {}
        for rule_file in self.rules_dir.rglob("*.mdc"):
            rule = self.load_rule(rule_file)
            rules[rule.name] = rule
        return rules
    
    def load_category(self, category: str) -> Dict[str, Rule]:
        """Load all rules in a category"""
        category_path = self.rules_dir / category
        if not category_path.exists():
            return {}
            
        rules = {}
        for rule_file in category_path.glob("*.mdc"):
            rule = self.load_rule(rule_file)
            rules[rule.name] = rule
        return rules
    
    def search_by_tag(self, tag: str) -> Dict[str, Rule]:
        """Find rules with specific tag"""
        matching = {}
        for rule_file in self.rules_dir.rglob("*.mdc"):
            rule = self.load_rule(rule_file)
            if tag in rule.metadata.get('tags', []):
                matching[rule.name] = rule
        return matching
    
    def get_dependency_graph(self) -> Dict[str, set]:
        """Build dependency graph"""
        graph = {}
        all_rules = self.load_all()
        
        for name, rule in all_rules.items():
            deps = set()
            if 'dependencies' in rule.metadata:
                deps_meta = rule.metadata['dependencies']
                if 'required' in deps_meta:
                    deps.update(deps_meta['required'])
                if 'recommended' in deps_meta:
                    deps.update(deps_meta['recommended'])
            graph[name] = deps
        
        return graph

# CLI interface
def main():
    import argparse
    import json
    
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['list', 'show', 'stats', 'deps'])
    parser.add_argument('--rule', help='Rule name for show command')
    parser.add_argument('--category', help='Filter by category')
    parser.add_argument('--tag', help='Filter by tag')
    parser.add_argument('--format', choices=['json', 'yaml', 'text'], default='text')
    args = parser.parse_args()
    
    loader = RuleLoader(Path('./rules'))
    
    if args.command == 'list':
        if args.category:
            rules = loader.load_category(args.category)
        elif args.tag:
            rules = loader.search_by_tag(args.tag)
        else:
            rules = loader.load_all()
            
        for name in sorted(rules.keys()):
            print(f"{name}: v{rules[name].version}")
    
    elif args.command == 'show':
        if not args.rule:
            print("Error: --rule required for show command")
            return
            
        rules = loader.load_all()
        if args.rule in rules:
            rule = rules[args.rule]
            if args.format == 'json':
                print(json.dumps({
                    'name': rule.name,
                    'metadata': rule.metadata,
                    'content': rule.content
                }, indent=2))
            else:
                print(f"=== {rule.name} ===")
                print(f"Version: {rule.version}")
                print(f"Category: {rule.category}")
                print(f"\n{rule.content}")
    
    elif args.command == 'stats':
        rules = loader.load_all()
        total_tokens = sum(r.tokens for r in rules.values())
        
        stats = {
            'total_rules': len(rules),
            'total_tokens': int(total_tokens),
            'avg_tokens': int(total_tokens / len(rules)) if rules else 0,
            'categories': {}
        }
        
        for rule in rules.values():
            cat = rule.category
            if cat not in stats['categories']:
                stats['categories'][cat] = 0
            stats['categories'][cat] += 1
        
        print(json.dumps(stats, indent=2))
    
    elif args.command == 'deps':
        graph = loader.get_dependency_graph()
        if args.format == 'json':
            # Convert sets to lists for JSON
            json_graph = {k: list(v) for k, v in graph.items()}
            print(json.dumps(json_graph, indent=2))
        else:
            for rule, deps in sorted(graph.items()):
                if deps:
                    print(f"{rule}:")
                    for dep in sorted(deps):
                        print(f"  → {dep}")

if __name__ == '__main__':
    main()
