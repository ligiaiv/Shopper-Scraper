from datetime import datetime
import requests
# from bs4 import BeautifulSoup as bs
import pandas as pd
from connect import DBConnector
import getProduct,getProductList
from tableSpecs import tableProducts


def getMerchant(item):
    return [merch['name'] for merch in item.get('merchant',[])]


headers = {
    'authority': 'programada.shopper.com.br',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'pt-BR,pt;q=0.9',
    'cookie': 'popup_news=1; msg-cep-invalido=1; _ga=GA1.3.509024539.1645174743; _gid=GA1.3.773678562.1645174743; _fbp=fb.2.1645174743611.398038812; __zlcmid=18bkiQBip9QS6V2; csrftoken=5sY98H8rr0wtVavEN4qhGK73KTLyTd7uvdvwk57iXCODndX0pqk9ZJgohdPrjHzL; sessionid=h1kg6bwwouoe85foyttjufbexnavicfj; _pin_unauth=dWlkPU5qTmpPVFV5TWpVdE9HUTNOQzAwWm1NNUxUZzVNek10TURNelpXSXdNamM0TmpVMw; _pin_unauth=dWlkPU5qTmpPVFV5TWpVdE9HUTNOQzAwWm1NNUxUZzVNek10TURNelpXSXdNamM0TmpVMw; _hjSession_218777=eyJpZCI6ImU0MDk0YjFlLTU2ODAtNGU5Mi05NmQ3LWUzMGJmODIwYWUwZSIsImNyZWF0ZWQiOjE2NDUxNzYwOTQ5ODcsImluU2FtcGxlIjp0cnVlfQ==; _hjSessionUser_218777=eyJpZCI6IjE4OWVmM2E4LWJmODYtNTg0ZS1hNTQ4LTU5MGMyZDU4YTY5NCIsImNyZWF0ZWQiOjE2NDUxNzYwOTQ5NzAsImV4aXN0aW5nIjp0cnVlfQ==; shopper_session_info="eyJuYW1lIjogIkxcdTAwZWRnaWEifQ=="; shopper_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXN0b21lcklkIjo3OTA4MjQsImRldmljZVVVSUQiOiI2MjA0OTEyYy01MmI5LTRhZWMtYWQ3ZC03YWFkMDczMTMwMjEiLCJpYXQiOjE2NDUxNjU5MzZ9.1n0TXlb2-2ZKIcdrRDZtGJMSJ1hbmA3ZMzzoPDEg3XI; shopper_stores=[{%22name%22:%22mensal%22%2C%22number%22:1%2C%22subdomain%22:%22programada%22}]; shopper_current_store={%22name%22:%22mensal%22%2C%22number%22:1%2C%22subdomain%22:%22programada%22}; _gat=1; AWSALBTG=5SIxmNOXZQCJLl+FP30BnqztfOF2HP9YU745hyqi3qcL/1HnRlvnz/pB462GZPwm/vNmWYmRK/hRpGn1nIe/xLevv/TtCYcQBXKdQzSYcYBXZi5a733SoowCGZQUE3dccPw8ugjMbIrM66rwbBLc6EP/ngxm9CltXpGkqQWqOw2rB/mrrjk=; AWSALBTGCORS=5SIxmNOXZQCJLl+FP30BnqztfOF2HP9YU745hyqi3qcL/1HnRlvnz/pB462GZPwm/vNmWYmRK/hRpGn1nIe/xLevv/TtCYcQBXKdQzSYcYBXZi5a733SoowCGZQUE3dccPw8ugjMbIrM66rwbBLc6EP/ngxm9CltXpGkqQWqOw2rB/mrrjk=; outbrain_cid_fetch=true',
}

cookies = {
    'popup_news':'1',
    ' msg-cep-invalido':'1',
    ' _ga':'GA1.3.509024539.1645174743',
    ' _gid':'GA1.3.773678562.1645174743',
    ' _fbp':'fb.2.1645174743611.398038812',
    ' __zlcmid':'18bkiQBip9QS6V2',
    ' csrftoken':'5sY98H8rr0wtVavEN4qhGK73KTLyTd7uvdvwk57iXCODndX0pqk9ZJgohdPrjHzL',
    ' sessionid':'h1kg6bwwouoe85foyttjufbexnavicfj',
    ' _pin_unauth':'dWlkPU5qTmpPVFV5TWpVdE9HUTNOQzAwWm1NNUxUZzVNek10TURNelpXSXdNamM0TmpVMw',
    ' _pin_unauth':'dWlkPU5qTmpPVFV5TWpVdE9HUTNOQzAwWm1NNUxUZzVNek10TURNelpXSXdNamM0TmpVMw',
    ' _hjSession_218777':'eyJpZCI6ImU0MDk0YjFlLTU2ODAtNGU5Mi05NmQ3LWUzMGJmODIwYWUwZSIsImNyZWF0ZWQiOjE2NDUxNzYwOTQ5ODcsImluU2FtcGxlIjp0cnVlfQ==',
    ' _hjSessionUser_218777':'eyJpZCI6IjE4OWVmM2E4LWJmODYtNTg0ZS1hNTQ4LTU5MGMyZDU4YTY5NCIsImNyZWF0ZWQiOjE2NDUxNzYwOTQ5NzAsImV4aXN0aW5nIjp0cnVlfQ==',
    ' shopper_session_info':'"eyJuYW1lIjogIkxcdTAwZWRnaWEifQ=="',
    ' shopper_token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXN0b21lcklkIjo3OTA4MjQsImRldmljZVVVSUQiOiI2MjA0OTEyYy01MmI5LTRhZWMtYWQ3ZC03YWFkMDczMTMwMjEiLCJpYXQiOjE2NDUxNjU5MzZ9.1n0TXlb2-2ZKIcdrRDZtGJMSJ1hbmA3ZMzzoPDEg3XI',
    ' shopper_stores':'[{%22name%22:%22mensal%22%2C%22number%22:1%2C%22subdomain%22:%22programada%22}]',
    ' shopper_current_store':'{%22name%22:%22mensal%22%2C%22number%22:1%2C%22subdomain%22:%22programada%22}',
    ' _gat':'1',
    ' AWSALBTG':'5SIxmNOXZQCJLl+FP30BnqztfOF2HP9YU745hyqi3qcL/1HnRlvnz/pB462GZPwm/vNmWYmRK/hRpGn1nIe/xLevv/TtCYcQBXKdQzSYcYBXZi5a733SoowCGZQUE3dccPw8ugjMbIrM66rwbBLc6EP/ngxm9CltXpGkqQWqOw2rB/mrrjk=',
    ' AWSALBTGCORS':'5SIxmNOXZQCJLl+FP30BnqztfOF2HP9YU745hyqi3qcL/1HnRlvnz/pB462GZPwm/vNmWYmRK/hRpGn1nIe/xLevv/TtCYcQBXKdQzSYcYBXZi5a733SoowCGZQUE3dccPw8ugjMbIrM66rwbBLc6EP/ngxm9CltXpGkqQWqOw2rB/mrrjk=',
    ' outbrain_cid_fetch':'true',
}
response = requests.get('https://programada.shopper.com.br/shop-cn/alimentos/', headers=headers,cookies=cookies)
print(response.text)

products = getProductList.getProductList(22,11)["products"]
connector = DBConnector()

dfProduct = pd.DataFrame({c: pd.Series(dtype=t) for c, t in tableProducts.items()})
# pd.DataFrame(columns=list(tableProducts.keys()),dtype=[str,str,str)

for item in products:
    print(item)
    # item_info = getProduct()
    item_dict = {
            'name': item['name'],
            'sku': item['id'],
            'department': item['metadata']['department_url'],
            'category': item['metadata']['subdepartment_url'],
            'url': '/'.join(['https://programada.shopper.com.br/shop-cn',item['metadata']['department_url'],item['metadata']['subdepartment_url'],item['url']]),
            'image': item['image'],
            'price_to': float(item['price'].replace('R$','').replace(',','.')),
            'discount': item['savingPercentage'],
            'store': getMerchant(item),
            'created_at': datetime.timestamp(datetime.today()),
            'hour': datetime.timestamp(datetime.now())
    }
    dfProduct = dfProduct.append(item_dict, ignore_index=True)

print(dfProduct)
print(dfProduct.to_sql("products", con=connector.db_engine, if_exists='append'))





