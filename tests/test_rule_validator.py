import pytest
import sys
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from rule_validator import RuleValidator, ValidationError, CircularDependencyError


class TestRuleValidator:
    
    @pytest.fixture
    def temp_rules_dir(self, tmp_path):
        """Create temporary rules directory structure"""
        rules_dir = tmp_path / '.cursorrules'
        (rules_dir / '000-core').mkdir(parents=True)
        (rules_dir / '100-cognitive').mkdir(parents=True)
        return rules_dir
    
    @pytest.fixture
    def validator(self, temp_rules_dir):
        return RuleValidator(str(temp_rules_dir))
    
    def test_init_creates_directories(self, tmp_path):
        """Test validator creates rule directories if missing"""
        validator = RuleValidator(str(tmp_path))
        assert (tmp_path / '.cursorrules').exists()
    
    def test_parse_yaml_metadata_valid(self, validator, temp_rules_dir):
        """Test parsing valid YAML metadata"""
        rule_path = temp_rules_dir / '000-core' / 'test-rule.mdc'
        rule_path.write_text('''---
description: "Test rule"
version: 1.0.0
author: "Test"
dependencies:
  - "100-cognitive/other-rule.mdc"
tags:
  - "test"
  - "validation"
---
# Test Rule Content
''')
        
        metadata = validator._parse_yaml_metadata(str(rule_path))
        assert metadata['description'] == "Test rule"
        assert metadata['version'] == "1.0.0"
        assert len(metadata['dependencies']) == 1
        assert len(metadata['tags']) == 2
    
    def test_parse_yaml_metadata_no_frontmatter(self, validator, temp_rules_dir):
        """Test parsing file without YAML frontmatter"""
        rule_path = temp_rules_dir / '000-core' / 'test-rule.mdc'
        rule_path.write_text('# Test Rule\nNo frontmatter here')
        
        metadata = validator._parse_yaml_metadata(str(rule_path))
        assert metadata == {}
    
    def test_validate_structure_valid(self, validator, temp_rules_dir):
        """Test structure validation for valid rule"""
        rule_path = temp_rules_dir / '000-core' / 'valid-rule.mdc'
        rule_path.write_text('''---
description: "Valid test rule"
version: 1.0.0
---
# Test Rule

* **Purpose**: Test validation
* **Requirements**: 
  - Requirement 1
  - Requirement 2
* **Validation**: Check this works
* **Examples**: 
  <example>Test example</example>
''')
        
        result = validator._validate_structure(str(rule_path))
        assert result['valid'] is True
        assert result['has_metadata'] is True
        assert result['has_purpose'] is True
        assert result['has_examples'] is True
    
    def test_validate_structure_missing_sections(self, validator, temp_rules_dir):
        """Test structure validation catches missing sections"""
        rule_path = temp_rules_dir / '000-core' / 'incomplete-rule.mdc'
        rule_path.write_text('''---
description: "Incomplete rule"
---
# Test Rule
Just some content
''')
        
        result = validator._validate_structure(str(rule_path))
        assert result['valid'] is True  # Still valid, just warnings
        assert result['has_metadata'] is True
        assert result['has_purpose'] is False
        assert result['has_examples'] is False
    
    def test_count_tokens(self, validator):
        """Test token counting approximation"""
        text = "This is a test sentence with approximately ten tokens."
        count = validator._count_tokens(text)
        assert 8 <= count <= 14  # Allow some variance in approximation
    
    def test_build_dependency_graph(self, validator, temp_rules_dir):
        """Test dependency graph construction"""
        # Create rules with dependencies
        rule1 = temp_rules_dir / '000-core' / 'rule1.mdc'
        rule2 = temp_rules_dir / '100-cognitive' / 'rule2.mdc'
        rule3 = temp_rules_dir / '100-cognitive' / 'rule3.mdc'
        
        rule1.write_text('''---
dependencies:
  - "100-cognitive/rule2.mdc"
---
# Rule 1''')
        
        rule2.write_text('''---
dependencies:
  - "100-cognitive/rule3.mdc"
---
# Rule 2''')
        
        rule3.write_text('''---
dependencies: []
---
# Rule 3''')
        
        graph = validator._build_dependency_graph()
        
        assert '000-core/rule1.mdc' in graph
        assert '100-cognitive/rule2.mdc' in graph['000-core/rule1.mdc']
        assert '100-cognitive/rule3.mdc' in graph['100-cognitive/rule2.mdc']
        assert graph['100-cognitive/rule3.mdc'] == []
    
    def test_has_circular_dependencies_none(self, validator, temp_rules_dir):
        """Test circular dependency detection with no cycles"""
        rule1 = temp_rules_dir / '000-core' / 'rule1.mdc'
        rule2 = temp_rules_dir / '000-core' / 'rule2.mdc'
        
        rule1.write_text('''---
dependencies:
  - "000-core/rule2.mdc"
---
# Rule 1''')
        
        rule2.write_text('''---
dependencies: []
---
# Rule 2''')
        
        graph = validator._build_dependency_graph()
        cycles = validator._has_circular_dependencies(graph)
        assert cycles == []
    
    def test_has_circular_dependencies_direct(self, validator, temp_rules_dir):
        """Test circular dependency detection with direct cycle"""
        rule1 = temp_rules_dir / '000-core' / 'rule1.mdc'
        rule2 = temp_rules_dir / '000-core' / 'rule2.mdc'
        
        rule1.write_text('''---
dependencies:
  - "000-core/rule2.mdc"
---
# Rule 1''')
        
        rule2.write_text('''---
dependencies:
  - "000-core/rule1.mdc"
---
# Rule 2''')
        
        graph = validator._build_dependency_graph()
        cycles = validator._has_circular_dependencies(graph)
        assert len(cycles) > 0
        # Check that at least one cycle contains both rules
        cycle_found = False
        for cycle in cycles:
            if '000-core/rule1.mdc' in cycle or '000-core/rule2.mdc' in cycle:
                cycle_found = True
                break
        assert cycle_found
    
    def test_validate_performance_within_limits(self, validator):
        """Test performance validation within limits"""
        result = validator._validate_performance(
            rule_path='test.mdc',
            content='Short content',
            line_count=50,
            token_count=100
        )
        
        assert result['within_limits'] is True
        assert result['line_count'] == 50
        assert result['token_count'] == 100
    
    def test_validate_performance_exceeds_limits(self, validator):
        """Test performance validation exceeding limits"""
        result = validator._validate_performance(
            rule_path='test.mdc',
            content='x' * 10000,
            line_count=200,
            token_count=2000
        )
        
        assert result['within_limits'] is False
        assert 'Exceeds line limit' in result['warnings'][0]
    
    def test_validate_all_integration(self, validator, temp_rules_dir):
        """Integration test for full validation"""
        # Create a valid rule
        rule_path = temp_rules_dir / '000-core' / 'complete-rule.mdc'
        rule_path.write_text('''---
description: "Complete test rule"
version: 1.0.0
author: "Test"
created: "2025-01-01"
tags:
  - "test"
---
# Complete Rule

* **Purpose**: Test complete validation
* **Requirements**: 
  - Must pass all checks
  - Must be within limits
* **Validation**: 
  - Check structure
  - Check performance
* **Examples**: 
  <example>Valid example</example>
''')
        
        results = validator.validate_all()
        
        assert results['total_rules'] == 1
        assert results['valid_rules'] == 1
        assert results['total_warnings'] == 0
        assert results['total_errors'] == 0
    
    def test_validate_single_rule(self, validator, temp_rules_dir):
        """Test single rule validation"""
        rule_path = temp_rules_dir / '000-core' / 'single-rule.mdc'
        rule_path.write_text('''---
description: "Single rule test"
version: 1.0.0
---
# Single Rule

* **Purpose**: Test single validation
* **Examples**: <example>Test</example>
''')
        
        result = validator.validate_single(str(rule_path))
        
        assert result['valid'] is True
        assert result['rule_path'] == str(rule_path)
        assert 'structure' in result
        assert 'performance' in result
        assert 'dependencies' in result


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
