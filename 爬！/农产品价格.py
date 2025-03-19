import requests
import csv

# 目标URL和请求头
url = "https://ncpscxx.moa.gov.cn/product/homeWholesalePrice/selectWholesalePrice"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}

# 查询字符串参数（根据开发者工具中的载荷构建）
payload = {
    "startTime": "20241217",        # 起始时间
    "endTime": "20250317",          # 结束时间
    "productId": "AE01001,AE01005,AE01006,AE01019,AE02002",  # 产品ID
    "productClass1Code": "AE",      # 一级分类
    "productClass2Code": "AE01",    # 二级分类
    "marketName": "",               # 市场名称（留空）
    "province": "",                 # 省份（留空）
    "timetype": "r"                 # 时间类型
}

# 发送POST请求（忽略SSL验证）
response = requests.post(
    url=url,
    data=payload,                   # 使用表单数据传递参数
    headers=headers,
    verify=False                    # 忽略SSL证书验证
)

# 解析JSON响应
json_data = response.json()
data = json_data['data']

# 提取关键字段
products = data['codes']    # 产品列表，如 ["大白菜", "生菜", ...]
dates = data['names']       # 日期列表，如 ["2024年12月17日", ...]
prices = data['values']     # 价格二维数组，每个子列表对应一个产品的每日价格

# 写入CSV文件
with open('价格数据.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['产品名称', '日期', '价格'])  # 表头
    
    # 遍历每个产品和对应的价格列表
    for product, price_list in zip(products, prices):
        # 遍历每个日期和对应的价格
        for date, price in zip(dates, price_list):
            writer.writerow([product, date, price])

print("数据已保存到 价格数据.csv")