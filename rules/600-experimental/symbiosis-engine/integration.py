#!/usr/bin/env python3
"""
Integration module for using evolved rule profiles in Mirror project
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import random

@dataclass
class EvolvedProfile:
    """Represents an evolved rule profile"""
    name: str
    profile_id: str
    rules: List[str]
    fitness: float
    recommended_tasks: List[str]
    performance_metrics: Dict[str, float]
    constraint_level: float = 0.6  # Discovered optimal

class RuleProfileSelector:
    """Selects optimal rule profile based on task characteristics"""
    
    def __init__(self, profiles_path: Path):
        self.profiles = self._load_profiles(profiles_path)
        self.task_patterns = self._initialize_task_patterns()
        
    def _load_profiles(self, path: Path) -> Dict[str, EvolvedProfile]:
        """Load evolved profiles from YAML"""
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
            
        profiles = {}
        for key, value in data.items():
            if key.startswith('evolved_'):
                profile = EvolvedProfile(
                    name=value['name'],
                    profile_id=key,
                    rules=value['rules'],
                    fitness=value['fitness'],
                    recommended_tasks=value['recommended_for'],
                    performance_metrics=value['performance_metrics']
                )
                profiles[key] = profile
                
        return profiles
        
    def _initialize_task_patterns(self) -> Dict[str, List[str]]:
        """Initialize task pattern matching"""
        return {
            'creative': ['design', 'innovative', 'novel', 'brainstorm', 'ideate'],
            'analytical': ['analyze', 'investigate', 'research', 'evaluate', 'assess'],
            'rapid': ['quick', 'fast', 'prototype', 'mvp', 'hackathon'],
            'cross_domain': ['biomimetic', 'inspired', 'analogy', 'transfer', 'pattern'],
            'safety_critical': ['medical', 'financial', 'compliance', 'secure', 'critical']
        }
        
    def select_profile(self, task_description: str, 
                      constraints: Optional[Dict] = None) -> Tuple[str, EvolvedProfile]:
        """Select best profile for given task"""
        task_lower = task_description.lower()
        
        # Score each profile based on task match
        scores = {}
        for profile_id, profile in self.profiles.items():
            score = profile.fitness  # Base score
            
            # Check recommended tasks
            for rec_task in profile.recommended_tasks:
                if any(word in task_lower for word in rec_task.lower().split()):
                    score += 0.1
                    
            # Check task patterns
            for pattern_type, keywords in self.task_patterns.items():
                if any(keyword in task_lower for keyword in keywords):
                    # Boost profiles that excel at this pattern
                    if pattern_type == 'creative' and 'wildcard-brainstorm' in profile.rules:
                        score += 0.15
                    elif pattern_type == 'analytical' and 'philosophers-stone' in profile.rules:
                        score += 0.15
                    elif pattern_type == 'rapid' and 'ultrathink-prompting' in profile.rules:
                        score += 0.15
                        
            # Apply constraints
            if constraints:
                if 'max_tokens' in constraints and profile.performance_metrics.get('token_efficiency', 0) > 0.85:
                    score += 0.1
                if 'safety_required' in constraints and profile.performance_metrics.get('safety_score', 0) > 0.9:
                    score += 0.2
                    
            scores[profile_id] = score
            
        # Select best scoring profile
        best_profile_id = max(scores, key=scores.get)
        return best_profile_id, self.profiles[best_profile_id]

class ConstraintOptimizer:
    """Optimizes constraint levels based on discovered patterns"""
    
    def __init__(self):
        self.optimal_levels = {
            'temporal': 0.6,
            'safety': 0.6,
            'resource': 0.6
        }
        self.enhancement_factors = {
            'temporal': 1.35,
            'safety': 1.28,
            'resource': 1.42
        }
        
    def calculate_optimal_constraints(self, task_type: str, 
                                    current_performance: Dict[str, float]) -> Dict[str, float]:
        """Calculate optimal constraint levels for task"""
        constraints = {}
        
        # Base constraints
        for constraint_type in ['temporal', 'safety', 'resource']:
            constraints[constraint_type] = self.optimal_levels[constraint_type]
            
        # Adjust based on current performance
        if current_performance.get('creativity_score', 0) < 0.5:
            # Reduce constraints to boost creativity
            constraints['safety'] *= 0.8
            constraints['temporal'] *= 0.8
        elif current_performance.get('safety_score', 0) < 0.7:
            # Increase safety constraints
            constraints['safety'] *= 1.2
            
        # Task-specific adjustments
        if 'exploration' in task_type:
            constraints['temporal'] *= 0.7  # More time for exploration
        elif 'production' in task_type:
            constraints['safety'] *= 1.3  # Extra safety for production
            
        return constraints

class SymbiosisIntegration:
    """Main integration class for Mirror project"""
    
    def __init__(self, rules_dir: Path):
        self.rules_dir = rules_dir
        self.profiles_path = rules_dir / "600-experimental" / "symbiosis-engine" / "evolved-profiles.yaml"
        self.selector = RuleProfileSelector(self.profiles_path)
        self.optimizer = ConstraintOptimizer()
        
    def configure_for_task(self, task_description: str,
                          requirements: Optional[Dict] = None) -> Dict:
        """Generate complete configuration for task"""
        # Select profile
        profile_id, profile = self.selector.select_profile(
            task_description, requirements
        )
        
        # Calculate constraints
        constraints = self.optimizer.calculate_optimal_constraints(
            task_description,
            requirements.get('current_performance', {}) if requirements else {}
        )
        
        # Build configuration
        config = {
            'profile': profile_id,
            'profile_name': profile.name,
            'rules': self._resolve_rule_paths(profile.rules),
            'constraints': constraints,
            'expected_performance': profile.performance_metrics,
            'monitoring': {
                'track_metrics': ['token_efficiency', 'creativity_score', 
                                'safety_score', 'execution_speed'],
                'alert_thresholds': {
                    'token_efficiency': 0.7,
                    'safety_score': 0.8
                }
            }
        }
        
        # Add task-specific optimizations
        if 'wildcard-brainstorm' in profile.rules:
            config['llm_params'] = {
                'temperature': 0.9,
                'top_p': 0.9,
                'frequency_penalty': 0.5
            }
            
        return config
        
    def _resolve_rule_paths(self, rule_names: List[str]) -> List[str]:
        """Resolve rule names to full paths"""
        paths = []
        for rule_name in rule_names:
            # Search for rule file
            for rule_file in self.rules_dir.rglob(f"*{rule_name}.mdc"):
                if "deprecated" not in str(rule_file):
                    paths.append(str(rule_file.relative_to(self.rules_dir)))
                    break
        return paths
        
    def apply_configuration(self, config: Dict) -> str:
        """Generate config file content"""
        yaml_content = f"""# Auto-generated configuration using Rule Symbiosis Evolution
# Profile: {config['profile_name']}
# Generated: {config.get('timestamp', 'now')}

profile: {config['profile']}

rules:
{chr(10).join(f'  - {rule}' for rule in config['rules'])}

constraints:
  temporal_pressure: {config['constraints']['temporal']:.2f}
  safety_threshold: {config['constraints']['safety']:.2f}
  resource_limit: {config['constraints']['resource']:.2f}

llm_params:
  temperature: {config.get('llm_params', {}).get('temperature', 0.7)}
  top_p: {config.get('llm_params', {}).get('top_p', 0.95)}

monitoring:
  enabled: true
  metrics: {config['monitoring']['track_metrics']}
  alert_on:
    token_efficiency_below: {config['monitoring']['alert_thresholds']['token_efficiency']}
    safety_score_below: {config['monitoring']['alert_thresholds']['safety_score']}

expected_performance:
  token_efficiency: {config['expected_performance']['token_efficiency']:.2f}
  creativity_score: {config['expected_performance'].get('creativity_score', 0.7):.2f}
  safety_score: {config['expected_performance']['safety_score']:.2f}
  execution_speed: {config['expected_performance'].get('execution_speed', 0.8):.2f}
"""
        return yaml_content

def demonstrate_integration():
    """Demonstrate integration usage"""
    rules_dir = Path("/Users/hamzaamjad/mirror/.cursor/rules")
    integration = SymbiosisIntegration(rules_dir)
    
    # Example tasks
    tasks = [
        {
            'description': "Design an innovative caching system for our distributed application",
            'requirements': {'safety_required': True, 'max_tokens': 10000}
        },
        {
            'description': "Quickly prototype a new user dashboard feature",
            'requirements': {'time_limit': '30m', 'current_performance': {'creativity_score': 0.4}}
        },
        {
            'description': "Analyze our database performance and suggest optimizations",
            'requirements': {'max_tokens': 5000}
        },
        {
            'description': "Create a biomimetic design for network routing inspired by ant colonies",
            'requirements': {'safety_required': True}
        }
    ]
    
    print("🧬 Rule Symbiosis Integration Demonstration\n")
    
    for i, task in enumerate(tasks, 1):
        print(f"Task {i}: {task['description']}")
        
        # Generate configuration
        config = integration.configure_for_task(
            task['description'],
            task.get('requirements')
        )
        
        print(f"  Selected Profile: {config['profile_name']}")
        print(f"  Rules: {len(config['rules'])} rules")
        print(f"  Constraints: T={config['constraints']['temporal']:.1f}, "
              f"S={config['constraints']['safety']:.1f}, "
              f"R={config['constraints']['resource']:.1f}")
        print(f"  Expected Performance:")
        for metric, value in config['expected_performance'].items():
            print(f"    - {metric}: {value:.2%}")
        print()
        
    # Generate example config file
    print("\n📄 Example Generated Configuration:")
    print("-" * 50)
    config = integration.configure_for_task(tasks[0]['description'], tasks[0]['requirements'])
    print(integration.apply_configuration(config))

class RuleSymbiosisMonitor:
    """Monitor and adapt rule performance in real-time"""
    
    def __init__(self):
        self.performance_history = []
        self.adaptation_threshold = 0.15  # 15% deviation triggers adaptation
        
    def track_execution(self, profile_id: str, metrics: Dict[str, float]):
        """Track execution metrics"""
        self.performance_history.append({
            'profile_id': profile_id,
            'metrics': metrics,
            'timestamp': 'now'  # Would use real timestamp
        })
        
    def recommend_adaptation(self, current_metrics: Dict[str, float],
                           expected_metrics: Dict[str, float]) -> Optional[Dict]:
        """Recommend adaptations if performance deviates"""
        adaptations = {}
        
        for metric, expected in expected_metrics.items():
            current = current_metrics.get(metric, 0)
            deviation = abs(current - expected) / expected
            
            if deviation > self.adaptation_threshold:
                if metric == 'creativity_score' and current < expected:
                    adaptations['increase_temperature'] = 0.1
                    adaptations['reduce_safety_constraint'] = 0.1
                elif metric == 'safety_score' and current < expected:
                    adaptations['increase_safety_constraint'] = 0.15
                    adaptations['enable_risk_checkpoint'] = True
                elif metric == 'token_efficiency' and current < expected:
                    adaptations['increase_context_trim'] = 0.2
                    adaptations['enable_concise_comms'] = True
                    
        return adaptations if adaptations else None

if __name__ == "__main__":
    demonstrate_integration()
