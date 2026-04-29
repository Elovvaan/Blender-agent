from __future__ import annotations

from typing import Any, Dict


def create_stone_material_script(material_name: str = "SANE_Stone") -> Dict[str, Any]:
    code = f"""
import bpy
mat = bpy.data.materials.new(name=\"{material_name}\")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get('Principled BSDF')
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0.35, 0.35, 0.35, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.9
result = {{
    \"success\": True,
    \"objects_created\": [mat.name],
    \"file_path\": \"\",
    \"errors\": []
}}
""".strip()
    return {
        "success": True,
        "objects_created": [],
        "file_path": "",
        "errors": [],
        "script": code,
    }
