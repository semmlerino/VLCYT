#!/usr/bin/env python3
"""
Setup script for VLCYT YouTube Player
Handles installation of dependencies and initial setup.
"""

import os
import platform
import subprocess
import sys
from pathlib import Path


def run_command(cmd, check=True, shell=False):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            cmd, check=check, capture_output=True, text=True, shell=shell
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr
    except FileNotFoundError:
        return (
            False,
            "",
            f"Command not found: {cmd[0] if isinstance(cmd, list) else cmd}",
        )


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python version: {sys.version}")
    return True


def check_system_dependencies():
    """Check for system-level dependencies."""
    print("\n🔍 Checking system dependencies...")

    # Check for VLC
    vlc_found = False
    vlc_paths = [
        "/usr/bin/vlc",
        "/usr/local/bin/vlc",
        "/Applications/VLC.app/Contents/MacOS/VLC",
        "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
        "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe",
    ]

    for vlc_path in vlc_paths:
        if os.path.exists(vlc_path):
            vlc_found = True
            print(f"✅ VLC found at: {vlc_path}")
            break

    if not vlc_found:
        success, stdout, stderr = run_command(["vlc", "--version"])
        if success:
            print("✅ VLC found in PATH")
            vlc_found = True

    if not vlc_found:
        print("⚠️  VLC Media Player not found!")
        print("   Please install VLC from: https://www.videolan.org/vlc/")
        if platform.system() == "Linux":
            print("   Ubuntu/Debian: sudo apt install vlc")
            print("   Fedora: sudo dnf install vlc")
            print("   Arch: sudo pacman -S vlc")
        elif platform.system() == "Darwin":
            print("   macOS: brew install --cask vlc")
        return False

    return True


def setup_virtual_environment():
    """Set up virtual environment if needed."""
    venv_path = Path("venv")

    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True

    print("🔧 Creating virtual environment...")
    success, stdout, stderr = run_command(
        [sys.executable, "-m", "venv", "venv", "--system-site-packages"]
    )

    if not success:
        print(f"❌ Failed to create virtual environment: {stderr}")
        return False

    print("✅ Virtual environment created")
    return True


def install_python_dependencies():
    """Install Python dependencies."""
    print("\n📦 Installing Python dependencies...")

    # Check if we're in a virtual environment or can use pip directly
    pip_cmd = None

    # Try virtual environment first
    if os.path.exists("venv"):
        if platform.system() == "Windows":
            pip_cmd = ["venv\\Scripts\\pip.exe"]
        else:
            pip_cmd = ["venv/bin/pip"]

    # Fall back to system pip
    if not pip_cmd or not os.path.exists(pip_cmd[0]):
        pip_cmd = ["pip3"] if os.path.exists("/usr/bin/pip3") else ["pip"]

    # Install requirements
    install_cmd = pip_cmd + ["install", "-r", "requirements.txt"]

    print(f"Running: {' '.join(install_cmd)}")
    success, stdout, stderr = run_command(install_cmd)

    if not success:
        print(f"❌ Failed to install dependencies: {stderr}")

        # Try alternative installation methods
        print("\n🔄 Trying alternative installation...")

        # Try with --user flag
        user_cmd = pip_cmd + ["install", "--user", "-r", "requirements.txt"]
        success, stdout, stderr = run_command(user_cmd)

        if not success:
            print(f"❌ Alternative installation failed: {stderr}")
            print("\n💡 Manual installation options:")
            print("1. Create virtual environment: python3 -m venv venv")
            print(
                "2. Activate it: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)"
            )
            print("3. Install deps: pip install -r requirements.txt")
            print("\nOr install system packages:")
            if platform.system() == "Linux":
                print("   sudo apt install python3-pyside6 python3-requests")
            return False
        else:
            print("✅ Dependencies installed with --user flag")
    else:
        print("✅ Dependencies installed successfully")

    return True


def test_imports():
    """Test that all critical imports work."""
    print("\n🧪 Testing imports...")

    test_modules = [
        ("PySide6.QtCore", "PySide6 Qt framework"),
        ("vlc", "python-vlc bindings"),
        ("yt_dlp", "yt-dlp YouTube extractor"),
        ("requests", "HTTP requests library"),
    ]

    all_good = True

    for module, description in test_modules:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError as e:
            print(f"❌ {module} - {description}: {e}")
            all_good = False

    # Test our custom modules
    custom_modules = ["exceptions", "validators", "logging_config"]
    for module in custom_modules:
        try:
            __import__(module)
            print(f"✅ {module} - Custom module")
        except ImportError as e:
            print(f"❌ {module} - Custom module: {e}")
            all_good = False

    return all_good


def create_run_script():
    """Create platform-specific run scripts."""
    print("\n📝 Creating run scripts...")

    # Linux/Mac script
    run_script = """#!/bin/bash
# VLCYT YouTube Player launcher script

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the application
echo "Starting VLCYT YouTube Player..."
python3 VLCYT.py "$@"
"""

    with open("run.sh", "w") as f:
        f.write(run_script)

    os.chmod("run.sh", 0o755)
    print("✅ Created run.sh")

    # Windows script
    windows_script = """@echo off
REM VLCYT YouTube Player launcher script

REM Check if virtual environment exists and activate it
if exist "venv\\Scripts\\activate.bat" (
    echo Activating virtual environment...
    call venv\\Scripts\\activate.bat
)

REM Run the application
echo Starting VLCYT YouTube Player...
python VLCYT.py %*
"""

    with open("run.bat", "w") as f:
        f.write(windows_script)

    print("✅ Created run.bat")


def main():
    """Main setup routine."""
    print("🚀 VLCYT YouTube Player Setup")
    print("=" * 40)

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Check system dependencies
    if not check_system_dependencies():
        print("\n⚠️  Setup completed with warnings.")
        print("Please install VLC Media Player before running the application.")

    # Set up virtual environment
    if not setup_virtual_environment():
        print("⚠️  Continuing without virtual environment...")

    # Install Python dependencies
    if not install_python_dependencies():
        print("\n❌ Setup failed due to dependency installation issues.")
        sys.exit(1)

    # Test imports
    if not test_imports():
        print("\n⚠️  Some imports failed. The application may not work correctly.")

    # Create run scripts
    create_run_script()

    print("\n✅ Setup completed successfully!")
    print("\n🎯 To run the application:")
    print("   Linux/Mac: ./run.sh")
    print("   Windows:   run.bat")
    print("   Direct:    python3 VLCYT.py")

    print("\n📁 Log files will be created in: ~/.vlcyt/logs/")


if __name__ == "__main__":
    main()
