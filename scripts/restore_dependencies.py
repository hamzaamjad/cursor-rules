#!/usr/bin/env python3
"""Restore dependency metadata from git history"""

import subprocess
import yaml
from pathlib import Path
import json

def get_original_dependencies():
    """Extract original dependencies from git history"""
    import os
    os.chdir(Path(__file__).parent.parent)  # Ensure we're in repo root
    
    rules_dir = Path('rules')
    dependencies_map = {}
    
    # Get list of all YAML files
    yaml_files = list(rules_dir.rglob('*.yaml'))
    
    for yaml_file in yaml_files:
        if yaml_file.name == '_category.yaml':
            continue
            
        # Get original content from git
        file_path = str(yaml_file)
        try:
            original_content = subprocess.check_output(
                ['git', 'show', f'9a3315b35da964f27de82871e195d691999f6bd1:{file_path}'],
                text=True
            )
            
            # Handle YAML files with multiple documents
            try:
                # Try single document first
                original_meta = yaml.safe_load(original_content)
            except yaml.composer.ComposerError:
                # Multiple documents - take the first one
                docs = list(yaml.safe_load_all(original_content))
                original_meta = docs[0] if docs else None
            
            if original_meta and 'dependencies' in original_meta:
                # Extract dependency paths from old format
                deps = []
                old_deps = original_meta['dependencies']
                
                if isinstance(old_deps, dict):
                    # Old format with required/recommended
                    if 'required' in old_deps and isinstance(old_deps['required'], list):
                        deps.extend(old_deps['required'])
                    if 'recommended' in old_deps and isinstance(old_deps['recommended'], list):
                        for dep in old_deps['recommended']:
                            if dep not in deps:
                                deps.append(dep)
                elif isinstance(old_deps, list):
                    # Already in new format
                    deps = old_deps
                
                if deps:
                    dependencies_map[yaml_file] = deps
                    
        except subprocess.CalledProcessError:
            # File might be new
            continue
    
    return dependencies_map

def restore_dependencies():
    """Restore dependencies to YAML files"""
    deps_map = get_original_dependencies()
    restored_count = 0
    
    for yaml_file, dependencies in deps_map.items():
        with open(yaml_file, 'r') as f:
            content = f.read()
            metadata = yaml.safe_load(content)
        
        if metadata and 'dependencies' not in metadata:
            # Add dependencies back
            metadata['dependencies'] = dependencies
            
            # Write back
            with open(yaml_file, 'w') as f:
                yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)
            
            print(f"✅ Restored dependencies for: {yaml_file.name}")
            restored_count += 1
    
    print(f"\n✅ Restored dependencies to {restored_count} files")

if __name__ == '__main__':
    restore_dependencies()
