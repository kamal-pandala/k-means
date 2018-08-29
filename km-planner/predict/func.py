import fdk
import json
import sys
import uuid
import asyncio
import logging
from helper import *


def get_logger(ctx):
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stderr)
    call_id = ctx.CallID()
    formatter = logging.Formatter(
        '[call: {0}] - '.format(call_id) +
        '%(asctime)s - '
        '%(name)s - '
        '%(levelname)s - '
        '%(message)s'
    )
    ch.setFormatter(formatter)
    root.addHandler(ch)
    return root


async def planner(body, logger):
    storage_client = StorageClient(body.get('endpoint'), body.get('port'), body.get('access_key'),
                                   body.get('secret_key'), body.get('secure'), body.get('region'))
    predict_data_object = DataObject(body.get('data_bucket_name'), body.get('data_object_name'),
                                     body.get('data_object_prefix_name'), body.get('data_file_delimiter'))

    unique_id = uuid.uuid4()
    output_object = OutputObject(body.get('output_bucket_name'),
                                 output_object_prefix_name=str(unique_id))

    model_object = ModelObject(body.get('model_object_bucket_name'), body.get('model_object_prefix_name'),
                               body.get('model_object_name'))

    lb_endpoint = body.get('lb_planner_endpoint')
    estimator_client = EstimatorClient(lb_endpoint, '8081', False)

    output_object = estimator_client.predict(storage_client, predict_data_object, model_object, output_object, 0)

    return output_object


async def handler(ctx, data=None, loop=None):
    if data and len(data) > 0:
        logger = get_logger(ctx)
        body = json.loads(data)

        logger.info('Resuming loop in handler!!!')
        if loop is None:
            loop = asyncio.get_event_loop()
            logger.info('Created new loop in handler!!!')

        output_object = await asyncio.ensure_future(planner(body, logger), loop=loop)
        logger.info('Loop completed in handler!!!')

    return json.dumps(output_object.__dict__)



if __name__ == "__main__":
    fdk.handle(handler)

