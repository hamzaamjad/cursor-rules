import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from generate_docs import DocsGenerator


class TestDocsGeneratorEdgeCases:
    
    def test_generate_rule_doc_full(self, tmp_path):
        """Test rule doc generation with all fields"""
        generator = DocsGenerator(tmp_path, tmp_path)
        
        # Setup comprehensive metadata
        generator.rules_metadata = {
            'test-rule': {
                'metadata': {
                    'description': 'Test rule description',
                    'version': '1.0.0',
                    'author': 'Test Author',
                    'created': '2025-01-01',
                    'last_modified': '2025-01-07',
                    'tags': ['tag1', 'tag2'],
                    'performance': {
                        'avg_tokens': 100,
                        'p95_latency': '10ms',
                        'success_rate': 95.5,
                        'token_budget': 1000
                    },
                    'dependencies': ['dep1.mdc', 'dep2.mdc'],
                    'conflicts': [
                        {'rule': 'conflict1.mdc', 'resolution': 'override'},
                        'conflict2.mdc'
                    ]
                },
                'path': tmp_path / 'test-rule.yaml',
                'category': '000-core'
            },
            'dep1': {
                'metadata': {'description': 'Dependency 1'},
                'category': '000-core'
            }
        }
        
        # Add dependent to metadata
        generator.rules_metadata['dependent-rule'] = {
            'metadata': {'description': 'Dependent rule'},
            'category': '100-cognitive'
        }
        
        # Add to dependency graph
        generator.dependency_graph.add_edge('dependent-rule', 'test-rule')
        
        doc = generator.generate_rule_doc('test-rule')
        
        # Verify all sections present
        assert '# test-rule' in doc
        assert 'Test rule description' in doc
        assert 'Version | 1.0.0' in doc
        assert 'Tags | tag1, tag2' in doc
        assert 'Average Tokens | 100' in doc
        assert 'Success Rate | 95.5%' in doc
        assert '## Dependencies' in doc
        assert '[dep1]' in doc
        assert '## Used By' in doc
        assert 'dependent-rule' in doc
        assert '## Conflicts' in doc
        assert 'conflict1.mdc' in doc
        assert 'override' in doc
    
    def test_load_metadata_with_errors(self, tmp_path):
        """Test metadata loading with invalid files"""
        rules_dir = tmp_path / 'rules'
        rules_dir.mkdir()
        
        # Create invalid YAML
        bad_yaml = rules_dir / 'bad.yaml'
        bad_yaml.write_text('invalid: yaml: content:')
        
        # Create valid YAML
        good_yaml = rules_dir / 'good.yaml'
        good_yaml.write_text('description: Good rule\nversion: 1.0.0')
        
        generator = DocsGenerator(rules_dir, tmp_path)
        generator.load_all_metadata()
        
        # Should load good file, skip bad
        assert 'good' in generator.rules_metadata
        assert 'bad' not in generator.rules_metadata
    
    def test_empty_rules_directory(self, tmp_path):
        """Test with empty rules directory"""
        rules_dir = tmp_path / 'empty'
        rules_dir.mkdir()
        
        generator = DocsGenerator(rules_dir, tmp_path)
        generator.load_all_metadata()
        
        assert len(generator.rules_metadata) == 0
        
        # Should still generate index
        index = generator.generate_index()
        assert 'Total Rules: 0' in index
