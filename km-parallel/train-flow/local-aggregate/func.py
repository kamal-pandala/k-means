import fdk
import os
import json
from aggregate_helper import *
from sklearn.externals import joblib


def handler(ctx, data=None, loop=None):
    if data and len(data) > 0:
        logger = get_logger(ctx)
        body = json.loads(data)

        node_number = body.get('node_number')
        logger.info('Aggregate function on node {0} has started running!'.format(node_number))

        # TODO - validation and exception handling
        # Parameters required for initialising minio client
        endpoint = body.get('endpoint')
        port = body.get('port')
        if port is not None and port != 0:
            endpoint += ':' + str(port)

        access_key = body.get('access_key')
        secret_key = body.get('secret_key')
        secure = body.get('secure')
        region = body.get('region')

        # Parameters for the output model file
        model_object_bucket_name = body.get('model_object_bucket_name')
        model_object_prefix_name = body.get('model_object_prefix_name')
        model_object_name = model_object_prefix_name + '/local/local_model_' + node_number + '.pkl'

        # Establishing connection to remote storage
        minio_client = minio_init_client(endpoint, access_key=access_key, secret_key=secret_key,
                                         secure=secure, region=region)

        # Creating directories in function's local storage
        if not os.path.exists('/tmp'):
            os.mkdir('/tmp')

        if not os.path.exists('/tmp/model'):
            os.mkdir('/tmp/model')
        else:
            for the_file in os.listdir('/tmp/model'):
                file_path = os.path.join('/tmp/model', the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    logger.info('Unable to delete files in the model directory!')

        # Downloading all the model files
        minio_get_all_objects(minio_client, model_object_bucket_name, model_object_prefix_name + '/' + node_number,
                              '/tmp/model', logger)

        # Loading the models into memory and storing them as a dict referenced
        # by their file path with inertia as their values
        intermediate_models_inertias = {}
        for the_file in os.listdir('/tmp/model'):
            file_path = os.path.join('/tmp/model', the_file)
            try:
                if os.path.isfile(file_path):
                    intermediate_model = joblib.load(file_path)
                    intermediate_models_inertias[file_path] = intermediate_model.inertia_
            except Exception as e:
                logger.info('Unable to read files in the output directory!')

        # Finding the model with the least inertia
        final_model_file_path = min(intermediate_models_inertias, key=intermediate_models_inertias.get)

        # TODO cleanup of other model files in remote storage required
        # Uploading the model into remote storage
        minio_put_object(minio_client, model_object_bucket_name,  model_object_name, final_model_file_path, logger)
        logger.info('Uploaded file to bucket: {0} with object name: {1}!'.format(model_object_bucket_name,
                                                                                 model_object_name))

        return {"message": "Completed successfully!!!"}
    else:
        return {"message": "Data not sent!"}



if __name__ == "__main__":
    fdk.handle(handler)

