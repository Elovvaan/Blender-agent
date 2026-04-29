@echo off
setlocal ENABLEDELAYEDEXPANSION
cd /d "%~dp0"
if not exist logs mkdir logs
set "BLENDER_EXE="
for /d %%D in ("C:\Program Files\Blender Foundation\Blender*" "C:\Program Files\Blender Foundation\*") do (
  if exist "%%~fD\blender.exe" set "BLENDER_EXE=%%~fD\blender.exe"
)
if "%BLENDER_EXE%"=="" (
  echo Blender not auto-detected.
  set /p BLENDER_EXE=Enter full path to blender.exe: 
)
if not exist "%BLENDER_EXE%" (
  echo ERROR: blender.exe not found: %BLENDER_EXE%
  exit /b 1
)
set "BRIDGE_SCRIPT=%~dp0blender_bridge.py"
"%BLENDER_EXE%" --python "%BRIDGE_SCRIPT%"
