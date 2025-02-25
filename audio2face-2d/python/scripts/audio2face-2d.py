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
import io
import grpc

sys.path.append(os.path.join(os.getcwd(), "../interfaces"))
# Importing gRPC compiler auto-generated maxine audio2face-2d library
import audio2face2d_pb2  # noqa: E402
import audio2face2d_pb2_grpc  # noqa: E402
from audio2face2d_pb2 import (  # noqa: E402
    QuaternionStream,
    Quaternion,
    Vector3fStream,
    Vector3f,
    ModelSelection,
    AnimationCroppingMode,
    HeadPoseMode,
)


def parse_args() -> None:
    """
    Parse command-line arguments using argparse.
    """
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Process input audio and portrait files and apply audio2face-2d effect."
    )
    parser.add_argument(
        "--ssl-mode",
        type=str,
        help="Flag to set SSL mode, default is None",
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
        help="IP:port of gRPC service, when hosted locally.",
    )
    parser.add_argument(
        "--audio-input",
        type=str,
        default="../../assets/sample_audio.wav",
        help="The path to the input audio file.",
    )
    parser.add_argument(
        "--portrait-input",
        type=str,
        default="../../assets/sample_portrait_image.png",
        help="The path to the input portrait file.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output.mp4",
        help="The path for the output video file.",
    )
    parser.add_argument(
        "--head-rotation-animation-filepath",
        type=str,
        default="../../assets/head_rotation_animation.csv",
        help="The path for the head_rotation_animation.csv file. "
        "Only required for HEAD_POSE_MODE_USER_DEFINED_ANIMATION",
    )
    parser.add_argument(
        "--head-translation-animation-filepath",
        type=str,
        default="../../assets/head_translation_animation.csv",
        help="The path for the head_translation_animation.csv file. "
        "Only required for HEAD_POSE_MODE_USER_DEFINED_ANIMATION",
    )
    return parser.parse_args()


def read_file_content(file_path: os.PathLike) -> None:
    """Function to read file content as bytes.

    Args:
      file_path: Path to input file
    """
    with open(file_path, "rb") as file:
        return file.read()


def generate_request_for_inference(audio_filepath: str, params: dict):
    """Generator to produce the request data stream

    Args:
      audio_filepath: Path to input file
      params: Parameters for the feature
    """
    yield audio2face2d_pb2.AnimateRequest(config=audio2face2d_pb2.AnimateConfig(**params))
    file = open(audio_filepath, "rb")
    while True:
        buffer = file.read(1024 * 1024)
        if buffer == b"":
            break
        yield audio2face2d_pb2.AnimateRequest(audio_file_data=buffer)
    print("Data sending done")


def process_head_pose_data(head_rotation_path, head_translation_path):
    """
    Process head rotation and translation data.

    Args:
        head_rotation_path (str): Path to the head rotation animation file.
        head_translation_path (str): Path to the head translation animation file.

    Returns:
        Tuple[QuaternionStream, Vector3fStream]: Processed rotation and translation data streams.
    """
    # Read the head rotation data
    with io.StringIO(open(head_rotation_path, "rb").read().decode("utf-8")) as file:
        head_rotation_data = []
        for line in file:
            values = line.strip().split(",")
            if len(values) == 4:
                head_rotation_data.append([float(val) for val in values])

    # Validate the data
    assert len(head_rotation_data) > 0, "Head rotation data is empty"
    assert all(len(row) == 4 for row in head_rotation_data), "Each row must have 4 values"

    # Create the QuaternionStream
    rotation_data_stream = QuaternionStream()
    for x in head_rotation_data:
        q = Quaternion()
        q.x, q.y, q.z, q.w = x
        rotation_data_stream.values.append(q)

    # Read the head translation data
    with io.StringIO(open(head_translation_path, "rb").read().decode("utf-8")) as file:
        head_translation_data = []
        for line in file:
            values = line.strip().split(",")
            if len(values) == 3:
                head_translation_data.append([float(val) for val in values])

    # Validate the data
    assert len(head_translation_data) > 0, "Head translation data is empty"
    assert all(len(row) == 3 for row in head_translation_data), "Each row must have 3 values"

    # Create the Vector3fStream
    translation_data_stream = Vector3fStream()
    for x in head_translation_data:
        v = Vector3f()
        v.x, v.y, v.z = x
        translation_data_stream.values.append(v)

    return rotation_data_stream, translation_data_stream


def process_request(
    channel: any,
    audio_filepath: os.PathLike,
    params: dict,
    output_filepath: os.PathLike,
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
        stub = audio2face2d_pb2_grpc.Audio2Face2DServiceStub(channel)
        start_time = time.time()
        responses = stub.Animate(
            generate_request_for_inference(audio_filepath=audio_filepath, params=params)
        )
        next(responses)
        file = open(output_filepath, "wb")
        print(f"Writing output in {output_filepath}")
        for response in responses:
            if response.HasField("video_file_data"):
                file.write(response.video_file_data)
        end_time = time.time()
        print(
            f"Function invocation completed in {end_time-start_time:.2f}s, "
            f"{output_filepath} file is generated."
        )
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    """
    Main client function
    """
    args = parse_args()
    portrait_filepath = args.portrait_input
    audio_filepath = args.audio_input
    output_filepath = args.output

    # Check file path
    if os.path.isfile(portrait_filepath):
        print(f"The image file '{portrait_filepath}' exists. Checking for audio file.")
    else:
        raise FileNotFoundError(f"The image file '{portrait_filepath}' does not exist. Exiting.")
    if os.path.isfile(audio_filepath):
        print(f"The audio file '{audio_filepath}' exists. Proceeding with processing.")
    else:
        raise FileNotFoundError(f"The audio file '{audio_filepath}' does not exist. Exiting.")

    portrait_image_encoded = open(portrait_filepath, "rb").read()

    # Configure head pose mode
    head_pose_mode = HeadPoseMode.HEAD_POSE_MODE_RETAIN_FROM_PORTRAIT_IMAGE

    # Provide head pose animation values for head pose mode HEAD_POSE_MODE_USER_DEFINED_ANIMATION
    if head_pose_mode == HeadPoseMode.HEAD_POSE_MODE_USER_DEFINED_ANIMATION:
        rotation_data_stream, translation_data_stream = process_head_pose_data(
            args.head_rotation_animation_filepath,
            args.head_translation_animation_filepath,
        )

    # Supply params as shown below, refer to the docs for more info.
    feature_params = {
        "portrait_image": portrait_image_encoded,
        "model_selection": ModelSelection.MODEL_SELECTION_QUALITY,
        "animation_crop_mode": AnimationCroppingMode.ANIMATION_CROPPING_MODE_REGISTRATION_BLENDING,
        "enable_lookaway": 1,  # can be 0 or 1
        "lookaway_max_offset": 20,  # value in [5, 25]
        "lookaway_interval_min": 240,  # value in [1, 600]
        "lookaway_interval_range": 90,  # value in [1, 600]
        "blink_frequency": 15,  # value in [0, 120]
        "blink_duration": 6,  # value in [2, 150]
        "mouth_expression_multiplier": 1.4,  # value in [1.0, 2.0]
        "head_pose_mode": head_pose_mode,
        "head_pose_multiplier": 1.0,  # value in [0.0, 1.0]
        # "input_head_rotation": rotation_data_stream,  # HEAD_POSE_MODE_USER_DEFINED_ANIMATION
        # "input_head_translation": translation_data_stream, # HEAD_POSE_MODE_USER_DEFINED_ANIMATION
    }

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
                audio_filepath=audio_filepath,
                params=feature_params,
                output_filepath=output_filepath,
            )
    else:
        # Establish insecure channel when ssl-mode is DISABLED
        with grpc.insecure_channel(target=args.target) as channel:
            process_request(
                channel=channel,
                audio_filepath=audio_filepath,
                params=feature_params,
                output_filepath=output_filepath,
            )


if __name__ == "__main__":
    main()
