# SnapSalon Aura

## SEE IT. SAY IT. SAVE IT. BOOK IT.

SnapSalon Aura is a privacy-first AI Style Passport prototype designed for Snapdragon-powered HP PCs. It turns hairstyle inspiration and explicit user preferences into a structured **Barber Brief**, then saves the selected preferences locally as a Style Passport.

## What is implemented

- Hairstyle reference upload UI
- Natural-language style preference input
- Structured Barber Brief generation
- Local Style Passport persistence
- Local-first/offline-capable prototype server
- Clear AI provider boundary for Snapdragon integration
- Privacy and limitation messaging

## Snapdragon AI path

The intended production AI path uses Qualcomm AI Hub models such as Qwen3-VL-4B-Instruct for vision-language understanding and Distil-Whisper for speech-to-text, running through a Qualcomm-supported Snapdragon Windows runtime.

**This repository does not falsely claim NPU execution.** The default demo uses a deterministic local engine so judges can run it without downloading large models. Snapdragon-specific latency, memory and NPU/provider measurements must be recorded on the actual target HP Snapdragon PC after integration.

## Run locally

Requirements: Python 3.9+.

```bat
python app\main.py
```

Then open:

`http://127.0.0.1:8000`

No external package is required for the MVP.

## Demo flow

1. Upload a hairstyle reference.
2. Describe the desired style.
3. Generate the Barber Brief.
4. Save it to the Style Passport.
5. Refresh and verify that the preferences persist locally.
6. For the Snapdragon build, replace the DemoEngine with the validated Qualcomm AI Hub/runtime provider.

## Responsible scope

SnapSalon Aura does not perform identity recognition, medical/dermatological analysis, personality inference, or guaranteed appearance prediction.

## Project structure

```text
app/          Local API and AI-provider boundary
frontend/     Web UI
ai/           Snapdragon model/runtime notes
screenshots/  Demo evidence
```

## Competition

Snapdragon AI Lab Build & Present Challenge.
