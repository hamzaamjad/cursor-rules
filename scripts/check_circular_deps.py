#!/usr/bin/env python3
"""Check for circular dependencies in rule metadata"""

from pathlib import Path
import yaml
import sys

def check_circular_dependencies():
    rules_dir = Path('rules')
    dependency_graph = {}
    
    # Build dependency graph
    for yaml_file in rules_dir.rglob('*.yaml'):
        with open(yaml_file) as f:
            meta = yaml.safe_load(f)
            if meta and 'dependencies' in meta:
                rule_name = yaml_file.stem
                dependency_graph[rule_name] = [Path(dep).stem for dep in meta['dependencies']]
    
    # Check for cycles using DFS
    def has_cycle(graph):
        visited = set()
        rec_stack = set()
        
        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            
            for dep in graph.get(node, []):
                if dep not in visited:
                    if dfs(dep):
                        return True
                elif dep in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in graph:
            if node not in visited:
                if dfs(node):
                    return True
        return False
    
    if has_cycle(dependency_graph):
        print('ERROR: Circular dependencies detected!')
        sys.exit(1)
    else:
        print('✓ No circular dependencies found')

if __name__ == '__main__':
    check_circular_dependencies()
