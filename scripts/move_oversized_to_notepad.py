#!/usr/bin/env python3
"""Move oversized rules to notepad system"""

from pathlib import Path
import shutil

def move_to_notepad():
    rules_dir = Path(__file__).parent.parent / 'rules'
    notepads_dir = Path(__file__).parent.parent / 'notepads'
    
    # Dynamic detection of oversized rules
    oversized_rules = []
    
    # Scan all MDC files for oversized content
    for mdc_file in rules_dir.rglob("*.mdc"):
        with open(mdc_file) as f:
            content = f.read()
            lines = len(content.splitlines())
            
        if lines > 150:  # Threshold for oversized
            oversized_rules.append((mdc_file, lines))
    
    if not oversized_rules:
        print("✅ No oversized rules found")
        return
    
    print(f"Found {len(oversized_rules)} oversized rules:")
    for rule_path, line_count in oversized_rules:
        print(f"  - {rule_path.relative_to(rules_dir)}: {line_count} lines")
    
    # Process each oversized rule
    for rule_path, line_count in oversized_rules:
        # Determine notepad path
        relative_path = rule_path.relative_to(rules_dir)
        notepad_path = notepads_dir / relative_path.parent / f"{rule_path.stem}-extended.md"
        
        # Create notepad directory if needed
        notepad_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Read original content
        with open(rule_path) as f:
            content = f.read()
        
        # Split into concise rule and extended content
        lines = content.splitlines()
        
        # Keep first 100 lines in main rule
        concise_content = '\n'.join(lines[:100])
        extended_content = '\n'.join(lines[100:])
        
        # Add reference to notepad in concise version
        concise_content += f"\n\n---\n**Extended content**: See `{notepad_path.relative_to(rules_dir.parent)}`"
        
        # Write concise version
        with open(rule_path, 'w') as f:
            f.write(concise_content)
        
        # Write extended content to notepad
        with open(notepad_path, 'w') as f:
            f.write(f"# Extended content for {rule_path.stem}\n\n")
            f.write(extended_content)
        
        print(f"✅ Moved extended content: {rule_path.name} → {notepad_path.name}")
    
    print(f"\n✅ Processed {len(oversized_rules)} oversized rules")

if __name__ == '__main__':
    move_to_notepad()
