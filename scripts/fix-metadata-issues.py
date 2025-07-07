#!/usr/bin/env python3
"""
Fix metadata issues in rule files
- Remove duplicate frontmatter
- Restore missing descriptions
- Fix formatting issues
"""

import os
import re
from pathlib import Path

def fix_duplicate_frontmatter(file_path):
    """Fix files with duplicate frontmatter blocks"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to match duplicate frontmatter
    pattern = r'^---\n(.*?)\n---\n---\n(.*?)\n---\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    
    if match:
        first_meta = match.group(1)
        second_meta = match.group(2)
        body = match.group(3)
        
        # Parse second metadata for description and globs
        desc_match = re.search(r'description:\s*(.+)', second_meta)
        globs_match = re.search(r'globs:\s*(.+)', second_meta)
        
        if desc_match:
            # Update description in first metadata
            desc_value = desc_match.group(1).strip()
            first_meta = re.sub(r"description:\s*''", f"description: '{desc_value}'", first_meta)
        
        if globs_match:
            # Update globs in first metadata
            globs_value = globs_match.group(1).strip()
            # Convert comma-separated to YAML list
            if ',' in globs_value:
                globs_list = [f"'{g.strip()}'" for g in globs_value.split(',')]
                globs_yaml = '[' + ', '.join(globs_list) + ']'
                first_meta = re.sub(r'globs:\s*\[]', f'globs: {globs_yaml}', first_meta)
        
        # Reconstruct file with single frontmatter
        new_content = f"---\n{first_meta}\n---\n{body}"
        
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        return True
    
    return False

def main():
    rules_dir = Path("/Users/hamzaamjad/cursor-rules/rules")
    fixed_files = []
    
    for rule_file in rules_dir.rglob("*.mdc"):
        if fix_duplicate_frontmatter(rule_file):
            fixed_files.append(rule_file.relative_to(rules_dir))
            print(f"Fixed: {rule_file.name}")
    
    print(f"\nTotal files fixed: {len(fixed_files)}")
    
    if fixed_files:
        print("\nFixed files:")
        for f in sorted(fixed_files):
            print(f"  - {f}")

if __name__ == "__main__":
    main()
