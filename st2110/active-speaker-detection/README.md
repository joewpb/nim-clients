# NVIDIA Active Speaker Detection ST 2110 NIM

## Overview

Active Speaker Detection ST 2110 NIM is designed for live IP video workflows that require real-time speaker intelligence. The feature analyzes video, audio, and diarization data to identify and track active speakers across frames. It returns per-frame speaker data, including bounding boxes, speaker identifiers, active speaking state, and confidence scores. For ST 2110 deployments, this NIM is intended to run with [NVIDIA Holoscan for Media](https://docs.nvidia.com/holoscan-for-media/latest/index.html).

---

## Helm Charts

Add the Helm repository and pull the charts.

```bash

export NGC_API_KEY=<PASTE_API_KEY_HERE>

helm repo add nim-repo \
  https://helm.ngc.nvidia.com/nim/nvidia/ \
  --username='$oauthtoken' \
  --password=$NGC_API_KEY

helm repo update

helm pull nim-repo/nvidia-active-speaker-detection-h4m-sample   --version 1.0.0
helm pull nim-repo/nvidia-active-speaker-detection-h4m-service  --version 1.0.0
helm pull nim-repo/nvidia-active-speaker-detection-h4m-operator --version 1.0.0
```

| Chart | Description |
|-------|-------------|
| `nvidia-active-speaker-detection-h4m-sample` | End-to-end demo-sender, NIM service, and receiver in a single release. |
| `nvidia-active-speaker-detection-h4m-service` | NIM service only — for integration into a custom pipeline. |
| `nvidia-active-speaker-detection-h4m-operator` | Kubernetes operator and `NvidiaActiveSpeakerDetectionMediaFunction` Custom Resource Definition. |

For initial evaluation, the sample chart provides a complete end-to-end pipeline. For production integration, use the NIM service chart for direct deployment or the operator chart for Kubernetes-native lifecycle management.

---

## Container Images

| Image | Description |
|-------|-------------|
| `nvcr.io/nim/nvidia/active-speaker-detection-h4m-nim` | Active Speaker Detection NIM |
| `nvcr.io/nim/nvidia/active-speaker-detection-h4m-operator` | Kubernetes operator |
| `nvcr.io/nim/nvidia/active-speaker-detection-h4m-sample-sender` | Sample sender (for the demo chart) |
| `nvcr.io/nim/nvidia/active-speaker-detection-h4m-sample-receiver` | Sample receiver (for the demo chart) |

---

## Try It Out

You can try out the feature here: [Active Speaker Detection](https://build.nvidia.com/nvidia/active-speaker-detection).

---

## Documentation

- [Developer Guide — Active Speaker Detection on Holoscan for Media](https://docs.nvidia.com/nim/maxine/active-speaker-detection-h4m/latest/index.html)
- [NVIDIA Holoscan for Media](https://docs.nvidia.com/holoscan-for-media/latest/index.html)
- [AI for Media Private Access Program](https://developer.nvidia.com/topics/ai/generative-ai/ai-for-media/private-access)

---
