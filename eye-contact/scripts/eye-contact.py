import argparse
import os
import sys
import time
from typing import Iterator

import grpc

sys.path.append(os.path.join(os.getcwd(), "../interfaces"))
# Importing gRPC compiler auto-generated maxine eyecontact library
from eye_contact import eyecontact_pb2, eyecontact_pb2_grpc


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
    ):  # if params is supplied, the first item in the input stream is a config object with parameters
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
    with open(output_filepath, "wb") as fd:
        for response in response_iter:
            if response.HasField("video_file_data"):
                fd.write(response.video_file_data)


def parse_args() -> None:
    """
    Parse command-line arguments using argparse.
    """
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Process mp4 video files using gRPC and apply eye-contact."
    )
    parser.add_argument(
        "--use-ssl",
        action="store_true",
        help="Flag to control if SSL/TLS encryption should be used. When running preview SSL must be used.",
    )
    parser.add_argument(
        "--target",
        type=str,
        default="127.0.0.1:8004",
        help="IP:port of gRPC service, when hosted locally. Use grpc.nvcf.nvidia.com:443 when hosted on NVCF.",
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
        help="NGC API key required for authentication, utilized when using TRY API ignored otherwise",
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
      request_metadata: Credentials to process request
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
            " the output file is generated."
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
    # supply params as shown below, refer to the docs for more info.
    # params = {"eye_size_sensitivity": 4, "detect_closure": 1 }

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
                params=params,
                output_filepath=output_filepath,
                request_metadata=request_metadata,
            )
    else:
        with grpc.insecure_channel(target=args.target) as channel:
            process_request(
                channel=channel,
                input_filepath=input_filepath,
                params=params,
                output_filepath=output_filepath,
            )


if __name__ == "__main__":
    main()
