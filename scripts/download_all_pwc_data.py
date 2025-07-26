#!/usr/bin/env python3
"""
下载Papers with Code的所有可用数据
"""

import json
import os
import sys
import time
from datetime import datetime
import gzip

# 添加客户端路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'repositories', 'paperswithcode-client-develop'))

try:
    from paperswithcode import PapersWithCodeClient
    from paperswithcode.config import config
    print("✓ 成功导入Papers with Code客户端")
except ImportError as e:
    print(f"✗ 无法导入客户端: {e}")
    sys.exit(1)

# 创建数据保存目录
os.makedirs('../data/api_dumps', exist_ok=True)

def save_data(data, filename):
    """保存数据到JSON文件"""
    filepath = f'../data/api_dumps/{filename}'
    with gzip.open(filepath, 'wt', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  ✓ 已保存: {filepath}")
    return filepath

def download_with_pagination(func, name, **kwargs):
    """处理分页下载"""
    all_items = []
    page = 1
    items_per_page = 1000  # 每页最大项目数
    
    print(f"\n正在下载 {name}...")
    
    try:
        while True:
            print(f"  获取第 {page} 页...")
            result = func(page=page, items_per_page=items_per_page, **kwargs)
            
            if hasattr(result, 'results'):
                items = result.results
                all_items.extend([item.dict() if hasattr(item, 'dict') else item for item in items])
                
                print(f"    获取了 {len(items)} 个项目，总计: {len(all_items)}")
                
                # 检查是否有下一页
                if not result.next_page or len(items) < items_per_page:
                    break
                    
                page += 1
                time.sleep(0.5)  # 避免请求过快
            else:
                print(f"    意外的返回格式")
                break
                
    except Exception as e:
        print(f"  ✗ 下载失败: {e}")
        
    return all_items

def test_api_connection():
    """测试API连接"""
    print("\n=== 测试API连接 ===")
    client = PapersWithCodeClient()
    
    try:
        # 尝试获取一个小数据集测试连接
        papers = client.paper_list(page=1, items_per_page=1)
        print("✓ API连接正常")
        return client
    except Exception as e:
        print(f"✗ API连接失败: {e}")
        print("\n注意：API可能已经关闭。将分析本地已有数据。")
        return None

def download_all_data(client):
    """下载所有可用数据"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. 下载论文数据
    print("\n=== 下载论文数据 ===")
    papers = download_with_pagination(client.paper_list, "论文")
    if papers:
        save_data(papers, f'papers_{timestamp}.json.gz')
    
    # 2. 下载任务数据
    print("\n=== 下载任务数据 ===")
    tasks = download_with_pagination(client.task_list, "任务")
    if tasks:
        save_data(tasks, f'tasks_{timestamp}.json.gz')
    
    # 3. 下载数据集信息
    print("\n=== 下载数据集信息 ===")
    datasets = download_with_pagination(client.dataset_list, "数据集")
    if datasets:
        save_data(datasets, f'datasets_api_{timestamp}.json.gz')
    
    # 4. 下载方法/算法
    print("\n=== 下载方法/算法 ===")
    methods = download_with_pagination(client.method_list, "方法")
    if methods:
        save_data(methods, f'methods_api_{timestamp}.json.gz')
    
    # 5. 下载作者信息
    print("\n=== 下载作者信息 ===")
    authors = download_with_pagination(client.author_list, "作者")
    if authors:
        save_data(authors, f'authors_{timestamp}.json.gz')
    
    # 6. 下载会议信息
    print("\n=== 下载会议信息 ===")
    conferences = download_with_pagination(client.conference_list, "会议")
    if conferences:
        save_data(conferences, f'conferences_{timestamp}.json.gz')
    
    # 7. 下载代码仓库
    print("\n=== 下载代码仓库信息 ===")
    repositories = download_with_pagination(client.repository_list, "代码仓库")
    if repositories:
        save_data(repositories, f'repositories_{timestamp}.json.gz')
    
    # 8. 下载研究领域
    print("\n=== 下载研究领域 ===")
    areas = download_with_pagination(client.area_list, "研究领域")
    if areas:
        save_data(areas, f'areas_{timestamp}.json.gz')
    
    # 9. 下载评估表
    print("\n=== 下载评估表 ===")
    evaluations = download_with_pagination(client.evaluation_list, "评估表")
    if evaluations:
        save_data(evaluations, f'evaluations_api_{timestamp}.json.gz')
    
    # 统计信息
    print("\n=== 下载统计 ===")
    print(f"论文数量: {len(papers)}")
    print(f"任务数量: {len(tasks)}")
    print(f"数据集数量: {len(datasets)}")
    print(f"方法数量: {len(methods)}")
    print(f"作者数量: {len(authors)}")
    print(f"会议数量: {len(conferences)}")
    print(f"代码仓库数量: {len(repositories)}")
    print(f"研究领域数量: {len(areas)}")
    print(f"评估表数量: {len(evaluations)}")

def download_detailed_data(client, sample_size=10):
    """下载部分详细数据作为示例"""
    print("\n=== 下载详细数据示例 ===")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 获取一些任务的详细信息
    try:
        tasks = client.task_list(page=1, items_per_page=sample_size)
        detailed_tasks = []
        
        for task in tasks.results[:sample_size]:
            print(f"获取任务详情: {task.name}")
            try:
                # 获取子任务
                children = client.task_child_list(task.id, page=1, items_per_page=100)
                
                # 获取相关论文
                papers = client.task_paper_list(task.id, page=1, items_per_page=10)
                
                # 获取评估表
                evaluations = client.task_evaluation_list(task.id, page=1, items_per_page=10)
                
                detailed_task = {
                    'task': task.dict(),
                    'children': [child.dict() for child in children.results] if hasattr(children, 'results') else [],
                    'papers': [paper.dict() for paper in papers.results] if hasattr(papers, 'results') else [],
                    'evaluations': [eval.dict() for eval in evaluations.results] if hasattr(evaluations, 'results') else []
                }
                detailed_tasks.append(detailed_task)
                
            except Exception as e:
                print(f"  ✗ 获取任务 {task.name} 的详情失败: {e}")
        
        if detailed_tasks:
            save_data(detailed_tasks, f'tasks_detailed_sample_{timestamp}.json.gz')
            
    except Exception as e:
        print(f"✗ 获取详细数据失败: {e}")

def main():
    # 测试连接
    client = test_api_connection()
    
    if client:
        print("\n开始下载所有数据...")
        print("这可能需要一些时间，请耐心等待...")
        
        try:
            # 下载所有基础数据
            download_all_data(client)
            
            # 下载一些详细数据示例
            download_detailed_data(client)
            
            print("\n✓ 数据下载完成！")
            print(f"所有数据已保存到: {os.path.abspath('../data/api_dumps/')}")
            
        except KeyboardInterrupt:
            print("\n\n下载被用户中断")
        except Exception as e:
            print(f"\n下载过程中出错: {e}")
    else:
        print("\n由于API不可用，将分析本地已有数据...")
        print("本地数据文件位于: ../data/")

if __name__ == "__main__":
    main()