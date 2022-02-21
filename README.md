# Shopper-Scraper
Scraping script for product information on Shopper

# To run:

To be able to run this script, first you need to place 2 files inside the "python" folder:
    - database.ini
    - bearer.py
    OBS: those files were not places on GitHub because they carry password and authentication codes.
    
# 1- Run the DB application
docker run --name database_postgres -e POSTGRES_PASSWORD=sample_pwd -p 5430:5432 -d postgres

# 2- Build the image for the scraper application
docker build -t shopper_scraper .

# 3- Run the scrapper application
docker run --name shopper_scraper --net=host -i --rm  shopper_scraper 

