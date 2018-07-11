package com.example.fn;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.io.Serializable;

@JsonIgnoreProperties(ignoreUnknown = true)
public class AggregateParams implements Serializable {
    @JsonProperty("endpoint")
    private String endpoint;

    @JsonProperty("access_key")
    private String accessKey;

    @JsonProperty("secret_key")
    private String secretKey;

    @JsonProperty("secure")
    private Boolean secure = true;

    @JsonProperty("region")
    private String region;

    @JsonProperty("model_bucket_name")
    private String modelBucketName;

    @JsonProperty("model_object_name_prefix")
    private String modelObjectNamePrefix;

    @JsonProperty("endpoint")
    public String getEndpoint() {
        return endpoint;
    }

    @JsonProperty("endpoint")
    public void setEndpoint(String endpoint) {
        this.endpoint = endpoint;
    }

    @JsonProperty("access_key")
    public String getAccessKey() {
        return accessKey;
    }

    @JsonProperty("access_key")
    public void setAccessKey(String accessKey) {
        this.accessKey = accessKey;
    }

    @JsonProperty("secret_key")
    public String getSecretKey() {
        return secretKey;
    }

    @JsonProperty("secret_key")
    public void setSecretKey(String secretKey) {
        this.secretKey = secretKey;
    }

    @JsonProperty("secure")
    public Boolean getSecure() {
        return secure;
    }

    @JsonProperty("secure")
    public void setSecure(Boolean secure) {
        this.secure = secure;
    }

    @JsonProperty("region")
    public String getRegion() {
        return region;
    }

    @JsonProperty("region")
    public void setRegion(String region) {
        this.region = region;
    }

    @JsonProperty("model_bucket_name")
    public String getModelBucketName() {
        return modelBucketName;
    }

    @JsonProperty("model_bucket_name")
    public void setModelBucketName(String modelBucketName) {
        this.modelBucketName = modelBucketName;
    }

    @JsonProperty("model_object_name_prefix")
    public String getModelObjectNamePrefix() {
        return modelObjectNamePrefix;
    }

    @JsonProperty("model_object_name_prefix")
    public void setModelObjectNamePrefix(String modelObjectNamePrefix) {
        this.modelObjectNamePrefix = modelObjectNamePrefix;
    }
}
