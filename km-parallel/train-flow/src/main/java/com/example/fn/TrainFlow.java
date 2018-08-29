package com.example.fn;

import java.util.UUID;
import java.util.ArrayList;

import com.fnproject.fn.api.flow.FlowFuture;
import com.fnproject.fn.api.flow.HttpResponse;
import static com.fnproject.fn.api.flow.Flows.currentFlow;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class TrainFlow {

    static {
        System.setProperty("org.slf4j.simpleLogger.defaultLogLevel", "debug");
    }

    private static final Logger log = LoggerFactory.getLogger(TrainFlow.class);
    private static final int FUNCTION_LIMIT = 12;
    private static final int N_CORES_PER_FUNCTION = 1;

    public TrainResponse handleRequest(TrainParams trainParams) {

        // Setting unique prefix for the local name for data
        String dataLocalName = UUID.randomUUID().toString();
        trainParams.setDataLocalName(dataLocalName);

        // Configuring number of required functions and jobs per function
        int nIterationsRequired = trainParams.getEstimatorParams().getnInit();
        int nIterationsPerFunction = 1;
        int nFunctionsRequired = nIterationsRequired;
        int nRemainderIterations = 0;
        if (nIterationsRequired > FUNCTION_LIMIT) {
            nIterationsPerFunction = nIterationsRequired / FUNCTION_LIMIT;
            nFunctionsRequired = FUNCTION_LIMIT;
            nRemainderIterations = nIterationsRequired % FUNCTION_LIMIT;
        }

        // Setting no. of cores per function
        trainParams.getEstimatorParams().setnJobs(N_CORES_PER_FUNCTION);

        // Invoking training jobs and storing references to their futures
        ArrayList<FlowFuture<HttpResponse>> trainParamsList = new ArrayList<>();
        for(int i = 0; i < nFunctionsRequired; i++) {
            trainParams.setFnNum(i);
            if (nRemainderIterations > 0) {
                trainParams.getEstimatorParams().setnInit(nIterationsPerFunction + 1);
                nRemainderIterations--;
            } else {
                trainParams.getEstimatorParams().setnInit(nIterationsPerFunction);
            }

            trainParamsList.add(currentFlow().invokeFunction("km-parallel/train-flow/train",
                    trainParams));
        }

        FlowFuture<HttpResponse> aggregateFlow = currentFlow().allOf(trainParamsList.toArray(new FlowFuture[nFunctionsRequired]))
                .thenCompose((v) -> {
                    // TODO - Failure logic

                    AggregateParams aggregateParams = new AggregateParams();
                    aggregateParams.setNodeNumber(trainParams.getNodeNumber());
                    aggregateParams.setEndpoint(trainParams.getEndpoint());
                    aggregateParams.setPort(trainParams.getPort());
                    aggregateParams.setAccessKey(trainParams.getAccessKey());
                    aggregateParams.setSecretKey(trainParams.getSecretKey());
                    aggregateParams.setSecure(trainParams.getSecure());
                    aggregateParams.setRegion(trainParams.getRegion());
                    aggregateParams.setModelObjectBucketName(trainParams.getModelObjectBucketName());
                    aggregateParams.setModelObjectPrefixName(trainParams.getModelObjectPrefixName());

                    return currentFlow().invokeFunction("km-parallel/train-flow/local-aggregate",
                            aggregateParams);
                });

        FlowFuture<TrainResponse> trainFuture = aggregateFlow.thenCompose((v) -> {
            // TODO - Failure logic

            TrainResponse trainResponse = new TrainResponse();
            trainResponse.setTrainSucess(true);
            trainResponse.setModelObjectBucketName(trainParams.getModelObjectBucketName());
            trainResponse.setModelObjectPrefixName(trainParams.getModelObjectPrefixName());

            return currentFlow().completedValue(trainResponse);
        });

        return trainFuture.get();
    }

}