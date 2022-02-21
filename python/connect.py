from datetime import date,datetime
from sqlalchemy import MetaData,Column,Table, Integer, Float,String,Date,DateTime
from sqlalchemy import create_engine
from configparser import ConfigParser

class DBConnector:
    def __init__(self):
        #   Dictionary that maps python types to SQL types
        self.DATA_MAP = {    str: String,
                            int:Integer,
                            datetime:DateTime,
                            date:Date,
                            float: Float
                        }
        #   Creates engine used to acess DB
        self.db_engine = create_engine(self.db_config_url(), echo = True)

    #   Loads file with DB information and saves in a dict
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


    #   Using dictionary with DB info, creates url for connection
    def db_config_url(self):

        params = self.config()
        config_url = f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['database']}"
        
        return config_url
        