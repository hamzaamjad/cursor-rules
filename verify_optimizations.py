#!/usr/bin/env python3
"""Verify metadata parsing optimizations"""

import yaml
import time
import logging
from pathlib import Path

def benchmark_yaml_parse(file_path):
    """Measure YAML metadata parsing time"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract metadata section
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            metadata_str = parts[1]
        else:
            return None, 0
    else:
        return None, 0
    
    # Benchmark parsing
    start = time.perf_counter()
    for _ in range(100):  # Run 100 times for accuracy
        metadata = yaml.safe_load(metadata_str)
    elapsed = (time.perf_counter() - start) / 100 * 1000  # ms per parse
    
    return metadata, elapsed

def main():
    rules_dir = Path('/Users/hamzaamjad/cursor-rules/rules')
    
    # Test optimized rules
    test_rules = [
        '400-patterns/427-stigmergic-workflows.mdc',
        '400-patterns/model-selection.mdc', 
        '400-patterns/436-code-generation-patterns.mdc'
    ]
    
    results = []
    for rule_path in test_rules:
        full_path = rules_dir / rule_path
        if full_path.exists():
            metadata, parse_time = benchmark_yaml_parse(full_path)
            results.append({
                'rule': rule_path.split('/')[-1],
                'parse_time_ms': round(parse_time, 2),
                'has_metadata': metadata is not None
            })
            logging.info(f"{rule_path.split('/')[-1]}: {parse_time:.2f}ms")
    
    # Compare with baseline
    logging.info("\nOptimization Results:")
    logging.info("Rule                          | Before | After | Improvement")
    logging.info("-" * 60)
    
    baselines = {
        '427-stigmergic-workflows.mdc': 4.19,
        'model-selection.mdc': 4.36,
        '436-code-generation-patterns.mdc': 3.40
    }
    
    total_before = 0
    total_after = 0
    
    for result in results:
        rule = result['rule']
        before = baselines.get(rule, 0)
        after = result['parse_time_ms']
        improvement = ((before - after) / before * 100) if before > 0 else 0
        
        total_before += before
        total_after += after
        
        logging.info(f"{rule:<30} | {before:5.2f} | {after:5.2f} | {improvement:+6.1f}%")
    
    logging.info("-" * 60)
    total_improvement = ((total_before - total_after) / total_before * 100) if total_before > 0 else 0
    logging.info(f"{'TOTAL':<30} | {total_before:5.2f} | {total_after:5.2f} | {total_improvement:+6.1f}%")

if __name__ == '__main__':
    main()