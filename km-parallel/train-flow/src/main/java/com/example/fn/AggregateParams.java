package com.example.fn;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.io.Serializable;

@JsonIgnoreProperties(ignoreUnknown = true)
public class AggregateParams implements Serializable {
    @JsonProperty("node_number")
    private String nodeNumber;

    @JsonProperty("endpoint")
    private String endpoint;

    @JsonProperty("port")
    private int port = 0;

    @JsonProperty("access_key")
    private String accessKey;

    @JsonProperty("secret_key")
    private String secretKey;

    @JsonProperty("secure")
    private Boolean secure = true;

    @JsonProperty("region")
    private String region;

    @JsonProperty("model_object_bucket_name")
    private String modelObjectBucketName;

    @JsonProperty("model_object_prefix_name")
    private String modelObjectPrefixName;

    @JsonProperty("node_number")
    public String getNodeNumber() {
        return nodeNumber;
    }

    @JsonProperty("node_number")
    public void setNodeNumber(String nodeNumber) {
        this.nodeNumber = nodeNumber;
    }

    @JsonProperty("endpoint")
    public String getEndpoint() {
        return endpoint;
    }

    @JsonProperty("endpoint")
    public void setEndpoint(String endpoint) {
        this.endpoint = endpoint;
    }

    @JsonProperty("port")
    public int getPort() {
        return port;
    }

    @JsonProperty("port")
    public void setPort(int port) {
        this.port = port;
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
}
