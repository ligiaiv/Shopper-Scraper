docker run --name database_postgres -e POSTGRES_PASSWORD=sample_pwd -p 5430:5432 -d postgres
docker build -t shopper_scraper .
docker run --name shopper_scraper --net=host -i --rm  shopper_scraper 
# If you want to visualize the database with a GUI, you can use Postbird
