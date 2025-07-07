import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import yaml
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from generate_docs import DocsGenerator


class TestDocsGenerator:
    
    @pytest.fixture
    def temp_docs_dir(self, tmp_path):
        rules_dir = tmp_path / 'rules'
        output_dir = tmp_path / 'docs'
        rules_dir.mkdir()
        return rules_dir, output_dir
    
    def test_docs_generator_init(self, temp_docs_dir):
        """Test DocsGenerator initialization"""
        rules_dir, output_dir = temp_docs_dir
        generator = DocsGenerator(rules_dir, output_dir)
        
        assert generator.rules_dir == rules_dir
        assert generator.output_dir == output_dir
        assert generator.rules_metadata == {}
        assert generator.dependency_graph is not None
    
    def test_load_all_metadata(self, temp_docs_dir):
        """Test loading metadata from YAML files"""
        rules_dir, output_dir = temp_docs_dir
        
        # Create test YAML files
        (rules_dir / '000-core').mkdir()
        yaml1 = rules_dir / '000-core' / 'rule1.yaml'
        yaml1.write_text(yaml.dump({
            'description': 'Test rule 1',
            'version': '1.0.0',
            'dependencies': ['100-cognitive/rule2.yaml']
        }))
        
        yaml2 = rules_dir / '100-cognitive.yaml'
        yaml2.write_text(yaml.dump({
            'description': 'Test rule 2',
            'version': '2.0.0'
        }))
        
        generator = DocsGenerator(rules_dir, output_dir)
        generator.load_all_metadata()
        
        assert 'rule1' in generator.rules_metadata
        assert 'rule2' not in generator.rules_metadata  # Wrong location
        assert len(generator.dependency_graph.nodes) > 0
    
    def test_generate_index(self, temp_docs_dir):
        """Test index generation"""
        rules_dir, output_dir = temp_docs_dir
        generator = DocsGenerator(rules_dir, output_dir)
        
        # Add test metadata
        generator.rules_metadata = {
            'rule1': {
                'metadata': {'description': 'Test 1', 'performance': {'avg_tokens': 100}},
                'category': '000-core',
                'path': Path('000-core/rule1.yaml')
            },
            'rule2': {
                'metadata': {'description': 'Test 2', 'performance': {'avg_tokens': 200}},
                'category': '100-cognitive',
                'path': Path('100-cognitive/rule2.yaml')
            }
        }
        
        index = generator.generate_index()
        
        assert '# Cursor Rules Documentation' in index
        assert 'Total Rules: 2' in index
        assert '000-core' in index
        assert '100-cognitive' in index
        assert 'Total Token Budget' in index
    
    def test_generate_category_doc(self, temp_docs_dir):
        """Test category documentation generation"""
        rules_dir, output_dir = temp_docs_dir
        generator = DocsGenerator(rules_dir, output_dir)
        
        # Create category metadata
        (rules_dir / '000-core').mkdir()
        cat_yaml = rules_dir / '000-core' / '_category.yaml'
        cat_yaml.write_text(yaml.dump({
            'name': 'Core Rules',
            'description': 'Foundation rules',
            'purpose': 'Base functionality'
        }))
        
        generator.rules_metadata = {
            'rule1': {
                'metadata': {
                    'description': 'Test rule',
                    'version': '1.0.0',
                    'performance': {'avg_tokens': 100, 'success_rate': 95},
                    'tags': ['test', 'core']
                },
                'category': '000-core',
                'path': Path('000-core/rule1.yaml')
            }
        }
        
        doc = generator.generate_category_doc('000-core')
        
        assert '# Category: 000-core' in doc
        assert 'Core Rules' in doc
        assert 'Foundation rules' in doc
        assert 'Base functionality' in doc
        assert '[rule1]' in doc
        assert 'Version 1.0.0' in doc
        assert '100' in doc  # tokens
        assert '95%' in doc  # success rate
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_generate_dependency_graph(self, mock_close, mock_savefig, temp_docs_dir):
        """Test dependency graph generation"""
        rules_dir, output_dir = temp_docs_dir
        generator = DocsGenerator(rules_dir, output_dir)
        
        # Add nodes to graph
        generator.dependency_graph.add_edge('rule1', 'rule2')
        generator.dependency_graph.add_edge('rule2', 'rule3')
        
        generator.rules_metadata = {
            'rule1': {'category': '000-core'},
            'rule2': {'category': '100-cognitive'},
            'rule3': {'category': '000-core'}
        }
        
        # Create output dir
        output_dir.mkdir(exist_ok=True)
        
        generator.generate_dependency_graph()
        
        # Verify graph was saved
        mock_savefig.assert_called_once()
        mock_close.assert_called_once()
        assert (output_dir / 'images').exists()
    
    def test_generate_all(self, temp_docs_dir):
        """Test complete documentation generation"""
        rules_dir, output_dir = temp_docs_dir
        generator = DocsGenerator(rules_dir, output_dir)
        
        # Mock methods to avoid full execution
        generator.load_all_metadata = MagicMock()
        generator.generate_dependency_graph = MagicMock()
        generator.generate_index = MagicMock(return_value='# Index')
        generator.generate_rule_doc = MagicMock(return_value='# Rule')
        generator.generate_category_doc = MagicMock(return_value='# Category')
        
        generator.rules_metadata = {
            'rule1': {'category': '000-core'}
        }
        
        generator.generate_all()
        
        # Verify all methods called
        generator.load_all_metadata.assert_called_once()
        generator.generate_dependency_graph.assert_called_once()
        generator.generate_index.assert_called_once()
        
        # Verify output structure created
        assert output_dir.exists()
        assert (output_dir / 'rules').exists()
        assert (output_dir / 'categories').exists()
