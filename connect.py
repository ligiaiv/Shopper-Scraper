from datetime import date,datetime
from sqlalchemy import MetaData,Column,Table, Integer, Float,String,Date,DateTime
from sqlalchemy import create_engine
from configparser import ConfigParser

class DBConnector:
    def __init__(self):

        self.DATA_MAP = {    str: String,
                        int:Integer,
                        datetime:DateTime,
                        date:Date,
                        float: Float
                        }
        self.db_engine = create_engine(self.db_config_url(), echo = True)

    def config(self,filename='database.ini', section='postgresql'):
        parser = ConfigParser()
        parser.read(filename)

        db = {}
        
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        self.db_config = db
        return db


    def db_config_url(self):

        params = self.config()
        config_url = f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['database']}"
        
        return config_url
        
    def commit(self,meta):

        meta.create_all(self.db_engine)


    def create_tables(self,column_names, column_types):

        column_types = list(map(self.DATA_MAP.get,column_types))
        
        meta = MetaData()

        columns = [Column(col_name,col_type) for col_name,col_type in zip(column_names,column_types) ]
        this_table = Table(
                'items', meta, 
                Column('id', Integer, primary_key = True), *columns)

        self.commit(meta)

    # if __name__ == '__main__':
    #     create_tables()
