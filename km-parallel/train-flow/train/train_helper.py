import sys
import logging
from minio import Minio
from minio.error import ResponseError


def minio_init_client(endpoint, access_key=None, secret_key=None, secure=True,
                      region=None, http_client=None):
    client = Minio(endpoint, access_key, secret_key, secure, region, http_client)
    return client


def minio_get_object(client, bucketname, objectname, filepath, logger):
    try:
        client.fget_object(bucketname, objectname, filepath)
    except ResponseError as err:
        logger.info(err)


def minio_put_object(client, bucketname, objectname, filepath, logger):
    try:
        client.fput_object(bucketname, objectname, filepath)
    except ResponseError as err:
        logger.info(err)


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


def convert_to_int(value):
    try:
        converted_value = int(value)
        return converted_value
    except ValueError:
        return None


def convert_to_float(value):
    try:
        converted_value = float(value)
        return converted_value
    except ValueError:
        return None


def param_type_conversion(estimator_params, param_name):
    if estimator_params[param_name] is not None:
        param_value = convert_to_int(estimator_params[param_name])
        if param_value is not None:
            estimator_params[param_name] = param_value
        else:
            param_value = convert_to_float(estimator_params[param_name])
            if param_value is not None:
                estimator_params[param_name] = param_value
    return estimator_params
