package com.example.fn;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.io.Serializable;

@JsonIgnoreProperties(ignoreUnknown = true)
public class TrainResponse implements Serializable {
    @JsonProperty("train_success")
    private Boolean trainSucess;

    @JsonProperty("model_object_bucket_name")
    private String modelObjectBucketName;

    @JsonProperty("model_object_prefix_name")
    private String modelObjectPrefixName;

    @JsonProperty("model_object_name")
    private String modelObjectName;

    @JsonProperty("train_success")
    public Boolean getTrainSucess() {
        return trainSucess;
    }

    @JsonProperty("train_success")
    public void setTrainSucess(Boolean trainSucess) {
        this.trainSucess = trainSucess;
    }

    @JsonProperty("model_object_bucket_name")
    public String getModelObjectBucketName() {
        return modelObjectBucketName;
    }

    @JsonProperty("model_object_bucket_name")
    public void setModelObjectBucketName(String modelObjectBucketName) {
        this.modelObjectBucketName = modelObjectBucketName;
    }

    @JsonProperty("model_object_prefix_name")
    public String getModelObjectPrefixName() {
        return modelObjectPrefixName;
    }

    @JsonProperty("model_object_prefix_name")
    public void setModelObjectPrefixName(String modelObjectPrefixName) {
        this.modelObjectPrefixName = modelObjectPrefixName;
    }

    @JsonProperty("model_object_name")
    public String getModelObjectName() {
        return modelObjectName;
    }

    @JsonProperty("model_object_name")
    public void setModelObjectName(String modelObjectName) {
        this.modelObjectName = modelObjectName;
    }
}
