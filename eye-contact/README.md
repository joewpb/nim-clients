
# NVIDIA Maxine Eye Contact NIM Client

This package has a sample client which demonstrates interaction with a Maxine Eye Contact NIM

## Getting Started

NVIDIA Maxine NIM Client packages use gRPC APIs. Instructions below demonstrate usage of Eye contact NIM using Python gRPC client.

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

### 4. Run the Python Client

- Go to the scripts directory

```bash
    cd scripts
```

- Usage

```bash
    python eye-contact.py --target <server_ip:port> --input <input file path> --output <output file path and the file name>
 ```

- Example command to process the packaged sample video


```bash
    // The following command uses the sample video file & generates an ouput.mp4 file in the current folder

    python eye-contact.py --target 127.0.0.1:8004 --input ../assets/sample_input.mp4 --output output.mp4
 ```

- Note the supported file type is mp4

#### Command line arguments

- `--target`- server IP with hosted container, default value is `127.0.0.1:8004`
- `--input`- input file to apply effect, default value is `../assets/sample_input.mp4`
- `--output`- output file name and path, default is current directory (scripts) with name output.mp4

Refer the [docs](https://docs.nvidia.com/nim/maxine/eye-contact/latest/index.html) for more information
