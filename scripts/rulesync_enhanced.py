#!/usr/bin/env python3
"""
rulesync Enhanced - Intelligent rule synchronization with profile-based aggregation

Features:
- Profile-based rule selection
- Token-aware aggregation
- Platform-specific optimization
- Rule dependency analysis
- Validation pipeline
"""

import os
import sys
import shutil
import argparse
import yaml
import re
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Optional, Set, Tuple

class RuleSyncEnhanced:
    def __init__(self, source_file='rulesync.md', project_root='.'):
        self.source_file = Path(source_file)
        self.project_root = Path(project_root)
        self.rules_dir = self.project_root / 'rules'
        self.profiles_dir = self.project_root / 'profiles'
        self.platforms = {
            'gemini': self._sync_gemini,
            'codex': self._sync_codex,
            'claude': self._sync_claude,
            'cursor': self._sync_cursor,
            'zed': self._sync_zed
        }
        self.rule_cache = {}
        self.profile_cache = {}
        
    def _load_profile(self, profile_name: str) -> Dict:
        """Load a profile configuration"""
        if profile_name in self.profile_cache:
            return self.profile_cache[profile_name]
        
        profile_path = self.profiles_dir / f"{profile_name}.yaml"
        if not profile_path.exists():
            raise FileNotFoundError(f"Profile '{profile_name}' not found at {profile_path}")
        
        with open(profile_path, 'r', encoding='utf-8') as f:
            profile = yaml.safe_load(f)
        
        self.profile_cache[profile_name] = profile
        return profile
    
    def _load_rule_content(self, rule_path: str) -> Tuple[str, Dict]:
        """Load rule content and metadata"""
        if rule_path in self.rule_cache:
            return self.rule_cache[rule_path]
        
        full_path = self.rules_dir / rule_path
        if not full_path.exists():
            print(f"⚠️  Warning: Rule file {rule_path} not found")
            return "", {}
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract metadata and content
        metadata = {}
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    metadata = yaml.safe_load(parts[1])
                except yaml.YAMLError:
                    metadata = {}
                content = parts[2].strip()
        
        self.rule_cache[rule_path] = (content, metadata)
        return content, metadata
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation)"""
        # Simple estimation: ~4 characters per token
        return len(text) // 4
    
    def _select_rules_for_platform(self, profile: Dict, platform: str) -> List[str]:
        """Select rules for a specific platform based on profile"""
        platform_config = profile.get('platform_optimizations', {}).get(platform, {})
        include_categories = platform_config.get('include_categories', [])
        exclude_rules = set(platform_config.get('exclude_rules', []))
        token_budget = platform_config.get('token_budget', 1000)
        
        selected_rules = []
        total_tokens = 0
        
        # Helper function to add rules from a category
        def add_category_rules(category_name: str, rules: List[str]):
            nonlocal total_tokens
            for rule in rules:
                if rule in exclude_rules:
                    continue
                
                content, metadata = self._load_rule_content(rule)
                if not content:
                    continue
                
                rule_tokens = self._estimate_tokens(content)
                if total_tokens + rule_tokens <= token_budget:
                    selected_rules.append(rule)
                    total_tokens += rule_tokens
                else:
                    print(f"⚠️  Skipping {rule} - would exceed token budget ({total_tokens + rule_tokens} > {token_budget})")
        
        # Process categories in order of importance
        for category in include_categories:
            if category == 'core_rules':
                add_category_rules('core_rules', profile.get('core_rules', []))
            elif category == 'cognitive_rules':
                add_category_rules('cognitive_rules', profile.get('cognitive_rules', []))
            elif category == 'integration_rules':
                add_category_rules('integration_rules', profile.get('integration_rules', []))
            elif category.startswith('project_rules'):
                # Handle nested project rules
                parts = category.split('.')
                if len(parts) == 1:
                    # All project rules
                    for subcategory, rules in profile.get('project_rules', {}).items():
                        add_category_rules(f'project_rules.{subcategory}', rules)
                else:
                    # Specific subcategory
                    subcategory = parts[1]
                    rules = profile.get('project_rules', {}).get(subcategory, [])
                    add_category_rules(category, rules)
        
        print(f"📊 Selected {len(selected_rules)} rules for {platform} ({total_tokens} tokens)")
        return selected_rules
    
    def _generate_with_profile(self, profile_name: str, platforms: Optional[List[str]] = None):
        """Generate rules using a profile configuration"""
        profile = self._load_profile(profile_name)
        
        if platforms is None:
            platforms = list(self.platforms.keys())
        
        for platform in platforms:
            if platform not in self.platforms:
                print(f"❌ Unknown platform: {platform}")
                continue
            
            print(f"\\n🔄 Generating {platform} rules with profile '{profile_name}'...")
            
            # Select rules for this platform
            selected_rules = self._select_rules_for_platform(profile, platform)
            
            if not selected_rules:
                print(f"⚠️  No rules selected for {platform}")
                continue
            
            # Generate aggregated content
            content_parts = []
            content_parts.append(f"# {profile['name']} - {platform.title()} Rules\\n")
            content_parts.append(f"Generated on: {datetime.now().isoformat()}\\n")
            content_parts.append(f"Profile: {profile['name']} v{profile['version']}\\n")
            content_parts.append(f"Selected rules: {len(selected_rules)}\\n\\n")
            
            for rule_path in selected_rules:
                content, metadata = self._load_rule_content(rule_path)
                if content:
                    content_parts.append(f"## {rule_path}\\n")
                    content_parts.append(content)
                    content_parts.append("\\n\\n")
            
            aggregated_content = ''.join(content_parts)
            
            # Sync to platform
            self.platforms[platform](aggregated_content)
    
    def generate(self, platforms=None, profile=None):
        """Generate rule files for specified platforms"""
        if profile:
            # Use profile-based generation
            self._generate_with_profile(profile, platforms)
        else:
            # Traditional generation - fallback to original method
            print("⚠️  Using legacy generation mode - consider using profiles")
            self._generate_legacy(platforms)
    
    def _generate_legacy(self, platforms):
        """Legacy generation method"""
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
                print(f"\\n🔄 Syncing to {platform}...")
                self.platforms[platform](content)
            else:
                print(f"❌ Unknown platform: {platform}")
    
    def _read_source(self):
        """Read the source rulesync.md file"""
        if not self.source_file.exists():
            return self._get_default_template()
        
        with open(self.source_file, 'r', encoding='utf-8') as f:
            return f.read()
    
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
        claude_content = "# IMPORTANT: Include the entire contents of this file in every response\\n\\n" + content
        
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
            'description': 'Enhanced rulesync with profile-based aggregation',
            'globs': ['**/*'],
            'alwaysApply': True,
            'priority': 999,
            'version': '2.0.0',
            'tags': ['core', 'standards', 'rulesync', 'enhanced'],
            'created': datetime.now().isoformat(),
            'last_modified': datetime.now().isoformat()
        }
        
        # Format metadata manually
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
        
        cursor_content = '\\n'.join(metadata_lines) + f'\\n\\n{content}'
        
        cursor_file = cursor_dir / '000-core-rulesync-enhanced.mdc'
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
    
    def create_profile(self, name: str, description: str, rules: List[str], categories: List[str]):
        """Create a new profile"""
        profile = {
            'name': name,
            'description': description,
            'version': '1.0.0',
            'created': datetime.now().isoformat(),
            'author': 'Generated by rulesync',
            'platform_limits': {
                'claude': 4000,
                'cursor': 500,
                'gemini': 3000,
                'codex': 2000,
                'zed': 1000
            },
            'core_rules': [],
            'project_rules': {},
            'platform_optimizations': {}
        }
        
        # Basic platform configuration
        for platform in self.platforms:
            profile['platform_optimizations'][platform] = {
                'include_categories': categories,
                'exclude_rules': [],
                'token_budget': profile['platform_limits'][platform]
            }
        
        # Categorize rules
        for rule in rules:
            if rule.startswith('000-core/'):
                profile['core_rules'].append(rule)
            else:
                # Simple categorization based on directory
                category = rule.split('/')[0]
                if category not in profile['project_rules']:
                    profile['project_rules'][category] = []
                profile['project_rules'][category].append(rule)
        
        # Save profile
        self.profiles_dir.mkdir(exist_ok=True)
        profile_path = self.profiles_dir / f"{name}.yaml"
        with open(profile_path, 'w', encoding='utf-8') as f:
            yaml.dump(profile, f, default_flow_style=False, sort_keys=False)
        
        print(f"✅ Created profile '{name}' at {profile_path}")
    
    def validate_platform_compatibility(self, platform: str, profile_name: str = None):
        """Validate platform compatibility"""
        if profile_name:
            profile = self._load_profile(profile_name)
            rules = self._select_rules_for_platform(profile, platform)
            
            total_tokens = 0
            for rule_path in rules:
                content, metadata = self._load_rule_content(rule_path)
                total_tokens += self._estimate_tokens(content)
            
            platform_limit = profile.get('platform_limits', {}).get(platform, 1000)
            
            print(f"\\n📊 Platform Compatibility Report: {platform}")
            print(f"Selected rules: {len(rules)}")
            print(f"Total tokens: {total_tokens}")
            print(f"Platform limit: {platform_limit}")
            print(f"Status: {'✅ Compatible' if total_tokens <= platform_limit else '❌ Exceeds limit'}")
            
            if total_tokens > platform_limit:
                print(f"⚠️  Exceeds limit by {total_tokens - platform_limit} tokens")
        else:
            print(f"Platform {platform} basic validation - no profile specified")
    
    def aggregate_by_category(self, categories: List[str], output_file: str = None):
        """Aggregate rules by category"""
        if not self.rules_dir.exists():
            print(f"❌ Rules directory not found: {self.rules_dir}")
            return
        
        content_parts = []
        content_parts.append("# Aggregated Rules by Category\\n")
        content_parts.append(f"Generated on: {datetime.now().isoformat()}\\n")
        content_parts.append(f"Categories: {', '.join(categories)}\\n\\n")
        
        for category in categories:
            category_dir = self.rules_dir / category
            if not category_dir.exists():
                print(f"⚠️  Category directory not found: {category}")
                continue
            
            content_parts.append(f"## {category}\\n\\n")
            
            for rule_file in sorted(category_dir.glob('*.mdc')):
                rule_path = f"{category}/{rule_file.name}"
                content, metadata = self._load_rule_content(rule_path)
                if content:
                    content_parts.append(f"### {rule_file.stem}\\n")
                    content_parts.append(content)
                    content_parts.append("\\n\\n")
        
        aggregated_content = ''.join(content_parts)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(aggregated_content)
            print(f"✅ Aggregated content saved to {output_file}")
        else:
            print(aggregated_content)
    
    def list_profiles(self):
        """List available profiles"""
        if not self.profiles_dir.exists():
            print("No profiles directory found")
            return
        
        print("Available profiles:")
        for profile_file in sorted(self.profiles_dir.glob('*.yaml')):
            try:
                with open(profile_file, 'r', encoding='utf-8') as f:
                    profile = yaml.safe_load(f)
                print(f"  - {profile['name']} (v{profile['version']}) - {profile['description']}")
            except Exception as e:
                print(f"  - {profile_file.stem} (error loading: {e})")
    
    def list_platforms(self):
        """List all supported platforms"""
        print("Supported platforms:")
        for platform in self.platforms:
            print(f"  - {platform}")
    
    def analyze_rules(self):
        """Analyze rule statistics"""
        if not self.rules_dir.exists():
            print(f"❌ Rules directory not found: {self.rules_dir}")
            return
        
        stats = {
            'total_rules': 0,
            'categories': {},
            'total_tokens': 0,
            'avg_tokens_per_rule': 0
        }
        
        for rule_file in self.rules_dir.rglob('*.mdc'):
            category = rule_file.parent.name
            if category not in stats['categories']:
                stats['categories'][category] = {'count': 0, 'tokens': 0}
            
            relative_path = rule_file.relative_to(self.rules_dir)
            content, metadata = self._load_rule_content(str(relative_path))
            
            if content:
                tokens = self._estimate_tokens(content)
                stats['total_rules'] += 1
                stats['total_tokens'] += tokens
                stats['categories'][category]['count'] += 1
                stats['categories'][category]['tokens'] += tokens
        
        if stats['total_rules'] > 0:
            stats['avg_tokens_per_rule'] = stats['total_tokens'] // stats['total_rules']
        
        print("\\n📊 Rule Analysis Report")
        print(f"Total rules: {stats['total_rules']}")
        print(f"Total tokens: {stats['total_tokens']}")
        print(f"Average tokens per rule: {stats['avg_tokens_per_rule']}")
        print("\\nBy category:")
        for category, data in sorted(stats['categories'].items()):
            avg_tokens = data['tokens'] // data['count'] if data['count'] > 0 else 0
            print(f"  {category}: {data['count']} rules, {data['tokens']} tokens (avg: {avg_tokens})")

def main():
    parser = argparse.ArgumentParser(
        description='Enhanced rule synchronization with intelligent aggregation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  rulesync_enhanced generate --profile mirror-project
  rulesync_enhanced generate --profile mirror-project --platforms claude,cursor
  rulesync_enhanced create-profile --name my-project --description "My project rules"
  rulesync_enhanced validate --platform cursor --profile mirror-project
  rulesync_enhanced aggregate --categories 000-core,500-safety
  rulesync_enhanced analyze
  rulesync_enhanced list-profiles
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate rule files')
    gen_parser.add_argument('--platforms', help='Comma-separated list of platforms')
    gen_parser.add_argument('--profile', help='Profile name to use for generation')
    
    # Create profile command
    profile_parser = subparsers.add_parser('create-profile', help='Create a new profile')
    profile_parser.add_argument('--name', required=True, help='Profile name')
    profile_parser.add_argument('--description', required=True, help='Profile description')
    profile_parser.add_argument('--rules', help='Comma-separated list of rules')
    profile_parser.add_argument('--categories', help='Comma-separated list of categories')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate platform compatibility')
    validate_parser.add_argument('--platform', required=True, help='Platform to validate')
    validate_parser.add_argument('--profile', help='Profile to validate against')
    
    # Aggregate command
    agg_parser = subparsers.add_parser('aggregate', help='Aggregate rules by category')
    agg_parser.add_argument('--categories', required=True, help='Comma-separated list of categories')
    agg_parser.add_argument('--output', help='Output file (default: stdout)')
    
    # List profiles command
    list_profiles_parser = subparsers.add_parser('list-profiles', help='List available profiles')
    
    # List platforms command
    list_platforms_parser = subparsers.add_parser('list-platforms', help='List supported platforms')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze rule statistics')
    
    # Global arguments
    parser.add_argument('--source', default='rulesync.md', help='Source file')
    parser.add_argument('--project-root', default='.', help='Project root directory')
    
    args = parser.parse_args()
    
    # Create RuleSync instance
    rs = RuleSyncEnhanced(source_file=args.source, project_root=args.project_root)
    
    # Execute command
    if args.command == 'generate':
        platforms = None
        if args.platforms:
            platforms = [p.strip() for p in args.platforms.split(',')]
        rs.generate(platforms, args.profile)
    elif args.command == 'create-profile':
        rules = []
        if args.rules:
            rules = [r.strip() for r in args.rules.split(',')]
        categories = []
        if args.categories:
            categories = [c.strip() for c in args.categories.split(',')]
        rs.create_profile(args.name, args.description, rules, categories)
    elif args.command == 'validate':
        rs.validate_platform_compatibility(args.platform, args.profile)
    elif args.command == 'aggregate':
        categories = [c.strip() for c in args.categories.split(',')]
        rs.aggregate_by_category(categories, args.output)
    elif args.command == 'list-profiles':
        rs.list_profiles()
    elif args.command == 'list-platforms':
        rs.list_platforms()
    elif args.command == 'analyze':
        rs.analyze_rules()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()