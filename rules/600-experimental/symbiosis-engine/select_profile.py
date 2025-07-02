#!/usr/bin/env python3
"""Quick profile selector based on task description"""

def select_profile(task_desc):
    task_lower = task_desc.lower()
    
    if any(word in task_lower for word in ['creative', 'design', 'innovative', 'novel']):
        if 'safe' in task_lower or 'complian' in task_lower:
            return 'paradoxical_innovation'
        return 'wildcard_explorer'
    
    elif any(word in task_lower for word in ['analyz', 'research', 'investigat']):
        if 'large' in task_lower or 'data' in task_lower:
            return 'efficient_explorer'
        return 'analytical_depth'
    
    elif any(word in task_lower for word in ['quick', 'fast', 'prototype', 'mvp']):
        return 'rapid_prototyping'
    
    elif any(word in task_lower for word in ['biomimetic', 'inspired', 'pattern']):
        return 'cross_domain_sage'
    
    else:
        return 'paradoxical_innovation'  # Default

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        task = ' '.join(sys.argv[1:])
        profile = select_profile(task)
        print(f"Recommended profile: {profile}")
    else:
        print("Usage: python3 select_profile.py <task description>")
