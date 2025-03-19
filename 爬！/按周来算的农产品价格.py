import requests
import csv

# 目标URL（已移除查询参数）
url = "https://ncpscxx.moa.gov.cn/product/homeWholesalePrice/selectWholesalePrice"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}

# 查询参数（全部通过POST表单传递）
payload = {
    "startTime": "201701",        # 2017年第1周
    "endTime": "202511",          # 2025年第11周
    "productId": "AE01001,AE01005,AE01006,AE01019,AE02002",
    "productClass1Code": "AE",
    "productClass2Code": "AE01",
    "marketName": "",
    "province": "",
    "timetype": "w"               # 周数据模式
}

# 发送POST请求
response = requests.post(
    url=url,
    data=payload,                # 使用表单数据传递参数
    headers=headers,
    verify=False                 # 忽略SSL验证
)

# 解析响应
json_data = response.json()
data = json_data['data']

# 提取数据
products = data['codes']    # ["大白菜", "生菜", ...]
dates = data['names']       # ["2017年1周", "2017年2周", ...]
prices = data['values']     # 二维价格数组

# 写入CSV（带长度校验）
with open('周价格数据.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['产品名称', '周次', '价格(元)'])  # 优化表头
    
    # 遍历每个产品
    for product_idx, product in enumerate(products):
        # 获取对应产品的价格列表
        price_list = prices[product_idx]
        
        # 确保日期与价格数量一致
        total_weeks = min(len(dates), len(price_list))
        
        # 写入每周数据
        for week_idx in range(total_weeks):
            writer.writerow([ 
                product,
                dates[week_idx],
                price_list[week_idx]
            ])

print(f"成功保存 {len(products)} 个产品共 {total_weeks} 周数据到 周价格数据.csv")