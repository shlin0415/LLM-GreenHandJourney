
It is ok to use conda to pnpm in a conda env 

```.bat
@echo off
setlocal enabledelayedexpansion

:: --- SETTINGS ---
set "CONDA_ACTIVATE_PATH=D:\aaa-new\setups\conda\conda-files\Scripts\activate.bat"
set "CONDA_ENV_NAME=2c943ed-lingchat"
:: ----------------

echo [1/4] Activating environment...

if not exist "%CONDA_ACTIVATE_PATH%" (
    echo [ERROR] Cannot find activate.bat at:
    echo %CONDA_ACTIVATE_PATH%
    pause
    exit /b 1
)

:: Activate the environment
call "%CONDA_ACTIVATE_PATH%" %CONDA_ENV_NAME%

echo [2/4] Verifying Node.js...
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found in this environment.
    pause
    exit /b 1
)

echo [3/4] Updating pnpm...
call npm install -g pnpm --quiet

echo [4/4] Starting Vue project...
call pnpm install
call pnpm run dev --host

pause

@REM @echo off
@REM call pnpm install
@REM call pnpm format
@REM call pnpm run dev --host
@REM pause
```
