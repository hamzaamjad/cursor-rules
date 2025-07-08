#!/usr/bin/env python3
"""Simplified rule benchmarking without external dependencies"""

import os
import json
import time
from pathlib import Path
from datetime import datetime

def benchmark_rule(rule_path):
    """Benchmark a single rule file"""
    start_time = time.time()
    
    # Read file
    with open(rule_path, 'r') as f:
        content = f.read()
    
    read_time = time.time() - start_time
    
    # Parse YAML header
    parse_start = time.time()
    lines = content.split('\n')
    in_header = False
    header_lines = []
    
    for line in lines:
        if line.strip() == '---':
            in_header = not in_header
            continue
        if in_header:
            header_lines.append(line)
    
    parse_time = time.time() - parse_start
    
    # Calculate metrics
    file_size = os.path.getsize(rule_path)
    line_count = len(lines)
    token_estimate = len(content) // 4  # Simple estimation
    
    return {
        'rule_name': Path(rule_path).stem,
        'rule_path': str(rule_path),
        'load_time_ms': read_time * 1000,
        'parse_time_ms': parse_time * 1000,
        'validation_time_ms': (read_time + parse_time) * 1000,
        'token_count': token_estimate,
        'line_count': line_count,
        'file_size_bytes': file_size,
        'timestamp': datetime.now().isoformat()
    }

def main():
    rules_dir = Path('/Users/hamzaamjad/cursor-rules/rules')
    
    # Benchmark original (from deprecated)
    original_path = rules_dir / '900-deprecated' / '427-stigmergic-workflows-v2.mdc'
    if original_path.exists():
        original_result = benchmark_rule(original_path)
        print(f"Original: {original_result['validation_time_ms']:.2f}ms, {original_result['token_count']} tokens")
    
    # Benchmark optimized modules
    optimized_results = []
    for module in ['427-stigmergic-core', '427-stigmergic-markers', '427-stigmergic-artifacts']:
        module_path = rules_dir / '400-patterns' / f'{module}.mdc'
        if module_path.exists():
            result = benchmark_rule(module_path)
            optimized_results.append(result)
            print(f"{module}: {result['validation_time_ms']:.2f}ms, {result['token_count']} tokens")
    
    # Calculate totals
    total_time = sum(r['validation_time_ms'] for r in optimized_results)
    total_tokens = sum(r['token_count'] for r in optimized_results)
    
    print(f"\nOptimized total: {total_time:.2f}ms, {total_tokens} tokens")
    print(f"Improvement: {((original_result['validation_time_ms'] - total_time) / original_result['validation_time_ms']) * 100:.1f}% faster")
    print(f"Token reduction: {((original_result['token_count'] - total_tokens) / original_result['token_count']) * 100:.1f}%")
    
    # Save results
    with open('benchmark_results.json', 'w') as f:
        json.dump({
            'original': original_result,
            'optimized': optimized_results,
            'summary': {
                'time_improvement_percent': ((original_result['validation_time_ms'] - total_time) / original_result['validation_time_ms']) * 100,
                'token_reduction_percent': ((original_result['token_count'] - total_tokens) / original_result['token_count']) * 100
            }
        }, f, indent=2)

if __name__ == '__main__':
    main()