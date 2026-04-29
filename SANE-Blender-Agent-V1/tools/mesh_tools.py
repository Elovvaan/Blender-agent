from __future__ import annotations

from typing import Any, Dict


def _script_result(success: bool, code: str = "", errors: list[str] | None = None) -> Dict[str, Any]:
    return {
        "success": success,
        "objects_created": [],
        "file_path": "",
        "errors": errors or [],
        "script": code,
    }


def create_cube_script(name: str = "SANE_Cube", size: float = 2.0) -> Dict[str, Any]:
    code = f"""
import bpy
bpy.ops.mesh.primitive_cube_add(size={size}, location=(0, 0, {size / 2}))
obj = bpy.context.view_layer.objects.active
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
obj.name = \"{name}\"
result = {{
    \"success\": True,
    \"objects_created\": [obj.name],
    \"file_path\": \"\",
    \"errors\": []
}}
""".strip()
    return _script_result(True, code)


def create_platform_script(name: str = "SANE_Platform", radius: float = 5.0, depth: float = 0.5) -> Dict[str, Any]:
    code = f"""
import bpy
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius={radius}, depth={depth}, location=(0, 0, {depth / 2}))
obj = bpy.context.view_layer.objects.active
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
obj.name = \"{name}\"
result = {{
    \"success\": True,
    \"objects_created\": [obj.name],
    \"file_path\": \"\",
    \"errors\": []
}}
""".strip()
    return _script_result(True, code)


def create_tree_script(name: str = "SANE_Tree") -> Dict[str, Any]:
    code = f"""
import bpy
bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.25, depth=2.5, location=(0, 0, 1.25))
trunk = bpy.context.view_layer.objects.active
bpy.context.view_layer.objects.active = trunk
trunk.select_set(True)
trunk.name = \"{name}_Trunk\"
bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=1.6, depth=3.0, location=(0, 0, 3.5))
canopy = bpy.context.view_layer.objects.active
bpy.context.view_layer.objects.active = canopy
canopy.select_set(True)
canopy.name = \"{name}_Canopy\"
result = {{
    \"success\": True,
    \"objects_created\": [trunk.name, canopy.name],
    \"file_path\": \"\",
    \"errors\": []
}}
""".strip()
    return _script_result(True, code)


def create_building_script(name: str = "SANE_Building", floors: int = 4) -> Dict[str, Any]:
    height = max(2, floors) * 3
    code = f"""
import bpy
bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, {height / 2}))
obj = bpy.context.view_layer.objects.active
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
obj.name = \"{name}\"
obj.scale = (2.5, 2.5, {height / 2})
result = {{
    \"success\": True,
    \"objects_created\": [obj.name],
    \"file_path\": \"\",
    \"errors\": []
}}
""".strip()
    return _script_result(True, code)


def create_terrain_tile_script(name: str = "SANE_TerrainTile", size: float = 10.0) -> Dict[str, Any]:
    code = f"""
import bpy
bpy.ops.mesh.primitive_plane_add(size={size}, location=(0, 0, 0))
obj = bpy.context.view_layer.objects.active
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
obj.name = \"{name}\"
bpy.ops.object.modifier_add(type='SUBSURF')
obj.modifiers[\"Subdivision\"].levels = 2
result = {{
    \"success\": True,
    \"objects_created\": [obj.name],
    \"file_path\": \"\",
    \"errors\": []
}}
""".strip()
    return _script_result(True, code)
