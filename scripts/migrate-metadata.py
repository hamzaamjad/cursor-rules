#!/usr/bin/env python3
"""
Rule Metadata Migration Script
Migrates existing rule files to enhanced metadata format
Version: 1.0.0
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple

class MetadataMigrator:
    def __init__(self, rules_dir: str, template_path: str):
        self.rules_dir = Path(rules_dir)
        self.template_path = Path(template_path)
        self.migration_log = []
        self.errors = []
        
        # Load template
        with open(self.template_path, 'r') as f:
            self.template = yaml.safe_load(f.read().split('---')[1])
    
    def extract_current_metadata(self, content: str) -> Tuple[Dict, str]:
        """Extract existing YAML frontmatter and remaining content"""
        # Handle potential duplicate frontmatter blocks
        if content.startswith('---'):
            parts = content.split('---', 3)
            if len(parts) >= 3:
                try:
                    # Try to parse the second part as YAML
                    metadata = yaml.safe_load(parts[1])
                    remaining_content = '---'.join(parts[2:])
                    return metadata or {}, remaining_content
                except:
                    pass
        
        return {}, content    
    def infer_category(self, file_path: Path) -> str:
        """Infer category from file path"""
        relative_path = file_path.relative_to(self.rules_dir)
        if len(relative_path.parts) > 1:
            return relative_path.parts[0]
        return "root"
    
    def infer_performance_metrics(self, rule_name: str, content: str) -> Dict:
        """Infer performance metrics from rule content and known data"""
        metrics = {
            "tokenReduction": "0%",
            "accuracyImprovement": "0%",
            "processingOverhead": "minimal",
            "empiricalValidation": "To be measured"
        }
        
        # Known performance data from v1.1.0
        performance_data = {
            "context-trim": {"tokenReduction": "93%", "processingOverhead": "minimal"},
            "concise-comms": {"tokenReduction": "48.7%", "processingOverhead": "minimal"},
            "divergence-convergence": {"processingOverhead": "moderate", "empiricalValidation": "15% overhead due to two-phase process"},
            "wildcard-brainstorm": {"accuracyImprovement": "25-50%", "empiricalValidation": "Creativity increase measured"},
            "chain-of-code": {"accuracyImprovement": "17.9%", "empiricalValidation": "IEEE study 2024"},
            "sparring-partner": {"accuracyImprovement": "41%", "empiricalValidation": "Critical thinking preservation"}
        }
        
        # Check if rule matches known performance data
        for pattern, data in performance_data.items():
            if pattern in rule_name.lower():
                metrics.update(data)
                break
        
        # Infer overhead based on content analysis
        if "tree of thoughts" in content.lower() or "multiple branches" in content.lower():
            metrics["processingOverhead"] = "significant"
        elif "phase" in content.lower() or "multi-step" in content.lower():
            metrics["processingOverhead"] = "moderate"
        
        return metrics
    
    def detect_dependencies(self, content: str) -> Dict[str, list]:
        """Detect rule dependencies from content"""
        dependencies = {
            "required": [],
            "recommended": [],
            "incompatible": []
        }
        
        # Look for explicit rule references
        rule_refs = re.findall(r'@Rule:([a-zA-Z0-9\-_.]+)', content)
        dependencies["required"].extend(rule_refs)
        
        # Look for implicit dependencies
        dependency_patterns = {
            "divergence-convergence": ["internal_thought", "user_facing_response", "phase"],
            "risk-checkpoint": ["safety", "validation", "checkpoint"],
            "context-trim": ["compression", "token budget", "trim"]
        }        
        for rule, patterns in dependency_patterns.items():
            if any(pattern in content.lower() for pattern in patterns):
                if rule not in dependencies["recommended"]:
                    dependencies["recommended"].append(rule)
        
        # Known incompatibilities
        if "wildcard-brainstorm" in content.lower() and "concise-comms" in content.lower():
            dependencies["incompatible"] = ["concise-comms", "wildcard-brainstorm"]
        
        return dependencies
    
    def generate_tags(self, rule_name: str, content: str, category: str) -> list:
        """Generate relevant tags based on content analysis"""
        tags = []
        
        # Category-based tags
        category_tags = {
            "000-core": ["foundational", "strategic"],
            "100-cognitive": ["cognitive-enhancement", "reasoning"],
            "200-domain": ["domain-specific", "specialized"],
            "300-integration": ["integration", "tooling"],
            "400-patterns": ["patterns", "best-practices"],
            "600-experimental": ["experimental", "research"],
            "700-evolution": ["evolution", "meta-learning"]
        }
        
        if category in category_tags:
            tags.extend(category_tags[category])        
        # Content-based tags
        if "performance" in content.lower() or "efficiency" in content.lower():
            tags.append("performance")
        if "safety" in content.lower() or "risk" in content.lower():
            tags.append("safety")
        if "token" in content.lower() or "compression" in content.lower():
            tags.append("optimization")
        if "test" in content.lower() or "validation" in content.lower():
            tags.append("quality")
        
        return list(set(tags))  # Remove duplicates
    
    def migrate_rule(self, file_path: Path) -> bool:
        """Migrate a single rule file to enhanced metadata format"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Extract current metadata and content
            current_metadata, remaining_content = self.extract_current_metadata(content)
            
            # Create enhanced metadata
            enhanced_metadata = self.template.copy()
            
            # Preserve existing fields
            enhanced_metadata["description"] = current_metadata.get("description", "")
            enhanced_metadata["alwaysApply"] = current_metadata.get("alwaysApply", False)
            enhanced_metadata["globs"] = current_metadata.get("globs", [])            
            # Add new fields
            enhanced_metadata["version"] = "1.0.0"
            enhanced_metadata["lastUpdated"] = datetime.now().strftime("%Y-%m-%d")
            enhanced_metadata["author"] = "migrated"
            
            # Infer category
            category = self.infer_category(file_path)
            enhanced_metadata["category"] = category
            
            # Infer performance metrics
            rule_name = file_path.stem
            enhanced_metadata["performance"] = self.infer_performance_metrics(rule_name, remaining_content)
            
            # Detect dependencies
            enhanced_metadata["dependencies"] = self.detect_dependencies(remaining_content)
            
            # Generate tags
            enhanced_metadata["tags"] = self.generate_tags(rule_name, remaining_content, category)
            
            # Remove template defaults for research and examples if not populated
            enhanced_metadata["research"] = []
            enhanced_metadata["examples"] = []
            enhanced_metadata["conflicts"] = []
            enhanced_metadata["notes"] = ""
            
            # Build new content
            new_content = f"---\n{yaml.dump(enhanced_metadata, default_flow_style=False, sort_keys=False)}---\n{remaining_content}"
            
            # Write back
            with open(file_path, 'w') as f:
                f.write(new_content)
            
            self.migration_log.append(f"✓ Migrated: {file_path.relative_to(self.rules_dir)}")
            return True
            
        except Exception as e:
            self.errors.append(f"✗ Failed to migrate {file_path}: {str(e)}")
            return False
    
    def generate_report(self) -> str:
        """Generate migration report"""
        report = []
        report.append("# Metadata Migration Report")
        report.append(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"\nTotal files processed: {len(self.migration_log) + len(self.errors)}")
        report.append(f"Successful migrations: {len(self.migration_log)}")
        report.append(f"Failed migrations: {len(self.errors)}")
        
        if self.migration_log:
            report.append("\n## Successfully Migrated Rules")
            for log in sorted(self.migration_log):
                report.append(log)
        
        if self.errors:
            report.append("\n## Migration Errors")
            for error in self.errors:
                report.append(error)
        
        return "\n".join(report)    
    def run(self, dry_run: bool = False) -> str:
        """Execute migration for all rule files"""
        rule_files = list(self.rules_dir.rglob("*.mdc"))
        
        if dry_run:
            return f"Dry run: Would migrate {len(rule_files)} rule files"
        
        for rule_file in rule_files:
            self.migrate_rule(rule_file)
        
        return self.generate_report()

def main():
    """Main migration entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate rule metadata to enhanced format")
    parser.add_argument("--rules-dir", default="./rules", help="Rules directory")
    parser.add_argument("--template", default="./templates/enhanced-metadata-template.yaml", help="Template file")
    parser.add_argument("--dry-run", action="store_true", help="Preview migration without changes")
    
    args = parser.parse_args()
    
    migrator = MetadataMigrator(args.rules_dir, args.template)
    report = migrator.run(dry_run=args.dry_run)
    
    print(report)
    
    # Save report only if not dry run
    if not args.dry_run:
        report_path = Path(args.rules_dir).parent / "METADATA_MIGRATION_REPORT.md"
        with open(report_path, 'w') as f:
            f.write(report)
        print(f"\nReport saved to: {report_path}")

if __name__ == "__main__":
    main()