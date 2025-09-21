"""
BSS Pro Macro - Test Script
Comprehensive testing and validation script
"""

import os
import sys
import json
import time
import logging
from pathlib import Path

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    
    required_modules = [
        ('cv2', 'opencv-python'),
        ('numpy', 'numpy'), 
        ('PIL', 'pillow'),
        ('pyautogui', 'pyautogui'),
        ('keyboard', 'keyboard'),
        ('psutil', 'psutil'),
        ('tkinter', 'tkinter (built-in)'),
        ('threading', 'threading (built-in)'),
        ('json', 'json (built-in)'),
        ('time', 'time (built-in)'),
        ('random', 'random (built-in)'),
        ('logging', 'logging (built-in)')
    ]
    
    failed_imports = []
    
    for module, package in required_modules:
        try:
            if module == 'PIL':
                from PIL import Image
            elif module == 'cv2':
                import cv2
            else:
                __import__(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - FAILED ({e})")
            failed_imports.append((module, package))
    
    if failed_imports:
        print(f"\n❌ Failed imports: {len(failed_imports)}")
        for module, package in failed_imports:
            print(f"  Install: pip install {package}")
        return False
    
    print(f"✅ All imports successful ({len(required_modules)} modules)")
    return True

def test_files():
    """Test required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'bss_pro_macro.py',
        'main_controller.py',
        'core_systems.py',
        'field_system.py',
        'quest_system.py',
        'mob_system.py',
        'planter_system.py',
        'boost_system.py',
        'gui_interface.py',
        'advanced_safety.py',
        'config.json',
        'requirements.txt',
        'README.md'
    ]
    
    required_directories = [
        'templates',
        'logs',
        'screenshots'
    ]
    
    missing_files = []
    missing_dirs = []
    
    # Check files
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    # Check directories
    for dir_path in required_directories:
        if os.path.isdir(dir_path):
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ - MISSING")
            missing_dirs.append(dir_path)
    
    if missing_files or missing_dirs:
        print(f"\n❌ Missing files: {len(missing_files)}")
        print(f"❌ Missing directories: {len(missing_dirs)}")
        return False
    
    print(f"✅ All files and directories present")
    return True

def test_config():
    """Test configuration file"""
    print("\nTesting configuration...")
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        required_sections = [
            'general', 'farming', 'quests', 'mobs', 
            'planters', 'boosts', 'hive', 'dispensers', 
            'safety', 'hotkeys'
        ]
        
        missing_sections = []
        for section in required_sections:
            if section in config:
                print(f"✅ config['{section}']")
            else:
                print(f"❌ config['{section}'] - MISSING")
                missing_sections.append(section)
        
        if missing_sections:
            print(f"❌ Missing config sections: {missing_sections}")
            return False
        
        print("✅ Configuration file valid")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config.json: {e}")
        return False
    except FileNotFoundError:
        print("❌ config.json not found")
        return False
    except Exception as e:
        print(f"❌ Config test error: {e}")
        return False

def test_module_loading():
    """Test loading macro modules"""
    print("\nTesting module loading...")
    
    modules_to_test = [
        'core_systems',
        'field_system', 
        'quest_system',
        'mob_system',
        'planter_system',
        'boost_system',
        'gui_interface',
        'advanced_safety',
        'main_controller'
    ]
    
    failed_modules = []
    
    for module_name in modules_to_test:
        try:
            # Add current directory to path
            if '.' not in sys.path:
                sys.path.insert(0, '.')
            
            module = __import__(module_name)
            print(f"✅ {module_name}")
        except ImportError as e:
            print(f"❌ {module_name} - IMPORT ERROR: {e}")
            failed_modules.append(module_name)
        except Exception as e:
            print(f"❌ {module_name} - ERROR: {e}")
            failed_modules.append(module_name)
    
    if failed_modules:
        print(f"❌ Failed to load modules: {failed_modules}")
        return False
    
    print("✅ All modules loaded successfully")
    return True

def test_system_requirements():
    """Test system requirements"""
    print("\nTesting system requirements...")
    
    # Test Python version
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"❌ Python {version.major}.{version.minor} (requires 3.7+)")
        return False
    
    # Test screen resolution
    try:
        import pyautogui
        screen_size = pyautogui.size()
        if screen_size.width >= 1280 and screen_size.height >= 720:
            print(f"✅ Screen resolution: {screen_size.width}x{screen_size.height}")
        else:
            print(f"⚠️  Low screen resolution: {screen_size.width}x{screen_size.height} (recommended: 1280x720+)")
    except Exception as e:
        print(f"⚠️  Could not detect screen resolution: {e}")
    
    # Test system resources
    try:
        import psutil
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        
        if memory_gb >= 4:
            print(f"✅ System RAM: {memory_gb:.1f} GB")
        else:
            print(f"⚠️  Low system RAM: {memory_gb:.1f} GB (recommended: 4GB+)")
        
        cpu_count = psutil.cpu_count()
        print(f"✅ CPU cores: {cpu_count}")
        
    except Exception as e:
        print(f"⚠️  Could not check system resources: {e}")
    
    print("✅ System requirements check completed")
    return True

def test_gui():
    """Test GUI initialization"""
    print("\nTesting GUI initialization...")
    
    try:
        import tkinter as tk
        
        # Test basic tkinter functionality
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        # Test if we can create basic widgets
        frame = tk.Frame(root)
        label = tk.Label(frame, text="Test")
        button = tk.Button(frame, text="Test")
        
        root.destroy()
        
        print("✅ GUI framework functional")
        return True
        
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        return False

def test_image_recognition():
    """Test image recognition capabilities"""
    print("\nTesting image recognition...")
    
    try:
        import cv2
        import numpy as np
        from PIL import Image
        
        # Test OpenCV
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        success = cv2.imwrite('test_image.png', test_image)
        
        if success:
            # Test PIL
            pil_image = Image.open('test_image.png')
            
            # Clean up
            os.remove('test_image.png')
            
            print("✅ Image recognition libraries functional")
            return True
        else:
            print("❌ OpenCV image write failed")
            return False
            
    except Exception as e:
        print(f"❌ Image recognition test failed: {e}")
        return False

def test_input_automation():
    """Test input automation capabilities"""
    print("\nTesting input automation...")
    
    try:
        import pyautogui
        
        # Test basic pyautogui functionality
        screen_size = pyautogui.size()
        current_pos = pyautogui.position()
        
        # Test failsafe
        pyautogui.FAILSAFE = True
        
        print("✅ Input automation functional")
        print(f"   Screen size: {screen_size}")
        print(f"   Mouse position: {current_pos}")
        print(f"   Failsafe: {pyautogui.FAILSAFE}")
        
        return True
        
    except Exception as e:
        print(f"❌ Input automation test failed: {e}")
        return False

def run_comprehensive_test():
    """Run comprehensive test suite"""
    print("=" * 60)
    print("  BSS Pro Macro - Comprehensive Test Suite")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("File Structure Test", test_files),
        ("Configuration Test", test_config),
        ("Module Loading Test", test_module_loading),
        ("System Requirements Test", test_system_requirements),
        ("GUI Test", test_gui),
        ("Image Recognition Test", test_image_recognition),
        ("Input Automation Test", test_input_automation)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed_tests += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    # Test summary
    print("\n" + "=" * 60)
    print("  Test Summary")
    print("=" * 60)
    print(f"Tests passed: {passed_tests}/{total_tests}")
    print(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("✅ ALL TESTS PASSED - Macro is ready to use!")
        print("\nNext steps:")
        print("1. Start Roblox and load Bee Swarm Simulator")
        print("2. Run: python bss_pro_macro.py")
        print("3. Configure settings and start with a test run")
    else:
        print("❌ SOME TESTS FAILED - Please fix issues before using")
        print("\nCommon solutions:")
        print("- Install missing dependencies: pip install -r requirements.txt")
        print("- Check file structure and ensure all files are present")
        print("- Verify Python 3.7+ is installed")
    
    print("=" * 60)
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = run_comprehensive_test()
    
    print("\nPress Enter to exit...")
    input()
    
    sys.exit(0 if success else 1)