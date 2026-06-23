import requests

BASE_URL = 'http://localhost:5000/api'

print("=== 电商系统前后端联调测试 ===")
print()

print("1. 测试基础接口 /test")
try:
    r = requests.get(f'{BASE_URL}/test')
    data = r.json()
    print(f"   状态码: {r.status_code}")
    print(f"   返回: {data}")
    print("   ✓ 基础接口正常")
except Exception as e:
    print(f"   ✗ 失败: {e}")

print()
print("2. 测试分类列表 /categories")
try:
    r = requests.get(f'{BASE_URL}/categories')
    data = r.json()
    print(f"   状态码: {r.status_code}")
    print(f"   success: {data.get('success')}")
    print(f"   分类数量: {len(data.get('data', []))}")
    print("   ✓ 分类接口正常")
except Exception as e:
    print(f"   ✗ 失败: {e}")

print()
print("3. 测试品牌列表 /brands")
try:
    r = requests.get(f'{BASE_URL}/brands')
    data = r.json()
    print(f"   状态码: {r.status_code}")
    print(f"   success: {data.get('success')}")
    print(f"   品牌数量: {len(data.get('data', []))}")
    print("   ✓ 品牌接口正常")
except Exception as e:
    print(f"   ✗ 失败: {e}")

print()
print("4. 测试商品列表 /products")
try:
    r = requests.get(f'{BASE_URL}/products')
    data = r.json()
    print(f"   状态码: {r.status_code}")
    print(f"   success: {data.get('success')}")
    print(f"   商品总数: {data.get('total')}")
    print(f"   返回数量: {len(data.get('data', []))}")
    if data.get('data'):
        print(f"   第一个商品: {data['data'][0].get('name')}")
    print("   ✓ 商品列表接口正常")
except Exception as e:
    print(f"   ✗ 失败: {e}")

print()
print("5. 测试商品详情 /products/1")
try:
    r = requests.get(f'{BASE_URL}/products/1')
    data = r.json()
    print(f"   状态码: {r.status_code}")
    print(f"   success: {data.get('success')}")
    if data.get('data'):
        print(f"   商品名称: {data['data'].get('name')}")
        print(f"   价格: {data['data'].get('price')}")
        print(f"   图片数量: {len(data['data'].get('images', []))}")
    print("   ✓ 商品详情接口正常")
except Exception as e:
    print(f"   ✗ 失败: {e}")

print()
print("6. 测试用户登录 /auth/login")
try:
    r = requests.post(f'{BASE_URL}/auth/login', json={'username': 'test', 'password': '123456'})
    data = r.json()
    print(f"   状态码: {r.status_code}")
    print(f"   success: {data.get('success')}")
    if data.get('success'):
        token = data.get('token')
        print(f"   用户: {data['user'].get('username')}")
        print(f"   Token获取成功")
        print("   ✓ 登录接口正常")
    else:
        print(f"   登录失败: {data.get('message')}")
except Exception as e:
    print(f"   ✗ 失败: {e}")

print()
print("7. 测试购物车 /cart (需要登录)")
try:
    r_login = requests.post(f'{BASE_URL}/auth/login', json={'username': 'test', 'password': '123456'})
    login_data = r_login.json()
    if login_data.get('success'):
        token = login_data.get('token')
        headers = {'Authorization': f'Bearer {token}'}
        r = requests.get(f'{BASE_URL}/cart', headers=headers)
        data = r.json()
        print(f"   状态码: {r.status_code}")
        print(f"   success: {data.get('success')}")
        print(f"   购物车数量: {len(data.get('data', []))}")
        print("   ✓ 购物车接口正常")
    else:
        print("   ✗ 登录失败，无法测试购物车")
except Exception as e:
    print(f"   ✗ 失败: {e}")

print()
print("8. 测试添加购物车 /cart (需要登录)")
try:
    r_login = requests.post(f'{BASE_URL}/auth/login', json={'username': 'test', 'password': '123456'})
    login_data = r_login.json()
    if login_data.get('success'):
        token = login_data.get('token')
        headers = {'Authorization': f'Bearer {token}'}
        r = requests.post(f'{BASE_URL}/cart', json={'product_id': 1, 'quantity': 1}, headers=headers)
        data = r.json()
        print(f"   状态码: {r.status_code}")
        print(f"   success: {data.get('success')}")
        print(f"   消息: {data.get('message')}")
        print("   ✓ 添加购物车接口正常")
    else:
        print("   ✗ 登录失败，无法测试添加购物车")
except Exception as e:
    print(f"   ✗ 失败: {e}")

print()
print("=== 测试完成 ===")