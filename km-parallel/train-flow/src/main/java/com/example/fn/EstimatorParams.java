package com.example.fn;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.io.Serializable;

@JsonIgnoreProperties(ignoreUnknown = true)
public class EstimatorParams implements Serializable {
    @JsonProperty("n_clusters")
    private int nClusters = 8;

    @JsonProperty("init")
    private String init = "k-means++";

    @JsonProperty("n_init")
    private int nInit = 10;

    @JsonProperty("max_iter")
    private int maxIter = 300;

    @JsonProperty("tol")
    private double tol = 1e-4;

    @JsonProperty("precompute_distances")
    private String precomputeDistances = "auto";

    @JsonProperty("verbose")
    private int verbose = 0;

    @JsonProperty("random_state")
    private Integer randomState = null;

    @JsonProperty("copy_x")
    private boolean copyX = true;

    @JsonProperty("n_jobs")
    private int nJobs = 1;

    @JsonProperty("algorithm")
    private String algorithm = "auto";

    @JsonProperty("n_clusters")
    public int getnClusters() {
        return nClusters;
    }

    @JsonProperty("n_clusters")
    public void setnClusters(int nClusters) {
        this.nClusters = nClusters;
    }

    @JsonProperty("init")
    public String getInit() {
        return init;
    }

    @JsonProperty("init")
    public void setInit(String init) {
        this.init = init;
    }

    @JsonProperty("n_init")
    public int getnInit() {
        return nInit;
    }

    @JsonProperty("n_init")
    public void setnInit(int nInit) {
        this.nInit = nInit;
    }

    @JsonProperty("max_iter")
    public int getMaxIter() {
        return maxIter;
    }

    @JsonProperty("max_iter")
    public void setMaxIter(int maxIter) {
        this.maxIter = maxIter;
    }

    @JsonProperty("tol")
    public double getTol() {
        return tol;
    }

    @JsonProperty("tol")
    public void setTol(double tol) {
        this.tol = tol;
    }

    @JsonProperty("precompute_distances")
    public String getPrecomputeDistances() {
        return precomputeDistances;
    }

    @JsonProperty("precompute_distances")
    public void setPrecomputeDistances(String precomputeDistances) {
        this.precomputeDistances = precomputeDistances;
    }

    @JsonProperty("verbose")
    public int getVerbose() {
        return verbose;
    }

    @JsonProperty("verbose")
    public void setVerbose(int verbose) {
        this.verbose = verbose;
    }

    @JsonProperty("random_state")
    public Integer getRandomState() {
        return randomState;
    }

    @JsonProperty("random_state")
    public void setRandomState(Integer randomState) {
        this.randomState = randomState;
    }

    @JsonProperty("copy_x")
    public boolean isCopyX() {
        return copyX;
    }

    @JsonProperty("copy_x")
    public void setCopyX(boolean copyX) {
        this.copyX = copyX;
    }

    @JsonProperty("n_jobs")
    public int getnJobs() {
        return nJobs;
    }

    @JsonProperty("n_jobs")
    public void setnJobs(int nJobs) {
        this.nJobs = nJobs;
    }

    @JsonProperty("algorithm")
    public String getAlgorithm() {
        return algorithm;
    }

    @JsonProperty("algorithm")
    public void setAlgorithm(String algorithm) {
        this.algorithm = algorithm;
    }
}
