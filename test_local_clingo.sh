#!/bin/bash

# Script to test locally built Clingo Python extension
# This sets up all necessary environment variables and paths

# Get the absolute path to the repository root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${REPO_ROOT}/build"

# Determine which python to validate against.
# - If run as: ./test_local_clingo.sh python3 test_clingo.py
#   then validate against that python.
# - If sourced, default to python3 (best effort).
PYTHON_CMD="${1:-python3}"

# Check if build directory exists
if [ ! -d "$BUILD_DIR" ]; then
    echo "Error: Build directory not found at $BUILD_DIR"
    echo "Please build the project first with CMake"
    exit 1
fi

# Check if the Python extension exists
PYTHON_EXT_SUFFIX="$("$PYTHON_CMD" -c 'import sysconfig; print(sysconfig.get_config_var("EXT_SUFFIX") or "")' 2>/dev/null)"
if [ -z "$PYTHON_EXT_SUFFIX" ]; then
    echo "Error: could not determine EXT_SUFFIX from '$PYTHON_CMD'"
    echo "Hint: run './test_local_clingo.sh python3 test_clingo.py' or source the script from an environment with python3."
    exit 1
fi

PYTHON_EXT="${BUILD_DIR}/bin/python/_clingo${PYTHON_EXT_SUFFIX}"
if [ ! -f "$PYTHON_EXT" ]; then
    echo "Error: Python extension not found for $PYTHON_CMD at:"
    echo "  $PYTHON_EXT"
    echo ""
    echo "This usually means clingo was built against a different Python version."
    echo "Reconfigure your build directory with the desired Python, e.g.:"
    echo "  cmake -S . -B build -DPython_EXECUTABLE=\"$($PYTHON_CMD -c 'import sys; print(sys.executable)')\""
    echo "  cmake --build build"
    exit 1
fi

# Check if libclingo exists
LIBCLINGO=""
if [ -f "${BUILD_DIR}/bin/libclingo.dylib" ]; then
    LIBCLINGO="${BUILD_DIR}/bin/libclingo.dylib"
elif [ -f "${BUILD_DIR}/bin/libclingo.so" ]; then
    LIBCLINGO="${BUILD_DIR}/bin/libclingo.so"
else
    # Handle versioned .so names
    LIBCLINGO="$(ls -1 "${BUILD_DIR}/bin/libclingo.so."* 2>/dev/null | head -n 1)"
fi
if [ -z "$LIBCLINGO" ] || [ ! -f "$LIBCLINGO" ]; then
    echo "Error: libclingo shared library not found under ${BUILD_DIR}/bin"
    echo "Please build the project first"
    exit 1
fi

# Set up environment variables
echo "Setting up environment for local Clingo testing..."

# Add the directory containing libclingo to the dynamic library path
if [ "$(uname -s)" = "Darwin" ]; then
    export DYLD_LIBRARY_PATH="${BUILD_DIR}/bin:${DYLD_LIBRARY_PATH}"
else
    export LD_LIBRARY_PATH="${BUILD_DIR}/bin:${LD_LIBRARY_PATH}"
fi

# Add the directory containing the Python extension to Python path
export PYTHONPATH="${BUILD_DIR}/bin/python:${REPO_ROOT}/libpyclingo:${PYTHONPATH}"

echo "Environment configured:"
if [ "$(uname -s)" = "Darwin" ]; then
    echo "  DYLD_LIBRARY_PATH includes: ${BUILD_DIR}/bin"
else
    echo "  LD_LIBRARY_PATH includes: ${BUILD_DIR}/bin"
fi
echo "  PYTHONPATH includes: ${BUILD_DIR}/bin/python and ${REPO_ROOT}/libpyclingo"
echo "  Using extension: ${PYTHON_EXT}"
echo ""

# If arguments are provided, run them as a command
if [ $# -gt 0 ]; then
    echo "Running: $@"
    exec "$@"
else
    echo "Usage: $0 [command]"
    echo "Examples:"
    echo "  $0 python test_clingo.py"
    echo "  $0 python -c \"import clingo; print('Success!')\""
    echo ""
    echo "Or source this script to set up your shell environment:"
    echo "  source $0"
fi
