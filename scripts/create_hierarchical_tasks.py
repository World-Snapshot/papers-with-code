#!/usr/bin/env python3
"""
Create hierarchical task structures for each domain (CV, NLP, Audio, Other)
Combines information from task_hierarchy.csv with domain-specific task lists
"""

import pandas as pd
import json
import os
from collections import defaultdict

def load_data():
    """Load all necessary CSV files"""
    # Load task hierarchy
    hierarchy_df = pd.read_csv('../results/task_hierarchy.csv')
    
    # Load domain-specific tasks
    cv_tasks = pd.read_csv('../results/cv/cv_tasks_detailed.csv')
    nlp_tasks = pd.read_csv('../results/nlp/nlp_tasks_detailed.csv')
    audio_tasks = pd.read_csv('../results/audio/audio_tasks_detailed.csv')
    other_tasks = pd.read_csv('../results/other/other_tasks_detailed.csv')
    
    return hierarchy_df, cv_tasks, nlp_tasks, audio_tasks, other_tasks

def create_task_lookup(tasks_df):
    """Create a lookup dictionary for task details"""
    lookup = {}
    for _, row in tasks_df.iterrows():
        task_name = row['Task Name']
        lookup[task_name] = {
            'name': task_name,
            'description': row.get('Description', ''),
            'dataset_count': int(row.get('Dataset Count', 0)),
            'benchmarks': row.get('Benchmarks', '').split('; ') if pd.notna(row.get('Benchmarks')) else [],
            'metrics': row.get('Metrics', '').split('; ') if pd.notna(row.get('Metrics')) else [],
            'task_id': row.get('task_id', ''),
            'area': row.get('area', '')
        }
    return lookup

def parse_child_tasks(child_tasks_str):
    """Parse the child tasks string which may contain ellipsis"""
    if pd.isna(child_tasks_str):
        return []
    
    # Remove the ellipsis indicator if present
    child_tasks_str = child_tasks_str.replace('...', '')
    
    # Split by semicolon and clean up
    tasks = [task.strip() for task in child_tasks_str.split(';') if task.strip()]
    return tasks

def build_hierarchy(hierarchy_df, task_lookup, domain_filter=None):
    """Build hierarchical structure for tasks"""
    hierarchy = {}
    parent_to_children = defaultdict(list)
    
    # First pass: collect all parent-child relationships
    for _, row in hierarchy_df.iterrows():
        parent = row['Parent Task']
        categories = row.get('Categories', '')
        
        # Skip empty parent tasks
        if pd.isna(parent) or str(parent).strip() == '':
            continue
        
        # Filter by domain if specified
        if domain_filter:
            if pd.isna(categories) or domain_filter not in str(categories):
                continue
        
        child_tasks = parse_child_tasks(row['Child Tasks'])
        parent_to_children[parent] = child_tasks
    
    # Find root tasks (tasks that are parents but not children)
    all_parents = set(parent_to_children.keys())
    all_children = set()
    for children in parent_to_children.values():
        all_children.update(children)
    
    root_tasks = all_parents - all_children
    
    # Build tree structure
    def build_node(task_name, visited=None):
        if visited is None:
            visited = set()
        
        if task_name in visited:
            return None
        
        visited.add(task_name)
        
        node = {
            'name': task_name,
            'children': []
        }
        
        # Add task details if available
        if task_name in task_lookup:
            node.update(task_lookup[task_name])
        
        # Add children
        if task_name in parent_to_children:
            for child in parent_to_children[task_name]:
                child_node = build_node(child, visited.copy())
                if child_node:
                    node['children'].append(child_node)
        
        return node
    
    # Build trees from root tasks
    trees = []
    for root in sorted(root_tasks):
        tree = build_node(root)
        if tree:
            trees.append(tree)
    
    # Add orphan tasks (tasks in lookup but not in hierarchy)
    orphan_tasks = []
    all_hierarchical_tasks = all_parents | all_children
    
    for task_name in task_lookup:
        if task_name not in all_hierarchical_tasks:
            orphan_tasks.append({
                'name': task_name,
                'children': [],
                **task_lookup[task_name]
            })
    
    # Sort orphan tasks by dataset count
    orphan_tasks.sort(key=lambda x: x.get('dataset_count', 0), reverse=True)
    
    return trees, orphan_tasks

def save_hierarchical_data(trees, orphans, domain, output_dir):
    """Save hierarchical data as JSON"""
    data = {
        'domain': domain,
        'hierarchical_tasks': trees,
        'standalone_tasks': orphans,
        'total_tasks': count_all_tasks(trees) + len(orphans)
    }
    
    output_file = os.path.join(output_dir, f'{domain.lower()}_hierarchy.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {domain} hierarchy to {output_file}")
    print(f"  - Hierarchical tasks: {len(trees)} root tasks")
    print(f"  - Standalone tasks: {len(orphans)}")
    print(f"  - Total tasks: {data['total_tasks']}")

def count_all_tasks(trees):
    """Count all tasks in hierarchical structure"""
    count = 0
    
    def count_node(node):
        nonlocal count
        count += 1
        for child in node.get('children', []):
            count_node(child)
    
    for tree in trees:
        count_node(tree)
    
    return count

def create_flat_hierarchy_csv(trees, orphans, domain, output_dir):
    """Create a flat CSV representation of the hierarchy"""
    rows = []
    
    def process_node(node, parent_name='', level=0):
        row = {
            'Task Name': node['name'],
            'Parent Task': parent_name,
            'Level': level,
            'Dataset Count': node.get('dataset_count', 0),
            'Description': node.get('description', ''),
            'Benchmarks': '; '.join(node.get('benchmarks', [])),
            'Metrics': '; '.join(node.get('metrics', [])),
            'Children Count': len(node.get('children', []))
        }
        rows.append(row)
        
        for child in node.get('children', []):
            process_node(child, node['name'], level + 1)
    
    # Process hierarchical tasks
    for tree in trees:
        process_node(tree)
    
    # Process orphan tasks
    for task in orphans:
        row = {
            'Task Name': task['name'],
            'Parent Task': '',
            'Level': 0,
            'Dataset Count': task.get('dataset_count', 0),
            'Description': task.get('description', ''),
            'Benchmarks': '; '.join(task.get('benchmarks', [])),
            'Metrics': '; '.join(task.get('metrics', [])),
            'Children Count': 0
        }
        rows.append(row)
    
    # Create DataFrame and save
    df = pd.DataFrame(rows)
    df = df.sort_values(['Level', 'Dataset Count'], ascending=[True, False])
    
    output_file = os.path.join(output_dir, f'{domain.lower()}_hierarchy.csv')
    df.to_csv(output_file, index=False)
    print(f"Saved {domain} flat hierarchy to {output_file}")

def main():
    # Load data
    hierarchy_df, cv_tasks, nlp_tasks, audio_tasks, other_tasks = load_data()
    
    # Create output directory
    output_dir = '../results/hierarchical'
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each domain
    domains = [
        ('Computer Vision', cv_tasks, 'cv'),
        ('Natural Language Processing', nlp_tasks, 'nlp'),
        ('Audio', audio_tasks, 'audio'),
        ('Other', other_tasks, 'other')
    ]
    
    for domain_name, tasks_df, domain_code in domains:
        print(f"\nProcessing {domain_name} tasks...")
        
        # Create task lookup
        task_lookup = create_task_lookup(tasks_df)
        
        # Build hierarchy
        trees, orphans = build_hierarchy(hierarchy_df, task_lookup, domain_name)
        
        # Save hierarchical JSON
        save_hierarchical_data(trees, orphans, domain_code, output_dir)
        
        # Save flat CSV representation
        create_flat_hierarchy_csv(trees, orphans, domain_code, output_dir)

if __name__ == '__main__':
    main()