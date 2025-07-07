#!/usr/bin/env python3
"""
Migrate metadata from rule files to separate YAML files
Following dbt's model.sql + model.yaml pattern
"""

import re
import yaml
from pathlib import Path
from typing import Dict, Tuple

class MetadataSeparator:
    def __init__(self, rules_dir: Path):
        self.rules_dir = Path(rules_dir)
        self.stats = {
            'files_processed': 0,
            'tokens_saved': 0,
            'metadata_files_created': 0
        }
    
    def separate_all(self):
        """Process all rule files"""
        for rule_file in self.rules_dir.rglob("*.mdc"):
            self.separate_file(rule_file)
        
        return self.stats
    
    def separate_file(self, rule_path: Path) -> bool:
        """Extract metadata to separate YAML file"""
        try:
            with open(rule_path, 'r') as f:
                content = f.read()
            
            # Parse frontmatter
            match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
            if not match:
                # No frontmatter to separate
                return False
            
            metadata_str = match.group(1)
            body = match.group(2).strip()
            
            # Parse metadata
            metadata = yaml.safe_load(metadata_str)
            
            # Create or overwrite YAML file
            yaml_path = rule_path.with_suffix('.yaml')
            with open(yaml_path, 'w') as f:
                yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)
            
            # Rewrite MDC file with just content
            with open(rule_path, 'w') as f:
                f.write(body)
            
            # Calculate token savings
            metadata_lines = len(metadata_str.split('\n'))
            self.stats['tokens_saved'] += metadata_lines * 10
            self.stats['files_processed'] += 1
            self.stats['metadata_files_created'] += 1
            
            print(f"✓ Separated: {rule_path.name}")
            return True
            
        except Exception as e:
            print(f"Error processing {rule_path}: {e}")
            return False
    
    def create_category_configs(self):
        """Create shared category configuration files"""
        categories = {}
        
        # Collect common patterns per category
        for yaml_file in self.rules_dir.rglob("*.yaml"):
            # Skip config files
            if yaml_file.name in ['rule-config.yaml', 'meta-rules-config.yaml', '_category.yaml']:
                continue
                
            category = yaml_file.parent.name
            if category not in categories:
                categories[category] = {
                    'common_tags': set(),
                    'common_deps': set(),
                    'performance_defaults': {}
                }
            
            try:
                with open(yaml_file) as f:
                    metadata = yaml.safe_load(f)
                    
                if metadata and 'tags' in metadata:
                    categories[category]['common_tags'].update(metadata['tags'])
            except Exception as e:
                print(f"Skipping {yaml_file}: {e}")
                continue
        
        # Write category configs
        for category, data in categories.items():
            category_dir = self.rules_dir / category
            
            # Ensure directory exists
            if not category_dir.exists():
                print(f"Warning: Category directory '{category}' doesn't exist, skipping")
                continue
                
            config_path = category_dir / '_category.yaml'
            
            config = {
                'category': category,
                'description': f'Rules for {category}',
                'common_tags': sorted(list(data['common_tags'])),
                'defaults': {
                    'performance': {
                        'processingOverhead': 'minimal',
                        'empiricalValidation': 'To be measured'
                    }
                }
            }
            
            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)

def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--rules-dir', default='./rules')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    
    separator = MetadataSeparator(args.rules_dir)
    
    if args.dry_run:
        print("DRY RUN - Analyzing token savings...")
        # Just calculate without modifying
    else:
        stats = separator.separate_all()
        separator.create_category_configs()
        
        print(f"✅ Metadata separation complete!")
        print(f"📊 Files processed: {stats['files_processed']}")
        print(f"💾 Metadata files created: {stats['metadata_files_created']}")
        print(f"🎯 Estimated tokens saved: {stats['tokens_saved']:,}")

if __name__ == '__main__':
    main()
