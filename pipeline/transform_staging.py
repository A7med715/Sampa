import pandas as pd
import numpy as np
import logging

logger=logging.getLogger(__name__)

def staging(data):
    try:
        for df in data.values():
            df.columns=df.columns.str.strip()
            df.columns=df.columns.str.lower()
            df.columns = df.columns.str.replace(' ', '_')
            for column in df.columns:
                if df[column].dtype == 'object':
                    df[column] = df[column].str.strip()
        logger.info("The data is staged")
        return data
    except Exception as e:
        logger.error(f"there was an error in staging data:{e}")
        raise
    