#!/bin/bash
# VLCYT YouTube Player launcher script

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the application
echo "Starting VLCYT YouTube Player..."
python3 VLCYT.py "$@"
