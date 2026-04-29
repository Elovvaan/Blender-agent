from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


def default_export_dir() -> Path:
    return Path.home() / "Desktop" / "SANE_Exports"


def _script_result(success: bool, code: str = "", errors: list[str] | None = None) -> Dict[str, Any]:
    return {
        "success": success,
        "objects_created": [],
        "file_path": "",
        "errors": errors or [],
        "script": code,
    }


def export_fbx_script(filename: str = "scene_export.fbx") -> Dict[str, Any]:
    export_dir = default_export_dir().as_posix()
    file_path = f"{export_dir}/{filename}"
    code = f"""
import bpy, os
export_dir = r\"{export_dir}\"
os.makedirs(export_dir, exist_ok=True)
file_path = r\"{file_path}\"
bpy.ops.export_scene.fbx(filepath=file_path, use_selection=False, apply_unit_scale=True)
result = {{
    \"success\": True,
    \"objects_created\": [],
    \"file_path\": file_path,
    \"errors\": []
}}
""".strip()
    return _script_result(True, code)


def export_glb_script(filename: str = "scene_export.glb") -> Dict[str, Any]:
    export_dir = default_export_dir().as_posix()
    file_path = f"{export_dir}/{filename}"
    code = f"""
import bpy, os
export_dir = r\"{export_dir}\"
os.makedirs(export_dir, exist_ok=True)
file_path = r\"{file_path}\"
bpy.ops.export_scene.gltf(filepath=file_path, export_format='GLB', use_selection=False)
result = {{
    \"success\": True,
    \"objects_created\": [],
    \"file_path\": file_path,
    \"errors\": []
}}
""".strip()
    return _script_result(True, code)
