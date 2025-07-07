import pytest
import sys
import json
import time
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from benchmark_rules import RuleBenchmarker, BenchmarkResult


class TestBenchmarkRules:
    
    @pytest.fixture
    def mock_rule_content(self):
        return '''---
description: "Test rule for benchmarking"
version: 1.0.0
author: "Test"
---
# Test Rule

* **Purpose**: Benchmark testing
* **Requirements**: 
  - Must measure performance
  - Must track metrics
* **Examples**: 
  <example>Performance test</example>
'''
    
    def test_benchmark_result_dataclass(self):
        """Test BenchmarkResult dataclass"""
        result = BenchmarkResult(
            rule_name="test",
            rule_path="test.mdc",
            load_time_ms=1.0,
            parse_time_ms=2.0,
            token_count=100,
            line_count=10,
            file_size_bytes=1000,
            memory_usage_kb=50.0,
            timestamp="2025-01-07T10:00:00"
        )
        
        dict_result = result.to_dict()
        assert dict_result['rule_name'] == 'test'
        assert dict_result['load_time_ms'] == 1.0
        assert dict_result['token_count'] == 100
    
    def test_rule_benchmarker_init(self, tmp_path):
        """Test RuleBenchmarker initialization"""
        benchmarker = RuleBenchmarker(tmp_path)
        assert benchmarker.rules_dir == tmp_path
        assert benchmarker.results == []
        assert benchmarker.process is not None
    
    def test_estimate_tokens_fallback(self, tmp_path):
        """Test token estimation with fallback method"""
        benchmarker = RuleBenchmarker(tmp_path)
        # Test fallback (4 chars per token)
        text = "This is a test string with approximately 40 characters."
        tokens = benchmarker.estimate_tokens(text)
        assert 10 <= tokens <= 15  # ~56 chars / 4
    
    @pytest.mark.skip(reason="tiktoken is optional dependency")
    @patch('benchmark_rules.tiktoken.encoding_for_model')
    def test_estimate_tokens_tiktoken(self, mock_encoding_for_model, tmp_path):
        """Test token estimation with tiktoken"""
        mock_enc = MagicMock()
        mock_enc.encode.return_value = [1, 2, 3, 4, 5]  # 5 tokens
        mock_encoding_for_model.return_value = mock_enc
        
        benchmarker = RuleBenchmarker(tmp_path)
        tokens = benchmarker.estimate_tokens("test text")
        
        assert tokens == 5
        mock_encoding_for_model.assert_called_once_with("gpt-4")
    
    def test_benchmark_single_rule(self, tmp_path, mock_rule_content):
        """Test benchmarking single rule"""
        rules_dir = tmp_path / '.cursorrules'
        rules_dir.mkdir()
        rule_path = rules_dir / 'test-rule.mdc'
        rule_path.write_text(mock_rule_content)
        
        benchmarker = RuleBenchmarker(rules_dir)
        result = benchmarker.benchmark_rule(rule_path)
        
        assert result.rule_name == 'test-rule'
        assert result.rule_path.endswith('test-rule.mdc')
        assert result.load_time_ms >= 0
        assert result.parse_time_ms >= 0
        assert result.token_count > 0
        assert result.line_count == mock_rule_content.count('\n') + 1
        assert result.file_size_bytes == len(mock_rule_content.encode())
        assert result.memory_usage_kb >= 0
    
    def test_benchmark_all_rules(self, tmp_path):
        """Test benchmarking all rules in directory"""
        rules_dir = tmp_path / '.cursorrules'
        (rules_dir / '000-core').mkdir(parents=True)
        (rules_dir / '100-cognitive').mkdir(parents=True)
        
        # Create test rules
        rule1 = rules_dir / '000-core' / 'rule1.mdc'
        rule2 = rules_dir / '100-cognitive' / 'rule2.mdc'
        
        rule1.write_text('# Rule 1\nContent')
        rule2.write_text('# Rule 2\nMore content')
        
        benchmarker = RuleBenchmarker(rules_dir)
        benchmarker.benchmark_all()
        
        assert len(benchmarker.results) == 2
        rule_names = [r.rule_name for r in benchmarker.results]
        assert 'rule1' in rule_names
        assert 'rule2' in rule_names
    
    def test_generate_report(self, tmp_path):
        """Test report generation"""
        benchmarker = RuleBenchmarker(tmp_path)
        
        # Add sample results
        benchmarker.results = [
            BenchmarkResult(
                rule_name="fast-rule",
                rule_path="fast.mdc",
                load_time_ms=0.5,
                parse_time_ms=1.0,
                token_count=100,
                line_count=10,
                file_size_bytes=500,
                memory_usage_kb=25.0,
                timestamp="2025-01-07T10:00:00"
            ),
            BenchmarkResult(
                rule_name="slow-rule",
                rule_path="slow.mdc",
                load_time_ms=5.0,
                parse_time_ms=10.0,
                token_count=1000,
                line_count=100,
                file_size_bytes=5000,
                memory_usage_kb=250.0,
                timestamp="2025-01-07T10:00:00"
            )
        ]
        
        report = benchmarker.generate_report()
        
        assert isinstance(report, dict)
        assert "summary" in report
        assert "outliers" in report
        assert report["summary"]["total_rules"] == 2
    
    def test_save_baseline(self, tmp_path):
        """Test saving baseline metrics"""
        benchmarker = RuleBenchmarker(tmp_path)
        
        # Add sample result
        benchmarker.results = [
            BenchmarkResult(
                rule_name="test-rule",
                rule_path="test.mdc",
                load_time_ms=1.0,
                parse_time_ms=2.0,
                token_count=100,
                line_count=10,
                file_size_bytes=1000,
                memory_usage_kb=50.0,
                timestamp="2025-01-07T10:00:00"
            )
        ]
        
        output_file = tmp_path / 'baseline.json'
        benchmarker.save_baseline(output_file)
        
        assert output_file.exists()
        
        # Verify saved content
        with open(output_file) as f:
            loaded = json.load(f)
        
        assert 'test-rule' in loaded
        assert loaded['test-rule']['token_count'] == 100


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])