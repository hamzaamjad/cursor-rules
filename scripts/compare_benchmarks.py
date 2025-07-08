#!/usr/bin/env python3
"""Compare benchmark results and generate markdown report"""

import json
import sys
from pathlib import Path
from typing import Dict, Any

def load_metrics(filepath: str) -> Dict[str, Any]:
    """Load benchmark metrics from JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)

def compare_metrics(baseline: Dict, current: Dict) -> str:
    """Generate markdown comparison report"""
    report = ["# 📊 Performance Comparison Report\n"]
    
    # Track changes
    improvements = []
    regressions = []
    new_rules = []
    
    # Compare each rule
    for rule_name, current_metrics in current.items():
        if rule_name not in baseline:
            new_rules.append(rule_name)
            continue
        
        base_metrics = baseline[rule_name]
        
        # Calculate deltas
        token_delta = current_metrics['token_count'] - base_metrics['token_count']
        time_delta = current_metrics['validation_time_ms'] - base_metrics['validation_time_ms']
        
        # Percentage changes
        token_pct = (token_delta / base_metrics['token_count'] * 100) if base_metrics.get('token_count', 0) > 0 else 0
        time_pct = (time_delta / base_metrics['validation_time_ms'] * 100) if base_metrics.get('validation_time_ms', 0) > 0 else 0
        
        # Categorize changes
        if token_pct > 10 or time_pct > 20:
            regressions.append({
                'rule': rule_name,
                'token_delta': token_delta,
                'token_pct': token_pct,
                'time_delta': time_delta,
                'time_pct': time_pct
            })
        elif token_pct < -10 or time_pct < -20:
            improvements.append({
                'rule': rule_name,
                'token_delta': token_delta,
                'token_pct': token_pct,
                'time_delta': time_delta,
                'time_pct': time_pct
            })
    
    # Summary section
    report.append("## Summary\n")
    report.append(f"- **Improvements**: {len(improvements)} rules")
    report.append(f"- **Regressions**: {len(regressions)} rules")
    report.append(f"- **New Rules**: {len(new_rules)} rules\n")
    
    # Improvements
    if improvements:
        report.append("## ✅ Improvements\n")
        report.append("| Rule | Token Change | Time Change |")
        report.append("|------|--------------|-------------|")
        for imp in sorted(improvements, key=lambda x: x['token_pct']):
            report.append(f"| {imp['rule']} | {imp['token_delta']:+d} ({imp['token_pct']:+.1f}%) | {imp['time_delta']:+.1f}ms ({imp['time_pct']:+.1f}%) |")
        report.append("")
    
    # Regressions
    if regressions:
        report.append("## ⚠️ Performance Regressions\n")
        report.append("| Rule | Token Change | Time Change |")
        report.append("|------|--------------|-------------|")
        for reg in sorted(regressions, key=lambda x: x['token_pct'], reverse=True):
            report.append(f"| {reg['rule']} | {reg['token_delta']:+d} ({reg['token_pct']:+.1f}%) | {reg['time_delta']:+.1f}ms ({reg['time_pct']:+.1f}%) |")
        report.append("")
    
    # New rules
    if new_rules:
        report.append("## 🆕 New Rules\n")
        for rule in sorted(new_rules):
            metrics = current[rule]
            report.append(f"- **{rule}**: {metrics['token_count']} tokens, {metrics['validation_time_ms']:.1f}ms")
        report.append("")
    
    # Overall metrics
    report.append("## 📈 Overall Metrics\n")
    
    baseline_total_tokens = sum(m.get('token_count', 0) for m in baseline.values())
    current_total_tokens = sum(m.get('token_count', 0) for m in current.values())
    
    report.append(f"- **Total Tokens**: {baseline_total_tokens:,} → {current_total_tokens:,} "
                  f"({current_total_tokens - baseline_total_tokens:+,} / "
                  f"{(current_total_tokens - baseline_total_tokens) / baseline_total_tokens * 100:+.1f}%)")
    
    baseline_avg_time = sum(m.get('validation_time_ms', 0) for m in baseline.values()) / len(baseline)
    current_avg_time = sum(m.get('validation_time_ms', 0) for m in current.values()) / len(current)
    
    report.append(f"- **Avg Validation Time**: {baseline_avg_time:.1f}ms → {current_avg_time:.1f}ms "
                  f"({current_avg_time - baseline_avg_time:+.1f}ms)")
    
    return "\n".join(report)

def main():
    if len(sys.argv) != 3:
        print("Usage: compare_benchmarks.py <baseline.json> <current.json>")
        sys.exit(1)
    
    baseline_path = sys.argv[1]
    current_path = sys.argv[2]
    
    baseline = load_metrics(baseline_path)
    current = load_metrics(current_path)
    
    report = compare_metrics(baseline, current)
    print(report)

if __name__ == '__main__':
    main()