#!/usr/bin/env python3
"""Migrate old dependency format to new list-based format"""

import yaml
from pathlib import Path

def migrate_dependencies():
    rules_dir = Path(__file__).parent.parent / 'rules'
    yaml_files = list(rules_dir.rglob("*.yaml"))
    
    migrated_count = 0
    
    for yaml_file in yaml_files:
        if yaml_file.name == '_category.yaml':
            continue
            
        with open(yaml_file, 'r') as f:
            content = f.read()
            metadata = yaml.safe_load(content)
        
        if metadata and 'dependencies' in metadata:
            # Check if using old dictionary format
            if isinstance(metadata['dependencies'], dict):
                print(f"🔧 Migrating: {yaml_file.name}")
                
                # Extract all dependency paths from old format
                new_deps = []
                old_deps = metadata['dependencies']
                
                # Extract from 'required' section
                if 'required' in old_deps and isinstance(old_deps['required'], list):
                    new_deps.extend(old_deps['required'])
                
                # Extract from 'recommended' section (optional dependencies)
                if 'recommended' in old_deps and isinstance(old_deps['recommended'], list):
                    # Add recommended deps with comment marker
                    for dep in old_deps['recommended']:
                        if dep not in new_deps:
                            new_deps.append(dep)
                
                # Update to new format
                if new_deps:
                    metadata['dependencies'] = new_deps
                else:
                    # Remove empty dependencies
                    del metadata['dependencies']
                
                # Add conflicts if old format had incompatible rules
                if 'incompatible' in old_deps and isinstance(old_deps['incompatible'], list):
                    if 'conflicts' not in metadata:
                        metadata['conflicts'] = []
                    for incomp in old_deps['incompatible']:
                        conflict_entry = {
                            'rule': incomp,
                            'resolution': 'avoid'
                        }
                        if conflict_entry not in metadata['conflicts']:
                            metadata['conflicts'].append(conflict_entry)
                
                # Write back
                with open(yaml_file, 'w') as f:
                    yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)
                
                migrated_count += 1
    
    print(f"\n✅ Migrated {migrated_count} files from old to new dependency format")

if __name__ == '__main__':
    migrate_dependencies()
