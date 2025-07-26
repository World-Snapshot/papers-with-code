#!/usr/bin/env python3
"""
从Papers with Code的官方数据导出链接下载所有可用数据
"""

import os
import urllib.request
import urllib.error
from datetime import datetime

# 数据下载链接（来自paperswithcode-data README）
DATA_URLS = {
    'papers-with-abstracts.json.gz': 'https://production-media.paperswithcode.com/about/papers-with-abstracts.json.gz',
    'links-between-papers-and-code.json.gz': 'https://production-media.paperswithcode.com/about/links-between-papers-and-code.json.gz',
    'evaluation-tables.json.gz': 'https://production-media.paperswithcode.com/about/evaluation-tables.json.gz',
    'methods.json.gz': 'https://production-media.paperswithcode.com/about/methods.json.gz',
    'datasets.json.gz': 'https://production-media.paperswithcode.com/about/datasets.json.gz'
}

def download_file(url, filename):
    """下载文件并显示进度"""
    print(f"\n正在下载: {filename}")
    print(f"URL: {url}")
    
    try:
        # 添加User-Agent避免被拒绝
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        request = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(request) as response:
            # 获取文件大小
            file_size = int(response.headers.get('Content-Length', 0))
            
            # 下载文件
            downloaded = 0
            block_size = 8192
            
            with open(filename, 'wb') as f:
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break
                    
                    downloaded += len(buffer)
                    f.write(buffer)
                    
                    # 显示进度
                    if file_size > 0:
                        percent = (downloaded / file_size) * 100
                        print(f"\r  进度: {percent:.1f}% ({downloaded:,} / {file_size:,} bytes)", end='')
            
            print(f"\n✓ 下载完成: {filename} ({downloaded:,} bytes)")
            return True
            
    except urllib.error.HTTPError as e:
        print(f"✗ HTTP错误 {e.code}: {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"✗ URL错误: {e.reason}")
        return False
    except Exception as e:
        print(f"✗ 下载失败: {e}")
        return False

def check_existing_files():
    """检查已有的文件"""
    print("\n=== 检查已有文件 ===")
    existing = []
    missing = []
    
    for filename in DATA_URLS.keys():
        filepath = os.path.join('../data', filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"✓ 已存在: {filename} ({size:,} bytes)")
            existing.append(filename)
        else:
            print(f"✗ 缺失: {filename}")
            missing.append(filename)
    
    return existing, missing

def main():
    # 确保数据目录存在
    os.makedirs('../data', exist_ok=True)
    
    print("=== Papers with Code 数据下载工具 ===")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查已有文件
    existing, missing = check_existing_files()
    
    if not missing:
        print("\n所有数据文件都已存在！")
        return
    
    print(f"\n需要下载 {len(missing)} 个文件")
    
    # 下载缺失的文件
    success_count = 0
    for filename in missing:
        url = DATA_URLS[filename]
        filepath = os.path.join('../data', filename)
        
        if download_file(url, filepath):
            success_count += 1
        else:
            # 如果下载失败，尝试检查是否网站已关闭
            print("  提示：Papers with Code可能已停止提供数据下载服务")
    
    # 总结
    print(f"\n=== 下载完成 ===")
    print(f"成功下载: {success_count} / {len(missing)} 个文件")
    
    if success_count < len(missing):
        print("\n注意：部分文件下载失败。")
        print("Papers with Code网站可能已经完全关闭。")
        print("你已有的数据文件是最后的备份！")

if __name__ == "__main__":
    main()