package com.example.fn;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.io.Serializable;

@JsonIgnoreProperties(ignoreUnknown = true)
public class PredictResponse implements Serializable {
    @JsonProperty("predict_success")
    private Boolean predictSucess;

    @JsonProperty("output_bucket_name")
    private String outputBucketName;

    @JsonProperty("output_object_prefix_name")
    private String outputObjectPrefixName;

    @JsonProperty("output_object_name")
    private String outputObjectName;

    @JsonProperty("output_file_delimiter")
    private String outputFileDelimiter;

    @JsonProperty("predict_success")
    public Boolean getPredictSucess() {
        return predictSucess;
    }

    @JsonProperty("predict_success")
    public void setPredictSucess(Boolean predictSucess) {
        this.predictSucess = predictSucess;
    }

    @JsonProperty("output_bucket_name")
    public String getOutputBucketName() {
        return outputBucketName;
    }

    @JsonProperty("output_bucket_name")
    public void setOutputBucketName(String outputBucketName) {
        this.outputBucketName = outputBucketName;
    }

    @JsonProperty("output_object_prefix_name")
    public String getOutputObjectPrefixName() {
        return outputObjectPrefixName;
    }

    @JsonProperty("output_object_prefix_name")
    public void setOutputObjectPrefixName(String outputObjectPrefixName) {
        this.outputObjectPrefixName = outputObjectPrefixName;
    }

    @JsonProperty("output_object_name")
    public String getOutputObjectName() {
        return outputObjectName;
    }

    @JsonProperty("output_object_name")
    public void setOutputObjectName(String outputObjectName) {
        this.outputObjectName = outputObjectName;
    }

    @JsonProperty("output_file_delimiter")
    public String getOutputFileDelimiter() {
        return outputFileDelimiter;
    }

    @JsonProperty("output_file_delimiter")
    public void setOutputFileDelimiter(String outputFileDelimiter) {
        this.outputFileDelimiter = outputFileDelimiter;
    }
}
