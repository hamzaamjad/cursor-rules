#!/usr/bin/env python3
"""Move oversized rules to notepad system"""

from pathlib import Path

def move_to_notepad():
    rules_dir = Path(__file__).parent.parent / 'rules'
    notepads_dir = Path(__file__).parent.parent / 'notepads'
    
    oversized_rules = [
        ('400-patterns/448-prompt-eval.mdc', 167),
        ('400-patterns/prompt-eval-data-analytics.mdc', 169),
        ('400-patterns/447-prompt-eval-data-analytics.mdc', 169),
        ('400-patterns/prompt-eval.mdc', 167),
        ('100-cognitive/108-cognitive-load-balancing.mdc', 159)
    ]
    
    for rule_path, line_count in oversized_rules:
        mdc_file = rules_dir / rule_path
        if not mdc_file.exists():
            print(f"❌ Not found: {rule_path}")
            continue
            
        # Read content
        content = mdc_file.read_text()
        lines = content.splitlines()
        
        # Extract first 100 lines for rule, rest for notepad
        rule_content = '\n'.join(lines[:100])
        notepad_content = '\n'.join(lines[100:])
        
        # Add reference to notepad
        rule_content += '\n\n## Extended Content\n\nSee notepad: `' + mdc_file.stem + '-extended.md`'
        
        # Write trimmed rule
        mdc_file.write_text(rule_content)
        print(f"✂️ Trimmed: {mdc_file.name} to 100 lines")
        
        # Create notepad
        notepad_path = notepads_dir / mdc_file.parent.name / f'{mdc_file.stem}-extended.md'
        notepad_path.parent.mkdir(parents=True, exist_ok=True)
        notepad_path.write_text(f'# Extended content for {mdc_file.stem}\n\n' + notepad_content)
        print(f"📄 Created notepad: {notepad_path.name}")

if __name__ == '__main__':
    move_to_notepad()