#!/usr/bin/env python3
"""
分析Papers with Code客户端结构和数据
"""

import json
import os
import sys

# 添加客户端路径
sys.path.insert(0, os.path.join(os.getcwd(), 'paperswithcode-client-develop'))

try:
    from paperswithcode import client
    print("✓ 成功导入Papers with Code客户端")
except ImportError as e:
    print(f"✗ 无法导入客户端: {e}")
    print("尝试分析本地数据文件...")

# 分析评估表结构
print("\n=== 分析评估表结构 ===")
import gzip

with gzip.open('evaluation-tables.json.gz', 'rt', encoding='utf-8') as f:
    eval_tables = json.load(f)
    
# 统计任务的层级关系
task_hierarchy = {}
task_areas = {}
task_categories = {}

for table in eval_tables:
    task_name = table.get('task', '')
    
    # 收集分类信息
    if 'categories' in table:
        task_categories[task_name] = table['categories']
        for category in table['categories']:
            if category not in task_areas:
                task_areas[category] = []
            if task_name not in task_areas[category]:
                task_areas[category].append(task_name)
    
    # 收集子任务信息
    if 'subtasks' in table and table['subtasks']:
        task_hierarchy[task_name] = []
        for subtask in table['subtasks']:
            if 'task' in subtask:
                task_hierarchy[task_name].append(subtask['task'])

print(f"\n发现 {len(task_hierarchy)} 个有子任务的任务")
print(f"发现 {len(task_areas)} 个研究领域/分类")

# 输出主要研究领域
print("\n=== 主要研究领域 ===")
sorted_areas = sorted(task_areas.items(), key=lambda x: len(x[1]), reverse=True)
for area, tasks in sorted_areas[:10]:
    print(f"{area}: {len(tasks)} 个任务")

# 分析任务层级深度
def get_task_depth(task, hierarchy, current_depth=0, visited=None):
    if visited is None:
        visited = set()
    
    if task in visited:
        return current_depth
    
    visited.add(task)
    
    if task not in hierarchy or not hierarchy[task]:
        return current_depth
    
    max_depth = current_depth
    for subtask in hierarchy[task]:
        depth = get_task_depth(subtask, hierarchy, current_depth + 1, visited)
        max_depth = max(max_depth, depth)
    
    return max_depth

# 找出层级最深的任务
task_depths = {}
for task in task_hierarchy:
    depth = get_task_depth(task, task_hierarchy)
    task_depths[task] = depth

print("\n=== 任务层级最深的前10个任务 ===")
sorted_depths = sorted(task_depths.items(), key=lambda x: x[1], reverse=True)
for task, depth in sorted_depths[:10]:
    print(f"{task}: 深度 {depth}")
    
# 分析数据集和基准的完整性
print("\n=== 数据集和基准统计 ===")
tasks_with_datasets = 0
tasks_with_benchmarks = 0
tasks_with_metrics = 0
all_metrics = set()

for table in eval_tables:
    if 'datasets' in table and table['datasets']:
        tasks_with_datasets += 1
        has_benchmarks = False
        has_metrics = False
        
        for dataset_info in table['datasets']:
            if 'dataset' in dataset_info:
                has_benchmarks = True
                
            if 'sota' in dataset_info and 'rows' in dataset_info['sota']:
                for row in dataset_info['sota']['rows']:
                    if 'metrics' in row:
                        has_metrics = True
                        all_metrics.update(row['metrics'].keys())
        
        if has_benchmarks:
            tasks_with_benchmarks += 1
        if has_metrics:
            tasks_with_metrics += 1

print(f"有数据集信息的任务: {tasks_with_datasets}")
print(f"有基准测试的任务: {tasks_with_benchmarks}")
print(f"有评估指标的任务: {tasks_with_metrics}")
print(f"发现的不同评估指标总数: {len(all_metrics)}")

# 输出最常见的评估指标
print("\n=== 最常见的评估指标 ===")
metric_counts = {}
for table in eval_tables:
    if 'datasets' in table:
        for dataset_info in table['datasets']:
            if 'sota' in dataset_info and 'rows' in dataset_info['sota']:
                for row in dataset_info['sota']['rows']:
                    if 'metrics' in row:
                        for metric in row['metrics'].keys():
                            metric_counts[metric] = metric_counts.get(metric, 0) + 1

sorted_metrics = sorted(metric_counts.items(), key=lambda x: x[1], reverse=True)
for metric, count in sorted_metrics[:20]:
    print(f"{metric}: {count} 次")

# 创建任务层级关系CSV
import csv

print("\n=== 创建任务层级关系CSV ===")
with open('task_hierarchy.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Parent Task', 'Child Tasks Count', 'Child Tasks', 'Task Depth', 'Categories'])
    
    for task, subtasks in sorted(task_hierarchy.items(), key=lambda x: len(x[1]), reverse=True):
        categories = task_categories.get(task, [])
        depth = task_depths.get(task, 0)
        writer.writerow([
            task,
            len(subtasks),
            '; '.join(subtasks[:10]) + ('...' if len(subtasks) > 10 else ''),
            depth,
            '; '.join(categories)
        ])

print("✓ 已创建 task_hierarchy.csv")

# 创建研究领域任务分类CSV
with open('research_areas.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Research Area', 'Task Count', 'Example Tasks'])
    
    for area, tasks in sorted_areas:
        writer.writerow([
            area,
            len(tasks),
            '; '.join(tasks[:15]) + ('...' if len(tasks) > 15 else '')
        ])

print("✓ 已创建 research_areas.csv")

print("\n分析完成！")