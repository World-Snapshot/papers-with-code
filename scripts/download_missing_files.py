#!/usr/bin/env python3
"""
下载缺失的Papers with Code数据文件
"""

import os
import urllib.request
import time
from datetime import datetime

# 需要下载的文件
FILES_TO_DOWNLOAD = {
    'papers-with-abstracts.json.gz': {
        'url': 'https://production-media.paperswithcode.com/about/papers-with-abstracts.json.gz',
        'size': '~540 MB',
        'description': '包含576,261篇论文的标题和摘要'
    },
    'links-between-papers-and-code.json.gz': {
        'url': 'https://production-media.paperswithcode.com/about/links-between-papers-and-code.json.gz', 
        'size': '~25 MB',
        'description': '包含300,161个论文与代码仓库的链接关系'
    }
}

def download_file(url, filename, description):
    """下载文件"""
    print(f"\n正在下载: {filename}")
    print(f"描述: {description}")
    print(f"URL: {url}")
    
    # 检查文件是否已存在
    if os.path.exists(filename):
        existing_size = os.path.getsize(filename)
        print(f"文件已存在，大小: {existing_size/1024/1024:.1f} MB")
        return True
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        request = urllib.request.Request(url, headers=headers)
        
        start_time = time.time()
        downloaded = 0
        block_size = 1024 * 1024  # 1MB
        
        with urllib.request.urlopen(request) as response:
            total_size = int(response.headers.get('Content-Length', 0))
            
            with open(filename, 'wb') as f:
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break
                    
                    downloaded += len(buffer)
                    f.write(buffer)
                    
                    # 显示进度
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        elapsed = time.time() - start_time
                        if elapsed > 0:
                            speed = downloaded / elapsed / 1024 / 1024  # MB/s
                            print(f"\r进度: {percent:.1f}% ({downloaded/1024/1024:.1f} MB / {total_size/1024/1024:.1f} MB) "
                                  f"速度: {speed:.1f} MB/s", end='')
            
            print(f"\n✓ 下载完成: {filename} ({downloaded/1024/1024:.1f} MB)")
            return True
            
    except Exception as e:
        print(f"\n✗ 下载失败: {e}")
        return False

def main():
    print("=== Papers with Code 数据文件下载 ===")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 确保在data目录中
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    os.chdir(data_dir)
    
    print(f"\n工作目录: {os.getcwd()}")
    
    # 下载文件
    success_count = 0
    for filename, info in FILES_TO_DOWNLOAD.items():
        if download_file(info['url'], filename, info['description']):
            success_count += 1
    
    print(f"\n=== 下载完成 ===")
    print(f"成功: {success_count}/{len(FILES_TO_DOWNLOAD)} 个文件")
    
    # 列出data目录的内容
    print("\n=== data目录内容 ===")
    for file in sorted(os.listdir('.')):
        if file.endswith('.gz') or file.endswith('.json'):
            size = os.path.getsize(file)
            print(f"{file}: {size/1024/1024:.1f} MB")

if __name__ == "__main__":
    main()