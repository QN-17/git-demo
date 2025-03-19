import requests
import pprint
import csv

url = 'https://hljcg.hlj.gov.cn/proxy/trade-service/mall/search/searchByParamFromEs'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}
json_data = {
    "queryPage": {"platformId": 20, "pageSize": 28, "pageNum": 1},
    "orderType": "desc",
    "homeType": 10,
    "isAggregation": "true",
    "publishType": "1",
    "cid": 1001171,
    "businessType": "1",
    "isThirdCategory": "false",
    "cids": []
}

response = requests.post(url=url, json=json_data, headers=headers)  # 使用正确的参数名 `json`
json_data = response.json()
pprint.pprint(json_data)  # 保留一个打印语句即可
result_list = json_data['data']['itemList']['resultList']
print(result_list)
for result in result_list:
    print(result)
    skuName = result['skuName']
    maxPrice = result['maxPrice']
    pictreUrl = result['pictureUrl']

    print(skuName,maxPrice,pictreUrl)
    with open('商品数据.csv',mode='a',encoding='utf-8',newline='')as f:
        csv_write=csv.writer(f)
        csv_write.writerow([skuName,maxPrice,pictreUrl])