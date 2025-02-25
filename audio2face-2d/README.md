
# NVIDIA Maxine Audio2Face-2D NIM Client

This package has a sample client which demonstrates interaction with a Maxine Audio2Face-2D NIM.

## Getting Started

NVIDIA Maxine NIM Client packages use gRPC APIs. Instructions below demonstrate usage of Audio2Face-2D NIM using Python and NodeJS gRPC clients.

## Pre-requisites

Access to NVIDIA Maxine Audio2Face-2D NIM Container / Service

### Python 
- Ensure you have Python 3.10 or above installed on your system. Please refer to the [Python documentation](https://www.python.org/downloads/) for download and installation instructions.

### NodeJS
- Ensure you have NodeJS 18 or above installed on your system. Please refer to the [NodeJS documentation](https://nodejs.org/en/download/package-manager) for download and installation instructions.

## Usage guide

### 1. Clone the repository

```bash
git clone https://github.com/nvidia-maxine/nim-clients.git

# Go to the 'audio2face-2d' folder
cd nim-clients/audio2face-2d/
```

### 2. Install dependencies
#### Python
```bash
# Install all the required packages using requirements.txt file in python directory  
pip install -r python/requirements.txt
```

#### NodeJS
```bash
# Install all the required packages using package.json file in nodejs directory  
npm install --prefix nodejs/ 
```

### 3. Compile the Protos (optional)

If you want to use the client code provided in the github Client repository, you can skip this step.
The proto files are available in the audio2face-2d/protos folder. You can compile them to generate client interfaces in your preferred programming language. For more details, refer to [Supported languages](https://grpc.io/docs/languages/) in the gRPC documentation.

Here is an example of how to compile the protos for Python and Node.js on Linux and Windows.

#### Python

The `grpcio` version needed for compilation can be referred at `requirements.txt`

To compile protos on Linux, run:
```bash
# Go to audio2face-2d/protos/linux/python folder
cd audio2face-2d/protos/linux/python

chmod +x compile_protos.sh
./compile_protos.sh
```

To compile protos on Windows, run:
```bash
# Go to audio2face-2d/protos/windows/python folder
cd audio2face-2d/protos/windows/python

./compile_protos.bat
```
The compiled proto files will be generated in `nim-clients/audio2face-2d/python/interfaces` directory.

#### NodeJS
Before running the NodeJS client, you can choose to compile the protos. 

To compile protos on Linux, run:
```bash
# Go to audio2face-2d/protos/linux/nodejs folder
cd audio2face-2d/protos/linux/nodejs

chmod +x compile_protos.sh
./compile_protos.sh
```

To compile protos on Windows, run:
```bash
# Go to audio2face-2d/protos/windows/nodejs folder
cd audio2face-2d/protos/windows/nodejs

./compile_protos.bat
```
The compiled proto files will be generated in `nim-clients/audio2face-2d/nodejs/interfaces` directory.

### 4. Host the NIM Server

Before running client part of Maxine Audio2Face-2D, please set up a server.
The simplest way to do that is to follow the [quick start guide](https://docs.nvidia.com/nim/maxine/audio2face-2d/latest/getting-started.html)

### 5. Run the Client
#### Python
- Go to the scripts directory

```bash
cd scripts
```

#### Usage for Hosted NIM request

```bash
python audio2face-2d.py \
  --target <server_ip:port> \
  --audio-input <input_audio_file_path> \
  --portrait-input <input_portrait_image_file_path> \
  --output <output_file_path_and_name> \
  --head-rotation-animation-filepath <rotation_animation_filepath> \
  --head-translation-animation-filepath <translation_animation_filepath> \
  --ssl-mode <ssl_mode_value> \
  --ssl-key <ssl_key_file_path> \
  --ssl-cert <ssl_cert_filepath> \
  --ssl-root-cert <ssl_root_cert_filepath>
```

To view details of command line arguments, run this command:
```bash
python audio2face-2d.py -h
```

- Example command to process the packaged sample inputs

The following command uses the sample audio and portrait file & generates an output.mp4 file in the current folder

```bash
    python audio2face-2d.py --target 127.0.0.1:8001 --audio-input ../assets/sample_audio.wav --portrait-input ../assets/sample_portrait_image.png --output out.mp4 
   ```

#### NodeJS
- Go to the scripts directory

```bash
cd scripts
```

#### Usage for Hosted NIM request

```bash
node audio2face-2d.js \
  --target <server_ip:port> \
  --audio-input <input_audio_file_path> \
  --portrait-input <input_portrait_image_file_path> \
  --output <output_file_path_and_name> \
  --format <wav/pcm> \
  --head-rotation-animation-filepath <rotation_animation_file_path> \
  --head-translation-animation-filepath <translation_animation_file_path> \
  --ssl-mode <ssl_mode_value> \
  --ssl-key <ssl_key_file_path> \
  --ssl-cert <ssl_cert_file_path> \
  --ssl-root-cert <ssl_root_cert_file_path>
 ```

- Example command to process the packaged sample inputs

The following command uses the sample audio and portrait file & generates an output.mp4 file in the current folder

```bash
    node audio2face-2d.js --target 127.0.0.1:8001 --audio-input ../assets/sample_audio.wav --portrait-input ../assets/sample_portrait_image.png --output out.mp4 --format wav
 ```

The NodeJS client supports both `wav` and `pcm` audio formats. The `--format` option can be used to specify the format. The default format is `wav`. 

The default configuration expected for PCM audio format in the NodeJS client is as follows:

- Sample rate: 48kHz
- Channels: Mono-channel
- Bit Depth: 16

If any other config is needed, please change it in the NodeJS client `audio2face-2d/nodejs/scripts/audio2face-2d.js` in the function `sendInputAudioChunks()`.

#### Note 
- The supported audio file format is `wav` or `pcm` and for image is `jpg, png, jpeg`.
- The supported languages are English, Spanish, Mandarin, French, a sample file for English language is provided in assets dir. 

#### Command line arguments

-  `-h, --help` show this help message and exit
- `--target` is `127.0.0.1:8001`
- `--portrait-input` is `../../assets/sample_portrait_image.png`
- `--audio-input` is `../../assets/sample_audio.wav`
- `--output` will be the current directory where the output file will be generated with name `output.mp4`
- `--head-rotation-animation-filepath` is `../../assets/head_rotation_animation.csv`. Used only if head_pose_mode is `HeadPoseMode.HEAD_POSE_MODE_USER_DEFINED_ANIMATION`.
- `--head-translation-animation-filepath` is `../../assets/head_translation_animation.csv`. Used only if head_pose_mode is `HeadPoseMode.HEAD_POSE_MODE_USER_DEFINED_ANIMATION`.
- `--ssl-mode` is DISABLED (no SSL). 
- `--ssl-key` is `../ssl_key/ssl_key_client.pem`. Used only if ssl-mode is `MTLS`. 
- `--ssl-cert` is `../ssl_key/ssl_cert_client.pem`. Used only if ssl-mode is `MTLS`.
- `--ssl-root-cert` is `../ssl_key/ssl_ca_cert.pem`. Used only if ssl-mode is `MTLS` or `TLS`.

Only for Nodejs

- `--format` - The audio format (wav or pcm) 

Refer the [docs](https://docs.nvidia.com/nim/maxine/audio2face-2d/latest/index.html) for more information
