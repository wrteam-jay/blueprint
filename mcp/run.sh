#!/usr/bin/env bash
# Blueprint MCP server launcher
# Creates a venv if needed, installs dependencies, and runs the server.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/venv"
REQ_FILE="${SCRIPT_DIR}/requirements.txt"
REQ_HASH_FILE="${VENV_DIR}/.req_hash"

# Create venv if it doesn't exist
if [ ! -d "${VENV_DIR}" ]; then
    python3 -m venv "${VENV_DIR}" 2>/dev/null
fi

# Install/update dependencies if requirements changed
CURRENT_HASH=$(md5sum "${REQ_FILE}" 2>/dev/null | cut -d' ' -f1 || md5 -q "${REQ_FILE}" 2>/dev/null || echo "unknown")
STORED_HASH=$(cat "${REQ_HASH_FILE}" 2>/dev/null || echo "none")

if [ "${CURRENT_HASH}" != "${STORED_HASH}" ]; then
    "${VENV_DIR}/bin/pip" install -q -r "${REQ_FILE}" 2>/dev/null
    echo "${CURRENT_HASH}" > "${REQ_HASH_FILE}"
fi

# Run the server from the mcp directory so Python finds the src package
export PROJECT_ROOT="${PROJECT_ROOT:-$(pwd)}"
cd "${SCRIPT_DIR}"
exec "${VENV_DIR}/bin/python" -m src.server
