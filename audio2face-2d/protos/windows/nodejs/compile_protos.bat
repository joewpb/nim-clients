:: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
::
:: Permission is hereby granted, free of charge, to any person obtaining a
:: copy of this software and associated documentation files (the "Software"),
:: to deal in the Software without restriction, including without limitation
:: the rights to use, copy, modify, merge, publish, distribute, sublicense,
:: and/or sell copies of the Software, and to permit persons to whom the
:: Software is furnished to do so, subject to the following conditions:
::
:: The above copyright notice and this permission notice shall be included in
:: all copies or substantial portions of the Software.
::
:: THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
:: IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
:: FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
:: THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
:: LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
:: FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
:: DEALINGS IN THE SOFTWARE.


:: This script compiles Protocol Buffer (protobuf) definitions for NVIDIA Maxine Audio2Face-2D NIM on a Windows Client.
::
:: Execute the script using `compile_protos.bat`.
::
:: For more details, refer to README.txt.


@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "PROTOS_DIR=%SCRIPT_DIR%../../proto/nvidia/maxine/audio2face2d/v1"
set "OUT_DIR=%SCRIPT_DIR%../../../nodejs/interfaces"

:: Install grpc-tools
call npm install -g grpc-tools

if %errorlevel% neq 0 (
    echo grpc-tools installation failed
    exit /b %errorlevel%
)

:: Check if running in PowerShell
call powershell -Command "exit $PSVersionTable.PSVersion.Major -ne $null"
if %errorlevel% equ 0 (
    :: Running in PowerShell
    powershell -Command "for /f 'delims=' %%i in ('Get-Command grpc_tools_node_protoc_plugin.cmd ^| Select-Object -ExpandProperty Source') do set GRPC_PLUGIN_PATH=%%i"
) else (
    :: Running in Command Prompt
    for /f "delims=" %%i in ('where grpc_tools_node_protoc_plugin.cmd') do set GRPC_PLUGIN_PATH=%%i
)

:: Generate the interface files
call grpc_tools_node_protoc --js_out=import_style=commonjs:%OUT_DIR%  %PROTOS_DIR%/audio2face2d.proto --proto_path=%PROTOS_DIR% --grpc_out=grpc_js:%OUT_DIR%   --plugin=protoc-gen-grpc=%GRPC_PLUGIN_PATH%
endlocal