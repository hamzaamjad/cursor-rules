#!/usr/bin/env python3
"""
Rule Performance Benchmarking System
Measures timing, memory, and token metrics for all rules
"""

import os
import json
import time
import psutil
import tracemalloc
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import yaml
import argparse
import subprocess

@dataclass
class BenchmarkResult:
    rule_name: str
    rule_path: str
    load_time_ms: float
    parse_time_ms: float
    token_count: int
    line_count: int
    file_size_bytes: int
    memory_usage_kb: float
    timestamp: str
    
    def to_dict(self) -> Dict:
        return asdict(self)

class RuleBenchmarker:
    def __init__(self, rules_dir: Path):
        self.rules_dir = rules_dir
        self.results: List[BenchmarkResult] = []
        self.process = psutil.Process()
    
    def estimate_tokens(self, content: str) -> int:
        """Estimate token count using tiktoken or fallback"""
        try:
            import tiktoken
            enc = tiktoken.encoding_for_model("gpt-4")
            return len(enc.encode(content))
        except ImportError:
            # Fallback: ~4 chars per token
            return len(content) // 4
    
    def benchmark_rule(self, mdc_path: Path) -> BenchmarkResult:
        """Benchmark single rule performance"""
        tracemalloc.start()
        start_memory = tracemalloc.get_traced_memory()[0]
        
        # Load timing
        load_start = time.perf_counter()
        with open(mdc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        load_time = (time.perf_counter() - load_start) * 1000
        
        # Parse timing
        parse_start = time.perf_counter()
        yaml_path = mdc_path.with_suffix('.yaml')
        if yaml_path.exists():
            with open(yaml_path, 'r', encoding='utf-8') as f:
                metadata = yaml.safe_load(f)
        else:
            metadata = {}
        parse_time = (time.perf_counter() - parse_start) * 1000
        
        # Metrics
        lines = content.count('\n') + 1
        tokens = self.estimate_tokens(content)
        file_size = mdc_path.stat().st_size
        
        # Memory usage
        end_memory = tracemalloc.get_traced_memory()[0]
        memory_used = (end_memory - start_memory) / 1024  # KB
        tracemalloc.stop()
        
        return BenchmarkResult(
            rule_name=mdc_path.stem,
            rule_path=str(mdc_path.relative_to(self.rules_dir)),
            load_time_ms=round(load_time, 2),
            parse_time_ms=round(parse_time, 2),
            token_count=tokens,
            line_count=lines,
            file_size_bytes=file_size,
            memory_usage_kb=round(memory_used, 2),
            timestamp=datetime.now().isoformat()
        )
    
    def benchmark_all(self) -> None:
        """Benchmark all rules in directory"""
        rule_files = list(self.rules_dir.rglob("*.mdc"))
        
        print(f"Benchmarking {len(rule_files)} rules...")
        
        for i, rule_path in enumerate(rule_files, 1):
            try:
                result = self.benchmark_rule(rule_path)
                self.results.append(result)
                
                # Progress indicator
                if i % 10 == 0:
                    print(f"  Processed {i}/{len(rule_files)} rules...")
                    
            except Exception as e:
                print(f"  Error benchmarking {rule_path.name}: {e}")
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive benchmark report"""
        if not self.results:
            return {"error": "No benchmark results"}
        
        # Calculate aggregates
        total_tokens = sum(r.token_count for r in self.results)
        total_lines = sum(r.line_count for r in self.results)
        avg_load_time = sum(r.load_time_ms for r in self.results) / len(self.results)
        
        # Find outliers
        largest_by_tokens = max(self.results, key=lambda r: r.token_count)
        largest_by_lines = max(self.results, key=lambda r: r.line_count)
        slowest_load = max(self.results, key=lambda r: r.load_time_ms)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_rules": len(self.results),
                "total_tokens": total_tokens,
                "total_lines": total_lines,
                "avg_load_time_ms": round(avg_load_time, 2),
                "avg_tokens_per_rule": round(total_tokens / len(self.results), 2)
            },
            "outliers": {
                "largest_by_tokens": largest_by_tokens.to_dict(),
                "largest_by_lines": largest_by_lines.to_dict(),
                "slowest_load": slowest_load.to_dict()
            },
            "rules": [r.to_dict() for r in self.results]
        }
    
    def save_baseline(self, output_path: Path) -> None:
        """Save benchmark results as baseline"""
        report = self.generate_report()
        
        # Also create simplified baseline format
        baseline = {}
        for result in self.results:
            baseline[result.rule_name] = {
                "load_time_ms": result.load_time_ms,
                "parse_time_ms": result.parse_time_ms,
                "validation_time_ms": result.load_time_ms + result.parse_time_ms,
                "token_count": result.token_count,
                "line_count": result.line_count,
                "file_size_bytes": result.file_size_bytes,
                "memory_usage_mb": result.memory_usage_kb / 1024
            }
        
        with open(output_path, 'w') as f:
            json.dump(baseline, f, indent=2)
        
        # Save full report
        report_path = output_path.with_name('benchmark_report.json')
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nBaseline saved to: {output_path}")
        print(f"Full report saved to: {report_path}")

def main():
    parser = argparse.ArgumentParser(description="Benchmark cursor rules performance")
    parser.add_argument('--output', default='baseline_metrics.json', 
                        help='Output file for baseline metrics')
    parser.add_argument('--rules-dir', type=Path, 
                        default=Path(__file__).parent.parent / 'rules',
                        help='Rules directory path')
    
    args = parser.parse_args()
    
    benchmarker = RuleBenchmarker(args.rules_dir)
    benchmarker.benchmark_all()
    benchmarker.save_baseline(Path(args.output))
    
    # Print summary
    report = benchmarker.generate_report()
    print(f"\n=== Benchmark Summary ===")
    print(f"Total rules: {report['summary']['total_rules']}")
    print(f"Total tokens: {report['summary']['total_tokens']:,}")
    print(f"Average load time: {report['summary']['avg_load_time_ms']:.2f}ms")
    print(f"\nLargest rule (tokens): {report['outliers']['largest_by_tokens']['rule_name']} "
          f"({report['outliers']['largest_by_tokens']['token_count']} tokens)")
    print(f"Slowest rule: {report['outliers']['slowest_load']['rule_name']} "
          f"({report['outliers']['slowest_load']['load_time_ms']:.2f}ms)")

if __name__ == '__main__':
    main()