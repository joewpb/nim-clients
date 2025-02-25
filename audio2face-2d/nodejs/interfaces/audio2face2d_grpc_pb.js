// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('@grpc/grpc-js');
var audio2face2d_pb = require('./audio2face2d_pb.js');
var google_protobuf_empty_pb = require('google-protobuf/google/protobuf/empty_pb.js');

function serialize_nvidia_maxine_audio2face2d_v1_AnimateRequest(arg) {
  if (!(arg instanceof audio2face2d_pb.AnimateRequest)) {
    throw new Error('Expected argument of type nvidia.maxine.audio2face2d.v1.AnimateRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_nvidia_maxine_audio2face2d_v1_AnimateRequest(buffer_arg) {
  return audio2face2d_pb.AnimateRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_nvidia_maxine_audio2face2d_v1_AnimateResponse(arg) {
  if (!(arg instanceof audio2face2d_pb.AnimateResponse)) {
    throw new Error('Expected argument of type nvidia.maxine.audio2face2d.v1.AnimateResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_nvidia_maxine_audio2face2d_v1_AnimateResponse(buffer_arg) {
  return audio2face2d_pb.AnimateResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


// The Audio2Face2DService provides APIs to run the
// Maxine Audio to Face - 2D feature.
var Audio2Face2DServiceService = exports.Audio2Face2DServiceService = {
  // Animate is a bidirectional streaming API to run the
// Audio2Face-2D.
//
// The input message can contain AnimateConfig or bytes.
// In the beginning of the stream, a request with AnimateConfig should
// be sent to the server to set the feature's parameters.
// The server will echo back a response with the config to signify that the
// parameters were properly set. It is mandatory to set the portrait_image
// config, other configuration parameters are optional and a default value will
// be used if not set. Any AnimateConfig sent during the middle of the stream
// will be ignored.
//
// After the configuration step, the client streams the input wav file in
// chunks in the input message and receives the output mp4 file in chunks in
// the output message. While the inference is running, the server will periodically
// echo empty message to keep the channel alive. The client should ignore this message.
//
// It is recommended that the client should pass one file per API invocation.
// The configurations are also set per invocation.
animate: {
    path: '/nvidia.maxine.audio2face2d.v1.Audio2Face2DService/Animate',
    requestStream: true,
    responseStream: true,
    requestType: audio2face2d_pb.AnimateRequest,
    responseType: audio2face2d_pb.AnimateResponse,
    requestSerialize: serialize_nvidia_maxine_audio2face2d_v1_AnimateRequest,
    requestDeserialize: deserialize_nvidia_maxine_audio2face2d_v1_AnimateRequest,
    responseSerialize: serialize_nvidia_maxine_audio2face2d_v1_AnimateResponse,
    responseDeserialize: deserialize_nvidia_maxine_audio2face2d_v1_AnimateResponse,
  },
};

exports.Audio2Face2DServiceClient = grpc.makeGenericClientConstructor(Audio2Face2DServiceService);
