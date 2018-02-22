# ck-request-asplos18-iot-farm
CK workflow for ReQuEST ASPLOS'18 submission:

## Artifact check-list

## Installation

### Install global prerequisites


### Install Collective Knowledge
```# pip install ck ```

### Install this CK repository with all dependencies (other CK repos to reuse artifacts)
```ck pull repo --url=https://github.com/ctuning/ck-request-asplos18-iot-farm```

### Detect and test CUDA driver (only on NVidia-based platform)
```$ ck detect platform.gpgpu --cuda ```
