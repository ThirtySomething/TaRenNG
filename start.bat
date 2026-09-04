@echo off
setlocal

@rem ***************************************************************************
@rem * Tweak variables here
@rem ***************************************************************************
@rem Configuration
set "VENV_NAME=.venv"
set "REQUIREMENTS_FILE=requirements.txt"
set "PROGRAM=program.py"
set "PYTHON_COMMAND=python"

@rem ***************************************************************************
@rem * Don't touch here unless you know what you're doing
@rem ***************************************************************************
set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%%VENV_NAME%"
set "REQUIREMENTS_PATH=%SCRIPT_DIR%%REQUIREMENTS_FILE%"
set "PROGRAM_PATH=%SCRIPT_DIR%%PROGRAM%"
set "ACTIVATE_SCRIPT=%VENV_DIR%\Scripts\activate.bat"
set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"
set "FIRST_RUN=0"

@rem ***************************************************************************
@rem * Current directory accessible?
@rem ***************************************************************************
pushd "%SCRIPT_DIR%" || (
    echo ERROR: Could not access the script directory.
    exit /b 1
)

@rem ***************************************************************************
@rem * Create virtual environment if it doesn't exist
@rem ***************************************************************************
if not exist "%VENV_PYTHON%" (
    set "FIRST_RUN=1"
    echo Creating virtual environment "%VENV_NAME%"...
    call %PYTHON_COMMAND% -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo ERROR: Could not create the virtual environment.
        popd
        exit /b 1
    )

    if not exist "%REQUIREMENTS_PATH%" (
        echo ERROR: Requirements file not found: "%REQUIREMENTS_FILE%"
        popd
        exit /b 1
    )
)

@rem ***************************************************************************
@rem * Activate the virtual environment
@rem ***************************************************************************
call "%ACTIVATE_SCRIPT%"
if errorlevel 1 (
    echo ERROR: Could not activate the virtual environment.
    popd
    exit /b 1
)

@rem ***************************************************************************
@rem * Install requirements after first run
@rem ***************************************************************************
if "%FIRST_RUN%"=="1" (
    echo Installing modules from "%REQUIREMENTS_FILE%"...
    python -m pip install -r "%REQUIREMENTS_PATH%"
    if errorlevel 1 (
        echo ERROR: Could not install the required modules.
        popd
        exit /b 1
    )
)

@rem ***************************************************************************
@rem * Install requirements after first run
@rem ***************************************************************************
if not exist "%PROGRAM_PATH%" (
    echo ERROR: Program not found: "%PROGRAM%"
    popd
    exit /b 1
)

echo Starting "%PROGRAM%"...
python "%PROGRAM_PATH%"
set "PROGRAM_EXIT_CODE=%errorlevel%"

popd
if defined PROGRAM_EXIT_CODE exit /b %PROGRAM_EXIT_CODE%
exit /b 0
