#!/usr/bin/env python3
"""
Documentation Generator for Cursor Rules
Creates comprehensive markdown documentation from rule metadata
"""

import yaml
import json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict


class DocsGenerator:
    def __init__(self, rules_dir: Path, output_dir: Path):
        self.rules_dir = rules_dir
        self.output_dir = output_dir
        self.rules_metadata = {}
        self.dependency_graph = nx.DiGraph()
    
    def load_all_metadata(self):
        """Load metadata from all YAML files"""
        for yaml_file in self.rules_dir.rglob('*.yaml'):
            if yaml_file.name.startswith('_'):
                continue
                
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)
                    
                if data and isinstance(data, dict):
                    rule_name = yaml_file.stem
                    self.rules_metadata[rule_name] = {
                        'metadata': data,
                        'path': yaml_file,
                        'category': yaml_file.parent.name
                    }
                    
                    # Build dependency graph
                    if 'dependencies' in data:
                        for dep in data['dependencies']:
                            dep_name = Path(dep).stem
                            self.dependency_graph.add_edge(rule_name, dep_name)
                            
            except yaml.YAMLError as e:
                pass  # Skip invalid YAML files
            except Exception as e:
                pass  # Skip files with other errors
    
    def generate_index(self) -> str:
        """Generate main index page"""
        content = ["# Cursor Rules Documentation\n"]
        content.append(f"Total Rules: {len(self.rules_metadata)}\n")
        
        # Summary by category
        categories = defaultdict(list)
        for rule_name, data in self.rules_metadata.items():
            categories[data['category']].append(rule_name)
        
        content.append("## Categories\n")
        for category in sorted(categories):
            count = len(categories[category])
            content.append(f"- [{category}](categories/{category}.md) ({count} rules)")
        
        # Dependency visualization
        content.append("\n## Dependencies\n")
        content.append("![Dependency Graph](images/dependency_graph.png)\n")
        
        # Performance summary
        content.append("## Performance Summary\n")
        total_tokens = sum(
            data['metadata'].get('performance', {}).get('avg_tokens', 0)
            for data in self.rules_metadata.values()
        )
        content.append(f"- **Total Token Budget**: {total_tokens:,}")
        content.append(f"- **Average Tokens per Rule**: {total_tokens // len(self.rules_metadata) if self.rules_metadata else 0:,}")
        
        # Recently updated
        content.append("\n## Recent Updates\n")
        recent = sorted(
            self.rules_metadata.items(),
            key=lambda x: x[1]['metadata'].get('last_modified', ''),
            reverse=True
        )[:10]
        
        for rule_name, data in recent:
            meta = data['metadata']
            content.append(f"- [{rule_name}](rules/{rule_name}.md) - {meta.get('last_modified', 'Unknown')}")
        
        return "\n".join(content)
    
    def generate_rule_doc(self, rule_name: str) -> str:
        """Generate documentation for a single rule"""
        rule_data = self.rules_metadata[rule_name]
        metadata = rule_data['metadata']
        
        content = [f"# {rule_name}\n"]
        
        # Metadata table
        content.append("## Metadata\n")
        content.append("| Field | Value |")
        content.append("|-------|-------|")
        content.append(f"| Description | {metadata.get('description', 'No description')} |")
        content.append(f"| Version | {metadata.get('version', 'Unknown')} |")
        content.append(f"| Author | {metadata.get('author', 'Unknown')} |")
        content.append(f"| Created | {metadata.get('created', 'Unknown')} |")
        content.append(f"| Last Modified | {metadata.get('last_modified', 'Unknown')} |")
        
        # Tags
        if 'tags' in metadata:
            content.append(f"| Tags | {', '.join(metadata['tags'])} |")
        content.append("")
        
        # Performance metrics
        if 'performance' in metadata:
            content.append("## Performance\n")
            perf = metadata['performance']
            content.append("| Metric | Value |")
            content.append("|--------|-------|")
            content.append(f"| Average Tokens | {perf.get('avg_tokens', 'N/A')} |")
            content.append(f"| P95 Latency | {perf.get('p95_latency', 'N/A')} |")
            content.append(f"| Success Rate | {perf.get('success_rate', 'N/A')}% |")
            content.append(f"| Token Budget | {perf.get('token_budget', 'N/A')} |")
            content.append("")
        
        # Dependencies
        if 'dependencies' in metadata:
            content.append("## Dependencies\n")
            for dep in metadata['dependencies']:
                dep_name = Path(dep).stem
                if dep_name in self.rules_metadata:
                    dep_desc = self.rules_metadata[dep_name]['metadata'].get('description', '')
                    content.append(f"- [{dep_name}]({dep_name}.md) - {dep_desc}")
                else:
                    content.append(f"- {dep} (external)")
            content.append("")
        
        # Dependents
        if rule_name in self.dependency_graph:
            dependents = list(self.dependency_graph.predecessors(rule_name))
            if dependents:
                content.append("## Used By\n")
                for dependent in sorted(dependents):
                    if dependent in self.rules_metadata:
                        dep_desc = self.rules_metadata[dependent]['metadata'].get('description', '')
                        content.append(f"- [{dependent}]({dependent}.md) - {dep_desc}")
                    else:
                        content.append(f"- {dependent}")
                content.append("")
        
        # Conflicts
        if 'conflicts' in metadata:
            content.append("## Conflicts\n")
            for conflict in metadata['conflicts']:
                if isinstance(conflict, dict):
                    content.append(f"- **{conflict.get('rule', 'Unknown')}** - Resolution: {conflict.get('resolution', 'none')}")
                else:
                    content.append(f"- {conflict}")
            content.append("")
        
        # Source files
        content.append("## Source Files\n")
        content.append(f"- [Metadata]({rule_data['path'].relative_to(self.rules_dir)})")
        mdc_path = rule_data['path'].with_suffix('.mdc')
        if mdc_path.exists():
            content.append(f"- [Rule Content]({mdc_path.relative_to(self.rules_dir)})")
        
        return "\n".join(content)
    
    def generate_category_doc(self, category: str) -> str:
        """Generate documentation for a category"""
        content = [f"# Category: {category}\n"]
        
        # Load category metadata if exists
        category_yaml = self.rules_dir / category / '_category.yaml'
        if category_yaml.exists():
            with open(category_yaml, 'r') as f:
                cat_meta = yaml.safe_load(f)
                if cat_meta:
                    content.append(f"**{cat_meta.get('name', category)}**\n")
                    content.append(f"*{cat_meta.get('description', '')}*\n")
                    if 'purpose' in cat_meta:
                        content.append("## Purpose\n")
                        content.append(cat_meta['purpose'] + "\n")
        
        # List all rules in category
        content.append("## Rules\n")
        category_rules = [(name, data) for name, data in self.rules_metadata.items() 
                         if data['category'] == category]
        
        for rule_name, rule_data in sorted(category_rules):
            meta = rule_data['metadata']
            content.append(f"### [{rule_name}](../rules/{rule_name}.md)")
            content.append(f"*Version {meta.get('version', 'N/A')}*\n")
            desc = meta.get('description', 'No description')
            if desc:
                content.append(desc + "\n")
            
            # Show key metrics
            if 'performance' in meta:
                perf = meta['performance']
                content.append(f"- **Tokens**: {perf.get('avg_tokens', 'N/A')}")
                content.append(f"- **Success Rate**: {perf.get('success_rate', 'N/A')}%")
            
            if 'tags' in meta:
                content.append(f"- **Tags**: {', '.join(meta['tags'])}")
            content.append("")
        
        return "\n".join(content)
    
    def generate_dependency_graph(self):
        """Create dependency graph visualization"""
        plt.figure(figsize=(20, 15))
        
        # Create layout
        pos = nx.spring_layout(self.dependency_graph, k=3, iterations=50)
        
        # Color nodes by category
        categories = list(set(data['category'] for data in self.rules_metadata.values()))
        colors = plt.cm.tab20(range(len(categories)))
        color_map = dict(zip(categories, colors))
        
        node_colors = []
        for node in self.dependency_graph.nodes():
            if node in self.rules_metadata:
                category = self.rules_metadata[node]['category']
                node_colors.append(color_map[category])
            else:
                node_colors.append('gray')
        
        # Draw graph
        nx.draw_networkx_nodes(self.dependency_graph, pos, 
                              node_color=node_colors, 
                              node_size=1000,
                              alpha=0.8)
        
        nx.draw_networkx_edges(self.dependency_graph, pos,
                              edge_color='gray',
                              arrows=True,
                              arrowsize=20,
                              alpha=0.5)
        
        nx.draw_networkx_labels(self.dependency_graph, pos,
                               font_size=8,
                               font_weight='bold')
        
        # Add legend
        legend_elements = []
        for category, color in color_map.items():
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                            markerfacecolor=color, markersize=10,
                                            label=category))
        plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))
        
        plt.title("Rule Dependencies Graph", fontsize=20)
        plt.axis('off')
        plt.tight_layout()
        
        # Save
        images_dir = self.output_dir / 'images'
        images_dir.mkdir(exist_ok=True)
        plt.savefig(images_dir / 'dependency_graph.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def generate_all(self):
        """Generate complete documentation"""
        # Loading metadata
        self.load_all_metadata()
        
        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'rules').mkdir(exist_ok=True)
        (self.output_dir / 'categories').mkdir(exist_ok=True)
        
        # Generate dependency graph
        # Generating dependency graph
        self.generate_dependency_graph()
        
        # Generate index
        # Generating index
        index_content = self.generate_index()
        with open(self.output_dir / 'README.md', 'w') as f:
            f.write(index_content)
        
        # Generate rule docs
        # Generating documentation for rules
        for rule_name in self.rules_metadata:
            rule_doc = self.generate_rule_doc(rule_name)
            with open(self.output_dir / 'rules' / f'{rule_name}.md', 'w') as f:
                f.write(rule_doc)
        
        # Generate category docs
        categories = set(data['category'] for data in self.rules_metadata.values())
        # Generating category documentation
        for category in categories:
            cat_doc = self.generate_category_doc(category)
            with open(self.output_dir / 'categories' / f'{category}.md', 'w') as f:
                f.write(cat_doc)
        
        # Documentation generated


# Functions for backwards compatibility
def extract_rule_info(filename: str, content: str) -> Dict[str, Any]:
    """Extract rule information from content"""
    info = {
        'name': Path(filename).stem,
        'description': 'No description',
        'version': 'Unknown',
        'author': 'Unknown',
        'created': 'Unknown',
        'last_modified': 'Unknown',
        'dependencies': [],
        'conflicts': [],
        'performance': {},
        'tags': [],
        'purpose': 'Unknown',
        'metadata': {}
    }
    
    # Try to parse YAML frontmatter
    if content.startswith('---'):
        try:
            parts = content.split('---', 2)
            if len(parts) >= 3:
                metadata = yaml.safe_load(parts[1])
                if metadata:
                    info['metadata'] = metadata
                    info.update({k: v for k, v in metadata.items() if k in info})
        except:
            pass
    
    # Extract purpose from content
    if '* **Purpose**:' in content:
        purpose_line = content.split('* **Purpose**:')[1].split('\n')[0].strip()
        info['purpose'] = purpose_line
    elif '**Purpose**:' in content:
        purpose_line = content.split('**Purpose**:')[1].split('\n')[0].strip()
        info['purpose'] = purpose_line
    
    return info


def generate_rule_doc(info: Dict[str, Any]) -> str:
    """Generate markdown documentation for a rule"""
    lines = [
        f"# {info['name']}",
        "",
        f"**Description**: {info['description']}",
        "",
        "## Metadata",
        "",
        f"- **Version**: {info['version']}",
        f"- **Author**: {info['author']}",
        f"- **Created**: {info['created']}",
        f"- **Last Modified**: {info['last_modified']}",
        ""
    ]
    
    if info['tags']:
        lines.extend([
            "## Tags",
            "",
            f"{', '.join(info['tags'])}",
            ""
        ])
    
    lines.extend([
        "## Purpose",
        "",
        info['purpose'],
        ""
    ])
    
    if info['dependencies']:
        lines.extend([
            "## Dependencies",
            ""
        ])
        for dep in info['dependencies']:
            lines.append(f"- {dep}")
        lines.append("")
    
    if info['performance']:
        lines.extend([
            "## Performance Metrics",
            ""
        ])
        perf = info['performance']
        if 'avg_tokens' in perf:
            lines.append(f"- **Average Tokens**: {perf['avg_tokens']}")
        if 'p95_latency' in perf:
            lines.append(f"- **P95 Latency**: {perf['p95_latency']}")
        if 'success_rate' in perf:
            lines.append(f"- **Success Rate**: {perf['success_rate']}%")
        lines.append("")
    
    return "\n".join(lines)


def generate_category_index(category: str, rules: List[Dict[str, Any]]) -> str:
    """Generate index for a category"""
    lines = [
        f"# Category: {category}",
        "",
        f"Total rules: {len(rules)}",
        "",
        "| Rule | Description | Version | Tokens |",
        "|------|-------------|---------|--------|"
    ]
    
    for rule in sorted(rules, key=lambda x: x['name']):
        tokens = rule.get('performance', {}).get('avg_tokens', 'N/A')
        lines.append(
            f"| [{rule['name']}]({rule['name']}.md) | "
            f"{rule['description']} | "
            f"{rule['version']} | "
            f"{tokens} |"
        )
    
    return "\n".join(lines)


def generate_main_index(categories: Dict[str, int], total_rules: int) -> str:
    """Generate main documentation index"""
    lines = [
        "# Cursor Rules Documentation",
        "",
        f"Total Rules: {total_rules}",
        "",
        "## Categories",
        "",
        "| Category | Rule Count |",
        "|----------|------------|"
    ]
    
    for category in sorted(categories.keys()):
        lines.append(f"| [{category}]({category}/index.md) | {categories[category]} |")
    
    return "\n".join(lines)


def generate_all_docs(rules_dir: str, output_dir: str) -> Dict[str, Any]:
    """Generate all documentation"""
    rules_path = Path(rules_dir)
    output_path = Path(output_dir)
    
    # Use new generator
    generator = DocsGenerator(rules_path, output_path)
    generator.generate_all()
    
    # Return stats
    categories = defaultdict(int)
    for data in generator.rules_metadata.values():
        categories[data['category']] += 1
    
    return {
        'total_rules': len(generator.rules_metadata),
        'categories': len(categories),
        'rules_per_category': dict(categories)
    }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate documentation from rule metadata")
    parser.add_argument('--rules-dir', type=Path, 
                        default=Path(__file__).parent.parent / 'rules',
                        help='Rules directory path')
    parser.add_argument('--output-dir', type=Path,
                        default=Path(__file__).parent.parent / 'docs' / 'generated',
                        help='Output directory for documentation')
    
    args = parser.parse_args()
    
    stats = generate_all_docs(str(args.rules_dir), str(args.output_dir))
    # Documentation generation complete


if __name__ == '__main__':
    main()
