# SANE Blender Agent V1

## Folder Tree

```
SANE-Blender-Agent-V1/
  server.py
  blender_bridge.py
  tools/
    mesh_tools.py
    export_tools.py
    material_tools.py
  logs/
  start-agent.bat
  start-blender-bridge.bat
  test.bat
  requirements.txt
  README.md
  tests/test_suite.py
```

## Setup (Fresh Windows Machine)

1. Install Python 3.10+ and Blender.
2. Unzip `SANE-Blender-Agent-V1`.
3. Double-click `start-blender-bridge.bat`.
4. Double-click `start-agent.bat`.

## Exact Commands (PowerShell/CMD)

```bat
cd SANE-Blender-Agent-V1
start-blender-bridge.bat
start-agent.bat
```

## Health Tests

```bat
curl http://127.0.0.1:3100/health
curl http://127.0.0.1:3100/tools
test.bat
```

## Demo Command (Create Mesh + Export for Unreal)

```bat
curl -X POST http://127.0.0.1:3100/agent/chat -H "Content-Type: application/json" -d "{\"message\":\"build me a stone platform\"}"
curl -X POST http://127.0.0.1:3100/agent/chat -H "Content-Type: application/json" -d "{\"message\":\"export this for Unreal\"}"
```

Exports are written to:

`%USERPROFILE%\Desktop\SANE_Exports`

## Endpoints

- `GET /health`
- `GET /tools`
- `POST /tool/run_blender_python`
- `POST /tool/create_cube`
- `POST /tool/create_building`
- `POST /tool/create_platform`
- `POST /tool/create_tree`
- `POST /tool/create_terrain_tile`
- `POST /tool/export_fbx`
- `POST /tool/export_glb`
- `POST /agent/chat`

## Notes

- If Blender bridge is not running on `127.0.0.1:6789`, tools return a real JSON error.
- If Ollama is unavailable, chat routing falls back to keyword routing.
