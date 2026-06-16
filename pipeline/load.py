import pandas as pd
import logging

logger=logging.getLogger(__name__)

def load(data,engine,case):
    try:   
        for name,df in data.items():
            try:
                df.to_sql(name=name,
                        con=engine,
                        if_exists=case,
                        index=False
                        ,chunksize=500)
                logger.info(f'the {name} table is loaded with {len(df)} rows')
            except Exception as e:
                logger.error(f'there was an error loading {e}')
                raise
        logger.info('the staged data is loaded')
    except Exception as e:
        logger.error(f'there was an error:{e}')
        raise