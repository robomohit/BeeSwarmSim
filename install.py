"""
BSS Pro Macro - Installation Script
Automated installation and setup for BSS Pro Macro
"""

import os
import sys
import subprocess
import urllib.request
import json
from pathlib import Path

def print_header():
    """Print installation header"""
    print("=" * 60)
    print("  BSS Pro Macro v1.0.0 - Installation Script")
    print("  Advanced Bee Swarm Simulator Automation")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("❌ Python 3.7 or higher is required")
        print("Please install Python 3.7+ from https://python.org")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_pip():
    """Check if pip is available"""
    print("Checking pip availability...")
    
    try:
        import pip
        print("✅ pip is available")
        return True
    except ImportError:
        print("❌ pip is not available")
        print("Please install pip or use a Python installation that includes pip")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    
    requirements = [
        "opencv-python==4.8.1.78",
        "pillow==10.0.1",
        "pyautogui==0.9.54",
        "numpy==1.24.3",
        "keyboard==0.13.5",
        "psutil==5.9.5",
        "requests==2.31.0"
    ]
    
    failed_packages = []
    
    for package in requirements:
        try:
            print(f"Installing {package}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {package} installed successfully")
            else:
                print(f"❌ Failed to install {package}")
                print(f"Error: {result.stderr}")
                failed_packages.append(package)
                
        except Exception as e:
            print(f"❌ Error installing {package}: {e}")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n❌ Failed to install: {', '.join(failed_packages)}")
        print("Please install them manually using:")
        for package in failed_packages:
            print(f"  pip install {package}")
        return False
    
    print("✅ All dependencies installed successfully")
    return True

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    
    directories = [
        "templates",
        "logs", 
        "screenshots",
        "configs",
        "backups"
    ]
    
    for directory in directories:
        try:
            Path(directory).mkdir(exist_ok=True)
            print(f"✅ Created directory: {directory}")
        except Exception as e:
            print(f"❌ Failed to create directory {directory}: {e}")
            return False
    
    return True

def create_template_placeholders():
    """Create placeholder template files"""
    print("Creating template placeholders...")
    
    templates_dir = Path("templates")
    
    # Create placeholder template files
    template_files = [
        "hive_entrance.png",
        "honey_dispenser.png", 
        "bag_full.png",
        "field_sunflower.png",
        "mob_ladybug.png",
        "npc_black_bear.png",
        "quest_dialog.png",
        "active_planter.png",
        "boost_field_dice.png"
    ]
    
    for template_file in template_files:
        template_path = templates_dir / template_file
        try:
            if not template_path.exists():
                # Create empty placeholder file
                template_path.touch()
                print(f"✅ Created template placeholder: {template_file}")
        except Exception as e:
            print(f"❌ Failed to create template {template_file}: {e}")
    
    print("⚠️  Template placeholders created - you'll need to add actual template images")
    return True

def create_desktop_shortcut():
    """Create desktop shortcut (Windows only)"""
    if os.name != 'nt':
        return True
    
    print("Creating desktop shortcut...")
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "BSS Pro Macro.lnk")
        target_path = os.path.join(os.getcwd(), "bss_pro_macro.py")
        working_directory = os.getcwd()
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target_path}"'
        shortcut.WorkingDirectory = working_directory
        shortcut.IconLocation = target_path
        shortcut.save()
        
        print("✅ Desktop shortcut created")
        return True
        
    except ImportError:
        print("⚠️  Could not create desktop shortcut (winshell not available)")
        return True
    except Exception as e:
        print(f"⚠️  Could not create desktop shortcut: {e}")
        return True

def test_installation():
    """Test if installation was successful"""
    print("Testing installation...")
    
    try:
        # Test imports
        import cv2
        import numpy as np
        from PIL import Image
        import pyautogui
        import keyboard
        import psutil
        
        print("✅ All dependencies import successfully")
        
        # Test main module
        if os.path.exists("bss_pro_macro.py"):
            print("✅ Main macro file found")
        else:
            print("❌ Main macro file not found")
            return False
        
        # Test config file
        if os.path.exists("config.json"):
            print("✅ Configuration file found")
        else:
            print("❌ Configuration file not found")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def print_next_steps():
    """Print next steps after installation"""
    print("\n" + "=" * 60)
    print("  Installation Complete!")
    print("=" * 60)
    print()
    print("Next Steps:")
    print("1. Start Roblox and load Bee Swarm Simulator")
    print("2. Run the macro:")
    print("   • GUI Mode: python bss_pro_macro.py")
    print("   • Console Mode: python bss_pro_macro.py --console")
    print("3. Configure settings in the GUI")
    print("4. Add template images to the 'templates' folder")
    print("5. Start with a short test run")
    print()
    print("Important Notes:")
    print("• Template images are required for image recognition")
    print("• Start with conservative settings for testing")
    print("• Monitor the macro during initial runs")
    print("• Use breaks and safety features")
    print()
    print("Hotkeys:")
    print("• F1: Start/Stop Macro")
    print("• F2: Pause/Resume")
    print("• F3: Emergency Stop")
    print("• F4: Show/Hide GUI")
    print()
    print("For help, check README.md or the troubleshooting section.")
    print("=" * 60)

def main():
    """Main installation function"""
    print_header()
    
    # Check requirements
    if not check_python_version():
        input("Press Enter to exit...")
        return False
    
    if not check_pip():
        input("Press Enter to exit...")
        return False
    
    # Install components
    success = True
    
    if not install_dependencies():
        success = False
    
    if not create_directories():
        success = False
    
    if not create_template_placeholders():
        success = False
    
    create_desktop_shortcut()  # Optional, don't fail on this
    
    if not test_installation():
        success = False
    
    if success:
        print_next_steps()
    else:
        print("\n❌ Installation encountered errors.")
        print("Please check the error messages above and try again.")
        print("You may need to install dependencies manually.")
    
    input("\nPress Enter to exit...")
    return success

if __name__ == "__main__":
    main()