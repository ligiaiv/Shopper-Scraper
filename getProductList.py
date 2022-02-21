import requests, sys
from pprint import pprint
from bearer import auth

get_product_headers = {
    'authority': 'siteapi.shopper.com.br',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'dnt': '1',
    'sec-ch-ua-mobile': '?0',
    'x-store-id': '1',
    'authorization': auth['auth'],
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'sec-ch-ua-platform': '"Linux"',
    'origin': 'https://programada.shopper.com.br',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://programada.shopper.com.br/shop-cn/alimentos/arroz-feijao-e-graos/',
    'accept-language': 'pt-BR,pt;q=0.9',
    # 'if-none-match': 'W/"2f35-C/VFEGSt0JMDnyrgkZiWEKxjG24"',
}

def getProductList(department,subdepartment,max_products = 200):

    params = (
        ('department', '22'),
        ('subdepartment', '11'),
        ('page', '1'),
        ('size', '200'),
    )

    response = requests.get('https://siteapi.shopper.com.br/catalog/products', headers=get_product_headers, params=params)
    products = response.json()
    pprint(products)
    print(len(products['products']))
    return products
# Note: original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
#response = requests.get('https://siteapi.shopper.com.br/catalog/products?department=22&subdepartment=11&page=1&size=20&', headers=headers)

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Not enough parameters.")
        exit()
    department,subdepartment = sys.argv[1:]
    getProductList(department,subdepartment)