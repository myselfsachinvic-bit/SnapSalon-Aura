import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND = os.path.join(ROOT, "frontend")
PASSPORT_FILE = os.path.join(ROOT, "data", "style_passport.json")

os.makedirs(os.path.dirname(PASSPORT_FILE), exist_ok=True)


def load_passport():
    if not os.path.exists(PASSPORT_FILE):
        return {"styles": [], "preferences": {}}

    try:
        with open(PASSPORT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"styles": [], "preferences": {}}


def save_passport(data):
    with open(PASSPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def infer_brief(text):
    t = (text or "").lower()

    keep = []
    change = []
    avoid = []

    if any(x in t for x in [
        "top long",
        "keep the top",
        "keep top",
        "length on top",
        "top length"
    ]):
        keep.append("Top length")

    if any(x in t for x in [
        "texture",
        "textured",
        "natural"
    ]):
        keep.append("Natural texture")

    if any(x in t for x in [
        "side",
        "sides",
        "cleaner sides",
        "fade"
    ]):
        change.append("Cleaner sides")

    if any(x in t for x in [
        "short side",
        "very short",
        "skin fade"
    ]):
        avoid.append("Very short sides")

    if any(x in t for x in [
        "low maintenance",
        "low-maintenance",
        "easy",
        "simple"
    ]):
        maintenance = "Low"

    elif any(x in t for x in [
        "high maintenance",
        "styling",
        "daily"
    ]):
        maintenance = "High"

    else:
        maintenance = "Medium"

    if not keep:
        keep = ["Overall reference shape"]

    if not change:
        change = [
            "Adapt shape to hair length and barber recommendation"
        ]

    if not avoid:
        avoid = [
            "Changes that conflict with the stated preferences"
        ]

    desc = (
        "Reference-inspired hairstyle with user-selected preferences."
    )

    questions = [
        "What guard or cutting technique best matches the requested sides?",
        "How often should this style be trimmed?"
    ]

    return {
        "reference_description": desc,
        "keep": keep,
        "change": change,
        "avoid": avoid,
        "maintenance": maintenance,
        "questions_for_barber": questions,
        "engine": "Demo local engine (deterministic prototype)",
        "privacy": (
            "No image is uploaded by this demo server; "
            "preferences are stored locally."
        )
    }


def get_ai_status():
    return {
        "application": "SnapSalon Aura",
        "mode": "demo-local",
        "network_required": False,

        "target": {
            "platform": "Windows on Snapdragon",
            "device": "Snapdragon-powered HP PC",
            "execution": "On-device AI target"
        },

        "vision": {
            "model": "Qwen3-VL-4B-Instruct",
            "provider": "Qualcomm AI Hub",
            "purpose": "Hairstyle image + preference understanding",
            "status": "integration-ready"
        },

        "speech": {
            "model": "Distil-Whisper",
            "provider": "Qualcomm AI Hub",
            "purpose": "Voice preference transcription",
            "status": "integration-ready"
        },

        "runtime": {
            "target": "Qualcomm Snapdragon AI runtime",
            "status": "integration-ready"
        },

        "validation": {
            "npu_verified": False,
            "latency_ms": None,
            "memory_mb": None,
            "note": (
                "Application-level Snapdragon measurements "
                "must be recorded on the target HP Snapdragon PC."
            )
        },

        "privacy": {
            "image_cloud_upload": False,
            "voice_cloud_upload": False,
            "style_passport_storage": "Local",
            "identity_recognition": False
        }
    }


class Handler(BaseHTTPRequestHandler):

    def _send(
        self,
        status,
        content,
        content_type="application/json; charset=utf-8"
    ):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

        if isinstance(content, str):
            content = content.encode("utf-8")

        self.wfile.write(content)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/api/passport":
            self._send(
                200,
                json.dumps(load_passport())
            )
            return

        if path == "/api/health":
            self._send(
                200,
                json.dumps({
                    "status": "ok",
                    "engine": "demo-local",
                    "network_required": False
                })
            )
            return

        if path == "/api/ai/status":
            self._send(
                200,
                json.dumps(
                    get_ai_status(),
                    ensure_ascii=False,
                    indent=2
                )
            )
            return

        if path == "/":
            path = "/index.html"

        safe = os.path.normpath(path.lstrip("/"))
        full = os.path.join(FRONTEND, safe)

        frontend_root = os.path.abspath(FRONTEND)

        if (
            not os.path.abspath(full).startswith(frontend_root)
            or not os.path.isfile(full)
        ):
            self._send(
                404,
                "Not found",
                "text/plain; charset=utf-8"
            )
            return

        ext = os.path.splitext(full)[1]

        ctype = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".svg": "image/svg+xml",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg"
        }.get(
            ext,
            "application/octet-stream"
        )

        with open(full, "rb") as f:
            self._send(
                200,
                f.read(),
                ctype
            )

    def do_POST(self):
        path = urlparse(self.path).path

        length = int(
            self.headers.get("Content-Length", "0")
        )

        try:
            body = json.loads(
                self.rfile.read(length) or "{}"
            )
        except Exception:
            body = {}

        if path == "/api/generate":
            brief = infer_brief(
                body.get("preferences", "")
            )

            self._send(
                200,
                json.dumps(
                    brief,
                    ensure_ascii=False
                )
            )
            return

        if path == "/api/passport":
            data = load_passport()
            brief = body.get("brief") or {}

            entry = {
                "reference_description":
                    brief.get(
                        "reference_description",
                        ""
                    ),

                "maintenance":
                    brief.get(
                        "maintenance",
                        ""
                    ),

                "keep":
                    brief.get(
                        "keep",
                        []
                    ),

                "avoid":
                    brief.get(
                        "avoid",
                        []
                    )
            }

            data["styles"].insert(
                0,
                entry
            )

            data["styles"] = data["styles"][:10]

            data["preferences"] = {
                "maintenance":
                    entry["maintenance"],

                "keep":
                    entry["keep"],

                "avoid":
                    entry["avoid"]
            }

            save_passport(data)

            self._send(
                201,
                json.dumps(
                    data,
                    ensure_ascii=False
                )
            )
            return

        self._send(
            404,
            "Not found",
            "text/plain; charset=utf-8"
        )

    def log_message(self, fmt, *args):
        print(
            "[SnapSalon Aura]",
            fmt % args
        )


if __name__ == "__main__":
    print(
        "SnapSalon Aura running at "
        "http://127.0.0.1:8000"
    )

    print(
        "Demo engine: local deterministic "
        "prototype; no network required."
    )

    print(
        "AI status: "
        "http://127.0.0.1:8000/api/ai/status"
    )

    ThreadingHTTPServer(
        ("127.0.0.1", 8000),
        Handler
    ).serve_forever()