import os 
import logging
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


logger=logging.getLogger(__name__)

def extract_all():
    path=os.getenv('DATA_PATH')
    data={}
    for file in os.listdir(path):
        name=''
        try:
            try:
                name=file.split('olist_')[1].split('_dataset')[0]
            except:
                name=file.split('.csv')[0]
            data[name]=pd.read_csv(path+r'\\'+file)
            logger.info(f'{name} table is loaded with {len(data[name])} rows')
        except Exception as e:
            logger.error(f'can not load {name} table due to an error{e}')
    
    return data

