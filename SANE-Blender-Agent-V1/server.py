from __future__ import annotations

import json
import logging
import socket
from pathlib import Path
from typing import Any

import requests
from fastapi import FastAPI
from pydantic import BaseModel

from tools.export_tools import export_fbx_script, export_glb_script
from tools.mesh_tools import (
    create_building_script,
    create_cube_script,
    create_platform_script,
    create_terrain_tile_script,
    create_tree_script,
)

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
logger = logging.getLogger("agent")
logger.setLevel(logging.INFO)
if not logger.handlers:
    fh = logging.FileHandler(LOG_DIR / "agent.log", encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)

app = FastAPI(title="SANE Blender Agent V1")


class ScriptPayload(BaseModel):
    script: str


class ChatPayload(BaseModel):
    message: str


def response(success: bool, objects_created: list[str] | None = None, file_path: str = "", errors: list[str] | None = None) -> dict[str, Any]:
    return {
        "success": success,
        "objects_created": objects_created or [],
        "file_path": file_path,
        "errors": errors or [],
    }


def run_blender_script(script: str) -> dict[str, Any]:
    try:
        with socket.create_connection(("127.0.0.1", 6789), timeout=15) as sock:
            sock.sendall((json.dumps({"script": script}) + "\n").encode("utf-8"))
            data = b""
            while not data.endswith(b"\n"):
                chunk = sock.recv(4096)
                if not chunk:
                    break
                data += chunk
        if not data:
            return response(False, errors=["No response from Blender bridge."])
        result = json.loads(data.decode("utf-8").strip())
        for key in ["success", "objects_created", "file_path", "errors"]:
            if key not in result:
                return response(False, errors=[f"Malformed response from Blender bridge: missing {key}"])
        return result
    except OSError as ex:
        logger.error("Blender bridge connection failed: %s", ex)
        return response(False, errors=["Blender bridge is not connected on 127.0.0.1:6789."])
    except Exception as ex:
        logger.error("Unexpected run_blender_script failure: %s", ex)
        return response(False, errors=[str(ex)])


def route_message(message: str) -> str:
    text = message.lower()
    if any(k in text for k in ["platform", "stone platform"]):
        return "create_platform"
    if any(k in text for k in ["tree", "low-poly tree", "low poly tree"]):
        return "create_tree"
    if "building" in text:
        return "create_building"
    if "terrain" in text:
        return "create_terrain_tile"
    if "cube" in text:
        return "create_cube"
    if "unreal" in text or "fbx" in text:
        return "export_fbx"
    if "glb" in text or "gltf" in text:
        return "export_glb"
    return "create_cube"


def ollama_route(message: str) -> str | None:
    try:
        prompt = (
            "Choose one tool name only from: create_cube, create_building, create_platform, create_tree, "
            "create_terrain_tile, export_fbx, export_glb. Message: "
            + message
        )
        resp = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=3,
        )
        if resp.status_code == 200:
            response_text = resp.json().get("response", "").strip()
            parts = response_text.split()
            if parts:
                out = parts[0]
                if out in {"create_cube", "create_building", "create_platform", "create_tree", "create_terrain_tile", "export_fbx", "export_glb"}:
                    return out
    except Exception:
        return None
    return None


@app.get("/health")
def health() -> dict[str, Any]:
    bridge_ok = run_blender_script("result = {'success': True, 'objects_created': [], 'file_path': '', 'errors': []}").get("success", False)
    return {"success": True, "objects_created": [], "file_path": "", "errors": [], "bridge_connected": bridge_ok}


@app.get("/tools")
def tools() -> dict[str, Any]:
    return {
        "success": True,
        "objects_created": [],
        "file_path": "",
        "errors": [],
        "tools": [
            "run_blender_python", "create_cube", "create_building", "create_platform", "create_tree",
            "create_terrain_tile", "export_fbx", "export_glb", "agent_chat"
        ],
        "tool_endpoints": {
            "run_blender_python": "/tool/run_blender_python",
            "create_cube": "/tool/create_cube",
            "create_building": "/tool/create_building",
            "create_platform": "/tool/create_platform",
            "create_tree": "/tool/create_tree",
            "create_terrain_tile": "/tool/create_terrain_tile",
            "export_fbx": "/tool/export_fbx",
            "export_glb": "/tool/export_glb",
            "agent_chat": "/agent/chat",
        },
    }


@app.post("/tool/run_blender_python")
def run_blender_python(payload: ScriptPayload):
    return run_blender_script(payload.script)


@app.post("/tool/create_cube")
def create_cube():
    return run_blender_script(create_cube_script()["script"])

@app.post("/tool/create_building")
def create_building():
    return run_blender_script(create_building_script()["script"])

@app.post("/tool/create_platform")
def create_platform():
    return run_blender_script(create_platform_script()["script"])

@app.post("/tool/create_tree")
def create_tree():
    return run_blender_script(create_tree_script()["script"])

@app.post("/tool/create_terrain_tile")
def create_terrain_tile():
    return run_blender_script(create_terrain_tile_script()["script"])

@app.post("/tool/export_fbx")
def export_fbx():
    return run_blender_script(export_fbx_script()["script"])

@app.post("/tool/export_glb")
def export_glb():
    return run_blender_script(export_glb_script()["script"])

@app.post("/agent/chat")
def agent_chat(payload: ChatPayload):
    tool = ollama_route(payload.message) or route_message(payload.message)
    logger.info("Chat route selected: %s for message=%s", tool, payload.message)
    tool_map = {
        "create_cube": create_cube,
        "create_building": create_building,
        "create_platform": create_platform,
        "create_tree": create_tree,
        "create_terrain_tile": create_terrain_tile,
        "export_fbx": export_fbx,
        "export_glb": export_glb,
    }
    return tool_map[tool]()


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting SANE Blender Agent on 127.0.0.1:3100")
    uvicorn.run(app, host="127.0.0.1", port=3100)
