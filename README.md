# Collective Knowledge workflow for image classification submitted to [ReQuEST at ASPLOS'18](http://cknowledge.org/request-cfp-asplos2018.html)

Linux/MacOS: [![Travis Build Status](https://travis-ci.org/ctuning/ck-request-asplos18-iot-farm.svg?branch=master)](https://travis-ci.org/ctuning/ck-request-asplos18-iot-farm)

* **Title:** Real-Time Image Recognition Using Collaborative IoT Devices
* **Authors:** Ramyad Hadidi, Jiashen Cao, Matthew Woodward, Michael S. Ryoo, Hyesoon Kim

## Artifact check-list (meta-information)

We use the standard [Artifact Description check-list](http://ctuning.org/ae/submission_extra.html) from systems conferences including CGO, PPoPP, PACT and SuperComputing.

* **Algorithm:** image classification
* **Program:** written scripts in Keras framework
* **Compilation:** Python 2.7+ (Python 3.x is not yet supported)
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

### Install global prerequisites (Ubuntu and similar)

```
$ sudo apt-get install libhdf5-dev
$ sudo apt-get install cython
$ sudo apt-get install python-h5py
$ sudo apt-get install python-pip
$ pip install matplotlib
$ pip install h5py
```

### Minimal CK installation

The minimal installation requires:

* Python 2.7 or 3.3+ (limitation is mainly due to unitests)
* Git command line client.

You can install CK in your local user space as follows:

```
$ git clone http://github.com/ctuning/ck
$ export PATH=$PWD/ck/bin:$PATH
$ export PYTHONPATH=$PWD/ck:$PYTHONPATH
```

You can also install CK via PIP with sudo to avoid setting up environment variables yourself:

```
$ sudo pip install ck
```

### Install this CK repository with all dependencies (other CK repos to reuse artifacts)
```$ ck pull repo:ck-request-asplos18-iot-farm```

### Install or detect TensorFlow via CK

We tested this workflow with TF 1.5. 

You can try to detect and use already installed TF on your machine as follows:
```
$ ck detect soft --tags=lib,tensorflow
```

Alternatively, you can install pre-built CPU version via CK as follows
(please select Python 2 if several Python installations are automatically detected by CK):
```
$ ck install package --tags=lib,tensorflow,v1.5.0,vcpu,vprebuilt
```
If you plan to use NVIDIA GPU, you can install CUDA version instead:
```
$ ck install package --tags=lib,tensorflow,v1.5.0,vcuda,vprebuilt
```

If you want to build TF from sources, you can install it different versions as follows
(you may need to limit the number of used processors on platforms with limited memory):
```
$ ck install package --tags=lib,tensorflow,v1.5.0,vsrc --env.CK_HOST_CPU_NUMBER_OF_PROCESSORS=1
```

Finally, you can install all available TF packages via CK as follows:

```
$ ck install package --tags=lib,tensorflow
```

Now you can install Keras via CK with all sub-dependencies for this workflow:
```
$ ck install package:lib-keras-2.1.3-request
```

## Benchmarking on a single device (CPU)

* AlexNet:
```
$ ck run program:request-iot-benchmark --cmd_key=benchmark-alexnet-single-device-cpu 
```

* VGG16:
```
$ ck run program:request-iot-benchmark --cmd_key=benchmark-vgg16-single-device-cpu
```
## Benchmarking on a single device (GPU)

First test that CUDA-powered GPU is detected by CK:

```$ ck detect platform.gpgpu --cuda```

* AlexNet:
```
$ ck run program:request-iot-benchmark --cmd_key=benchmark-alexnet-single-device-gpu 
```

* VGG16:
```
$ ck run program:request-iot-benchmark --cmd_key=benchmark-vgg16-single-device-gpu
```

## Benchmarking on a farm of machines (AlexNet)

First you need to describe configuration of your farm via CK. 

For example, for 5 device configuration for AlexNet,
prepare JSON file with any name such as '''farm-5.json''' 
describing all IP addresses of your nodes:

```
{
    "node":
    {
        "initial": [
            "192.168.1.8"
        ],
        "block1": [
            "192.168.1.3"
        ],
        "block2": [
            "192.168.1.4", "192.168.1.5"
        ],
        "block3": [
            "192.168.1.6"
        ]
    }
}
```

Note that IP of "initial" node is the one where you will run benchmarking.

Now you must register this configuration in the CK with some name such as "farm-5" as follows:
```
$ ck add machine:farm-5 --access_type=avro --avro_config=farm-5.json
```

Select linux-32 or linux-64 depending on your nodes. 
You can view all registered configurations of target platforms as follows:
```
$ ck show machine
```

Now must log in to all your nodes and perform all above installation steps
to install Python, CK, TensorFlow and Keras. Then you can start servers
on all nodes (apart from "initial") as follows:

```
$ ck run program:request-iot-benchmark --cmd_key=benchmark-alexnet-farm-5-nodes-start-server --target=farm-5 
```
Now you can run benchmark for distributed inference as follows:
```
$ ck run program:request-iot-benchmark --cmd_key=benchmark-alexnet-farm-5-nodes --target=farm-5 --env.STAT_REPEAT=5
```

You can change the number of repetitions using STAT_REPEAT environment variable.

## Benchmarking on a farm of machines (VGG16, 9 nodes)

For VGG16 with 9 nodes, create ''farm-9.json'' and register farm-9 machine:
```
{
    "node":
    {
        "initial": [
            "192.168.1.8"
        ],
        "block1": [
            "192.168.1.3"
        ],
        "block234": [
            "192.168.1.4", "192.168.1.5", "192.168.1.6"
        ],
        "block5": [
            "192.168.1.7"
        ],
        "fc1": [
            "192.168.1.9", "192.168.1.10"
        ],
        "fc2": [
            "192.168.1.11"
        ]
    }
}
```

```
$ ck add machine:farm-9 --access_type=avro --avro_config=farm-9.json
```

Now start server on all nodes as follows:
```
$ ck run program:request-iot-benchmark --cmd_key=benchmark-vgg16-farm-9-nodes-start-server --target=farm-9 
```
Now you can run benchmark for distributed inference as follows:
```
$ ck run program:request-iot-benchmark --cmd_key=benchmark-vgg16-farm-9-nodes --target=farm-9 --env.STAT_REPEAT=5
```

## Benchmarking on a farm of machines (VGG16, 11 nodes)

For VGG16 with 11 nodes, create ''farm-11.json'' and register farm-11 machine:
```
{
    "node":
    {
        "initial": [
            "192.168.1.8"
        ],
        "block12345": [
            "192.168.1.3","192.168.1.4","192.168.1.5","192.168.1.6","192.168.1.7","192.168.1.9","192.168.1.10"
        ],
        "fc1": [
            "192.168.1.11", "192.168.1.13"
        ],
        "fc2": [
            "192.168.1.12"
        ]
    }
}
```

```
$ ck add machine:farm-11 --access_type=avro --avro_config=farm-11.json
```

Now start server on all nodes as follows:
```
$ ck run program:request-iot-benchmark --cmd_key=benchmark-vgg16-farm-11-nodes-start-server --target=farm-11 
```
Now you can run benchmark for distributed inference as follows:
```
$ ck run program:request-iot-benchmark --cmd_key=benchmark-vgg16-farm-11-nodes --target=farm-11 --env.STAT_REPEAT=5
```

## Scripts for unified benchmarking for ReQuEST scoreboard

You can now perform unified benchmarking and collect statistics in the CK format using scripts in the following CK entry:
```
$ cd `ck find script:benchmark-request-iot-farm`
```

If you plan to benchmark workflow on your host machine (CPU,GPU) while you already added targets for distributed inference, 
you must also add a "host" target to the CK as follows:
```
$ ck add machine:host --use_host
```

You can now benchmark inference on your host as follows:
```
$ python benchmarking.py --cmd_key=benchmark-alexnet-single-device-cpu
$ python benchmarking.py --cmd_key=benchmark-alexnet-single-device-gpu
$ python benchmarking.py --cmd_key=benchmark-vgg16-single-device-cpu
$ python benchmarking.py --cmd_key=benchmark-vgg16-single-device-gpu
```

You can also benchmark distributed inference using target machines farm-5, farm-9 and farm-11:
(you must start servers on each node as described in previous section)
```
$ python benchmarking.py --cmd_key=benchmark-alexnet-farm-5-nodes --target=farm-5
$ python benchmarking.py --cmd_key=benchmark-vgg16-farm-9-nodes --target=farm-9
$ python benchmarking.py --cmd_key=benchmark-vgg16-farm-11-nodes --target=farm-11
```

CK will record experimental data in a unified format in the following entries:
```
$ ck ls local:experiment:ck-request-asplos18-iot-farm*
```

You can pack them and send "ckr-local.zip" to ReQuEST organizers as follows:
```
$ ck zip local:experiment:ck-request-asplos18-iot-farm*
```
