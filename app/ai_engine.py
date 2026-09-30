"""AI provider boundary.

The prototype uses DemoEngine so it runs without model downloads or credentials.
SnapdragonAIEngine is the integration boundary for a Qualcomm AI Hub / Snapdragon
runtime implementation. Do not claim NPU execution until it has been validated on
the target Snapdragon-powered HP PC.
"""
class DemoEngine:
    name = 'demo-local'

class SnapdragonAIEngine:
    name = 'snapdragon-ai'
    def generate(self, image_path, text):
        raise NotImplementedError('Connect this provider to the validated Qualcomm AI Hub runtime/model.')
