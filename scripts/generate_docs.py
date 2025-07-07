        
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
        dependents = list(self.dependency_graph.predecessors(rule_name))
        if dependents:
            content.append("## Used By\n")
            for dependent in sorted(dependents):
                dep_desc = self.rules_metadata[dependent]['metadata'].get('description', '')
                content.append(f"- [{dependent}]({dependent}.md) - {dep_desc}")
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
            content.append(meta.get('description', 'No description') + "\n")
            
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
        print("Loading metadata...")
        self.load_all_metadata()
        
        # Create output directories
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / 'rules').mkdir(exist_ok=True)
        (self.output_dir / 'categories').mkdir(exist_ok=True)
        
        # Generate dependency graph
        print("Generating dependency graph...")
        self.generate_dependency_graph()
        
        # Generate index
        print("Generating index...")
        index_content = self.generate_index()
        with open(self.output_dir / 'README.md', 'w') as f:
            f.write(index_content)
        
        # Generate rule docs
        print(f"Generating documentation for {len(self.rules_metadata)} rules...")
        for rule_name in self.rules_metadata:
            rule_doc = self.generate_rule_doc(rule_name)
            with open(self.output_dir / 'rules' / f'{rule_name}.md', 'w') as f:
                f.write(rule_doc)
        
        # Generate category docs
        categories = set(data['category'] for data in self.rules_metadata.values())
        print(f"Generating category documentation for {len(categories)} categories...")
        for category in categories:
            cat_doc = self.generate_category_doc(category)
            with open(self.output_dir / 'categories' / f'{category}.md', 'w') as f:
                f.write(cat_doc)
        
        print(f"\nDocumentation generated in: {self.output_dir}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate documentation from rule metadata")
    parser.add_argument('--rules-dir', type=Path, 
                        default=Path(__file__).parent.parent / 'rules',
                        help='Rules directory path')
    parser.add_argument('--output-dir', type=Path,
                        default=Path(__file__).parent.parent / 'docs' / 'reference',
                        help='Output directory for documentation')
    
    args = parser.parse_args()
    
    generator = DocumentationGenerator(args.rules_dir, args.output_dir)
    generator.generate_all()

if __name__ == '__main__':
    main()