
# NVIDIA Maxine Eye Contact NIM Client

This package has a sample client which demonstrates interaction with a Maxine Eye Contact NIM

## Getting Started

NVIDIA Maxine NIM Client packages use gRPC APIs. Instructions below demonstrate usage of Eye contact NIM using Python gRPC client.
To experience the NVIDIA Maxine Eye Contact NIM API without having to host your own servers, use the [Try API](https://build.nvidia.com/nvidia/eyecontact/api) feature, which uses the NVIDIA Cloud Function backend.

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

### 3. Compile the Protos (optional)

If you want to use the client code provided in the github Client repository, you can skip this step.
The proto files are available in the eye-contact/protos folder. You can compile them to generate client interfaces in your preferred programming language. For more details, refer to [Supported languages](https://grpc.io/docs/languages/) in the gRPC documentation.

Here is an example of how to compile the protos for Python on Linux and Windows.

#### Python

The `grpcio` version needed for compilation can be referred at `requirements.txt`

To compile protos on Linux, run:
```bash
# Go to eye-contact/protos/linux folder
cd eye-contact/protos/linux/

chmod +x compile_protos.sh
./compile_protos.sh
```

To compile protos on Windows, run:
```bash
# Go to eye-contact/protos/windows folder
cd eye-contact/protos/windows/

./compile_protos.bat
```
The compiled proto files will be generated in `nim-clients/eye-contact/interfaces` directory.

### 4. Host the NIM Server

Before running client part of Maxine Eye Contact, please set up a server.
The simplest way to do that is to follow the [quick start guide](https://docs.nvidia.com/nim/maxine/eye-contact/latest/index.html)
This step can be skipped when using [Try API](https://build.nvidia.com/nvidia/eyecontact/api).

### 5. Run the Python Client

- Go to the scripts directory

```bash
    cd scripts
```

#### Usage for Hosted NIM request

```bash
python eye-contact.py \
  --target <server_ip:port> \
  --input <input_file_path> \
  --output <output_file_path_and_name> \
  --ssl-mode <ssl_mode_value> \
  --ssl-key <ssl_key_file_path> \
  --ssl-cert <ssl_cert_filepath> \
  --ssl-root-cert <ssl_root_cert_filepath>
 ```

- Example command to process the packaged sample video

The following command uses the sample video file & generates an ouput.mp4 file in the current folder

```bash
    python eye-contact.py --target 127.0.0.1:8001 --input ../assets/sample_input.mp4 --output output.mp4
```

- Note the supported file type is mp4

#### Usage for Preview API request

```bash
    python eye-contact.py --preview-mode \
    --target grpc.nvcf.nvidia.com:443 \
    --function-id 15c6f1a0-3843-4cde-b5bc-803a4966fbb6 \
    --api-key $API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC \
    --input <input file path> \
    --output <output file path and the file name>
```

#### Command line arguments

-  `-h, --help` show this help message and exit
-  `--preview-mode` Flag to send request to preview NVCF NIM server on https://build.nvidia.com/nvidia/eyecontact/api.
-  `--ssl-mode` {DISABLED,MTLS,TLS} Flag to set SSL mode, default is DISABLED
-  `--ssl-key SSL_KEY`  The path to ssl private key.
-  `--ssl-cert SSL_CERT`    The path to ssl certificate chain.
-  `--ssl-root-cert`    The path to ssl root certificate.
-  `--target`   IP:port of gRPC service, when hosted locally. Use grpc.nvcf.nvidia.com:443 when hosted on NVCF.
-  `--input`    The path to the input video file.
-  `--output`   The path for the output video file.
-  `--api-key`  NGC API key required for authentication, utilized when using TRY API ignored otherwise
-  `--function-id`  NVCF function ID for the service, utilized when using TRY API ignored otherwise

Note when using SSL mode the default path for the credentials is `../ssl_key/<filename>.pem`

Refer the [docs](https://docs.nvidia.com/nim/maxine/eye-contact/latest/basic-inference.html) for more information
