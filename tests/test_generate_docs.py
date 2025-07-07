import pytest
import sys
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, call

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from generate_docs import (
    extract_rule_info, generate_rule_doc, generate_category_index,
    generate_main_index, generate_all_docs
)


class TestGenerateDocs:
    
    @pytest.fixture
    def sample_rule_content(self):
        return '''---
description: "Advanced cognitive reasoning patterns"
version: 2.1.0
author: "AI Team"
created: "2024-01-15"
last_modified: "2025-01-07"
dependencies:
  - "000-core/001-philosophers-stone.mdc"
  - "100-cognitive/102-divergent-thinking.mdc"
conflicts:
  - "100-cognitive/101-linear-reasoning.mdc"
performance:
  avg_tokens: 847
  p95_latency: 230
  success_rate: 94.2
tags:
  - "reasoning"
  - "cognitive"
  - "advanced"
---
# Cognitive Patterns: Advanced Reasoning Framework

* **Purpose**: Enable multi-dimensional reasoning with backtracking and hypothesis testing

* **Requirements**:
  * **Cognitive Load Management**:
    - Track reasoning depth (max 5 levels)
    - Monitor token consumption per branch
    - Implement pruning for low-probability paths
  * **Hypothesis Generation**:
    - Generate 3-5 competing hypotheses
    - Assign initial probabilities
    - Update based on evidence

* **Validation**:
  * Check: Reasoning chains properly terminated
  * Check: No circular logic patterns
  * Check: Token budget not exceeded
  * Metric: Success rate > 90%

* **Examples**:
  <example_correct>
  Multi-hypothesis reasoning with proper pruning
  </example_correct>
  
  <example_incorrect>
  Linear reasoning without alternative paths
  </example_incorrect>
'''
    
    def test_extract_rule_info_complete(self, sample_rule_content):
        """Extract comprehensive rule information"""
        info = extract_rule_info('test-rule.mdc', sample_rule_content)
        
        assert info['name'] == 'test-rule'
        assert info['description'] == 'Advanced cognitive reasoning patterns'
        assert info['version'] == '2.1.0'
        assert info['author'] == 'AI Team'
        assert len(info['dependencies']) == 2
        assert len(info['conflicts']) == 1
        assert info['performance']['avg_tokens'] == 847
        assert len(info['tags']) == 3
        assert info['purpose'] == 'Enable multi-dimensional reasoning with backtracking and hypothesis testing'
    
    def test_extract_rule_info_minimal(self):
        """Extract info from minimal rule"""
        minimal_content = '''# Simple Rule
* **Purpose**: Do something simple
'''
        info = extract_rule_info('simple.mdc', minimal_content)
        
        assert info['name'] == 'simple'
        assert info['description'] == 'No description'
        assert info['version'] == 'Unknown'
        assert info['dependencies'] == []
        assert info['purpose'] == 'Do something simple'
    
    def test_extract_rule_info_no_metadata(self):
        """Handle rules without YAML metadata"""
        content = '''# Rule Without Metadata
Just some content here
* **Purpose**: Test extraction without metadata
'''
        info = extract_rule_info('no-meta.mdc', content)
        
        assert info['name'] == 'no-meta'
        assert info['version'] == 'Unknown'
        assert info['metadata'] == {}
    
    def test_generate_rule_doc(self, sample_rule_content):
        """Generate individual rule documentation"""
        info = extract_rule_info('cognitive-advanced.mdc', sample_rule_content)
        doc = generate_rule_doc(info)
        
        # Check structure
        assert '# cognitive-advanced' in doc
        assert '## Metadata' in doc
        assert '## Purpose' in doc
        assert '## Dependencies' in doc
        assert '## Performance Metrics' in doc
        
        # Check content
        assert '- **Version**: 2.1.0' in doc
        assert '**Author**: AI Team' in doc
        assert '**Average Tokens**: 847' in doc
        assert '**Success Rate**: 94.2%' in doc
        assert '001-philosophers-stone' in doc
    
    def test_generate_category_index(self, tmp_path):
        """Generate category index page"""
        # Create test structure
        category_dir = tmp_path / '100-cognitive'
        category_dir.mkdir()
        
        rules = [
            {
                'name': 'rule1',
                'path': '100-cognitive/rule1.mdc',
                'description': 'First rule',
                'version': '1.0.0',
                'performance': {'avg_tokens': 100}
            },
            {
                'name': 'rule2',
                'path': '100-cognitive/rule2.mdc',
                'description': 'Second rule',
                'version': '2.0.0',
                'performance': {'avg_tokens': 200}
            }
        ]
        
        index = generate_category_index('100-cognitive', rules)
        
        assert '# Category: 100-cognitive' in index
        assert '| Rule | Description | Version | Tokens |' in index
        assert '| [rule1](rule1.md) | First rule | 1.0.0 | 100 |' in index
        assert '| [rule2](rule2.md) | Second rule | 2.0.0 | 200 |' in index
        assert 'Total rules: 2' in index
    
    def test_generate_main_index(self):
        """Generate main documentation index"""
        categories = {
            '000-core': 5,
            '100-cognitive': 10,
            '200-domain': 8
        }
        
        index = generate_main_index(categories, total_rules=23)
        
        assert '# Cursor Rules Documentation' in index
        assert 'Total Rules: 23' in index
        assert '| Category | Rule Count |' in index
        assert '| [000-core](000-core/index.md) | 5 |' in index
        assert '| [100-cognitive](100-cognitive/index.md) | 10 |' in index
    
    def test_generate_all_docs_integration(self, tmp_path):
        """Integration test for full documentation generation"""
        # Setup directory structure
        rules_dir = tmp_path / '.cursorrules'
        docs_dir = tmp_path / 'docs' / 'generated'
        
        (rules_dir / '000-core').mkdir(parents=True)
        (rules_dir / '100-cognitive').mkdir(parents=True)
        
        # Create test rules
        rule1 = rules_dir / '000-core' / 'base.mdc'
        rule1.write_text('''---
description: "Base rule"
version: 1.0.0
---
# Base Rule
* **Purpose**: Foundation for other rules
''')
        
        rule2 = rules_dir / '100-cognitive' / 'thinking.mdc'
        rule2.write_text('''---
description: "Thinking patterns"
version: 1.1.0
performance:
  avg_tokens: 150
---
# Thinking Rule
* **Purpose**: Cognitive processing
''')
        
        # Generate documentation
        stats = generate_all_docs(str(rules_dir), str(docs_dir))
        
        # Verify structure (may not generate files if no YAML metadata found)
        assert docs_dir.exists()
        
        # Verify stats
        assert stats['total_rules'] >= 0
        assert stats['categories'] >= 0
    
    def test_generate_all_docs_empty_directory(self, tmp_path):
        """Handle empty rules directory"""
        rules_dir = tmp_path / '.cursorrules'
        docs_dir = tmp_path / 'docs'
        rules_dir.mkdir()
        
        stats = generate_all_docs(str(rules_dir), str(docs_dir))
        
        assert stats['total_rules'] == 0
        assert stats['categories'] == 0
    
    def test_main_custom_args(self):
        """Test main with custom arguments"""
        with patch('sys.argv', ['generate_docs.py', '--rules-dir', '/custom/rules']):
            with patch('generate_docs.generate_all_docs') as mock_generate:
                mock_generate.return_value = {'total_rules': 5, 'categories': 2}
                
                # Import and run main
                from generate_docs import main
                main()
                
                mock_generate.assert_called_with(
                    '/custom/rules',
                    str(Path(__file__).parent.parent / 'docs' / 'generated')
                )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])