#!/usr/bin/env python3
"""Extract accurate creation dates from git history"""

import subprocess
import yaml
from pathlib import Path
from datetime import datetime

def get_file_creation_date(file_path: str) -> str:
    """Get first commit date for file"""
    try:
        # Get first commit that added this file
        cmd = ['git', 'log', '--follow', '--format=%aI', '--reverse', file_path]
        result = subprocess.check_output(cmd, text=True).strip()
        
        if result:
            # Take first line (oldest commit)
            first_date = result.split('\n')[0]
            # Convert to YYYY-MM-DD format
            dt = datetime.fromisoformat(first_date.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d')
    except subprocess.CalledProcessError:
        pass
    
    # Fallback to current date
    return datetime.now().strftime('%Y-%m-%d')

def fix_creation_dates():
    """Update creation dates based on git history"""
    import os
    os.chdir(Path(__file__).parent.parent)
    
    rules_dir = Path('rules')
    yaml_files = list(rules_dir.rglob('*.yaml'))
    
    updated_count = 0
    
    for yaml_file in yaml_files:
        if yaml_file.name == '_category.yaml':
            continue
            
        # Get actual creation date
        creation_date = get_file_creation_date(str(yaml_file))
        
        # Read current metadata
        with open(yaml_file, 'r') as f:
            content = f.read()
            try:
                metadata = yaml.safe_load(content)
            except yaml.composer.ComposerError:
                # Multiple documents - take first
                docs = list(yaml.safe_load_all(content))
                metadata = docs[0] if docs else None
        
        if metadata and metadata.get('created') != creation_date:
            old_date = metadata.get('created', 'None')
            metadata['created'] = creation_date
            
            # Write back
            with open(yaml_file, 'w') as f:
                yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)
            
            print(f"✅ {yaml_file.name}: {old_date} → {creation_date}")
            updated_count += 1
    
    print(f"\n✅ Updated {updated_count} creation dates")

if __name__ == '__main__':
    fix_creation_dates()
