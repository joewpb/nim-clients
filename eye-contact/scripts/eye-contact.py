# Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import argparse
import os
import sys
import time
from typing import Iterator

import grpc

sys.path.append(os.path.join(os.getcwd(), "../interfaces"))
# Importing gRPC compiler auto-generated maxine eyecontact library
import eyecontact_pb2  # noqa: E402
import eyecontact_pb2_grpc  # noqa: E402


def parse_args() -> None:
    """
    Parse command-line arguments using argparse.
    """
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Process mp4 video files using gRPC and apply eye-contact."
    )
    parser.add_argument(
        "--preview-mode",
        action="store_true",
        help="Flag to send request to preview NVCF NIM server on "
        "https://build.nvidia.com/nvidia/eyecontact/api. ",
    )
    parser.add_argument(
        "--ssl-mode",
        type=str,
        help="Flag to set SSL mode, default is DISABLED",
        default="DISABLED",
        choices=["DISABLED", "MTLS", "TLS"],
    )
    parser.add_argument(
        "--ssl-key",
        type=str,
        default="../ssl_key/ssl_key_client.pem",
        help="The path to ssl private key.",
    )
    parser.add_argument(
        "--ssl-cert",
        type=str,
        default="../ssl_key/ssl_cert_client.pem",
        help="The path to ssl certificate chain.",
    )
    parser.add_argument(
        "--ssl-root-cert",
        type=str,
        default="../ssl_key/ssl_ca_cert.pem",
        help="The path to ssl root certificate.",
    )
    parser.add_argument(
        "--target",
        type=str,
        default="127.0.0.1:8001",
        help="IP:port of gRPC service, when hosted locally. "
        "Use grpc.nvcf.nvidia.com:443 when hosted on NVCF.",
    )
    parser.add_argument(
        "--input",
        type=str,
        default="../assets/sample_input.mp4",
        help="The path to the input video file.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output.mp4",
        help="The path for the output video file.",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="NGC API key required for authentication, "
        "utilized when using TRY API ignored otherwise",
    )
    parser.add_argument(
        "--function-id",
        type=str,
        help="NVCF function ID for the service, utilized when using TRY API ignored otherwise",
    )
    return parser.parse_args()


def read_file_content(file_path: os.PathLike) -> None:
    """Function to read file content as bytes.

    Args:
      file_path: Path to input file
    """
    with open(file_path, "rb") as file:
        return file.read()


def generate_request_for_inference(
    input_filepath: os.PathLike = "input.mp4", params: dict = {}
) -> any:
    """Generator to produce the request data stream

    Args:
      input_filepath: Path to input file
      params: Parameters for the feature
    """
    DATA_CHUNKS = 64 * 1024  # bytes, we send the mp4 file in 64KB chunks
    if (
        params
    ):  # if params is supplied, the first item in the input stream is config object with parameters
        yield eyecontact_pb2.RedirectGazeRequest(config=eyecontact_pb2.RedirectGazeConfig(**params))
    with open(input_filepath, "rb") as fd:
        while True:
            buffer = fd.read(DATA_CHUNKS)
            if buffer == b"":
                break
            yield eyecontact_pb2.RedirectGazeRequest(video_file_data=buffer)


def write_output_file_from_response(
    response_iter: Iterator[eyecontact_pb2.RedirectGazeResponse],
    output_filepath: os.PathLike = "output.mp4",
) -> None:
    """Function to write the output file from the incoming gRPC data stream.

    Args:
      response_iter: Responses from the server to write into output file
      output_filepath: Path to output file
    """
    print(f"Writing output in {output_filepath}")
    with open(output_filepath, "wb") as fd:
        for response in response_iter:
            if response.HasField("video_file_data"):
                fd.write(response.video_file_data)


def process_request(
    channel: any,
    input_filepath: os.PathLike,
    params: dict,
    output_filepath: os.PathLike,
    request_metadata: dict = None,
) -> None:
    """Function to process gRPC request

    Args:
      channel: gRPC channel for server client communication
      input_filepath: Path to input file
      params: Parameters to control the feature
      output_filepath: Path to output file
      request_metadata: Credentials to process preview request
    """
    try:
        stub = eyecontact_pb2_grpc.MaxineEyeContactServiceStub(channel)
        start_time = time.time()
        responses = stub.RedirectGaze(
            generate_request_for_inference(input_filepath=input_filepath, params=params),
            metadata=request_metadata,
        )
        if params:
            _ = next(responses)  # Skip echo response if params are provided

        write_output_file_from_response(response_iter=responses, output_filepath=output_filepath)
        end_time = time.time()
        print(
            f"Function invocation completed in {end_time-start_time:.2f}s,"
            f" the output file {output_filepath} is generated."
        )
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    """
    Main client function
    """
    args = parse_args()
    input_filepath = args.input
    output_filepath = args.output
    if os.path.isfile(input_filepath):
        print(f"The file '{input_filepath}' exists. Proceeding with processing.")
    else:
        raise FileNotFoundError(f"The file '{input_filepath}' does not exist. Exiting.")

    params = {}
    # Supply params as shown below, refer to the docs for more info.
    # params = {"eye_size_sensitivity": 4, "detect_closure": 1 }

    # Check ssl-mode and create channel_credentials for that mode
    if args.ssl_mode != "DISABLED":
        channel_credentials = ""
        if args.ssl_mode == "MTLS":
            if not (args.ssl_key and args.ssl_cert and args.ssl_root_cert):
                raise RuntimeError(
                    "If --ssl-mode is MTLS, --ssl-key, --ssl-cert and --ssl-root-cert are required."
                )
            private_key = read_file_content(args.ssl_key)
            certificate_chain = read_file_content(args.ssl_cert)
            root_certificates = read_file_content(args.ssl_root_cert)
            channel_credentials = grpc.ssl_channel_credentials(
                root_certificates=root_certificates,
                private_key=private_key,
                certificate_chain=certificate_chain,
            )
        else:
            if not (args.ssl_root_cert):
                raise RuntimeError("If --ssl-mode is TLS, --ssl-root-cert is required.")
            root_certificates = read_file_content(args.ssl_root_cert)
            channel_credentials = grpc.ssl_channel_credentials(root_certificates=root_certificates)

        # Establish secure channel when ssl-mode is MTLS/TLS
        with grpc.secure_channel(target=args.target, credentials=channel_credentials) as channel:
            process_request(
                channel=channel,
                input_filepath=input_filepath,
                output_filepath=output_filepath,
                params=params,
            )

    elif args.preview_mode:
        if not args.api_key or not args.function_id:
            raise RuntimeError(
                "If --preview-mode is specified, both --api-key and --function-id are required."
            )
        # set metadata for NVCF autentication
        request_metadata = (
            ("authorization", "Bearer {}".format(args.api_key)),
            ("function-id", args.function_id),
        )
        # Establish secure channel when sending request to NVCF server
        with grpc.secure_channel(
            target=args.target, credentials=grpc.ssl_channel_credentials()
        ) as channel:
            process_request(
                channel=channel,
                input_filepath=input_filepath,
                params=params,
                output_filepath=output_filepath,
                request_metadata=request_metadata,
            )
    else:
        # Establish insecure channel when ssl-mode is DISABLED
        with grpc.insecure_channel(target=args.target) as channel:
            process_request(
                channel=channel,
                input_filepath=input_filepath,
                params=params,
                output_filepath=output_filepath,
            )


if __name__ == "__main__":
    main()
