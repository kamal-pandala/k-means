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
    private static final int FUNCTION_LIMIT = 32;
    private static final int N_CORES_PER_FUNCTION = 1;

    public void handleRequest(TrainParams trainParams) {
        System.out.println("Within the handle request method!");
        log.debug("Within the handle request method!");

        // Setting unique prefix for uploading model files
        String modelObjectNamePrefix = UUID.randomUUID().toString();
        trainParams.setModelObjectNamePrefix(modelObjectNamePrefix);

        // Configuring no. of required functions and trees per function
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

        // Creating clones of input params with fn_num as ID
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

        currentFlow().allOf(trainParamsList.toArray(new FlowFuture[nFunctionsRequired]))
                .whenComplete((v, throwable) -> {
                    if (throwable != null) {
                        log.error("Failed!");
                    } else {
                        log.info("Success!");

                        AggregateParams aggregateParams = new AggregateParams();
                        aggregateParams.setEndpoint(trainParams.getEndpoint());
                        aggregateParams.setAccessKey(trainParams.getAccessKey());
                        aggregateParams.setSecretKey(trainParams.getSecretKey());
                        aggregateParams.setSecure(trainParams.getSecure());
                        aggregateParams.setRegion(trainParams.getRegion());
                        aggregateParams.setModelBucketName(trainParams.getModelBucketName());
                        aggregateParams.setModelObjectNamePrefix(modelObjectNamePrefix);

                        currentFlow().invokeFunction("km-parallel/train-flow/aggregate",
                                aggregateParams);
                    }
                });

    }

}