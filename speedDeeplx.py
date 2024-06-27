#!/usr/bin/python3  
# -- coding: utf-8 --
# @Time : 2024/5/31 23:05
# -------------------------------
# cron "0 0 8 1/1 * ?" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('测试Deeplx延迟');

import requests
import time

# DeepLX接口列表
deepl_urls = [
    "https://deeplx.qikepai.cn/translate",
    "https://api.deeplx.org/lsYbQ4_OOSFOpAx0GdJsDoAS_iE4q4zd_ESD0rWk8a0/translate"
]

# 测试请求参数
test_data = {
    "text": "Hello, world!",
    "source_lang": "EN",
    "target_lang": "ZH"
}

# 用来收集可用接口及其响应时间
available_endpoints = []

# 检测每个接口的可用性和延迟
for url in deepl_urls:
    try:
        start_time = time.time()
        response = requests.post(url, json=test_data, timeout=5)
        latency = time.time() - start_time
        # 确保服务真正可用
        if response.status_code == 200 and ('data' in response.json() and len(str(response.json().get("data"))) > 0):
            available_endpoints.append((url, latency))
    except requests.exceptions.RequestException:
        continue  # 忽略错误，只关注可用接口

# 根据延迟时间排序接口
available_endpoints.sort(key=lambda x: x[1])

# 打印界面美化
print("\nAvailable DeepLX Endpoints with Latencies:")
print("-" * 60)
for endpoint, delay in available_endpoints:
    print(f"🚀 ({delay:.2f}s) {endpoint}")
print("-" * 60)

# 打印所有可用的接口，按延迟排序，格式为"DeepLX👌：(count)"
if available_endpoints:
    formatted_endpoints = ", ".join([endpoint[0] for endpoint in available_endpoints])
    print(f"\nDeepLX👌：({len(available_endpoints)}) {formatted_endpoints}\n")
else:
    print("No available endpoints found.\n")
