package com.example.fn;

import com.fnproject.fn.api.flow.FlowFuture;

import static com.fnproject.fn.api.flow.Flows.currentFlow;

public class PredictFlow {

    public PredictResponse handleRequest(PredictParams predictParams) {

        FlowFuture<PredictResponse> predictFuture = currentFlow().invokeFunction("km-parallel/predict-flow/predict", predictParams)
                .thenCompose((v) -> {
                    // TODO - Failure logic

                    PredictResponse predictResponse = new PredictResponse();
                    predictResponse.setPredictSucess(true);
                    predictResponse.setOutputBucketName(predictParams.getOutputBucketName());
                    predictResponse.setOutputObjectPrefixName(predictParams.getOutputObjectPrefixName());
                    predictResponse.setOutputObjectName("predictions.csv");
                    predictResponse.setOutputFileDelimiter(predictParams.getOutputFileDelimiter());

                    return currentFlow().completedValue(predictResponse);
                });

        return predictFuture.get();
    }

}