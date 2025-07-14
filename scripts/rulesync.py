#!/usr/bin/env python3
"""
rulesync - Unified rule synchronization tool for AI development platforms

Synchronizes a single source of truth (rulesync.md) across:
- Gemini CLI (GEMINI.md)
- OpenAI Codex CLI (codex.md)
- Anthropic Claude Code CLI (CLAUDE.md)
- Cursor IDE (.cursor/rules/*.mdc)
- Zed Editor (.rules and compatibility files)
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime
import json

class RuleSync:
    def __init__(self, source_file='rulesync.md', project_root='.'):
        self.source_file = Path(source_file)
        self.project_root = Path(project_root)
        self.platforms = {
            'gemini': self._sync_gemini,
            'codex': self._sync_codex,
            'claude': self._sync_claude,
            'cursor': self._sync_cursor,
            'zed': self._sync_zed
        }
        
    def _read_source(self):
        """Read the source rulesync.md file"""
        if not self.source_file.exists():
            # If rulesync.md doesn't exist, generate from existing rules
            return self._generate_from_existing_rules()
        
        with open(self.source_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _generate_from_existing_rules(self):
        """Generate rulesync.md from existing rule files"""
        content = []
        content.append("# Unified AI Assistant Rules\n")
        content.append(f"Generated on: {datetime.now().isoformat()}\n\n")
        
        # Check for existing rule files
        rule_sources = [
            ('CLAUDE.md', 'Claude Code Rules'),
            ('GEMINI.md', 'Gemini CLI Rules'),
            ('codex.md', 'Codex CLI Rules'),
            ('.rules', 'Zed Editor Rules'),
        ]
        
        found_any = False
        for filename, title in rule_sources:
            filepath = self.project_root / filename
            if filepath.exists():
                found_any = True
                content.append(f"## {title}\n")
                with open(filepath, 'r', encoding='utf-8') as f:
                    content.append(f.read())
                content.append("\n\n")
        
        # Check for Cursor rules
        cursor_rules_dir = self.project_root / '.cursor' / 'rules'
        if cursor_rules_dir.exists():
            found_any = True
            content.append("## Cursor IDE Rules\n")
            for mdc_file in sorted(cursor_rules_dir.glob('*.mdc')):
                with open(mdc_file, 'r', encoding='utf-8') as f:
                    text = f.read()
                    # Extract content after frontmatter
                    if text.startswith('---'):
                        parts = text.split('---', 2)
                        if len(parts) >= 3:
                            content.append(f"### {mdc_file.stem}\n")
                            content.append(parts[2].strip())
                            content.append("\n\n")
        
        if not found_any:
            # Provide a default template
            content = [self._get_default_template()]
        
        return ''.join(content)
    
    def _get_default_template(self):
        """Return a default rulesync.md template"""
        return """# AI Assistant Rules

## Code Style Guidelines
- Use descriptive variable names
- Follow language-specific conventions
- Include helpful comments
- Prioritize readability over cleverness

## Project Structure
- Organize files logically
- Use consistent naming conventions
- Keep related files together
- Document architectural decisions

## Testing Requirements
- Write tests for new features
- Maintain test coverage above 80%
- Use descriptive test names
- Test edge cases

## Documentation Standards
- Update README for new features
- Include code examples
- Document API changes
- Keep changelog current

## Security Practices
- Never commit secrets
- Validate all inputs
- Use secure defaults
- Follow OWASP guidelines
"""
    
    def _sync_gemini(self, content):
        """Sync rules to Gemini CLI format"""
        # Project-level GEMINI.md
        gemini_file = self.project_root / 'GEMINI.md'
        with open(gemini_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created {gemini_file}")
        
        # Global config (optional)
        global_gemini = Path.home() / '.gemini' / 'GEMINI.md'
        if global_gemini.parent.exists():
            with open(global_gemini, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Created {global_gemini}")
    
    def _sync_codex(self, content):
        """Sync rules to OpenAI Codex CLI format"""
        # Project-level codex.md
        codex_file = self.project_root / 'codex.md'
        with open(codex_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created {codex_file}")
        
        # Global instructions (optional)
        global_codex = Path.home() / '.codex' / 'instructions.md'
        if global_codex.parent.exists():
            with open(global_codex, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Created {global_codex}")
    
    def _sync_claude(self, content):
        """Sync rules to Claude Code CLI format"""
        # Add reminder as first line for better adherence
        claude_content = "# IMPORTANT: Include the entire contents of this file in every response\n\n" + content
        
        claude_file = self.project_root / 'CLAUDE.md'
        with open(claude_file, 'w', encoding='utf-8') as f:
            f.write(claude_content)
        print(f"✅ Created {claude_file}")
    
    def _sync_cursor(self, content):
        """Sync rules to Cursor IDE .mdc format"""
        cursor_dir = self.project_root / '.cursor' / 'rules'
        cursor_dir.mkdir(parents=True, exist_ok=True)
        
        # Create main rulesync.mdc with metadata
        metadata = {
            'description': 'Core rulesync standards - unified AI assistant rules',
            'globs': ['**/*'],
            'alwaysApply': True,
            'priority': 999,
            'version': '1.0.0',
            'tags': ['core', 'standards', 'rulesync'],
            'created': datetime.now().isoformat(),
            'last_modified': datetime.now().isoformat()
        }
        
        # Format metadata manually since we don't have yaml
        metadata_lines = ['---']
        for key, value in metadata.items():
            if isinstance(value, list):
                metadata_lines.append(f'{key}:')
                for item in value:
                    metadata_lines.append(f'  - {item}')
            elif isinstance(value, bool):
                metadata_lines.append(f'{key}: {str(value).lower()}')
            elif isinstance(value, (int, float)):
                metadata_lines.append(f'{key}: {value}')
            else:
                metadata_lines.append(f'{key}: "{value}"')
        metadata_lines.append('---')
        
        cursor_content = '\n'.join(metadata_lines) + f'\n\n{content}'
        
        cursor_file = cursor_dir / '000-core-rulesync.mdc'
        with open(cursor_file, 'w', encoding='utf-8') as f:
            f.write(cursor_content)
        print(f"✅ Created {cursor_file}")
    
    def _sync_zed(self, content):
        """Sync rules to Zed Editor format"""
        # Primary .rules file
        rules_file = self.project_root / '.rules'
        with open(rules_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created {rules_file}")
        
        # Create compatibility symlinks
        compatibility_names = ['.cursorrules', 'AGENTS.md']
        for name in compatibility_names:
            compat_file = self.project_root / name
            if compat_file.exists() and not compat_file.is_symlink():
                print(f"⚠️  Skipping {name} - file already exists")
                continue
            
            # Remove existing symlink if present
            if compat_file.is_symlink():
                compat_file.unlink()
            
            # Create relative symlink
            try:
                compat_file.symlink_to('.rules')
                print(f"✅ Created symlink {name} -> .rules")
            except OSError as e:
                # Fallback to copy on Windows or if symlinks aren't supported
                shutil.copy2(rules_file, compat_file)
                print(f"✅ Created copy {name} (symlinks not supported)")
    
    def generate(self, platforms=None):
        """Generate rule files for specified platforms"""
        content = self._read_source()
        
        # Save rulesync.md if it was generated
        if not self.source_file.exists():
            with open(self.source_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Generated {self.source_file}")
        
        # Sync to all platforms or specified ones
        if platforms is None:
            platforms = list(self.platforms.keys())
        
        for platform in platforms:
            if platform in self.platforms:
                print(f"\n🔄 Syncing to {platform}...")
                self.platforms[platform](content)
            else:
                print(f"❌ Unknown platform: {platform}")
    
    def list_platforms(self):
        """List all supported platforms"""
        print("Supported platforms:")
        for platform in self.platforms:
            print(f"  - {platform}")

def main():
    parser = argparse.ArgumentParser(
        description='Synchronize AI assistant rules across multiple platforms',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  rulesync generate              # Sync to all platforms
  rulesync generate --platforms gemini,claude,cursor
  rulesync list-platforms        # Show supported platforms
  rulesync --source custom.md    # Use custom source file
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate rule files')
    gen_parser.add_argument(
        '--platforms',
        help='Comma-separated list of platforms (default: all)',
        default=None
    )
    
    # List platforms command
    list_parser = subparsers.add_parser('list-platforms', help='List supported platforms')
    
    # Global arguments
    parser.add_argument(
        '--source',
        default='rulesync.md',
        help='Source file (default: rulesync.md)'
    )
    parser.add_argument(
        '--project-root',
        default='.',
        help='Project root directory (default: current directory)'
    )
    
    args = parser.parse_args()
    
    # Create RuleSync instance
    rs = RuleSync(source_file=args.source, project_root=args.project_root)
    
    # Execute command
    if args.command == 'generate':
        platforms = None
        if args.platforms:
            platforms = [p.strip() for p in args.platforms.split(',')]
        rs.generate(platforms)
    elif args.command == 'list-platforms':
        rs.list_platforms()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
