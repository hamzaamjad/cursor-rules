#!/usr/bin/env python3
"""
Rule Symbiosis Evolution Engine
Discovers optimal rule combinations through production monitoring and reinforcement learning
"""

import os
import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import hashlib
from collections import defaultdict, Counter
import networkx as nx
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import sqlite3
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Genetic Algorithm parameters
POPULATION_SIZE = 50
MUTATION_RATE = 0.15
CROSSOVER_RATE = 0.8
ELITE_SIZE = 5
TOURNAMENT_SIZE = 3
MAX_GENERATIONS = 100

# Reinforcement Learning parameters
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.95
EPSILON = 0.1  # Exploration rate
EPSILON_DECAY = 0.995

@dataclass
class RuleActivation:
    """Record of a rule being activated"""
    rule_id: str
    timestamp: datetime
    context_type: str  # 'divergence', 'convergence', 'analysis', etc.
    task_id: str
    token_count_before: int
    token_count_after: int
    execution_time_ms: int
    success: bool
    error_type: Optional[str] = None
    
@dataclass
class TaskOutcome:
    """Metrics for completed task"""
    task_id: str
    rule_sequence: List[str]
    total_tokens: int
    total_time_ms: int
    quality_score: float  # 0-1, from user feedback
    creativity_score: float  # 0-1, measured by uniqueness
    safety_incidents: int
    user_revisions: int
    completion_status: str  # 'success', 'partial', 'failed'

@dataclass
class EvolvedProfile:
    """A discovered rule combination pattern"""
    profile_id: str
    rule_combination: List[str]
    context_patterns: Dict[str, float]  # context_type -> probability
    fitness_score: float
    discovery_generation: int
    usage_count: int = 0
    success_rate: float = 0.0
    avg_performance_gain: float = 0.0
    
    def to_yaml(self) -> str:
        """Convert to YAML format for config file"""
        return f"""
  {self.profile_id}:
    name: "Evolved Profile {self.profile_id[:8]}"
    description: "Auto-discovered pattern with {self.fitness_score:.2f} fitness"
    discovery_generation: {self.discovery_generation}
    rules: {json.dumps(self.rule_combination)}
    context_affinity: {json.dumps(self.context_patterns)}
    metrics:
      usage_count: {self.usage_count}
      success_rate: {self.success_rate:.2%}
      performance_gain: {self.avg_performance_gain:.2%}
"""

class RuleSymbiosisEvolution:
    """Main evolution engine for discovering optimal rule combinations"""
    
    def __init__(self, db_path: str = "/Users/hamzaamjad/mirror/.cursor/evolution.db"):
        self.db_path = db_path
        self.rules_dir = Path("/Users/hamzaamjad/mirror/.cursor/rules")
        self.available_rules = self._load_available_rules()
        self.rule_graph = nx.DiGraph()
        self.population: List[EvolvedProfile] = []
        self.generation = 0
        self.best_profiles: List[EvolvedProfile] = []
        
        # Q-learning table for rule transitions
        self.q_table: Dict[Tuple[str, str], float] = defaultdict(float)
        
        # Pattern detection
        self.pattern_detector = PatternDetector()
        
        # Initialize database
        self._init_database()
        
    def _load_available_rules(self) -> List[str]:
        """Load all available rules from filesystem"""
        rules = []
        for rule_file in self.rules_dir.rglob("*.mdc"):
            if "deprecated" not in str(rule_file) and "evolution" not in str(rule_file):
                relative_path = rule_file.relative_to(self.rules_dir)
                rule_id = str(relative_path).replace('.mdc', '')
                rules.append(rule_id)
        return sorted(rules)
    
    def _init_database(self):
        """Initialize telemetry database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Rule activation telemetry
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rule_activations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_id TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                context_type TEXT,
                task_id TEXT NOT NULL,
                token_count_before INTEGER,
                token_count_after INTEGER,
                execution_time_ms INTEGER,
                success BOOLEAN,
                error_type TEXT
            )
        """)
        
        # Task outcomes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_outcomes (
                task_id TEXT PRIMARY KEY,
                rule_sequence TEXT NOT NULL,
                total_tokens INTEGER,
                total_time_ms INTEGER,
                quality_score REAL,
                creativity_score REAL,
                safety_incidents INTEGER,
                user_revisions INTEGER,
                completion_status TEXT
            )
        """)
        
        # Evolved profiles
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evolved_profiles (
                profile_id TEXT PRIMARY KEY,
                rule_combination TEXT NOT NULL,
                context_patterns TEXT,
                fitness_score REAL,
                discovery_generation INTEGER,
                usage_count INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                avg_performance_gain REAL DEFAULT 0.0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def record_activation(self, activation: RuleActivation):
        """Record a rule activation event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO rule_activations 
            (rule_id, timestamp, context_type, task_id, token_count_before,
             token_count_after, execution_time_ms, success, error_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            activation.rule_id,
            activation.timestamp,
            activation.context_type,
            activation.task_id,
            activation.token_count_before,
            activation.token_count_after,
            activation.execution_time_ms,
            activation.success,
            activation.error_type
        ))
        
        conn.commit()
        conn.close()
        
        # Update Q-table in real-time
        self._update_q_learning(activation)
    
    def _update_q_learning(self, activation: RuleActivation):
        """Update Q-learning values based on activation success"""
        # Simple reward: +1 for success, -1 for failure
        reward = 1.0 if activation.success else -1.0
        
        # Token efficiency bonus
        if activation.token_count_after < activation.token_count_before * 0.5:
            reward += 0.5
        
        # Speed bonus
        if activation.execution_time_ms < 100:
            reward += 0.3
        
        # Get previous rule from task context
        prev_rule = self._get_previous_rule(activation.task_id, activation.timestamp)
        if prev_rule:
            state_action = (prev_rule, activation.rule_id)
            old_q = self.q_table[state_action]
            
            # Q-learning update
            self.q_table[state_action] = old_q + LEARNING_RATE * (reward - old_q)
    
    def _get_previous_rule(self, task_id: str, current_timestamp: datetime) -> Optional[str]:
        """Get the previously activated rule in the same task"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT rule_id FROM rule_activations
            WHERE task_id = ? AND timestamp < ?
            ORDER BY timestamp DESC LIMIT 1
        """, (task_id, current_timestamp))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def initialize_population(self):
        """Create initial population of rule combinations"""
        self.population = []
        
        # Add known good combinations
        known_good = [
            # Creative stack
            ["105-context-trim", "103-divergence-convergence", "102-wildcard-brainstorm", 
             "104-analogy-transfer", "004-risk-checkpoint", "106-concise-comms"],
            # Analytical stack
            ["105-context-trim", "001-philosophers-stone", "002-pareto-prioritization",
             "003-stepwise-autonomy", "106-concise-comms"],
            # Rapid prototype stack
            ["101-ultrathink-prompting", "102-wildcard-brainstorm", "004-risk-checkpoint"],
        ]
        
        for combo in known_good:
            profile = EvolvedProfile(
                profile_id=self._generate_profile_id(combo),
                rule_combination=combo,
                context_patterns={"general": 1.0},
                fitness_score=0.7,  # Good starting fitness
                discovery_generation=0
            )
            self.population.append(profile)
        
        # Generate random combinations
        while len(self.population) < POPULATION_SIZE:
            # Random subset of rules (3-8 rules)
            size = np.random.randint(3, 9)
            combo = list(np.random.choice(self.available_rules, size, replace=False))
            
            # Ensure basic safety
            if "004-risk-checkpoint" not in combo:
                combo.append("004-risk-checkpoint")
            
            profile = EvolvedProfile(
                profile_id=self._generate_profile_id(combo),
                rule_combination=combo,
                context_patterns=self._random_context_pattern(),
                fitness_score=0.5,  # Neutral starting fitness
                discovery_generation=0
            )
            self.population.append(profile)
    
    def _generate_profile_id(self, rules: List[str]) -> str:
        """Generate unique ID for rule combination"""
        combo_str = "-".join(sorted(rules))
        return hashlib.md5(combo_str.encode()).hexdigest()
    
    def _random_context_pattern(self) -> Dict[str, float]:
        """Generate random context affinity pattern"""
        contexts = ["creative", "analytical", "production", "exploration", "optimization"]
        weights = np.random.dirichlet(np.ones(len(contexts)))
        return dict(zip(contexts, weights))
    
    def evaluate_fitness(self, profile: EvolvedProfile) -> float:
        """Evaluate fitness of a rule combination based on historical data"""
        conn = sqlite3.connect(self.db_path)
        
        # Query historical performance
        rule_sequence_str = json.dumps(profile.rule_combination)
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                AVG(quality_score) as avg_quality,
                AVG(creativity_score) as avg_creativity,
                AVG(CAST(total_tokens AS REAL) / 1000) as avg_tokens_k,
                AVG(CAST(total_time_ms AS REAL) / 1000) as avg_time_s,
                AVG(safety_incidents) as avg_incidents,
                AVG(user_revisions) as avg_revisions,
                COUNT(*) as usage_count,
                SUM(CASE WHEN completion_status = 'success' THEN 1 ELSE 0 END) as successes
            FROM task_outcomes
            WHERE rule_sequence LIKE ?
        """, (f"%{rule_sequence_str}%",))
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[6] > 0:  # Has usage data
            # Multi-objective fitness function
            quality = result[0] or 0.5
            creativity = result[1] or 0.5
            efficiency = 1.0 / (1.0 + result[2])  # Inverse tokens
            speed = 1.0 / (1.0 + result[3])  # Inverse time
            safety = 1.0 / (1.0 + result[4])  # Inverse incidents
            accuracy = 1.0 / (1.0 + result[5])  # Inverse revisions
            success_rate = result[7] / result[6]
            
            # Weighted combination
            fitness = (
                0.25 * quality +
                0.15 * creativity +
                0.20 * efficiency +
                0.15 * speed +
                0.15 * safety +
                0.05 * accuracy +
                0.05 * success_rate
            )
            
            # Bonus for discovering non-obvious synergies
            fitness += self._calculate_synergy_bonus(profile)
            
        else:
            # No historical data - use heuristics
            fitness = self._heuristic_fitness(profile)
        
        return min(1.0, fitness)
    
    def _calculate_synergy_bonus(self, profile: EvolvedProfile) -> float:
        """Calculate bonus for non-obvious beneficial combinations"""
        bonus = 0.0
        rules = profile.rule_combination
        
        # Check for unexpected synergies
        synergies = [
            # Constrained creativity
            (["004-risk-checkpoint", "102-wildcard-brainstorm"], 0.1),
            # Structured exploration
            (["003-stepwise-autonomy", "101-ultrathink-prompting"], 0.08),
            # Efficient divergence
            (["105-context-trim", "103-divergence-convergence"], 0.05),
            # Cross-domain validation
            (["104-analogy-transfer", "004-risk-checkpoint"], 0.07),
        ]
        
        for synergy_rules, synergy_bonus in synergies:
            if all(r in rules for r in synergy_rules):
                bonus += synergy_bonus
        
        # Check Q-learning discovered transitions
        for i in range(len(rules) - 1):
            transition = (rules[i], rules[i + 1])
            if self.q_table.get(transition, 0) > 0.8:
                bonus += 0.02
        
        return bonus
    
    def _heuristic_fitness(self, profile: EvolvedProfile) -> float:
        """Estimate fitness using heuristics when no data available"""
        rules = profile.rule_combination
        fitness = 0.5  # Base fitness
        
        # Essential rules bonus
        if "105-context-trim" in rules:
            fitness += 0.1
        if "004-risk-checkpoint" in rules:
            fitness += 0.1
        
        # Penalize conflicts
        if "102-wildcard-brainstorm" in rules and "106-concise-comms" in rules:
            # Check if divergence-convergence mediates
            if "103-divergence-convergence" not in rules:
                fitness -= 0.2
        
        # Reward balanced combinations
        cognitive_count = sum(1 for r in rules if r.startswith("100-cognitive/"))
        core_count = sum(1 for r in rules if r.startswith("000-core/"))
        
        if 2 <= cognitive_count <= 4 and 1 <= core_count <= 3:
            fitness += 0.1
        
        # Length penalty for overly complex combinations
        if len(rules) > 8:
            fitness -= 0.05 * (len(rules) - 8)
        
        return max(0.1, min(1.0, fitness))
    
    def crossover(self, parent1: EvolvedProfile, parent2: EvolvedProfile) -> EvolvedProfile:
        """Create offspring through crossover"""
        if np.random.random() > CROSSOVER_RATE:
            return parent1  # No crossover
        
        # Combine rule sets
        all_rules = list(set(parent1.rule_combination + parent2.rule_combination))
        
        # Select subset maintaining reasonable size
        target_size = int((len(parent1.rule_combination) + len(parent2.rule_combination)) / 2)
        target_size = max(3, min(8, target_size))
        
        # Prioritize rules that appear in both parents
        common_rules = list(set(parent1.rule_combination) & set(parent2.rule_combination))
        unique_rules = list(set(all_rules) - set(common_rules))
        
        offspring_rules = common_rules.copy()
        
        # Add unique rules until target size
        while len(offspring_rules) < target_size and unique_rules:
            rule = np.random.choice(unique_rules)
            offspring_rules.append(rule)
            unique_rules.remove(rule)
        
        # Ensure safety
        if "004-risk-checkpoint" not in offspring_rules:
            offspring_rules.append("004-risk-checkpoint")
        
        # Blend context patterns
        context_patterns = {}
        all_contexts = set(parent1.context_patterns.keys()) | set(parent2.context_patterns.keys())
        for context in all_contexts:
            p1_weight = parent1.context_patterns.get(context, 0)
            p2_weight = parent2.context_patterns.get(context, 0)
            context_patterns[context] = (p1_weight + p2_weight) / 2
        
        # Normalize
        total = sum(context_patterns.values())
        if total > 0:
            context_patterns = {k: v/total for k, v in context_patterns.items()}
        
        return EvolvedProfile(
            profile_id=self._generate_profile_id(offspring_rules),
            rule_combination=offspring_rules,
            context_patterns=context_patterns,
            fitness_score=0.0,  # Will be evaluated
            discovery_generation=self.generation
        )
    
    def mutate(self, profile: EvolvedProfile) -> EvolvedProfile:
        """Apply mutation to a profile"""
        if np.random.random() > MUTATION_RATE:
            return profile  # No mutation
        
        mutated_rules = profile.rule_combination.copy()
        mutation_type = np.random.choice(['add', 'remove', 'replace', 'reorder'])
        
        if mutation_type == 'add' and len(mutated_rules) < 8:
            # Add a random rule not already present
            available = [r for r in self.available_rules if r not in mutated_rules]
            if available:
                new_rule = np.random.choice(available)
                insert_pos = np.random.randint(0, len(mutated_rules) + 1)
                mutated_rules.insert(insert_pos, new_rule)
        
        elif mutation_type == 'remove' and len(mutated_rules) > 3:
            # Remove a random non-essential rule
            removable = [r for r in mutated_rules if r != "004-risk-checkpoint"]
            if removable:
                remove_rule = np.random.choice(removable)
                mutated_rules.remove(remove_rule)
        
        elif mutation_type == 'replace':
            # Replace a random rule
            if mutated_rules:
                idx = np.random.randint(0, len(mutated_rules))
                available = [r for r in self.available_rules if r not in mutated_rules]
                if available:
                    mutated_rules[idx] = np.random.choice(available)
        
        elif mutation_type == 'reorder':
            # Shuffle order (maintaining context-trim first if present)
            if "105-context-trim" in mutated_rules:
                mutated_rules.remove("105-context-trim")
                np.random.shuffle(mutated_rules)
                mutated_rules.insert(0, "105-context-trim")
            else:
                np.random.shuffle(mutated_rules)
        
        # Mutate context patterns slightly
        mutated_patterns = {}
        for context, weight in profile.context_patterns.items():
            noise = np.random.normal(0, 0.1)
            mutated_patterns[context] = max(0, weight + noise)
        
        # Normalize
        total = sum(mutated_patterns.values())
        if total > 0:
            mutated_patterns = {k: v/total for k, v in mutated_patterns.items()}
        
        return EvolvedProfile(
            profile_id=self._generate_profile_id(mutated_rules),
            rule_combination=mutated_rules,
            context_patterns=mutated_patterns,
            fitness_score=0.0,  # Will be evaluated
            discovery_generation=self.generation
        )
    
    def selection(self) -> List[EvolvedProfile]:
        """Select next generation using tournament selection"""
        new_population = []
        
        # Elite preservation
        sorted_pop = sorted(self.population, key=lambda p: p.fitness_score, reverse=True)
        new_population.extend(sorted_pop[:ELITE_SIZE])
        
        # Tournament selection for rest
        while len(new_population) < POPULATION_SIZE:
            tournament = np.random.choice(self.population, TOURNAMENT_SIZE, replace=False)
            winner = max(tournament, key=lambda p: p.fitness_score)
            new_population.append(winner)
        
        return new_population
    
    def evolve_generation(self):
        """Run one generation of evolution"""
        # Evaluate fitness for all profiles
        for profile in self.population:
            profile.fitness_score = self.evaluate_fitness(profile)
        
        # Selection
        selected = self.selection()
        
        # Create next generation
        next_generation = selected[:ELITE_SIZE]  # Keep elite
        
        while len(next_generation) < POPULATION_SIZE:
            # Select parents
            parent1 = np.random.choice(selected)
            parent2 = np.random.choice(selected)
            
            # Crossover
            offspring = self.crossover(parent1, parent2)
            
            # Mutation
            offspring = self.mutate(offspring)
            
            next_generation.append(offspring)
        
        self.population = next_generation
        self.generation += 1
        
        # Track best profiles
        best_profile = max(self.population, key=lambda p: p.fitness_score)
        self.best_profiles.append(best_profile)
        
        # Save promising profiles to database
        if best_profile.fitness_score > 0.8:
            self._save_evolved_profile(best_profile)
    
    def _save_evolved_profile(self, profile: EvolvedProfile):
        """Save successful evolved profile to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO evolved_profiles
            (profile_id, rule_combination, context_patterns, fitness_score,
             discovery_generation, usage_count, success_rate, avg_performance_gain)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            profile.profile_id,
            json.dumps(profile.rule_combination),
            json.dumps(profile.context_patterns),
            profile.fitness_score,
            profile.discovery_generation,
            profile.usage_count,
            profile.success_rate,
            profile.avg_performance_gain
        ))
        
        conn.commit()
        conn.close()
    
    async def run_evolution(self, generations: int = MAX_GENERATIONS):
        """Run the evolution process"""
        print(f"Starting Rule Symbiosis Evolution for {generations} generations...")
        
        self.initialize_population()
        
        for gen in range(generations):
            self.evolve_generation()
            
            if gen % 10 == 0:
                best = max(self.population, key=lambda p: p.fitness_score)
                print(f"Generation {gen}: Best fitness = {best.fitness_score:.3f}")
                print(f"  Rules: {' → '.join(best.rule_combination[:5])}...")
            
            # Early stopping if converged
            if len(self.best_profiles) > 10:
                recent_fitness = [p.fitness_score for p in self.best_profiles[-10:]]
                if max(recent_fitness) - min(recent_fitness) < 0.01:
                    print(f"Converged at generation {gen}")
                    break
        
        # Export best profiles
        await self.export_evolved_profiles()
    
    async def export_evolved_profiles(self):
        """Export evolved profiles to config file"""
        output_path = self.rules_dir / "700-evolution" / "evolved-profiles.yaml"
        
        # Get top profiles from database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM evolved_profiles
            WHERE fitness_score > 0.75
            ORDER BY fitness_score DESC
            LIMIT 20
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        # Generate YAML config
        config = """# Evolved Rule Profiles
# Auto-generated by Rule Symbiosis Evolution Engine
# Last updated: {timestamp}

evolved_profiles:
""".format(timestamp=datetime.now().isoformat())
        
        for row in results:
            profile = EvolvedProfile(
                profile_id=row[0],
                rule_combination=json.loads(row[1]),
                context_patterns=json.loads(row[2]),
                fitness_score=row[3],
                discovery_generation=row[4],
                usage_count=row[5],
                success_rate=row[6],
                avg_performance_gain=row[7]
            )
            config += profile.to_yaml()
        
        # Add integration instructions
        config += """
# Integration Instructions:
# 1. Add to rule-config.yaml under 'profiles' section
# 2. Reference by profile_id in .cursor/config.yaml
# 3. Monitor performance with telemetry dashboard
# 4. Profiles will continue to evolve with usage
"""
        
        with open(output_path, 'w') as f:
            f.write(config)
        
        print(f"Exported {len(results)} evolved profiles to {output_path}")


class PatternDetector:
    """Detect emergent patterns in rule usage"""
    
    def __init__(self):
        self.sequence_patterns = defaultdict(int)
        self.context_patterns = defaultdict(lambda: defaultdict(int))
        
    def analyze_sequences(self, db_path: str) -> List[Tuple[List[str], int]]:
        """Find frequently occurring rule sequences"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all task rule sequences
        cursor.execute("""
            SELECT task_id, rule_id, timestamp
            FROM rule_activations
            WHERE success = 1
            ORDER BY task_id, timestamp
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        # Group by task
        task_sequences = defaultdict(list)
        for task_id, rule_id, timestamp in results:
            task_sequences[task_id].append(rule_id)
        
        # Find common subsequences
        sequence_counts = defaultdict(int)
        
        for sequence in task_sequences.values():
            # Extract all subsequences of length 2-5
            for length in range(2, min(6, len(sequence) + 1)):
                for i in range(len(sequence) - length + 1):
                    subseq = tuple(sequence[i:i + length])
                    sequence_counts[subseq] += 1
        
        # Return most common patterns
        common_patterns = sorted(
            sequence_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:20]
        
        return [(list(pattern), count) for pattern, count in common_patterns]
    
    def find_context_correlations(self, db_path: str) -> Dict[str, Dict[str, float]]:
        """Find correlations between contexts and rule effectiveness"""
        conn = sqlite3.connect(db_path)
        
        # Analyze success rates by context and rule
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                context_type,
                rule_id,
                COUNT(*) as total,
                SUM(CASE WHEN success THEN 1 ELSE 0 END) as successes,
                AVG(execution_time_ms) as avg_time
            FROM rule_activations
            GROUP BY context_type, rule_id
            HAVING total > 10
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        # Calculate context-rule affinity scores
        context_affinities = defaultdict(dict)
        
        for context, rule, total, successes, avg_time in results:
            success_rate = successes / total
            speed_score = 1.0 / (1.0 + avg_time / 1000)  # Normalize to 0-1
            
            # Combined affinity score
            affinity = 0.7 * success_rate + 0.3 * speed_score
            context_affinities[context][rule] = affinity
        
        return dict(context_affinities)


class TelemetryCollector:
    """Collect rule activation telemetry from Mirror system"""
    
    def __init__(self, evolution_engine: RuleSymbiosisEvolution):
        self.engine = evolution_engine
        self.active_tasks = {}
        
    async def on_rule_activated(self, rule_id: str, context: Dict[str, Any]):
        """Hook called when a rule is activated"""
        task_id = context.get('task_id', 'unknown')
        
        activation = RuleActivation(
            rule_id=rule_id,
            timestamp=datetime.now(),
            context_type=context.get('phase', 'general'),
            task_id=task_id,
            token_count_before=context.get('tokens_before', 0),
            token_count_after=context.get('tokens_after', 0),
            execution_time_ms=context.get('execution_time', 0),
            success=context.get('success', True),
            error_type=context.get('error_type')
        )
        
        self.engine.record_activation(activation)
        
        # Track task progress
        if task_id not in self.active_tasks:
            self.active_tasks[task_id] = {
                'rules': [],
                'start_time': datetime.now(),
                'total_tokens': 0
            }
        
        self.active_tasks[task_id]['rules'].append(rule_id)
        self.active_tasks[task_id]['total_tokens'] += activation.token_count_after
    
    async def on_task_completed(self, task_id: str, outcome: Dict[str, Any]):
        """Hook called when a task is completed"""
        if task_id not in self.active_tasks:
            return
        
        task_data = self.active_tasks[task_id]
        
        task_outcome = TaskOutcome(
            task_id=task_id,
            rule_sequence=task_data['rules'],
            total_tokens=task_data['total_tokens'],
            total_time_ms=int((datetime.now() - task_data['start_time']).total_seconds() * 1000),
            quality_score=outcome.get('quality_score', 0.5),
            creativity_score=outcome.get('creativity_score', 0.5),
            safety_incidents=outcome.get('safety_incidents', 0),
            user_revisions=outcome.get('user_revisions', 0),
            completion_status=outcome.get('status', 'unknown')
        )
        
        # Save to database
        conn = sqlite3.connect(self.engine.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO task_outcomes
            (task_id, rule_sequence, total_tokens, total_time_ms,
             quality_score, creativity_score, safety_incidents,
             user_revisions, completion_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task_outcome.task_id,
            json.dumps(task_outcome.rule_sequence),
            task_outcome.total_tokens,
            task_outcome.total_time_ms,
            task_outcome.quality_score,
            task_outcome.creativity_score,
            task_outcome.safety_incidents,
            task_outcome.user_revisions,
            task_outcome.completion_status
        ))
        
        conn.commit()
        conn.close()
        
        # Clean up
        del self.active_tasks[task_id]


async def main():
    """Main entry point for evolution engine"""
    engine = RuleSymbiosisEvolution()
    
    # Run evolution
    await engine.run_evolution(generations=50)
    
    # Analyze patterns
    detector = PatternDetector()
    patterns = detector.analyze_sequences(engine.db_path)
    
    print("\n=== Discovered Sequence Patterns ===")
    for pattern, count in patterns[:10]:
        print(f"{' → '.join(pattern)}: {count} occurrences")
    
    # Context correlations
    correlations = detector.find_context_correlations(engine.db_path)
    
    print("\n=== Context-Rule Affinities ===")
    for context, rules in correlations.items():
        print(f"\n{context}:")
        top_rules = sorted(rules.items(), key=lambda x: x[1], reverse=True)[:5]
        for rule, affinity in top_rules:
            print(f"  {rule}: {affinity:.3f}")


if __name__ == "__main__":
    asyncio.run(main())
