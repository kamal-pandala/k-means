import requests


class StorageClient:
    def __init__(self, endpoint, port, access_key, secret_key, secure=True, region=None):
        self.endpoint = endpoint
        self.port = port
        self.access_key = access_key
        self.secret_key = secret_key
        self.secure = secure
        self.region = region


class DataObject:
    def __init__(self, data_bucket_name, data_object_name, data_object_prefix_name=None, data_file_delimiter=','):
        self.data_bucket_name = data_bucket_name
        self.data_object_name = data_object_name
        self.data_object_prefix_name = data_object_prefix_name
        self.data_file_delimiter = data_file_delimiter


class ModelObject:
    def __init__(self, model_object_bucket_name, model_object_prefix_name=None, model_object_name=None):
        self.model_object_bucket_name = model_object_bucket_name
        self.model_object_prefix_name = model_object_prefix_name
        self.model_object_name = model_object_name

    def set_model_object_prefix_name(self, model_object_prefix_name):
        self.model_object_prefix_name = model_object_prefix_name

    def set_model_object_name(self, model_object_name):
        self.model_object_name = model_object_name


class OutputObject:
    def __init__(self, output_bucket_name, output_object_name=None, output_object_prefix_name=None,
                 output_file_delimiter=',', output_attributes=None):
        self.output_bucket_name = output_bucket_name
        self.output_object_name = output_object_name
        self.output_object_prefix_name = output_object_prefix_name
        self.output_file_delimiter = output_file_delimiter
        self.output_attributes = output_attributes

    def set_output_object_prefix_name(self, output_object_prefix_name):
        self.output_object_prefix_name = output_object_prefix_name

    def set_output_object_name(self, output_object_name):
        self.output_object_name = output_object_name

    def set_output_file_delimiter(self, output_file_delimiter):
        self.output_file_delimiter = output_file_delimiter

    def set_output_attributes(self, output_attributes):
        self.output_attributes = output_attributes


class RandomForestClassifier:
    def __init__(self, name='RandomForestClassifier', n_estimators=10, criterion="gini", max_depth=None, min_samples_split=2,
                 min_samples_leaf=1, min_weight_fraction_leaf=0., max_features="auto",
                 max_leaf_nodes=None, min_impurity_decrease=0., min_impurity_split=None,
                 bootstrap=True, oob_score=False, n_jobs=1, random_state=None,
                 verbose=0, warm_start=False, class_weight=None):
        self.name = name
        self.n_estimators = n_estimators
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.min_weight_fraction_leaf = min_weight_fraction_leaf
        self.max_features = max_features
        self.max_leaf_nodes = max_leaf_nodes
        self.min_impurity_decrease = min_impurity_decrease
        self.min_impurity_split = min_impurity_split
        self.bootstrap = bootstrap
        self.oob_score = oob_score
        self.n_jobs = n_jobs
        self.random_state = random_state
        self.verbose = verbose
        self.warm_start = warm_start
        self.class_weight = class_weight


class KMeans:
    def __init__(self, n_clusters, name='KMeans', init='k-means++', precompute_distances='auto',
                 n_init=10, max_iter=300, verbose=0, tol=1e-4,
                 random_state=None, copy_x=True, n_jobs=1, algorithm="auto"):
        self.n_clusters = n_clusters
        self.name = name
        self.init = init
        self.precompute_distances = precompute_distances
        self.n_init = n_init
        self.max_iter = max_iter
        self.verbose = verbose
        self.tol = tol
        self.random_state = random_state
        self.copy_x = copy_x
        self.n_jobs = n_jobs
        self.algorithm = algorithm


class EstimatorClient:
    def __init__(self, endpoint, port, secure=False):
        self.endpoint = endpoint
        self.port = port
        if secure:
            self.protocol = 'https'
        else:
            self.protocol = 'http'

    def fit(self, estimator, storage_client, train_data_object, model_object, node_number, **kwargs):
        payload_dict = {**storage_client.__dict__, **train_data_object.__dict__, **model_object.__dict__,
                        'estimator_params': estimator.__dict__, 'node_number': node_number, **kwargs}

        endpoint_url = self.protocol + '://' + self.endpoint + ':' + self.port + '/r/km-parallel/train-flow'
        response = requests.post(endpoint_url, json=payload_dict)

        body = response.json()
        model_object.set_model_object_prefix_name(body.get('model_object_prefix_name'))
        model_object.set_model_object_name(body.get('model_object_name'))

        return model_object

    def predict(self, storage_client, predict_data_object, model_object, output_object, node_number, **kwargs):
        payload_dict = {**storage_client.__dict__, **predict_data_object.__dict__, **model_object.__dict__,
                        **output_object.__dict__, 'node_number': node_number, **kwargs}

        endpoint_url = self.protocol + '://' + self.endpoint + ':' + self.port + '/r/km-parallel/predict-flow'
        response = requests.post(endpoint_url, json=payload_dict)

        body = response.json()
        output_object.set_output_object_prefix_name(body.get('output_object_prefix_name'))
        output_object.set_output_object_name(body.get('output_object_name'))
        output_object.set_output_file_delimiter(body.get('output_file_delimiter'))

        return output_object
