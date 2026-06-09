# NVIDIA LipSync ST 2110 NIM

## Overview

The LipSync ST 2110 NIM is designed for real-time dubbing and localization workflows in live IP broadcast environments. The feature processes video and speech inputs to generate lip movements synchronized with the input speech while preserving the rest of the video.

The NIM supports per-frame speaker bounding box metadata for targeted lip synchronization in multi-speaker scenes. For SMPTE ST 2110 deployments, this NIM is intended to run with [NVIDIA Holoscan for Media](https://docs.nvidia.com/holoscan-for-media/latest/index.html).

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

helm pull nim-repo/nvidia-lipsync-h4m-sample   --version 1.0.0
helm pull nim-repo/nvidia-lipsync-h4m-service  --version 1.0.0
helm pull nim-repo/nvidia-lipsync-h4m-operator --version 1.0.0
```

| Chart | Description |
|-------|-------------|
| `nvidia-lipsync-h4m-sample` | End-to-end demo deployment including sender, LipSync NIM service, and receiver. |
| `nvidia-lipsync-h4m-service` | Standalone LipSync NIM service for integration into custom pipelines. |
| `nvidia-lipsync-h4m-operator` | Kubernetes operator and `NvidiaLipsyncMediaFunction` Custom Resource Definition. |

For initial evaluation, the sample chart provides a complete end-to-end pipeline. For production integration, use the NIM service chart for direct deployment or the operator chart for Kubernetes-native lifecycle management.

---

## Container Images

| Image | Description |
|-------|-------------|
| `nvcr.io/nim/nvidia/lipsync-h4m-nim` | LipSync NIM |
| `nvcr.io/nim/nvidia/lipsync-h4m-operator` | Kubernetes operator |
| `nvcr.io/nim/nvidia/lipsync-h4m-sample-sender` | Sample sender (for the demo chart) |
| `nvcr.io/nim/nvidia/lipsync-h4m-sample-receiver` | Sample receiver (for the demo chart) |

---

## Try It Out

You can try out the feature here: [https://build.nvidia.com/nvidia/lipsync](https://build.nvidia.com/nvidia/lipsync)

---

## Documentation

- [Developer Guide](https://docs.nvidia.com/nim/maxine/lipsync-h4m/latest/getting-started.html)
- [NVIDIA Holoscan for Media](https://docs.nvidia.com/holoscan-for-media/latest/index.html)
- [AI for Media Private Access Program](https://developer.nvidia.com/topics/ai/generative-ai/ai-for-media/private-access)

---
