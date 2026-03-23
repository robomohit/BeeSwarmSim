"""
BSS Pro Macro - Main Application
Advanced Bee Swarm Simulator Automation Tool

Features:
- Advanced field farming with rotation
- Automated quest completion for all NPCs
- Intelligent mob hunting and loot collection
- Smart planter management
- Safety features with anti-detection
- Modern GUI interface
- Comprehensive statistics tracking
- Hotkey support

Created by: Claude Sonnet 4
Version: 1.0.0
"""

import sys
import os
import json
import logging
import threading
import time
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main_controller import MacroController, HotkeyHandler
    from gui_interface import MacroGUI
    from core_systems import Logger
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all required dependencies are installed.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

class BSSProMacro:
    """Main application class"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.name = "BSS Pro Macro"
        self.config_file = "config.json"
        
        # Initialize logging
        self.setup_logging()
        
        # Load configuration
        self.config = self.load_config()
        
        # Initialize components
        self.macro_controller = None
        self.gui = None
        self.hotkey_handler = None
        
        logging.info(f"{self.name} v{self.version} starting up...")
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_filename = f"bss_macro_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        # Create logger instance
        self.logger = logging.getLogger(__name__)
    
    def load_config(self):
        """Load configuration file"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            logging.info(f"Configuration loaded from {self.config_file}")
            return config
        except FileNotFoundError:
            logging.warning(f"Config file {self.config_file} not found, creating default")
            return self.create_default_config()
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in config file: {e}")
            return self.create_default_config()
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            return self.create_default_config()
    
    def create_default_config(self):
        """Create and save default configuration"""
        default_config = {
            "general": {
                "macro_name": "BSS Pro Macro",
                "version": "1.0.0",
                "debug_mode": False,
                "safety_enabled": True,
                "randomization_enabled": True
            },
            "farming": {
                "enabled": True,
                "preferred_fields": ["Sunflower Field", "Dandelion Field", "Mushroom Field"],
                "field_rotation_enabled": True,
                "collect_time_min": 45,
                "collect_time_max": 90,
                "hive_return_threshold": 95
            },
            "quests": {
                "enabled": True,
                "black_bear_enabled": True,
                "brown_bear_enabled": True,
                "polar_bear_enabled": True,
                "panda_bear_enabled": True,
                "science_bear_enabled": False,
                "mother_bear_enabled": False,
                "auto_accept_quests": True
            },
            "mobs": {
                "enabled": True,
                "kill_ladybugs": True,
                "kill_rhinobeetles": True,
                "kill_spiders": True,
                "kill_mantis": False,
                "kill_scorpions": False,
                "kill_werewolves": False,
                "mob_detection_timeout": 30
            },
            "planters": {
                "enabled": True,
                "auto_plant": True,
                "auto_harvest": True,
                "planter_fields": ["Sunflower Field", "Dandelion Field", "Mushroom Field", "Blue Flower Field"],
                "planter_rotation": True
            },
            "boosts": {
                "enabled": True,
                "auto_use_field_dice": True,
                "auto_use_enzymes": True,
                "auto_use_glue": True,
                "boost_threshold": 50
            },
            "hive": {
                "auto_feed_bees": True,
                "auto_hatch_eggs": True,
                "feed_threshold": 80,
                "hatch_threshold": 90
            },
            "dispensers": {
                "enabled": True,
                "collect_all": True,
                "collection_interval": 300
            },
            "safety": {
                "movement_randomization": 0.3,
                "click_randomization": 0.2,
                "pause_randomization": 0.5,
                "break_interval_min": 1800,
                "break_interval_max": 3600,
                "break_duration_min": 120,
                "break_duration_max": 300
            },
            "hotkeys": {
                "start_stop": "F1",
                "pause_resume": "F2",
                "emergency_stop": "F3",
                "show_hide_gui": "F4"
            }
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            logging.info(f"Default configuration saved to {self.config_file}")
        except Exception as e:
            logging.error(f"Failed to save default config: {e}")
        
        return default_config
    
    def initialize_components(self):
        """Initialize all macro components"""
        try:
            # Initialize macro controller
            self.macro_controller = MacroController(self.config_file)
            logging.info("Macro controller initialized")
            
            # Initialize GUI
            self.gui = MacroGUI(self.config, self.macro_controller)
            logging.info("GUI initialized")
            
            # Initialize hotkey handler
            self.hotkey_handler = HotkeyHandler(self.macro_controller, self.config)
            logging.info("Hotkey handler initialized")
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to initialize components: {e}")
            return False
    
    def check_dependencies(self):
        """Check if all required dependencies are available"""
        required_packages = [
            'cv2', 'numpy', 'PIL', 'pyautogui', 'keyboard', 'psutil', 'tkinter'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                if package == 'cv2':
                    import cv2
                elif package == 'PIL':
                    from PIL import Image
                elif package == 'tkinter':
                    import tkinter
                else:
                    __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            logging.error(f"Missing required packages: {', '.join(missing_packages)}")
            print(f"\nMissing required packages: {', '.join(missing_packages)}")
            print("Please install them using: pip install -r requirements.txt")
            return False
        
        logging.info("All dependencies are available")
        return True
    
    def check_system_requirements(self):
        """Check system requirements"""
        import platform
        
        # Check OS
        if platform.system() != "Windows":
            logging.warning("This macro is designed for Windows. Other OS may not work correctly.")
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
            logging.error("Python 3.7 or higher is required")
            return False
        
        # Check screen resolution (for image recognition)
        try:
            import pyautogui
            screen_size = pyautogui.size()
            logging.info(f"Screen resolution: {screen_size}")
            
            if screen_size.width < 1280 or screen_size.height < 720:
                logging.warning("Low screen resolution detected. Macro may not work correctly.")
        except:
            logging.warning("Could not detect screen resolution")
        
        return True
    
    def create_directories(self):
        """Create necessary directories"""
        directories = ['templates', 'logs', 'screenshots', 'configs']
        
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
            except Exception as e:
                logging.error(f"Failed to create directory {directory}: {e}")
    
    def display_startup_info(self):
        """Display startup information"""
        print("=" * 60)
        print(f"  {self.name} v{self.version}")
        print("  Advanced Bee Swarm Simulator Automation")
        print("=" * 60)
        print()
        print("Features:")
        print("  ✓ Advanced field farming with intelligent rotation")
        print("  ✓ Automated quest completion for all NPCs")
        print("  ✓ Smart mob hunting and loot collection")
        print("  ✓ Planter management and optimization")
        print("  ✓ Safety features with anti-detection")
        print("  ✓ Modern GUI interface")
        print("  ✓ Comprehensive statistics tracking")
        print("  ✓ Hotkey support for easy control")
        print()
        print("Safety Notice:")
        print("  • This macro includes safety features to reduce detection risk")
        print("  • Use at your own discretion and follow game terms of service")
        print("  • The macro includes randomization and break systems")
        print()
        print("Controls:")
        print(f"  • {self.config['hotkeys']['start_stop']} - Start/Stop Macro")
        print(f"  • {self.config['hotkeys']['pause_resume']} - Pause/Resume")
        print(f"  • {self.config['hotkeys']['emergency_stop']} - Emergency Stop")
        print(f"  • {self.config['hotkeys']['show_hide_gui']} - Show/Hide GUI")
        print()
        print("=" * 60)
        print()
    
    def run_gui_mode(self):
        """Run the macro in GUI mode"""
        logging.info("Starting GUI mode")
        
        try:
            # Run GUI
            self.gui.run()
            
        except KeyboardInterrupt:
            logging.info("GUI interrupted by user")
        except Exception as e:
            logging.error(f"GUI error: {e}")
        finally:
            self.cleanup()
    
    def run_console_mode(self):
        """Run the macro in console mode (no GUI)"""
        logging.info("Starting console mode")
        
        try:
            print("Starting macro in console mode...")
            print("Press Ctrl+C to stop")
            
            # Start macro controller in separate thread
            macro_thread = threading.Thread(target=self.macro_controller.run)
            macro_thread.daemon = True
            macro_thread.start()
            
            # Keep main thread alive
            while macro_thread.is_alive():
                time.sleep(1)
                
                # Print stats periodically
                if int(time.time()) % 60 == 0:  # Every minute
                    stats = self.macro_controller.get_session_stats()
                    print(f"Runtime: {stats.get('runtime_formatted', '00:00:00')} | "
                          f"Pollen: {stats.get('pollen_collected', 0):,} | "
                          f"Honey: {stats.get('honey_made', 0):,} | "
                          f"Quests: {stats.get('quests_completed', 0)}")
            
        except KeyboardInterrupt:
            logging.info("Console mode interrupted by user")
            self.macro_controller.stop()
        except Exception as e:
            logging.error(f"Console mode error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        logging.info("Performing cleanup...")
        
        try:
            if self.macro_controller:
                self.macro_controller.stop()
                self.macro_controller.cleanup()
            
            if self.gui:
                self.gui.close()
            
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")
        
        logging.info("Cleanup completed")
    
    def run(self, gui_mode=True):
        """Main run method"""
        try:
            # Display startup info
            self.display_startup_info()
            
            # Check dependencies
            if not self.check_dependencies():
                return False
            
            # Check system requirements
            if not self.check_system_requirements():
                return False
            
            # Create directories
            self.create_directories()
            
            # Initialize components
            if not self.initialize_components():
                logging.error("Failed to initialize components")
                return False
            
            # Run in selected mode
            if gui_mode:
                self.run_gui_mode()
            else:
                self.run_console_mode()
            
            return True
            
        except Exception as e:
            logging.error(f"Fatal error in main run: {e}")
            return False

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="BSS Pro Macro - Advanced Bee Swarm Simulator Automation")
    parser.add_argument('--console', action='store_true', help='Run in console mode (no GUI)')
    parser.add_argument('--config', default='config.json', help='Configuration file path')
    parser.add_argument('--version', action='version', version='BSS Pro Macro v1.0.0')
    
    args = parser.parse_args()
    
    # Create and run application
    app = BSSProMacro()
    app.config_file = args.config
    
    success = app.run(gui_mode=not args.console)
    
    if success:
        print("\nMacro completed successfully!")
    else:
        print("\nMacro encountered errors. Check logs for details.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())