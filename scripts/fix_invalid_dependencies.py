#!/usr/bin/env python3
"""Fix invalid dependency entries in YAML metadata"""

import yaml
from pathlib import Path

def fix_dependencies():
    rules_dir = Path(__file__).parent.parent / 'rules'
    yaml_files = list(rules_dir.rglob("*.yaml"))
    
    fixed_count = 0
    
    for yaml_file in yaml_files:
        if yaml_file.name == '_category.yaml':
            continue
            
        with open(yaml_file, 'r') as f:
            content = f.read()
            metadata = yaml.safe_load(content)
        
        if metadata and 'dependencies' in metadata:
            # Check for invalid dependencies
            invalid_deps = ['required', 'recommended', 'incompatible']
            if any(dep in invalid_deps for dep in metadata['dependencies']):
                print(f"🔧 Fixing: {yaml_file.name}")
                
                # Keep only valid path-like dependencies
                valid_deps = [dep for dep in metadata['dependencies'] 
                             if dep not in invalid_deps and '/' in dep]
                
                if valid_deps:
                    metadata['dependencies'] = valid_deps
                else:
                    # Remove empty dependencies
                    del metadata['dependencies']
                
                # Write back
                with open(yaml_file, 'w') as f:
                    yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)
                
                fixed_count += 1
    
    print(f"\n✅ Fixed {fixed_count} files with invalid dependencies")

if __name__ == '__main__':
    fix_dependencies()