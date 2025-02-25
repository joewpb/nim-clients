// Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
//
// Permission is hereby granted, free of charge, to any person obtaining a
// copy of this software and associated documentation files (the "Software"),
// to deal in the Software without restriction, including without limitation
// the rights to use, copy, modify, merge, publish, distribute, sublicense,
// and/or sell copies of the Software, and to permit persons to whom the
// Software is furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
// THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
// FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
// DEALINGS IN THE SOFTWARE.

// Include/import modules
const assert = require('assert');
const fs = require('fs');
const grpc = require('@grpc/grpc-js');
const http = require('http');
const messages = require('../interfaces/audio2face2d_pb')
const memoryStream = require('memorystream');
const path=require("path");
const services = require('../interfaces/audio2face2d_grpc_pb');
const writer = require('wav').Writer;
const { Command } = require('commander');
const { parse } = require('csv-parse/sync')

// Set parameters
const chunkSize = 1024 * 1024 // Size of audio chunk to stream
const memStream = new memoryStream(); // To stream video output from server to the browser
const A2F2D_BROWSER_PORT = process.env.A2F2D_BROWSER_PORT || 3000; // check if system has env variable for browser streaming PORT, otherwise use 3000
 
/**
 * Sets up the video streaming server for streaming output video to browser
 *
 * @returns {handle} handle for the server object
 */
function setupVideoStreamingServer() {
  // Create the server
  const server = http.createServer((req, res)=>{
    if(req.method === 'GET' && req.url === "/"){
      // Send index.html page when user visits "/" endpoint
      // index.html will have video component that displays the video
      fs.createReadStream(path.resolve("index.html")).pipe(res);
      return;
    }

    //if video content is requested
    if(req.method === 'GET' && req.url === "/video"){
      const head = {
	      'Content-Type': 'video/mp4',
      }
      res.writeHead(200, head);
      memStream.pipe(res);
    }
    else{
      res.writeHead(400);
      res.end("bad request");
    }
  })

  return server;
}

/**
 * Processes the head pose mode animation input data from the provided file paths.
 * 
 * @param {string} headRotationAnimationFilepath - The path to the head rotation animation input file.
 * @param {string} headTranslationAnimationFilepath - The path to the head translation animation input file.
 * 
 * @returns {object} An object containing the processed rotation and translation data streams.
 */
function processHeadPoseModeAnimationInput(headRotationAnimationFilepath, headTranslationAnimationFilepath) {
  // Check if head rotation and translation input files exist
  if (!fs.existsSync(headRotationAnimationFilepath)) {
    console.error('Head rotation animation input file %s does not exist', headRotationAnimationFilepath);
    process.exit(1); // Exit the process with a non-zero status code
  }
  if (!fs.existsSync(headTranslationAnimationFilepath)) {
    console.error('Head translation animation input file %s does not exist', headTranslationAnimationFilepath);
    process.exit(1); // Exit the process with a non-zero status code
  }
  
  // Setup the head rotation and translation animation
  const rotation = fs.readFileSync(headRotationAnimationFilepath, 'utf8');
  const translation = fs.readFileSync(headTranslationAnimationFilepath, 'utf8');

  // Parse the CSV data
  const rotationCsv = parse(rotation, {
    delimiter: ',',
    columns: false,
    cast: (value) => parseFloat(value),
  });
  const translationCsv = parse(translation, {
    delimiter: ',',
    columns: false,
    cast: (value) => parseFloat(value),
  });

  // Convert data to float32
  const rotationData = rotationCsv.map(row => row.map(Number));
  const translationData = translationCsv.map(row => row.map(Number));

  // Assertions
  assert(Array.isArray(rotationData) && Array.isArray(rotationData[0]), 'Data should be a 2-dimensional array');
  assert(rotationData.length > 0, 'Data should have more than 0 rows');
  rotationData.forEach(row => {
    assert(row.length === 4, 'Each row should have 4 columns');
  });
  assert(Array.isArray(translationData) && Array.isArray(translationData[0]), 'Data should be a 2-dimensional array');
  assert(translationData.length > 0, 'Data should have more than 0 rows');
  translationData.forEach(row => {
    assert(row.length === 3, 'Each row should have 3 columns');
  });

  // Create rotation and translation data streams
  const rotationDataStream = new messages.QuaternionStream({ values: [] });
  const translationDataStream = new messages.Vector3fStream({ values: [] });

  // Populate the rotation and translation data streams
  for (const x of rotationData) {
    var q = new messages.Quaternion();
    q.setX(x[0]);
    q.setY(x[1]);
    q.setZ(x[2]);
    q.setW(x[3]);
    rotationDataStream.addValues(q);
  }

  for (const x of translationData) {
    var v = new messages.Vector3f();
    v.setX(x[0]);
    v.setY(x[1]);
    v.setZ(x[2]);
    translationDataStream.addValues(v);
  }

  return {rotationDataStream, translationDataStream};
}

/**
 * Sends the input config like portrait image, mode, model etc
 *
 * @param rpcCall - RPC call object
 * @param {string} portraitInputFile - Path to the portrait input file
 * @param {string} headRotationAnimationFilepath - Path to the rotation animation data file
 * @param {string} headTranslationAnimationFilepath - Path to the translation animation data file
 */
function sendInputConfig(rpcCall, portraitInputFile, headRotationAnimationFilepath, headTranslationAnimationFilepath) {
  // Open and read the portrait image in binary format
  const config = new messages.AnimateConfig();
  const imgData = fs.readFileSync(portraitInputFile);
  try {
    config.setPortraitImage(imgData);
  }
  catch (err) {
    console.error('Error reading the image file:', err);
    process.exit(1); // Exit the process with a non-zero status code
  }

  // Prepare the config for Audio2Face 2D
  const headPoseMode = messages.HeadPoseMode.HEAD_POSE_MODE_RETAIN_FROM_PORTRAIT_IMAGE;
  config.setAnimationCropMode(messages.AnimationCroppingMode.ANIMATION_CROPPING_MODE_REGISTRATION_BLENDING);
  config.setModelSelection(messages.ModelSelection.MODEL_SELECTION_QUALITY);
  config.setEnableLookaway(1);
  config.setLookawayMaxOffset(20);
  config.setLookawayIntervalMin(240);
  config.setLookawayIntervalRange(90);
  config.setBlinkFrequency(15);
  config.setBlinkDuration(6);
  config.setMouthExpressionMultiplier(1.4);
  config.setHeadPoseMode(headPoseMode);
  config.setHeadPoseMultiplier(0.4);

  if (headPoseMode == messages.HeadPoseMode.HEAD_POSE_MODE_USER_DEFINED_ANIMATION) {
    // Process the head pose rotation and translation animation data from input CSV files
    var animationData = processHeadPoseModeAnimationInput(headRotationAnimationFilepath, headTranslationAnimationFilepath);

    // Set the Audio2face 2D config with head rotation and animation data
    config.setInputHeadRotation(animationData.rotationDataStream);
    config.setInputHeadTranslation(animationData.translationDataStream);
  }

  var msg = new messages.AnimateRequest();
  msg.setConfig(config);

  // Write the config to the stream
  try {
    rpcCall.write(msg);
    console.log("Input config sent");
  } catch (writeError) {
    console.error('Write Error:', writeError.message);
    process.exit(1); // Exit the process with a non-zero status code
  }
}

/**
 * Sends input audio chunks
 *
 * @param rpcCall - RPC call object
 * @param format - type of audio format (pcm or wav)
 * @param {string} audioInputFile - Path to audio input file
 */
function sendInputAudioChunks(rpcCall, format, audioInputFile) {
  // Read audio file
  let readStream;
  if (format === 'wav') {
    readStream = fs.createReadStream(audioInputFile, { highWaterMark: chunkSize });
  } else if (format === 'pcm') {
    const pcm = fs.createReadStream(audioInputFile);

    // Convert pcm format to wav 
    // Change the pcm config here, if needed
    readStream = new writer({
      sampleRate: 48000,
      channels: 1,
      bitDepth: 16
    });

    pcm.pipe(readStream);
  }

  readStream.on('data', (chunk) => {
    // Process the chunk here
    var msg = new messages.AnimateRequest();
    msg.setAudioFileData(chunk);

    // Write the audio chunk to the stream
    rpcCall.write(msg);
  });

  readStream.on('end', () => {
    rpcCall.end();
    console.log('Input audio sent');
    console.log('Receiving and writing the video chunks from server to the output file');
  });

  readStream.on('error', (err) => {
    console.error('Error reading the audio file:', err);
    process.exit(1); // Exit the process with a non-zero status code
  });
}

/**
 * Sets up the infra to receive response(video chunks) from the server
 *
 * @param rpcCall - RPC call object
 * @param {string} outputFile - Path to video output file
 * @param {bool} browser - Specifies if the browser is enabled
 */
function receiveServerResponse(rpcCall, outputFile, browser) {
  // Open the mp4 file to write the video frames from the server
  const writeStream = fs.createWriteStream(outputFile);
  
  // Set up processing for the response
  rpcCall.on('data', function(response) {
    if (response.hasVideoFileData()) {
      const data = response.getVideoFileData();
      writeStream.write(data);

      if (browser) {
        memStream.write(data);
      }
    }
  });

  rpcCall.on('end', () => {
    writeStream.end();

    if (browser) {
      memStream.end();
    }

    // Log the elapsed time
    console.timeEnd('Function invocation completed in ');
    console.log(`video written to ${outputFile}`);

    if (browser) {
      console.log("Press Ctrl+C to stop the browser streaming server");
    }
  });

  rpcCall.on('error', (err) => {
    console.error('Error:', err);
    process.exit(1); // Exit the process with a non-zero status code
  });
}

function readFileContent(filePath) {
  /**
   * Function to read file content as bytes.
   *
   * @param {string} filePath - Path to the input file
   * @returns {Buffer} - File content as bytes
   * @throws {Error} - If the file cannot be read
   */
  try {
    return fs.readFileSync(filePath); // Reads the file content as a Buffer
  } catch (err) {
    console.error(`Error reading file at ${filePath}:`, err.message);
    throw err;
  }
}

/**
 * Parses the command line arguments
 *
 * @returns {options} options available from command-line
 */
function parseArguments() {
  const program = new Command();

  program
    .description('Node JS client for A2F2D NIM')
    .option('--ssl-mode <type>', 'Flag to set SSL mode, default is DISABLED', 'DISABLED')
    .option('--ssl-key <type>', 'The path to SSL private key.', '../ssl_key/ssl_key_client.pem')
    .option('--ssl-cert <type>', 'The path to SSL certificate chain.', '../ssl_key/ssl_cert_client.pem')
    .option('--ssl-root-cert <type>', 'The path to SSL root certificate.', '../ssl_key/ssl_ca_cert.pem')
    .option('--target <type>', 'IP:port of gRPC service, when hosted locally.', '127.0.0.1:8001')
    .option('--audio-input <type>', 'The path to the input audio file.', '../../assets/sample_audio.wav')
    .option('--head-rotation-animation-filepath <type>', 'The path to head rotation animation csv file.', '../../assets/head_rotation_animation.csv')
    .option('--head-translation-animation-filepath <type>', 'The path to head translation animation csv file.', '../../assets/head_translation_animation.csv')
    .option('--portrait-input <type>', 'The path to the input portrait file.', '../../assets/sample_portrait_image.png')
    .option('--format <type>', 'Audio format - wav or pcm', 'wav')
    .option('--browser', 'Specifies whether to enable browser streaming')
    .option('--output <type>', 'The path for the output video file.', 'output.mp4')
    .helpOption('-h, --help', 'Display help for command');

  program.parse(process.argv);
  return program.opts();
}

/**
 * Creates a gRPC client instance based on the provided options.
 * 
 * @param {object} options - The options object containing the following properties:
 *   - sslMode {string}: The SSL mode to use for the connection. Can be one of 'DISABLED', 'TLS', or 'MTLS'.
 *   - sslRootCert {string}: The path to the root certificate file (required for 'TLS' and 'MTLS' modes).
 *   - sslKey {string}: The path to the private key file (required for 'MTLS' mode).
 *   - sslCert {string}: The path to the certificate chain file (required for 'MTLS' mode).
 *   - target {string}: The target URL for the gRPC client.
 * 
 * @returns {object} The created gRPC client instance.
 * 
 * @throws {Error} If the provided SSL mode is invalid or if required certificate/key files are missing.
 */
function createGrpcClient(options) {
  let client;
  let credentials;

  switch (options.sslMode) {
    case 'DISABLED':
      console.log('Using insecure connection');
      credentials = grpc.credentials.createInsecure();
      break;

    case 'TLS':
      if (!options.sslRootCert) {
        console.error('If --ssl-mode is TLS, --ssl-root-cert is required.');
        process.exit(1);
      }
      const rootCert = readFileContent(options.sslRootCert);
      credentials = grpc.credentials.createSsl(rootCert);
      console.log('Using secure connection with TLS');
      break;

    case 'MTLS':
      if (!(options.sslKey && options.sslCert && options.sslRootCert)) {
        console.error(
          'If --ssl-mode is MTLS, --ssl-key, --ssl-cert, and --ssl-root-cert are required.'
        );
        process.exit(1);
      }
      const privateKey = readFileContent(options.sslKey);
      const certificateChain = readFileContent(options.sslCert);
      const rootCertificates = readFileContent(options.sslRootCert);
      credentials = grpc.credentials.createSsl(rootCertificates, privateKey, certificateChain);
      console.log('Using secure connection with MTLS');
      break;

    default:
      console.error(`Invalid SSL mode: ${options.sslMode}`);
      process.exit(1);
  }

  // Create the gRPC client
  client = new services.Audio2Face2DServiceClient(options.target, credentials);
  return client;
}

function main() {
  // Parse the commandline arguments
  // Note: commander package used for parsing arguments internally changes all options with dashes to camel case
  // For example audio-input to audioInput. Therefore, all the options with dashes will be referenced with camelcase notation
  const options = parseArguments();

  // Validate SSL mode
  const validSslModes = ['DISABLED', 'MTLS', 'TLS'];
  if (!validSslModes.includes(options['sslMode'])) {
    console.error(`Invalid SSL mode. Must be one of: ${validSslModes.join(', ')}`);
    process.exit(1);
  }

  // Validate the audio format
  if (options['format'] != 'pcm' && options['format'] != 'wav') {
    console.error('Audio format must be pcm or wav');
    process.exit(1); // Exit the process with a non-zero status code
  }

  // Validate the provided audio input file for correct format
  var ext = options['audioInput'].slice(((options['audioInput'].lastIndexOf(".") - 1) >>> 0) + 2);
  if (options['format'] == 'wav' && ext != 'wav' ||
    options['format'] == 'pcm' && ext != 'raw') {
      console.error('Input audio file format must match the audio format: file format (extension): %s, audio format: %s', ext, options['format']);
      process.exit(1); // Exit the process with a non-zero status code
  }

  // Check if required input files exist
  if (!fs.existsSync(options['audioInput'])) {
    console.error('Audio input file %s does not exist', options['audioInput']);
    process.exit(1); // Exit the process with a non-zero status code
  }
  if (!fs.existsSync(options['portraitInput'])) {
    console.error('Portrait input file %s does not exist', options['portraitInput']);
    process.exit(1); // Exit the process with a non-zero status code
  }

  // Setup and start the video streaming server, if enabled
  if (options['browser']) {
    const server = setupVideoStreamingServer();
    server.listen(A2F2D_BROWSER_PORT , () => {
      console.log(`Server listening on port:${A2F2D_BROWSER_PORT }`);
    });
  }

  // Set up the connection with the server
  var client = createGrpcClient(options);
  
  // Start the timer
  console.time('Function invocation completed in ');

  // Setup call to the remote function (animate is the remote procedure for A2F2D)
  const rpcCall = client.animate((error) => {
    if (error) {
      console.error('RPC call error ', error.message);
      process.exit(1); // Exit the process with a non-zero status code
    }
  });

  // Check for connection error
  rpcCall.on('error', (error) => {
    console.error('Connection failed:', error.message);
    process.exit(1); // Exit the process with a non-zero status code
  });

  // Write the Audio2face 2D config
  sendInputConfig(rpcCall, options['portraitInput'], options['headRotationAnimationFilepath'], options['headTranslationAnimationFilepath']);

  // Write the audio chunks of size chunkSize from the audio file
  sendInputAudioChunks(rpcCall, options['format'], options['audioInput']);
  
  // Sets up receiving response from server and writing to a file
  receiveServerResponse(rpcCall, options['output'], options['browser']);
}

main()
