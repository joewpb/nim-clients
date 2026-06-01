# NVIDIA Studio Voice ST 2110 NIM

## Overview

The Studio Voice ST 2110 NIM is designed for live broadcast and production workflows that need real-time speech enhancement over IP media networks. The NIM ingests a single PCM audio stream over SMPTE ST 2110-30, performs AI-based speech enhancement, and publishes enhanced audio over SMPTE ST 2110-30 for downstream broadcast equipment.

Studio Voice enhances input speech recorded through low-quality microphones in noisy and reverberant environments to produce studio-recorded quality speech. For SMPTE ST 2110 deployments, this NIM is intended to run with [NVIDIA Holoscan for Media](https://docs.nvidia.com/holoscan-for-media/latest/index.html).

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

helm pull nim-repo/nvidia-studio-voice-h4m-sample   --version 1.2.0
helm pull nim-repo/nvidia-studio-voice-h4m-service  --version 1.2.0
helm pull nim-repo/nvidia-studio-voice-h4m-operator --version 1.2.0
```

| Chart | Description |
|-------|-------------|
| `nvidia-studio-voice-h4m-sample` | End-to-end demo deployment including sender, Studio Voice NIM service, and receiver. |
| `nvidia-studio-voice-h4m-service` | Standalone Studio Voice ST 2110 NIM service for integration into custom pipelines. |
| `nvidia-studio-voice-h4m-operator` | Kubernetes operator and `NvidiaStudioVoiceMediaFunction` Custom Resource Definition. |

For initial evaluation, the sample chart provides a complete end-to-end pipeline. For production integration, use the NIM service chart for direct deployment or the operator chart for Kubernetes-native lifecycle management.

---

## Container Images

| Image | Description |
|-------|-------------|
| `nvcr.io/nim/nvidia/studio-voice-h4m` | Studio Voice ST 2110 NIM |
| `nvcr.io/nim/nvidia/studio-voice-h4m-operator` | Kubernetes operator |
| `nvcr.io/nim/nvidia/studio-voice-h4m-sample-client` | Sample client used by the demo chart sender and receiver |

---

## Try Out Studio Voice

You can try out the feature here: [Studio Voice](https://build.nvidia.com/nvidia/studiovoice).

---

## Documentation

- [Developer Guide](https://docs.nvidia.com/nim/maxine/studio-voice-h4m/latest/index.html)
- [NVIDIA Holoscan for Media](https://docs.nvidia.com/holoscan-for-media/latest/index.html)

---
