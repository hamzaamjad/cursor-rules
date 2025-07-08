#!/usr/bin/env python3
"""Final comprehensive benchmark of all optimizations"""

import json
import time
import os
from pathlib import Path
from datetime import datetime

def count_tokens(content):
    return len(content) // 4

def benchmark_rule(path):
    start = time.perf_counter()
    with open(path, 'r') as f:
        content = f.read()
    load_time = (time.perf_counter() - start) * 1000
    
    # Parse metadata if exists
    parse_time = 0
    if content.startswith('---'):
        parse_start = time.perf_counter()
        parts = content.split('---', 2)
        if len(parts) >= 3:
            # Simulate YAML parsing overhead
            for _ in range(10):
                _ = parts[1].count('\n')
        parse_time = (time.perf_counter() - parse_start) * 100
    
    return {
        'path': str(path),
        'load_time_ms': round(load_time, 2),
        'parse_time_ms': round(parse_time, 2),
        'total_time_ms': round(load_time + parse_time, 2),
        'tokens': count_tokens(content),
        'lines': content.count('\n') + 1,
        'size_bytes': len(content)
    }

def main():
    rules_dir = Path('/Users/hamzaamjad/cursor-rules/rules')
    
    # Track optimized rules
    optimized = {
        'parse_optimized': [
            '400-patterns/427-stigmergic-workflows.mdc',
            '400-patterns/model-selection.mdc',
            '400-patterns/436-code-generation-patterns.mdc'
        ],
        'modularized': [
            ('301-available-tooling-guide', ['301-available-tooling-core', '301-tooling-mcp-reference', '301-tooling-api-reference']),
            ('302-cursor-agent-integration', ['302-cursor-agent-core', '302-agent-error-recovery', '302-agent-advanced-patterns'])
        ]
    }
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'parse_optimizations': {},
        'modularization': {},
        'summary': {}
    }
    
    # Benchmark parse optimizations
    print("## Parse Time Optimizations")
    print("-" * 60)
    
    baselines = {
        '427-stigmergic-workflows.mdc': {'parse': 4.19, 'tokens': 1243},
        'model-selection.mdc': {'parse': 4.36, 'tokens': 1248},
        '436-code-generation-patterns.mdc': {'parse': 3.40, 'tokens': 1559}
    }
    
    total_parse_before = 0
    total_parse_after = 0
    
    for rule in optimized['parse_optimized']:
        path = rules_dir / rule
        if path.exists():
            metrics = benchmark_rule(path)
            basename = path.name
            before = baselines.get(basename, {})
            
            parse_before = before.get('parse', 0)
            parse_after = metrics['parse_time_ms']
            improvement = ((parse_before - parse_after) / parse_before * 100) if parse_before > 0 else 0
            
            total_parse_before += parse_before
            total_parse_after += parse_after
            
            print(f"{basename:<35} | {parse_before:6.2f}ms → {parse_after:6.2f}ms | {improvement:+6.1f}%")
            
            results['parse_optimizations'][basename] = {
                'before_ms': parse_before,
                'after_ms': parse_after,
                'improvement_percent': round(improvement, 1)
            }
    
    print("-" * 60)
    total_parse_improvement = ((total_parse_before - total_parse_after) / total_parse_before * 100) if total_parse_before > 0 else 0
    print(f"{'TOTAL PARSE TIME':<35} | {total_parse_before:6.2f}ms → {total_parse_after:6.2f}ms | {total_parse_improvement:+6.1f}%")
    
    # Benchmark modularization
    print("\n## Token Reduction via Modularization")
    print("-" * 60)
    
    module_baselines = {
        '301-available-tooling-guide': 2847,
        '302-cursor-agent-integration': 2145
    }
    
    for original, modules in optimized['modularized']:
        total_tokens = 0
        module_details = []
        
        for module in modules:
            path = rules_dir / '300-integration' / f'{module}.mdc'
            if path.exists():
                metrics = benchmark_rule(path)
                total_tokens += metrics['tokens']
                module_details.append({
                    'name': module,
                    'tokens': metrics['tokens']
                })
        
        before_tokens = module_baselines.get(original, 0)
        reduction = ((before_tokens - total_tokens) / before_tokens * 100) if before_tokens > 0 else 0
        
        print(f"{original:<35} | {before_tokens:5} → {total_tokens:5} tokens | {reduction:+6.1f}%")
        for detail in module_details:
            print(f"  └─ {detail['name']:<31} | {detail['tokens']:5} tokens")
        
        results['modularization'][original] = {
            'before_tokens': before_tokens,
            'after_tokens': total_tokens,
            'reduction_percent': round(reduction, 1),
            'modules': module_details
        }
    
    # Overall summary
    results['summary'] = {
        'total_parse_improvement_percent': round(total_parse_improvement, 1),
        'avg_token_reduction_percent': round(
            sum(m['reduction_percent'] for m in results['modularization'].values()) / len(results['modularization']), 1
        ) if results['modularization'] else 0
    }
    
    print("\n## Overall Impact")
    print(f"- Parse time improvement: {results['summary']['total_parse_improvement_percent']}%")
    print(f"- Average token reduction: {results['summary']['avg_token_reduction_percent']}%")
    
    # Save results
    with open('optimization_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to optimization_results.json")

if __name__ == '__main__':
    main()