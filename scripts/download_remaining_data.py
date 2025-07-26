#!/usr/bin/env python3
"""
下载Papers with Code剩余的数据文件
"""

import os
import urllib.request
import time
from datetime import datetime

# 剩余需要下载的文件
REMAINING_URLS = {
    'papers-with-abstracts.json.gz': 'https://production-media.paperswithcode.com/about/papers-with-abstracts.json.gz',
    'links-between-papers-and-code.json.gz': 'https://production-media.paperswithcode.com/about/links-between-papers-and-code.json.gz'
}

def download_file_with_resume(url, filename):
    """支持断点续传的下载函数"""
    print(f"\n正在下载: {filename}")
    print(f"URL: {url}")
    
    # 检查是否有部分下载的文件
    if os.path.exists(filename):
        resume_pos = os.path.getsize(filename)
        print(f"发现部分下载文件，从 {resume_pos:,} bytes 继续下载")
    else:
        resume_pos = 0
    
    try:
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # 如果需要断点续传，添加Range头
        if resume_pos > 0:
            headers['Range'] = f'bytes={resume_pos}-'
        
        request = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(request) as response:
            # 获取文件总大小
            if resume_pos > 0:
                # 断点续传时，Content-Length是剩余大小
                content_length = response.headers.get('Content-Length')
                if content_length:
                    total_size = resume_pos + int(content_length)
                else:
                    total_size = 0
            else:
                total_size = int(response.headers.get('Content-Length', 0))
            
            # 打开文件（追加模式如果是续传）
            mode = 'ab' if resume_pos > 0 else 'wb'
            
            downloaded = resume_pos
            block_size = 1024 * 1024  # 1MB块大小
            start_time = time.time()
            
            with open(filename, mode) as f:
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
                            speed = (downloaded - resume_pos) / elapsed / 1024 / 1024  # MB/s
                            remaining = (total_size - downloaded) / ((downloaded - resume_pos) / elapsed) if downloaded > resume_pos else 0
                            remaining_min = remaining / 60
                            
                            print(f"\r进度: {percent:.1f}% ({downloaded:,} / {total_size:,} bytes) "
                                  f"速度: {speed:.1f} MB/s "
                                  f"剩余时间: {remaining_min:.1f} 分钟", end='')
            
            print(f"\n✓ 下载完成: {filename} ({downloaded:,} bytes)")
            return True
            
    except urllib.error.HTTPError as e:
        print(f"\n✗ HTTP错误 {e.code}: {e.reason}")
        if e.code == 416:  # Range Not Satisfiable
            print("  文件可能已完整下载")
            return True
        return False
    except KeyboardInterrupt:
        print(f"\n\n下载被中断。已下载 {downloaded:,} bytes")
        print("可以重新运行脚本继续下载")
        return False
    except Exception as e:
        print(f"\n✗ 下载失败: {e}")
        return False

def main():
    # 确保数据目录存在
    os.makedirs('../data', exist_ok=True)
    os.chdir('../data')
    
    print("=== Papers with Code 剩余数据下载 ===")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success_count = 0
    total_files = len(REMAINING_URLS)
    
    for filename, url in REMAINING_URLS.items():
        if download_file_with_resume(url, filename):
            success_count += 1
        else:
            print(f"\n跳过 {filename}")
    
    print(f"\n=== 下载完成 ===")
    print(f"成功下载: {success_count} / {total_files} 个文件")
    
    # 列出所有数据文件
    print("\n=== 当前数据目录内容 ===")
    for file in sorted(os.listdir('.')):
        if file.endswith('.json.gz') or file.endswith('.json'):
            size = os.path.getsize(file)
            print(f"{file}: {size/1024/1024:.1f} MB")

if __name__ == "__main__":
    main()