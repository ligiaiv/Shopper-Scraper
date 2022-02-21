from datetime import datetime
import pandas as pd
from connect import DBConnector
import getProductList as getProductList
from tableSpecs import tableProducts
import sqlalchemy


def getMerchant(item):
    return [merch['name'] for merch in item.get('merchant',[])]

#
#   Scraps data from Shoppers 
#
def run_script():

    print("Scraping website...")
    products = getProductList.getProductList(22,11)["products"]

    print("Setting connector to DB...")
    connector = DBConnector()

    print("Organising the data...")

    #
    #   Creates Dataframe with same format as DB and populates with data from product
    #   Information received in dictionary format from products variable
    dfProduct = pd.DataFrame({c: pd.Series(dtype=t) for c, t in tableProducts.items()})

    for item in products:

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

    print("Saving Data do DB...")
    try:
        #   Using connector, applies dataframe to DB
        dfProduct.to_sql("products", con=connector.db_engine, if_exists='append')
    except sqlalchemy.exc.OperationalError as err:
        print(err)
        print("Check if you DB is operating correctly at port 5430.")
    print("Done!")

#
#   Interacts with user and runs main script
#
if __name__ == '__main__':

    while True:
        print("What would you like to do? \n (1) Scrap Shoppers\n (2) Quit\n")
        response = input("Choice:")
        if response == '1':
            run_script()
        elif response == '2':
            quit()
        else:
            print("Please choose a valid option")
            continue
