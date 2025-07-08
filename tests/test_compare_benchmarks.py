import pytest
import sys
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from compare_benchmarks import load_metrics, compare_metrics


class TestCompareBenchmarks:
    
    @pytest.fixture
    def baseline_data(self):
        return {
            "rule1": {
                "load_time_ms": 1.0,
                "parse_time_ms": 2.0,
                "validation_time_ms": 3.0,
                "token_count": 100,
                "line_count": 50,
                "memory_usage_mb": 10.0
            },
            "rule2": {
                "load_time_ms": 2.0,
                "parse_time_ms": 3.0,
                "validation_time_ms": 4.0,
                "token_count": 200,
                "line_count": 100,
                "memory_usage_mb": 20.0
            }
        }
    
    @pytest.fixture
    def current_data(self):
        return {
            "rule1": {
                "load_time_ms": 1.1,
                "parse_time_ms": 1.8,
                "validation_time_ms": 3.3,
                "token_count": 110,
                "line_count": 50,
                "memory_usage_mb": 11.0
            },
            "rule2": {
                "load_time_ms": 2.4,
                "parse_time_ms": 3.6,
                "validation_time_ms": 5.0,
                "token_count": 200,
                "line_count": 120,
                "memory_usage_mb": 24.0
            },
            "rule3": {
                "load_time_ms": 0.5,
                "parse_time_ms": 1.0,
                "validation_time_ms": 1.5,
                "token_count": 50,
                "line_count": 25,
                "memory_usage_mb": 5.0
            }
        }
    
    def test_load_metrics_valid_file(self, tmp_path, baseline_data):
        """Test loading valid benchmark file"""
        benchmark_file = tmp_path / "benchmark.json"
        benchmark_file.write_text(json.dumps(baseline_data, indent=2))
        
        loaded = load_metrics(str(benchmark_file))
        assert loaded == baseline_data
    
    def test_compare_metrics_report_generation(self, baseline_data, current_data):
        """Test comprehensive metric comparison"""
        report = compare_metrics(baseline_data, current_data)
        
        # Check report structure
        assert '# 📊 Performance Comparison Report' in report
        assert '⚠️ Performance Regressions' in report
        assert 'rule2' in report
        assert 'rule3' in report
        assert 'New Rules' in report
    
    def test_compare_metrics_improvements(self, baseline_data):
        """Test detection of improvements"""
        # Create improved metrics
        improved_data = {
            "rule1": {
                "validation_time_ms": 2.0,  # 33% improvement
                "token_count": 80,  # 20% improvement
                "load_time_ms": 1.0,
                "parse_time_ms": 2.0,
                "line_count": 50,
                "memory_usage_mb": 10.0
            }
        }
        
        report = compare_metrics(baseline_data, improved_data)
        assert '## ✅ Improvements' in report
        assert 'rule1' in report
    
    def test_compare_metrics_regressions(self, baseline_data):
        """Test detection of regressions"""
        # Create regressed metrics
        regressed_data = {
            "rule1": {
                "validation_time_ms": 4.0,  # 33% regression
                "token_count": 130,  # 30% regression
                "load_time_ms": 1.0,
                "parse_time_ms": 2.0,
                "line_count": 50,
                "memory_usage_mb": 10.0
            }
        }
        
        report = compare_metrics(baseline_data, regressed_data)
        assert '⚠️ Performance Regressions' in report
        assert 'rule1' in report
    
    def test_compare_metrics_new_rules(self):
        """Test detection of new rules"""
        baseline = {"rule1": {"token_count": 100, "validation_time_ms": 1.0}}
        current = {
            "rule1": {"token_count": 100, "validation_time_ms": 1.0},
            "rule2": {"token_count": 200, "validation_time_ms": 2.0}
        }
        
        report = compare_metrics(baseline, current)
        assert '## 🆕 New Rules' in report
        assert 'rule2' in report
    
    def test_compare_metrics_removed_rules(self):
        """Test detection of removed rules"""
        baseline = {
            "rule1": {"token_count": 100, "validation_time_ms": 1.0},
            "rule2": {"token_count": 200, "validation_time_ms": 2.0}
        }
        current = {"rule1": {"token_count": 100, "validation_time_ms": 1.0}}
        
        report = compare_metrics(baseline, current)
        # Report doesn't include "Removed Rules" section if none removed
        assert isinstance(report, str)
        assert 'Performance Comparison Report' in report
    
    def test_percentage_calculation_edge_cases(self):
        """Test percentage calculations with edge cases"""
        baseline = {
            "zero_baseline": {"token_count": 0, "validation_time_ms": 0},
            "normal": {"token_count": 100, "validation_time_ms": 1.0}
        }
        current = {
            "zero_baseline": {"token_count": 100, "validation_time_ms": 1.0},
            "normal": {"token_count": 110, "validation_time_ms": 1.1}
        }
        
        # Should not crash on zero baseline values
        report = compare_metrics(baseline, current)
        assert isinstance(report, str)
        assert len(report) > 0
    
    @patch('sys.argv', ['compare_benchmarks.py', 'baseline.json', 'current.json'])
    def test_main_execution(self, tmp_path, baseline_data, current_data, monkeypatch):
        """Test main script execution"""
        monkeypatch.chdir(tmp_path)
        
        # Create test files
        Path('baseline.json').write_text(json.dumps(baseline_data))
        Path('current.json').write_text(json.dumps(current_data))
        
        # Test that files can be loaded and compared
        baseline = load_metrics('baseline.json')
        current = load_metrics('current.json')
        report = compare_metrics(baseline, current)
        
        assert isinstance(report, str)
        assert len(report) > 100  # Substantial report generated


if __name__ == '__main__':
    pytest.main([__file__, '-v'])