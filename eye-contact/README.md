
# NVIDIA Maxine Eye Contact NIM Client

This package has a sample client which demonstrates interaction with a Maxine Eye Contact NIM

## Getting Started

NVIDIA Maxine NIM Client packages use gRPC APIs. Instructions below demonstrate usage of Eye contact NIM using Python gRPC client.
Additionally, access the [Try API](https://build.nvidia.com/nvidia/eyecontact/api) feature to experience the NVIDIA Maxine Eye Contact NIM API without hosting your own servers, as it leverages the NVIDIA Cloud Function backend.

## Pre-requisites

- Ensure you have Python 3.10 or above installed on your system.
Please refer to the [Python documentation](https://www.python.org/downloads/) for download and installation instructions.
- Access to NVIDIA Maxine Eye Contact NIM Container / Service

## Usage guide

### 1. Clone the repository

```bash
git clone https://github.com/nvidia-maxine/nim-clients.git

// Go to the 'eye-contact' folder
cd nim-clients/eye-contact
```

### 2. Install dependencies

```bash
sudo apt-get install python3-pip
pip install -r requirements.txt
```

### 3. Host the NIM Server

Before running client part of Maxine Eye Contact, please set up a server.
The simplest way to do that is to follow the [quick start guide](https://docs.nvidia.com/nim/maxine/eye-contact/latest/index.html)
This step can be skipped when using [Try API](https://build.nvidia.com/nvidia/eyecontact/api).

### 4. Run the Python Client

- Go to the scripts directory

```bash
    cd scripts
```

#### Usage for Hosted NIM request

```bash
    python eye-contact.py --target <server_ip:port> --input <input file path> --output <output file path and the file name>
 ```

- Example command to process the packaged sample video

The following command uses the sample video file & generates an ouput.mp4 file in the current folder

```bash
    python eye-contact.py --target 127.0.0.1:8004 --input ../assets/sample_input.mp4 --output output.mp4
 ```

- Note the supported file type is mp4

#### Usage for Preview API request

```bash
    python eye-contact.py --use-ssl \
    --target grpc.nvcf.nvidia.com:443 \
    --function-id 15c6f1a0-3843-4cde-b5bc-803a4966fbb6 \
    --api-key $API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC \
    --input <input file path> \
    --output <output file path and the file name>
```

#### Command line arguments

- `--use-ssl`       - Flag to control if SSL/TLS encryption should be used. When running preview SSL must be used.
- `--target`        - <IP:port> of gRPC service, when hosted locally. Use grpc.nvcf.nvidia.com:443 when hosted on NVCF.
- `--api-key`       - NGC API key required for authentication, utilized when using `TRY API` ignored otherwise
- `--function-id`   - NVCF function ID for the service, utilized when using `TRY API` ignored otherwise
- `--input`         - The path to the input video file. Default value is `../assets/sample_input.mp4`
- `--output`        - The path for the output video file. Default is current directory (scripts) with name `output.mp4`


Refer the [docs](https://docs.nvidia.com/nim/maxine/eye-contact/latest/index.html) for more information
