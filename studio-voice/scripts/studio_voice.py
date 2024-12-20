# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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
import grpc
import time
from typing import Iterator

sys.path.append(os.path.join(os.getcwd(), "../interfaces/studio_voice"))
# Importing gRPC compiler auto-generated maxine studiovoice library
import studiovoice_pb2, studiovoice_pb2_grpc  # noqa: E402


def generate_request_for_inference(input_filepath: os.PathLike) -> None:
    """Generator to produce the request data stream

    Args:
      input_filepath: Path to input file
    """
    DATA_CHUNKS = 64 * 1024  # bytes, we send the wav file in 64KB chunks
    with open(input_filepath, "rb") as fd:
        while True:
            buffer = fd.read(DATA_CHUNKS)
            if buffer == b"":
                break
            yield studiovoice_pb2.EnhanceAudioRequest(audio_stream_data=buffer)


def write_output_file_from_response(
    response_iter: Iterator[studiovoice_pb2.EnhanceAudioResponse], output_filepath: os.PathLike
) -> None:
    """Function to write the output file from the incoming gRPC data stream.

    Args:
      response_iter: Responses from the server to write into output file
      output_filepath: Path to output file
    """
    with open(output_filepath, "wb") as fd:
        for response in response_iter:
            if response.HasField("audio_stream_data"):
                fd.write(response.audio_stream_data)


def parse_args() -> None:
    """
    Parse command-line arguments using argparse.
    """
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Process wav audio files using gRPC and apply studio-voice."
    )
    parser.add_argument(
        "--use-ssl",
        action="store_true",
        help="Flag to control if SSL/TLS encryption should be used. "
        "When running preview SSL must be used.",
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
        default="../assets/studio_voice_48k_input.wav",
        help="The path to the input audio file.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="studio_voice_48k_output.wav",
        help="The path for the output audio file.",
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


def process_request(
    channel: any,
    input_filepath: os.PathLike,
    output_filepath: os.PathLike,
    request_metadata: dict = None,
) -> None:
    """Function to process gRPC request

    Args:
      channel: gRPC channel for server client communication
      input_filepath: Path to input file
      output_filepath: Path to output file
      request_metadata: Credentials to process request
    """
    try:
        stub = studiovoice_pb2_grpc.MaxineStudioVoiceStub(channel)
        start_time = time.time()

        responses = stub.EnhanceAudio(
            generate_request_for_inference(input_filepath=input_filepath),
            metadata=request_metadata,
        )

        write_output_file_from_response(response_iter=responses, output_filepath=output_filepath)

        end_time = time.time()
        print(
            f"Function invocation completed in {end_time-start_time:.2f}s, "
            "the output file is generated."
        )
    except BaseException as e:
        print(e)


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

    if args.use_ssl:
        if not args.api_key or not args.function_id:
            raise RuntimeError(
                "If --use-ssl is specified, both --api-key and --function-id are required."
            )
        request_metadata = (
            ("authorization", "Bearer {}".format(args.api_key)),
            ("function-id", args.function_id),
        )
        with grpc.secure_channel(
            target=args.target, credentials=grpc.ssl_channel_credentials()
        ) as channel:
            process_request(
                channel=channel,
                input_filepath=input_filepath,
                output_filepath=output_filepath,
                request_metadata=request_metadata,
            )
    else:
        with grpc.insecure_channel(target=args.target) as channel:
            process_request(
                channel=channel,
                input_filepath=input_filepath,
                output_filepath=output_filepath,
            )


if __name__ == "__main__":
    main()
