#!/usr/bin/python3  
# -- coding: utf-8 --
# @Time : 2024/5/31 23:05
# -------------------------------
# cron "0 0 8 1/1 * ?" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('测试Deeplx延迟');

import requests
import time
import threading
from tqdm import tqdm
import argparse
import os

# 命令行参数解析
parser = argparse.ArgumentParser(description='检查 DeepLX 接口。')
parser.add_argument('-t', '--threads', type=int, default=5, help='要使用的线程数。')
args = parser.parse_args()

# DeepLX 接口列表
with open('DeeplxUrl.txt', 'r') as file:
    deepl_urls = [line.strip() for line in file]

# 测试请求参数
test_data = {
    "text": "Hello, world!",
    "source_lang": "EN",
    "target_lang": "ZH"
}

# 用来收集可用接口及其响应时间
available_endpoints = []
lock = threading.Lock()

# 检测每个接口的可用性和延迟
def check_endpoint(url):
    try:
        start_time = time.time()
        response = requests.post(url, json=test_data, timeout=5)
        latency = time.time() - start_time
        # 确保服务真正可用
        if response.status_code == 200 and ('data' in response.json() and len(str(response.json().get("data"))) > 0):
            with lock:
                available_endpoints.append((url, latency))
    except requests.exceptions.RequestException:
        pass  # 忽略错误，只关注可用接口

# 创建线程
threads = []
for url in tqdm(deepl_urls, desc="检查接口中"):
    t = threading.Thread(target=check_endpoint, args=(url,))
    t.start()
    threads.append(t)
    # 限制最大线程数
    while threading.active_count() > args.threads:
        time.sleep(0.1)

# 等待所有线程完成
for t in threads:
    t.join()

# 根据延迟时间排序接口
available_endpoints.sort(key=lambda x: x[1])

# 写入所有可用的接口到 success.txt,按延迟时间排序
if available_endpoints:
    with open('success.txt', 'w') as f:
        for endpoint in available_endpoints:
            f.write(f"{endpoint[0]}\n")
else:
    print("未找到可用的接口。\n")