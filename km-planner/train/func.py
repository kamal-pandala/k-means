import fdk
import json
import sys
import uuid
import asyncio
import requests
import logging
import concurrent.futures
from helper import *
from functools import partial
from minio import Minio
from minio.error import ResponseError


def minio_init_client(endpoint, access_key=None, secret_key=None, secure=True,
                      region=None, http_client=None):
    client = Minio(endpoint, access_key, secret_key, secure, region, http_client)
    return client


def minio_count_objects(client, bucketname, prefixname, logger):
    try:
        objects = client.list_objects_v2(bucketname, prefix=prefixname, recursive=True)
        count = sum(1 for _ in objects)
        return count
    except ResponseError as err:
        logger.info(err)
        return 0


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


async def planner_1(body, logger):
    estimator_params = body.get('estimator_params')
    n_trials = estimator_params['n_init']
    logger.info('No. of required trials: ' + str(n_trials))

    storage_client = StorageClient(body.get('endpoint'), body.get('port'), body.get('access_key'),
                                   body.get('secret_key'), body.get('secure'), body.get('region'))
    train_data_object = DataObject(body.get('data_bucket_name'), body.get('data_object_name'))

    unique_id = uuid.uuid4()
    model_object = ModelObject(body.get('model_object_bucket_name'),
                               model_object_prefix_name=str(unique_id))

    lb_endpoint = body.get('lb_planner_endpoint')
    lb_response = requests.get('http://' + lb_endpoint + ':8081/1/lb/nodes')
    n_nodes = len(lb_response.json().get('nodes'))
    n_trials_per_node = n_trials // n_nodes
    n_r_trials = n_trials % n_nodes

    logger.info('No. of trials per node: ' + str(n_trials_per_node))
    logger.info('No. of remainder trials: ' + str(n_r_trials))

    fit_async = []
    for i in range(n_nodes):
        if n_r_trials > 0:
            n = n_trials_per_node + 1
            n_r_trials -= 1
        else:
            n = n_trials_per_node

        estimator_params['n_init'] = n
        rfc = KMeans(**estimator_params)
        estimator_client = EstimatorClient(lb_endpoint, '8081', False)

        fit_async.append(partial(estimator_client.fit, rfc, storage_client, train_data_object, model_object))
    logger.info('Initialised fit_async objects!!!')

    with concurrent.futures.ThreadPoolExecutor(max_workers=n_nodes) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor,
                fit_async[i],
                i
            )
            for i in range(n_nodes)
        ]
        model_list = []
        for model in await asyncio.gather(*futures):
            model_list.append(model)
        if all(model is not None for model in model_list):
            return model_object
        else:
            pass


async def planner_2(body, model_object, logger):
    logger.info('Inside planner_2!!!')

    storage_client = StorageClient(body.get('endpoint'), body.get('port'), body.get('access_key'),
                                   body.get('secret_key'), body.get('secure'), body.get('region'))

    payload_dict = {**storage_client.__dict__, **model_object.__dict__}

    lb_endpoint = body.get('lb_planner_endpoint')
    endpoint_url = 'http://' + lb_endpoint + ':8081' + '/r/km-parallel/train-flow/global-aggregate'
    response = requests.post(endpoint_url, json=payload_dict)
    logger.info(response.text)

    model_object.set_model_object_prefix_name(model_object.model_object_prefix_name + '/final')
    model_object.set_model_object_name('final_model.pkl')

    return model_object


async def handler(ctx, data=None, loop=None):
    if data and len(data) > 0:
        logger = get_logger(ctx)
        body = json.loads(data)

        logger.info('Resuming loop in handler!!!')
        if loop is None:
            loop = asyncio.get_event_loop()
            logger.info('Created new loop in handler!!!')

        model_object = await asyncio.ensure_future(planner_1(body, logger), loop=loop)
        model_object = await asyncio.ensure_future(planner_2(body, model_object, logger), loop=loop)
        logger.info('Loop completed in handler!!!')

    return json.dumps(model_object.__dict__)



if __name__ == "__main__":
    fdk.handle(handler)

