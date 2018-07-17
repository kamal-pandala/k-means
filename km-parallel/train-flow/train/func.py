import fdk
import os
import json
import numpy as np
import pandas as pd
from train_helper import *
from sklearn.externals import joblib
from sklearn.cluster import KMeans


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

        # Parameters for the input training dataset
        data_bucket_name = body.get('data_bucket_name')
        data_object_name = body.get('data_object_name')
        data_object_prefix_name = body.get('data_object_prefix_name')
        if data_object_prefix_name is not None:
            data_object_name = data_object_prefix_name + '/' + data_object_name
        data_file_delimiter = body.get('data_file_delimiter')

        # Parameters for the output model file
        fn_num = body.get('fn_num')
        model_object_bucket_name = body.get('model_object_bucket_name')
        model_object_prefix_name = body.get('model_object_prefix_name')
        model_object_name = model_object_prefix_name + '/model_' + str(fn_num) + '.pkl'

        estimator_params = body.get('estimator_params')

        # Establishing connection to remote storage
        minio_client = minio_init_client(endpoint, access_key=access_key, secret_key=secret_key,
                                         secure=secure, region=region)

        # Creating directories in function's local storage
        if not os.path.exists('data'):
            os.mkdir('data')
            # Downloading input training dataset from remote storage
            minio_get_object(minio_client, data_bucket_name, data_object_name, 'data/train_data.csv', logger)
            logger.info('Downloaded file!')
        else:
            # Downloading input training dataset from remote storage
            if not os.path.exists('data/train_data.csv'):
                minio_get_object(minio_client, data_bucket_name, data_object_name, 'data/train_data.csv', logger)
                logger.info('Downloaded file!')

        if not os.path.exists('model'):
            os.mkdir('model')
        else:
            for the_file in os.listdir('model'):
                file_path = os.path.join('model', the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    logger.info('Unable to delete files in the model directory!')

        # Loading the input training dataset into memory
        train_data = np.array(pd.read_csv('data/train_data.csv', sep=data_file_delimiter, header=None))
        logger.info('Loaded file!')

        # Initialisation of the Random Forest algorithm with the estimator_params
        if estimator_params is not None:
            km = KMeans(**estimator_params)
        else:
            km = KMeans()

        # Fitting the model to the input training data
        km.fit(train_data)
        logger.info('Finished training!')

        # Persisting the model into function's local storage
        joblib.dump(km, 'model/model.pkl')
        logger.info('Dumped model!')

        # Uploading the model into remote storage
        minio_put_object(minio_client, model_object_bucket_name,  model_object_name, 'model/model.pkl', logger)
        logger.info('Uploaded file to bucket: {0} with object name: {1}!'.format(model_object_bucket_name, model_object_name))

        return {"message": "Completed successfully!!!"}
    else:
        return {"message": "Data not sent!"}



if __name__ == "__main__":
    fdk.handle(handler)

