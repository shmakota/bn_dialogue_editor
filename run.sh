#!/bin/bash

# Cataclysm: Bright Nights Dialogue Editor - Run Script
# This script sets up a virtual environment and runs the dialogue editor

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${GREEN}Cataclysm: Bright Nights Dialogue Editor${NC}"
echo "======================================"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is not installed or not in PATH${NC}"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info[0])')
PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info[1])')

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
    echo -e "${RED}Error: Python 3.7 or higher is required (found $PYTHON_VERSION)${NC}"
    exit 1
fi

echo -e "${GREEN}Python version: $PYTHON_VERSION${NC}"
echo ""

# Virtual environment directory
VENV_DIR="venv"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}Virtual environment created${NC}"
else
    echo -e "${GREEN}Virtual environment already exists${NC}"
fi

echo ""

# Activate virtual environment and install requirements
echo -e "${YELLOW}Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
python -m pip install --upgrade pip --quiet

# Install requirements
echo -e "${YELLOW}Installing requirements...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    echo -e "${GREEN}Requirements installed${NC}"
else
    echo -e "${YELLOW}No requirements.txt found (no external dependencies needed)${NC}"
fi

echo ""

# Check for tkinter
echo -e "${YELLOW}Checking for tkinter...${NC}"
if python -c "import tkinter" 2>/dev/null; then
    echo -e "${GREEN}tkinter is available${NC}"
else
    echo -e "${RED}Error: tkinter is not available${NC}"
    echo "Please install tkinter:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  Fedora: sudo dnf install python3-tkinter"
    echo "  macOS: tkinter should be included with Python"
    echo "  Windows: tkinter should be included with Python"
    deactivate
    exit 1
fi

# Check DISPLAY variable (for X11)
if [ -z "$DISPLAY" ] && [ "$XDG_SESSION_TYPE" != "wayland" ]; then
    echo -e "${YELLOW}Warning: DISPLAY variable is not set${NC}"
    echo "This might prevent the GUI from opening."
    echo "If you're running via SSH, you may need X11 forwarding."
fi

echo ""
echo -e "${GREEN}Starting Dialogue Editor...${NC}"
echo ""

# Test if tkinter can actually create a window
if ! python -c "import tkinter as tk; root = tk.Tk(); root.destroy()" 2>/dev/null; then
    echo -e "${RED}Error: tkinter cannot create windows. This might be a display/display server issue.${NC}"
    echo "On Linux, ensure you have a display server running (X11 or Wayland)."
    deactivate
    exit 1
fi

# Run the application (with unbuffered output to see errors immediately)
# Don't catch errors - let them show up
python -u main.py

# Only deactivate if we reach here (app closed normally)
deactivate

