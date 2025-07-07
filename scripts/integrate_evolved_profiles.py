#!/usr/bin/env python3
"""Integrate evolved profiles into rule selection system"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class EvolvedProfileIntegrator:
    def __init__(self, rules_dir: Path):
        self.rules_dir = rules_dir
        self.rule_config_path = rules_dir.parent / 'rule-config.yaml'
        self.evolved_profiles = {}
        
    def discover_evolved_profiles(self) -> Dict[str, Any]:
        """Find all evolved profiles in experimental directories"""
        profiles = {}
        
        # Search for evolved patterns
        for yaml_file in self.rules_dir.rglob('*evolved*.yaml'):
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)
                    if data:
                        profile_name = yaml_file.stem
                        profiles[profile_name] = {
                            'path': str(yaml_file.relative_to(self.rules_dir)),
                            'data': data,
                            'category': yaml_file.parent.parent.name
                        }
            except Exception as e:
                print(f"Skipping {yaml_file}: {e}")
                
        return profiles
    
    def analyze_evolution_metrics(self) -> Dict[str, float]:
        """Extract performance metrics from evolved profiles"""
        metrics = {
            'total_evolved': 0,
            'avg_fitness': 0.0,
            'best_fitness': 0.0,
            'convergence_rate': 0.0
        }
        
        # Analyze 700-evolution rules
        evolution_rules = list(self.rules_dir.glob('700-evolution/*.yaml'))
        metrics['total_evolved'] = len(evolution_rules)
        
        fitness_scores = []
        for rule_file in evolution_rules:
            try:
                with open(rule_file, 'r') as f:
                    data = yaml.safe_load(f)
                    if data and 'performance' in data:
                        success_rate = data['performance'].get('success_rate', 0)
                        fitness_scores.append(success_rate)
            except:
                pass
                
        if fitness_scores:
            metrics['avg_fitness'] = sum(fitness_scores) / len(fitness_scores)
            metrics['best_fitness'] = max(fitness_scores)
            
        return metrics
    
    def create_evolved_profile(self) -> Dict[str, Any]:
        """Generate evolved profile from performance data"""
        metrics = self.analyze_evolution_metrics()
        
        profile = {
            'name': 'evolved_optimized',
            'version': '1.0.0',
            'created': datetime.now().isoformat(),
            'description': 'Auto-generated profile from evolution metrics',
            'metrics': metrics,
            'rules': {
                'primary': [
                    '000-core/001-philosophers-stone.mdc',
                    '700-evolution/702-self-modifying-rules.mdc',
                    '600-experimental/602-quantum-superposition.mdc'
                ],
                'conditional': {
                    'high_complexity': [
                        '600-experimental/603-swarm-intelligence.mdc',
                        '700-evolution/703-rule-combination-learning.mdc'
                    ],
                    'safety_critical': [
                        '500-safety/502-prompt-injection-defense.mdc',
                        '500-safety/503-output-sanitization.mdc'
                    ]
                },
                'weights': {
                    'experimental': 0.3,
                    'evolution': 0.4,
                    'safety': 0.3
                }
            }
        }
        
        return profile
    
    def integrate_into_config(self, profile: Dict[str, Any]):
        """Add evolved profile to rule-config.yaml"""
        # Load existing config
        config = {}
        if self.rule_config_path.exists():
            with open(self.rule_config_path, 'r') as f:
                config = yaml.safe_load(f) or {}
        
        # Add profiles section if missing
        if 'profiles' not in config:
            config['profiles'] = {}
            
        # Add evolved profile
        config['profiles']['evolved_optimized'] = {
            'source': '600-experimental/evolved-profile-integrated.yaml',
            'description': profile['description'],
            'metrics': profile['metrics'],
            'activation': {
                'conditions': ['high_complexity', 'experimental_mode'],
                'priority': 85
            }
        }
        
        # Add selection strategy
        if 'selection_strategy' not in config:
            config['selection_strategy'] = {}
            
        config['selection_strategy']['evolved_profiles'] = {
            'enabled': True,
            'threshold': 0.85,
            'fallback': 'default'
        }
        
        # Save updated config
        with open(self.rule_config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            
        # Save profile separately
        profile_path = self.rules_dir / '600-experimental' / 'evolved-profile-integrated.yaml'
        with open(profile_path, 'w') as f:
            yaml.dump(profile, f, default_flow_style=False)
            
        return config
    
    def generate_integration_report(self) -> str:
        """Create integration summary"""
        profiles = self.discover_evolved_profiles()
        metrics = self.analyze_evolution_metrics()
        
        report = [
            "# Evolved Profile Integration Report",
            f"\nGenerated: {datetime.now().isoformat()}",
            "\n## Discovery Results",
            f"- Evolved profiles found: {len(profiles)}",
            f"- Evolution rules: {metrics['total_evolved']}",
            f"\n## Performance Metrics",
            f"- Average fitness: {metrics['avg_fitness']:.1f}%",
            f"- Best fitness: {metrics['best_fitness']:.1f}%",
            "\n## Integration Actions",
            "1. Created evolved_optimized profile",
            "2. Updated rule-config.yaml",
            "3. Added selection strategy",
            "\n## Activation Conditions",
            "- High complexity problems",
            "- Experimental mode enabled",
            "- Performance threshold > 85%"
        ]
        
        return '\n'.join(report)


def main():
    rules_dir = Path(__file__).parent.parent / 'rules'
    integrator = EvolvedProfileIntegrator(rules_dir)
    
    # Generate and integrate profile
    profile = integrator.create_evolved_profile()
    config = integrator.integrate_into_config(profile)
    
    # Generate report
    report = integrator.generate_integration_report()
    print(report)
    
    # Save report
    report_path = Path(__file__).parent / 'evolved-integration-report.md'
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"\n✓ Integration complete")
    print(f"✓ Report saved to: {report_path}")


if __name__ == '__main__':
    main()
