#!/usr/bin/env bash

# ***************************************************************************
# * Tweak variables here
# ***************************************************************************
# Configuration
VENV_NAME=".venv"
REQUIREMENTS_FILE="requirements.txt"
PROGRAM="program.py"
PYTHON_COMMAND="python3"

# ***************************************************************************
# * Don't touch here unless you know what you're doing
# ***************************************************************************
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/${VENV_NAME}"
REQUIREMENTS_PATH="${SCRIPT_DIR}/${REQUIREMENTS_FILE}"
PROGRAM_PATH="${SCRIPT_DIR}/${PROGRAM}"
ACTIVATE_SCRIPT="${VENV_DIR}/bin/activate"
VENV_PYTHON="${VENV_DIR}/bin/python"
FIRST_RUN=0

# ***************************************************************************
# * Current directory accessible?
# ***************************************************************************
cd "${SCRIPT_DIR}" || {
    echo "ERROR: Could not access the script directory [${SCRIPT_DIR}]." >&2
    exit 1
}

# ***************************************************************************
# * Create virtual environment if it doesn't exist
# ***************************************************************************
if [ ! -x "${VENV_PYTHON}" ]; then
    FIRST_RUN=1
    echo "Creating virtual environment [${VENV_NAME}]..."
    if ! "${PYTHON_COMMAND}" -m venv "${VENV_DIR}"; then
        echo "ERROR: Could not create the virtual environment [${VENV_NAME}]." >&2
        exit 1
    fi
fi

# ***************************************************************************
# * Activate the virtual environment
# ***************************************************************************
if ! source "${ACTIVATE_SCRIPT}"; then
    echo "ERROR: Could not activate the virtual environment [${VENV_NAME}]." >&2
    exit 1
fi

# ***************************************************************************
# * Install requirements after first run
# ***************************************************************************
if [ "${FIRST_RUN}" -eq 1 ]; then
    if [ -f "${REQUIREMENTS_PATH}" ]; then
        echo "Installing modules from [${REQUIREMENTS_FILE}]..."
        if ! python -m pip install -r "${REQUIREMENTS_PATH}"; then
            echo "ERROR: Could not install the required modules from [${REQUIREMENTS_FILE}]." >&2
            exit 1
        fi
    else
        echo "INFO: No requirements file [${REQUIREMENTS_FILE}] found."
    fi
fi

# ***************************************************************************
# * Check that the program exists
# ***************************************************************************
if [ ! -f "${PROGRAM_PATH}" ]; then
    echo "ERROR: Program [${PROGRAM}] not found." >&2
    exit 1
fi

echo "Starting [${PROGRAM}]..."
python "${PROGRAM_PATH}" "$@"
PROGRAM_EXIT_CODE=$?

exit "${PROGRAM_EXIT_CODE}"
