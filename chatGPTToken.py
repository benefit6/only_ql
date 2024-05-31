#!/usr/bin/python3  
# -- coding: utf-8 --
# @Time : 2024/5/31 23:05
# -------------------------------
# cron "0 0 6 1/10 * ?" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('ChatGPT获取ShareToken');

import requests

# 获取新的 access token
def get_access_token(refresh_token):
    url = "https://token.oaifree.com/api/auth/refresh"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'refresh_token': refresh_token}
    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()
    print("Response Data:", response_data)  # 打印响应内容进行检查
    if "access_token" in response_data:
        return response_data["access_token"]
    else:
        return "Access token not found in response"

# 生成 share token
def generate_share_token(access_token):
    url = "https://chat.oaifree.com/token/register"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        'unique_name': 'benefit',
        'access_token': access_token,
        'site_limit': '',
        'expires_in': 0,
        'show_conversations': 'true',
    }
    response = requests.post(url, headers=headers, data=data)
    return response.text

# 提供 refresh token
refresh_token = os.environ.get("chatGPT_refresh_token"):

# 获取并打印 access token
access_token = get_access_token(refresh_token)
print("Access Token:", access_token)

# 使用 access token 生成并打印 share token
share_token_response = generate_share_token(access_token)
print("Share Token Response:", share_token_response)