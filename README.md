# Collective Knowledge workflow for image classification submitted to [ReQuEST at ASPLOS'18](http://cknowledge.org/request-cfp-asplos2018.html)

* **Title:** Real-Time Image Recognition Using Collaborative IoT Devices
* **Authors:** Ramyad Hadidi, Jiashen Cao, Matthew Woodward, Michael S. Ryoo, Hyesoon Kim

## Artifact check-list (meta-information)

We use the standard [Artifact Description check-list](http://ctuning.org/ae/submission_extra.html) from systems conferences including CGO, PPoPP, PACT and SuperComputing.

* **Algorithm:** image classification
* **Program:** written scripts in Keras framework
* **Compilation:** Python >= 2.7
* **Transformations:**
* **Binary:** will be compiled on a target platform
* **Data set:** ImageNet 2012 validation (50,000 images)
* **Run-time environment:** Ubuntu 16.04 ; Python version >= 2.7; Keras >= 2.1.3 with Tensorflow-gpu >= 1.5 for the backend; (for Raspberry PI systems) Apache Avro >= 1.8.2; (for TX2 GPU) CUDA 8.0 with cuDNN >= 5.1.
* **Hardware:** Nvidia Jetson TX2 ; up to 11 Raspberry PI 3 with 16GB SD cards; power analyzer;Wifi router (we use 300Mbps, 2.4 GHz 802.11n).
* **Run-time state:** 
* **Execution:**
* **Metrics:** Inference per second; static and dynamic energy consumption.
* **Output:** Scripts output end-to-end latency. User measures power consumption during idle state and inference operations
* **Experiments:** CK command line
* **How much disk space required (approximately)?** 
* **How much time is needed to prepare workflow (approximately)?** 
* **How much time is needed to complete experiments (approximately)?**
* **Collective Knowledge workflow framework used?** Yes
* **Publicly available?:** Yes
* **Experimental results:** https://github.com/ctuning/ck-request-asplos18-results-iot-farm
* **Scoreboard:** http://cKnowledge.org/request-results

## Installation

### Install global prerequisites


### Install Collective Knowledge
```# pip install ck ```

### Install this CK repository with all dependencies (other CK repos to reuse artifacts)
```ck pull repo --url=https://github.com/ctuning/ck-request-asplos18-iot-farm```

### Detect and test CUDA driver (only on NVidia-based platform)
```$ ck detect platform.gpgpu --cuda ```
