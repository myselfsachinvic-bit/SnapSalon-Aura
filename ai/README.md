# AI integration

SnapSalon Aura separates the application from the model provider.

- `DemoEngine`: dependency-free local prototype used for reproducible judging/demo.
- `SnapdragonAIEngine`: integration boundary for the Qualcomm AI Hub/Snapdragon runtime.

This separation prevents unsupported hardware or model claims while keeping the architecture ready for the Snapdragon implementation.
