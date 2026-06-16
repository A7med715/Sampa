from pipeline.extract import extract_all
from pipeline.utils import get_engine_stage
from pipeline.utils import get_engine_core
from pipeline.utils import get_engine_mart
from pipeline.utils import truncate_schema
from pipeline.transform_staging import staging
from pipeline.transform_core import core
from pipeline.transform_mart import mart
from pipeline.load import load
import logging

logger=logging.getLogger(__name__)
def main():
    stage_engine=get_engine_stage()
    core_engine=get_engine_core()
    mart_engine=get_engine_mart()
    try:
        logger.info('the pipeline started')
        data=extract_all()

        data=staging(data)
        truncate_schema(stage_engine,list(data.keys()))
        load(data,stage_engine,'append')

        data=core(data)
        tem=data['dim_date']
        del data['dim_date']
        truncate_schema(core_engine,list(data.keys()))
        load(data,core_engine,'append')

        data['dim_date']=tem
        data=mart(data)
        truncate_schema(mart_engine,list(data.keys()))
        load(data,mart_engine,'append')

    except Exception as e:
        logger.error(f'the pipeline failed:{e}')
        raise

if __name__ == "__main__":
    main()
