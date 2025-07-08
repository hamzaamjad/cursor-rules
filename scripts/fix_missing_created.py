#!/usr/bin/env python3
"""Fix missing created field in YAML metadata files"""

import yaml
from pathlib import Path
from datetime import datetime

def fix_created_field():
    rules_dir = Path(__file__).parent.parent / 'rules'
    yaml_files = list(rules_dir.rglob("*.yaml"))
    
    fixed_count = 0
    
    for yaml_file in yaml_files:
        if yaml_file.name == '_category.yaml':
            continue
            
        with open(yaml_file, 'r') as f:
            content = f.read()
            metadata = yaml.safe_load(content)
        
        if metadata and 'created' not in metadata:
            # Add created field using last_modified or current date
            if 'last_modified' in metadata:
                metadata['created'] = metadata['last_modified']
            else:
                metadata['created'] = datetime.now().strftime('%Y-%m-%d')
            
            # Write back
            with open(yaml_file, 'w') as f:
                yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)
            
            fixed_count += 1
            print(f"✅ Fixed: {yaml_file.name}")
    
    print(f"\n🎯 Total fixed: {fixed_count} files")

if __name__ == '__main__':
    fix_created_field()