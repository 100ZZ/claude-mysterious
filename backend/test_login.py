#!/usr/bin/env python3
"""
测试登录功能脚本
"""
import requests
import json

def test_login():
    """测试登录接口"""
    url = "http://localhost:2121/api/auth/login"
    
    # 测试正确的用户名和密码
    print("=" * 50)
    print("测试1: 正确的用户名和密码 (admin/admin)")
    print("=" * 50)
    
    data = {
        "username": "admin",
        "password": "admin"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("✅ 登录成功！")
            token = response.json().get('access_token')
            print(f"Token: {token[:50]}...")
        else:
            print("❌ 登录失败！")
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        print("请确保后端服务已启动: python main.py")
    
    print("\n" + "=" * 50)
    print("测试2: 错误的用户名或密码")
    print("=" * 50)
    
    wrong_data = {
        "username": "admin",
        "password": "wrong_password"
    }
    
    try:
        response = requests.post(url, json=wrong_data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求结果: {e}")

if __name__ == "__main__":
    test_login()

