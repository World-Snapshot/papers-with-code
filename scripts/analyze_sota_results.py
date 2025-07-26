#!/usr/bin/env python3
"""
分析SOTA（State of the Art）结果数据
"""

import json
import gzip
import pandas as pd
from collections import defaultdict

def analyze_sota_structure():
    """分析评估表中的SOTA结果结构"""
    print("=== 分析SOTA结果数据结构 ===\n")
    
    with gzip.open('../data/evaluation-tables.json.gz', 'rt', encoding='utf-8') as f:
        eval_tables = json.load(f)
    
    # 找一个有完整SOTA数据的例子
    for table in eval_tables:
        if 'datasets' in table and table['datasets']:
            for dataset_info in table['datasets']:
                if 'sota' in dataset_info and 'rows' in dataset_info['sota']:
                    rows = dataset_info['sota']['rows']
                    if len(rows) > 5:  # 找一个有多个结果的
                        print(f"任务: {table['task']}")
                        print(f"数据集: {dataset_info.get('dataset', 'Unknown')}")
                        print(f"SOTA结果数量: {len(rows)}")
                        print("\n前5个结果：")
                        
                        for i, row in enumerate(rows[:5]):
                            print(f"\n{i+1}. 模型: {row.get('model_name', 'Unknown')}")
                            print(f"   论文: {row.get('paper_title', 'Unknown')}")
                            print(f"   日期: {row.get('paper_date', 'Unknown')}")
                            print(f"   指标: {row.get('metrics', {})}")
                            print(f"   代码: {row.get('code_links', [])}")
                        
                        return table, dataset_info

def extract_leaderboard_data():
    """提取可以用于绘制排行榜的数据"""
    print("\n\n=== 提取排行榜数据示例 ===\n")
    
    with gzip.open('../data/evaluation-tables.json.gz', 'rt', encoding='utf-8') as f:
        eval_tables = json.load(f)
    
    # 收集一些经典任务的SOTA历史
    classic_tasks = ['Image Classification', 'Object Detection', 'Machine Translation', 
                     'Question Answering', 'Named Entity Recognition']
    
    leaderboards = {}
    
    for table in eval_tables:
        task_name = table.get('task', '')
        if any(task in task_name for task in classic_tasks):
            if 'datasets' in table:
                for dataset_info in table['datasets']:
                    if 'sota' in dataset_info and 'rows' in dataset_info['sota']:
                        dataset_name = dataset_info.get('dataset', 'Unknown')
                        rows = dataset_info['sota']['rows']
                        
                        if len(rows) > 3:  # 至少有3个结果
                            # 提取时间序列数据
                            timeline_data = []
                            for row in rows:
                                if 'paper_date' in row and 'metrics' in row:
                                    timeline_data.append({
                                        'date': row['paper_date'],
                                        'model': row.get('model_name', 'Unknown'),
                                        'paper': row.get('paper_title', ''),
                                        'metrics': row['metrics']
                                    })
                            
                            if timeline_data:
                                key = f"{task_name} - {dataset_name}"
                                # 过滤掉没有日期的记录
                                timeline_data_with_date = [x for x in timeline_data if x['date']]
                                if timeline_data_with_date:
                                    leaderboards[key] = sorted(timeline_data_with_date, key=lambda x: x['date'])
    
    # 展示一个例子
    for task_dataset, data in list(leaderboards.items())[:3]:
        print(f"\n任务-数据集: {task_dataset}")
        print(f"历史记录数: {len(data)}")
        
        # 找出主要指标
        if data and data[0]['metrics']:
            metric_names = list(data[0]['metrics'].keys())
            print(f"评估指标: {metric_names}")
            
            # 展示进步历程
            print("\nSOTA进步历程：")
            for i, record in enumerate(data[-5:]):  # 最近5个
                print(f"{record['date']}: {record['model']} - {record['metrics']}")

def create_visualization_data():
    """创建可用于可视化的数据文件"""
    print("\n\n=== 创建可视化数据文件 ===\n")
    
    with gzip.open('../data/evaluation-tables.json.gz', 'rt', encoding='utf-8') as f:
        eval_tables = json.load(f)
    
    # 收集所有SOTA数据
    all_sota_records = []
    
    for table in eval_tables:
        task_name = table.get('task', '')
        categories = table.get('categories', [])
        
        if 'datasets' in table:
            for dataset_info in table['datasets']:
                dataset_name = dataset_info.get('dataset', 'Unknown')
                
                if 'sota' in dataset_info and 'rows' in dataset_info['sota']:
                    for row in dataset_info['sota']['rows']:
                        record = {
                            'task': task_name,
                            'categories': '; '.join(categories),
                            'dataset': dataset_name,
                            'model': row.get('model_name', 'Unknown'),
                            'paper_title': row.get('paper_title', ''),
                            'paper_date': row.get('paper_date', ''),
                            'paper_url': row.get('paper_url', ''),
                            'code_available': len(row.get('code_links', [])) > 0,
                            'uses_additional_data': row.get('uses_additional_data', False)
                        }
                        
                        # 添加所有指标
                        metrics = row.get('metrics', {})
                        for metric_name, metric_value in metrics.items():
                            record[f'metric_{metric_name}'] = metric_value
                        
                        all_sota_records.append(record)
    
    # 保存为CSV
    import os
    os.makedirs('../results', exist_ok=True)
    df = pd.DataFrame(all_sota_records)
    df.to_csv('../results/sota_results_all.csv', index=False)
    print(f"✓ 已创建 sota_results_all.csv，包含 {len(df)} 条SOTA记录")
    
    # 创建一些特定任务的详细文件
    popular_tasks = df['task'].value_counts().head(20).index.tolist()
    
    for task in popular_tasks[:5]:  # 前5个最流行的任务
        task_df = df[df['task'] == task]
        filename = f"../results/sota_{task.lower().replace(' ', '_').replace('/', '_')}.csv"
        task_df.to_csv(filename, index=False)
        print(f"✓ 已创建 {filename}，包含 {len(task_df)} 条记录")

def analyze_metrics_evolution():
    """分析指标随时间的演进"""
    print("\n\n=== 分析指标演进趋势 ===\n")
    
    # 读取刚创建的数据
    df = pd.read_csv('../results/sota_results_all.csv')
    
    # 转换日期格式
    df['paper_date'] = pd.to_datetime(df['paper_date'], errors='coerce')
    
    # 找出有时间数据的记录
    df_with_date = df.dropna(subset=['paper_date'])
    
    print(f"总记录数: {len(df)}")
    print(f"有日期的记录数: {len(df_with_date)}")
    
    # 分析每年的SOTA数量
    df_with_date['year'] = df_with_date['paper_date'].dt.year
    yearly_counts = df_with_date['year'].value_counts().sort_index()
    
    print("\n每年SOTA记录数：")
    for year, count in yearly_counts.items():
        if 2015 <= year <= 2024:  # 只显示近10年
            print(f"{year}: {count} 条")

if __name__ == "__main__":
    # 1. 分析数据结构
    example_table, example_dataset = analyze_sota_structure()
    
    # 2. 提取排行榜数据
    extract_leaderboard_data()
    
    # 3. 创建可视化数据
    create_visualization_data()
    
    # 4. 分析趋势
    analyze_metrics_evolution()
    
    print("\n\n✅ 分析完成！你现在可以：")
    print("1. 使用 sota_results_all.csv 创建任何任务的排行榜")
    print("2. 使用特定任务的CSV文件绘制SOTA进步曲线")
    print("3. 按日期排序查看技术进步历程")
    print("4. 分析哪些模型/方法最成功")