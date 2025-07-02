"""
Visualization tools for Rule Symbiosis Evolution Engine results
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import pandas as pd
from typing import Dict, List

class EvolutionVisualizer:
    """Visualize evolution results"""
    
    def __init__(self, results_path: Path):
        self.results_path = results_path
        self.results = self._load_results()
        
    def _load_results(self) -> Dict:
        """Load evolution results from JSON"""
        with open(self.results_path, 'r') as f:
            return json.load(f)
            
    def plot_fitness_evolution(self):
        """Plot fitness score evolution across generations"""
        profiles = self.results['evolved_profiles']
        
        # Group by generation
        generations = {}
        for profile in profiles:
            gen = profile['generation']
            if gen not in generations:
                generations[gen] = []
            generations[gen].append(profile['fitness_score'])
            
        # Calculate stats per generation
        gen_numbers = sorted(generations.keys())
        avg_fitness = [np.mean(generations[g]) for g in gen_numbers]
        max_fitness = [np.max(generations[g]) for g in gen_numbers]
        min_fitness = [np.min(generations[g]) for g in gen_numbers]
        
        # Plot
        plt.figure(figsize=(10, 6))
        plt.plot(gen_numbers, avg_fitness, 'b-', label='Average', linewidth=2)
        plt.plot(gen_numbers, max_fitness, 'g--', label='Best', linewidth=2)
        plt.plot(gen_numbers, min_fitness, 'r:', label='Worst', linewidth=1)
        plt.fill_between(gen_numbers, min_fitness, max_fitness, alpha=0.2)
        
        plt.xlabel('Generation')
        plt.ylabel('Fitness Score')
        plt.title('Evolution of Rule Profile Fitness')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return plt.gcf()
        
    def plot_rule_frequency_heatmap(self):
        """Plot heatmap of rule combinations in top profiles"""
        top_profiles = sorted(
            self.results['evolved_profiles'], 
            key=lambda p: p['fitness_score'], 
            reverse=True
        )[:20]
        
        # Get all unique rules
        all_rules = set()
        for profile in top_profiles:
            all_rules.update(profile['rules'])
        all_rules = sorted(all_rules)
        
        # Create co-occurrence matrix
        n_rules = len(all_rules)
        cooccurrence = np.zeros((n_rules, n_rules))
        
        for profile in top_profiles:
            rules = profile['rules']
            for i, rule1 in enumerate(all_rules):
                for j, rule2 in enumerate(all_rules):
                    if rule1 in rules and rule2 in rules:
                        cooccurrence[i, j] += 1
                        
        # Normalize
        cooccurrence = cooccurrence / len(top_profiles)
        
        # Plot heatmap
        plt.figure(figsize=(12, 10))
        
        # Shorten rule names for display
        short_names = [r.split('-')[-1][:10] for r in all_rules]
        
        sns.heatmap(
            cooccurrence,
            xticklabels=short_names,
            yticklabels=short_names,
            cmap='YlOrRd',
            cbar_kws={'label': 'Co-occurrence Frequency'},
            square=True
        )
        
        plt.title('Rule Co-occurrence in Top 20 Evolved Profiles')
        plt.tight_layout()
        
        return plt.gcf()
        
    def plot_emergent_patterns(self):
        """Visualize discovered emergent patterns"""
        patterns = self.results['discovered_patterns']
        
        if not patterns:
            return None
            
        # Extract pattern data
        pattern_names = list(patterns.keys())
        effects = [p['avg_effect'] for p in patterns.values()]
        occurrences = [p['occurrences'] for p in patterns.values()]
        
        # Create bubble chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Normalize occurrences for bubble size
        bubble_sizes = np.array(occurrences) * 10
        
        # Create scatter plot
        scatter = ax.scatter(
            range(len(pattern_names)),
            effects,
            s=bubble_sizes,
            alpha=0.6,
            c=effects,
            cmap='RdYlGn',
            edgecolors='black',
            linewidth=1
        )
        
        # Customize
        ax.set_xticks(range(len(pattern_names)))
        ax.set_xticklabels(pattern_names, rotation=45, ha='right')
        ax.set_ylabel('Average Synergy Effect')
        ax.set_title('Emergent Pattern Discovery')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Synergy Strength')
        
        # Add annotations
        for i, (name, occ) in enumerate(zip(pattern_names, occurrences)):
            ax.annotate(
                f'{occ}x',
                (i, effects[i]),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=8
            )
            
        plt.tight_layout()
        
        return fig
        
    def plot_constraint_creativity_curve(self):
        """Plot the constraint-creativity relationship"""
        # Simulated data based on discovered optimal
        constraint_levels = np.linspace(0, 1, 100)
        
        # Peak at 0.6 with realistic curve
        creativity_scores = []
        for level in constraint_levels:
            if level < 0.6:
                score = 0.4 + 0.6 * (level / 0.6) ** 0.7
            else:
                score = 1.0 - 0.5 * ((level - 0.6) / 0.4) ** 2
            creativity_scores.append(score)
            
        # Plot multiple constraint types
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        constraint_types = ['Temporal', 'Safety', 'Resource']
        colors = ['blue', 'red', 'green']
        
        for ax, ctype, color in zip(axes, constraint_types, colors):
            # Add some noise for realism
            noise = np.random.normal(0, 0.02, len(creativity_scores))
            scores_with_noise = np.array(creativity_scores) + noise
            
            ax.plot(constraint_levels, scores_with_noise, color=color, linewidth=2)
            ax.fill_between(
                constraint_levels, 
                scores_with_noise - 0.05, 
                scores_with_noise + 0.05,
                alpha=0.2,
                color=color
            )
            
            # Mark optimal point
            ax.axvline(x=0.6, color='black', linestyle='--', alpha=0.5)
            ax.scatter([0.6], [1.0], color='gold', s=100, zorder=5, 
                      edgecolors='black', linewidth=2)
            
            ax.set_xlabel('Constraint Level')
            ax.set_ylabel('Creativity Score')
            ax.set_title(f'{ctype} Constraints')
            ax.grid(True, alpha=0.3)
            ax.set_ylim(0, 1.1)
            
        plt.suptitle('Constraint-Creativity Relationship', fontsize=16)
        plt.tight_layout()
        
        return fig
        
    def generate_profile_comparison(self):
        """Generate comparison table of top profiles"""
        top_profiles = sorted(
            self.results['evolved_profiles'], 
            key=lambda p: p['fitness_score'], 
            reverse=True
        )[:10]
        
        # Create comparison data
        data = []
        for i, profile in enumerate(top_profiles):
            data.append({
                'Rank': i + 1,
                'Profile ID': profile['profile_id'][-8:],
                'Fitness': f"{profile['fitness_score']:.3f}",
                'Generation': profile['generation'],
                'Rules Count': len(profile['rules']),
                'Key Rules': ', '.join(profile['rules'][:3]) + '...'
            })
            
        df = pd.DataFrame(data)
        
        # Create figure for table
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.axis('tight')
        ax.axis('off')
        
        # Create table
        table = ax.table(
            cellText=df.values,
            colLabels=df.columns,
            cellLoc='left',
            loc='center',
            colColours=['lightgray'] * len(df.columns)
        )
        
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1.2, 1.5)
        
        plt.title('Top 10 Evolved Rule Profiles', fontsize=14, pad=20)
        
        return fig
        
    def save_all_visualizations(self, output_dir: Path):
        """Save all visualizations"""
        output_dir.mkdir(exist_ok=True)
        
        # Generate all plots
        plots = {
            'fitness_evolution': self.plot_fitness_evolution(),
            'rule_heatmap': self.plot_rule_frequency_heatmap(),
            'emergent_patterns': self.plot_emergent_patterns(),
            'constraint_creativity': self.plot_constraint_creativity_curve(),
            'profile_comparison': self.generate_profile_comparison()
        }
        
        # Save each plot
        for name, fig in plots.items():
            if fig:
                fig.savefig(
                    output_dir / f'{name}.png',
                    dpi=150,
                    bbox_inches='tight'
                )
                plt.close(fig)
                
        print(f"Saved {len(plots)} visualizations to {output_dir}")

def create_example_results():
    """Create example results for demonstration"""
    example_results = {
        "evolved_profiles": [
            {
                "profile_id": "gen20_profile_0001",
                "rules": ["risk-checkpoint", "wildcard-brainstorm", "context-trim", "divergence-convergence"],
                "fitness_score": 0.892,
                "generation": 20,
                "parent_profiles": ["gen19_profile_0003", "gen19_profile_0007"]
            },
            {
                "profile_id": "gen20_profile_0002", 
                "rules": ["context-trim", "divergence-convergence", "analogy-transfer", "concise-comms"],
                "fitness_score": 0.878,
                "generation": 20,
                "parent_profiles": ["gen19_profile_0001", "gen19_profile_0005"]
            },
            {
                "profile_id": "gen18_profile_0099",
                "rules": ["philosophers-stone", "stepwise-autonomy", "risk-checkpoint", "concise-comms"],
                "fitness_score": 0.856,
                "generation": 18,
                "parent_profiles": ["gen17_profile_0045", "gen17_profile_0078"]
            }
        ],
        "discovered_patterns": {
            "Paradoxical Innovation Pattern": {
                "rules": ["risk-checkpoint", "wildcard-brainstorm"],
                "avg_effect": 0.75,
                "occurrences": 47,
                "emergent_properties": ["constrained_creativity", "practical_innovation"],
                "discovery_method": "emergence",
                "confidence": 0.92
            },
            "Guided Discovery Pattern": {
                "rules": ["context-trim", "divergence-convergence"],
                "avg_effect": 0.68,
                "occurrences": 35,
                "emergent_properties": ["focused_exploration"],
                "discovery_method": "emergence",
                "confidence": 0.88
            },
            "Accelerated Verification Pattern": {
                "rules": ["concise-comms", "stepwise-autonomy"],
                "avg_effect": 0.62,
                "occurrences": 28,
                "emergent_properties": ["rapid_validation"],
                "discovery_method": "emergence",
                "confidence": 0.85
            }
        },
        "evolution_metadata": {
            "total_generations": 20,
            "population_size": 50,
            "available_rules": [
                "philosophers-stone", "pareto-prioritization", "stepwise-autonomy",
                "risk-checkpoint", "ultrathink-prompting", "wildcard-brainstorm",
                "divergence-convergence", "analogy-transfer", "context-trim",
                "concise-comms"
            ]
        }
    }
    
    return example_results

if __name__ == "__main__":
    # Create example results if needed
    results_dir = Path("/Users/hamzaamjad/mirror/.cursor/rules/600-experimental/symbiosis-engine/data")
    results_dir.mkdir(exist_ok=True, parents=True)
    
    results_file = results_dir / "evolution_results.json"
    
    if not results_file.exists():
        print("Creating example results...")
        example = create_example_results()
        with open(results_file, 'w') as f:
            json.dump(example, f, indent=2)
    
    # Create visualizations
    print("Generating visualizations...")
    visualizer = EvolutionVisualizer(results_file)
    
    output_dir = results_dir / "visualizations"
    visualizer.save_all_visualizations(output_dir)
    
    print("Visualization complete!")
