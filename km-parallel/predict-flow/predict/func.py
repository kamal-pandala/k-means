import fdk
import os
import json
import numpy as np
import pandas as pd
from predict_helper import *
from sklearn.externals import joblib


def handler(ctx, data=None, loop=None):
    if data and len(data) > 0:
        logger = get_logger(ctx)
        body = json.loads(data)

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

        # Parameters for the input prediction dataset
        data_bucket_name = body.get('data_bucket_name')
        data_object_name = body.get('data_object_name')
        data_object_prefix_name = body.get('data_object_prefix_name')
        if data_object_prefix_name is not None:
            data_object_name = data_object_prefix_name + '/' + data_object_name
        data_file_delimiter = body.get('data_file_delimiter')

        # Parameters for the input model file
        model_object_bucket_name = body.get('model_object_bucket_name')
        model_object_prefix_name = body.get('model_object_prefix_name')
        model_object_name = body.get('model_object_name')
        model_object_name = model_object_prefix_name + '/' + model_object_name

        # Parameters for the output prediction file
        output_bucket_name = body.get('output_bucket_name')
        output_object_prefix_name = body.get('output_object_prefix_name')
        output_object_name = output_object_prefix_name + '/' + 'predictions.csv'
        output_file_delimiter = body.get("output_file_delimiter")

        # Establishing connection to remote storage
        minio_client = minio_init_client(endpoint, access_key=access_key, secret_key=secret_key,
                                         secure=secure, region=region)

        # Creating directories in function's local storage
        # Downloading input prediction dataset from remote storage
        if not os.path.exists('/tmp'):
            os.mkdir('/tmp')

        if not os.path.exists('/tmp/data'):
            os.mkdir('/tmp/data')
            minio_get_object(minio_client, data_bucket_name, data_object_name, '/tmp/data/test_data.csv', logger)
            logger.info('Downloaded file!')
        else:
            if not os.path.exists('/tmp/data/test_data.csv'):
                minio_get_object(minio_client, data_bucket_name, data_object_name, '/tmp/data/test_data.csv', logger)
                logger.info('Downloaded file!')

        # TODO - Delete folders as well
        # Cleaning up any existing model files and directories
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

        # Downloading the model file
        minio_get_object(minio_client, model_object_bucket_name, model_object_name, '/tmp/model/model.pkl', logger)
        logger.info('Downloaded model!')

        # Cleaning up any existing output files and directories
        if not os.path.exists('/tmp/output'):
            os.mkdir('/tmp/output')
        else:
            for the_file in os.listdir('/tmp/output'):
                file_path = os.path.join('/tmp/output', the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    logger.info('Unable to delete files in the output directory!')

        # Loading the input prediction dataset into memory
        test_data = pd.read_csv('/tmp/data/test_data.csv', sep=data_file_delimiter, header=None)
        test_X = np.array(test_data)
        logger.info('Loaded data!')

        # Loading the model into memory
        km = joblib.load('/tmp/model/model.pkl')

        # Predicting and persisting the predictions locally
        predictions = km.predict(test_X)
        np.savetxt('/tmp/output/predictions.csv', predictions, delimiter=output_file_delimiter)
        logger.info('Finished predictions!')

        # Uploading the prediction file into remote storage
        minio_put_object(minio_client, output_bucket_name, output_object_name, '/tmp/output/predictions.csv', logger)
        logger.info('Uploaded file to bucket: {0} with object name: {1}!'
                    .format(output_bucket_name, output_object_name))

        return {"message": "Completed successfully!!!"}
    else:
        return {"message": "Data not sent!"}



if __name__ == "__main__":
    fdk.handle(handler)

