import logging
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine,text


load_dotenv()
#configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger=logging.getLogger(__name__)


def truncate_schema(engine, tables):
    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

        for table in tables:
            conn.execute(text(f"TRUNCATE TABLE {table}"))

        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))


def _build_url(db_name_var):
    host     = os.getenv('DB_HOST')
    user     = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    db_name  = os.getenv(db_name_var)
    return f"mysql+pymysql://{user}:{password}@{host}/{db_name}"

#create engine
def get_engine_stage():
    try:
        engine=create_engine(_build_url('DB_NAME_STAGE'), echo=False)
        logger.info("The engine is created successfully")
        return engine
    except Exception as e:
        logger.error(f'Erro created at engine {e}')
        raise

def get_engine_core():
    try:
        engine=create_engine(_build_url('DB_NAME_CORE'), echo=False)
        logger.info("The engine is created successfully")
        return engine
    except Exception as e:
        logger.error(f'Erro created at engine {e}')
        raise

def get_engine_mart():
    try:
        engine=create_engine(_build_url('DB_NAME_MART'), echo=False)
        logger.info("The engine is created successfully")
        return engine
    except Exception as e:
        logger.error(f'Erro created at engine {e}')
        raise

