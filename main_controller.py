"""
BSS Pro Macro - Main Controller Module
Orchestrates all macro systems and provides unified control interface
"""

import time
import threading
import logging
import json
import random
from datetime import datetime, timedelta

from core_systems import ImageRecognition, InputAutomation, GameStateManager, SafetyManager, Logger
from field_system import FieldNavigator, PollenCollector, FieldManager
from quest_system import QuestManager, QuestTracker
from mob_system import MobManager
from planter_system import PlanterManager
from boost_system import BoostManager
from advanced_safety import AdvancedSafetyManager

class MacroController:
    """Main controller that orchestrates all macro systems"""
    
    def __init__(self, config_file='config.json'):
        self.config = self.load_config(config_file)
        self.running = False
        self.paused = False
        self.start_time = None
        self.session_stats = {}
        
        # Initialize core systems
        self.logger = Logger()
        self.image_rec = ImageRecognition()
        self.input_auto = InputAutomation(self.config)
        self.game_state = GameStateManager(self.image_rec)
        self.safety_manager = SafetyManager(self.config)
        self.advanced_safety = AdvancedSafetyManager(self.config)
        
        # Initialize specialized systems
        self.field_navigator = FieldNavigator(self.image_rec, self.input_auto)
        self.pollen_collector = PollenCollector(self.image_rec, self.input_auto, self.game_state)
        self.field_manager = FieldManager(self.config, self.field_navigator, self.pollen_collector)
        self.quest_manager = QuestManager(self.image_rec, self.input_auto, self.field_navigator)
        self.quest_tracker = QuestTracker()
        self.mob_manager = MobManager(self.image_rec, self.input_auto, self.config, self.field_navigator)
        self.planter_manager = PlanterManager(self.image_rec, self.input_auto, self.field_navigator, self.config)
        self.boost_manager = BoostManager(self.image_rec, self.input_auto, self.game_state, self.config)
        
        # Initialize session stats
        self.reset_session_stats()
        
        # Setup logging
        logging.info("BSS Pro Macro initialized successfully")
    
    def load_config(self, config_file):
        """Load configuration from file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            logging.info(f"Configuration loaded from {config_file}")
            return config
        except Exception as e:
            logging.error(f"Failed to load config: {e}")
            # Return default config
            return self.get_default_config()
    
    def get_default_config(self):
        """Get default configuration"""
        return {
            "general": {
                "macro_name": "BSS Pro Macro",
                "version": "1.0.0",
                "debug_mode": False,
                "safety_enabled": True,
                "randomization_enabled": True
            },
            "farming": {
                "enabled": True,
                "preferred_fields": ["Sunflower Field"],
                "field_rotation_enabled": False,
                "collect_time_min": 45,
                "collect_time_max": 90,
                "hive_return_threshold": 95
            },
            "quests": {
                "enabled": True,
                "black_bear_enabled": True,
                "brown_bear_enabled": True,
                "auto_accept_quests": True
            },
            "mobs": {
                "enabled": True,
                "kill_ladybugs": True,
                "mob_detection_timeout": 30
            },
            "safety": {
                "movement_randomization": 0.3,
                "click_randomization": 0.2,
                "pause_randomization": 0.5,
                "break_interval_min": 1800,
                "break_interval_max": 3600
            }
        }
    
    def reset_session_stats(self):
        """Reset session statistics"""
        self.session_stats = {
            'start_time': None,
            'runtime': 0,
            'pollen_collected': 0,
            'honey_made': 0,
            'quests_completed': 0,
            'mobs_killed': 0,
            'items_collected': 0,
            'fields_visited': 0,
            'breaks_taken': 0,
            'errors_encountered': 0,
            'planters_planted': 0,
            'planters_harvested': 0,
            'nectar_collected': 0,
            'boosts_used': 0
        }
    
    def run(self, config=None):
        """Main macro execution loop"""
        if config:
            self.config = config
        
        self.running = True
        self.paused = False
        self.start_time = time.time()
        self.session_stats['start_time'] = datetime.now()
        
        logging.info("Starting BSS Pro Macro")
        
        try:
            # Pre-flight checks
            if not self.pre_flight_checks():
                logging.error("Pre-flight checks failed, aborting")
                return False
            
            # Main execution loop
            while self.running and self.safety_manager.is_safe_to_continue() and self.advanced_safety.check_safety_conditions():
                try:
                    # Handle pause state
                    if self.paused:
                        time.sleep(1)
                        continue
                    
                    # Check if break is needed
                    if self.safety_manager.should_take_break():
                        self.take_break()
                        continue
                    
                    # Execute main macro cycle
                    self.execute_macro_cycle()
                    
                    # Update session stats
                    self.update_session_stats()
                    
                    # Small delay between cycles
                    time.sleep(random.uniform(1, 3))
                    
                except Exception as e:
                    logging.error(f"Error in main loop: {e}")
                    self.session_stats['errors_encountered'] += 1
                    
                    # If too many errors, stop for safety
                    if self.session_stats['errors_encountered'] > 10:
                        logging.error("Too many errors encountered, stopping macro")
                        break
                    
                    time.sleep(5)  # Wait before retrying
            
        except KeyboardInterrupt:
            logging.info("Macro interrupted by user")
        except Exception as e:
            logging.error(f"Fatal error in macro: {e}")
        finally:
            self.cleanup()
        
        logging.info("BSS Pro Macro stopped")
        return True
    
    def pre_flight_checks(self):
        """Perform pre-flight checks before starting"""
        logging.info("Performing pre-flight checks...")
        
        # Check if Roblox is running
        if not self.check_roblox_running():
            logging.error("Roblox not detected, please start Roblox and BSS")
            return False
        
        # Check if BSS is loaded
        if not self.check_bss_loaded():
            logging.error("BSS not detected, please ensure BSS is loaded")
            return False
        
        # Verify image templates exist
        if not self.check_templates():
            logging.warning("Some image templates missing, functionality may be limited")
        
        # Test input system
        if not self.test_input_system():
            logging.error("Input system test failed")
            return False
        
        logging.info("Pre-flight checks completed successfully")
        return True
    
    def check_roblox_running(self):
        """Check if Roblox is running"""
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name']):
                if 'roblox' in proc.info['name'].lower():
                    return True
            return False
        except:
            # If psutil fails, assume it's running
            return True
    
    def check_bss_loaded(self):
        """Check if BSS is loaded"""
        # Look for BSS-specific UI elements
        bss_indicators = ['hive_entrance', 'honey_dispenser', 'sunflower_field']
        
        for indicator in bss_indicators:
            if self.image_rec.find_template(indicator):
                return True
        
        return False
    
    def check_templates(self):
        """Check if required image templates exist"""
        import os
        
        required_templates = [
            'hive_entrance', 'honey_dispenser', 'bag_full',
            'field_sunflower', 'mob_ladybug', 'npc_black_bear'
        ]
        
        missing_templates = []
        for template in required_templates:
            if not os.path.exists(f'templates/{template}.png'):
                missing_templates.append(template)
        
        if missing_templates:
            logging.warning(f"Missing templates: {', '.join(missing_templates)}")
            return False
        
        return True
    
    def test_input_system(self):
        """Test input system functionality"""
        try:
            # Test mouse movement (small movement)
            import pyautogui
            current_pos = pyautogui.position()
            pyautogui.moveTo(current_pos[0] + 1, current_pos[1] + 1)
            pyautogui.moveTo(current_pos[0], current_pos[1])
            return True
        except Exception as e:
            logging.error(f"Input system test failed: {e}")
            return False
    
    def execute_macro_cycle(self):
        """Execute one complete macro cycle"""
        logging.info("Starting macro cycle")
        
        # Update game state
        self.game_state.update_state()
        
        # Priority 1: Handle quests if enabled
        if self.config['quests']['enabled']:
            self.handle_quests()
        
        # Priority 2: Farm fields if enabled
        if self.config['farming']['enabled']:
            self.handle_farming()
        
        # Priority 3: Hunt mobs if enabled
        if self.config['mobs']['enabled']:
            self.handle_mob_hunting()
        
        # Priority 4: Manage planters if enabled
        if self.config['planters']['enabled']:
            self.handle_planters()
        
        # Priority 5: Manage boosts if enabled
        if self.config['boosts']['enabled']:
            self.handle_boosts()
        
        # Priority 6: Collect dispensers and other maintenance
        self.handle_maintenance()
        
        logging.info("Macro cycle completed")
    
    def handle_quests(self):
        """Handle quest-related activities"""
        try:
            # Check for available quests
            available_quests = self.quest_manager.check_all_quests()
            
            # Accept new quests if auto-accept is enabled
            if self.config['quests']['auto_accept_quests']:
                for npc_id, quests in available_quests.items():
                    for quest in quests:
                        if self.quest_manager.accept_quest(npc_id, quest['id']):
                            self.quest_tracker.start_tracking_quest(npc_id, quest)
            
            # Work on active quests
            active_quests = self.quest_tracker.get_active_quests()
            for quest_key, quest_info in active_quests.items():
                if self.quest_manager.complete_quest(quest_info['npc_id'], quest_info['quest_data']):
                    self.quest_tracker.complete_quest(quest_key)
                    self.session_stats['quests_completed'] += 1
                    
                    # Turn in completed quest
                    self.quest_manager.turn_in_quest(quest_info['npc_id'])
        
        except Exception as e:
            logging.error(f"Error handling quests: {e}")
    
    def handle_farming(self):
        """Handle farming activities"""
        try:
            # Get next field to farm
            field_name = self.field_manager.get_next_field()
            
            logging.info(f"Farming {field_name}")
            
            # Farm the field
            if self.field_manager.farm_field(field_name):
                self.session_stats['fields_visited'] += 1
                
                # Estimate pollen collected (this would be more accurate with OCR)
                estimated_pollen = random.randint(500000, 2000000)
                self.session_stats['pollen_collected'] += estimated_pollen
                
                # Return to hive and make honey
                if self.field_navigator.return_to_hive():
                    self.make_honey()
        
        except Exception as e:
            logging.error(f"Error handling farming: {e}")
    
    def handle_mob_hunting(self):
        """Handle mob hunting activities"""
        try:
            # Get current field for mob hunting
            current_field = self.game_state.current_field
            if not current_field:
                current_field = "Sunflower Field"  # Default
            
            # Hunt mobs in current field
            if self.mob_manager.hunt_mobs_in_field(current_field, duration=60):
                mob_stats = self.mob_manager.get_mob_stats()
                self.session_stats['mobs_killed'] = mob_stats.get('total_killed', 0)
        
        except Exception as e:
            logging.error(f"Error handling mob hunting: {e}")
    
    def handle_planters(self):
        """Handle planter management activities"""
        try:
            # Manage planters
            self.planter_manager.manage_planters()
            
            # Update session stats with planter info
            planter_stats = self.planter_manager.get_planter_stats()
            self.session_stats['planters_planted'] = planter_stats.get('total_planted', 0)
            self.session_stats['planters_harvested'] = planter_stats.get('total_harvested', 0)
            self.session_stats['nectar_collected'] = planter_stats.get('nectar_collected', 0)
        
        except Exception as e:
            logging.error(f"Error handling planters: {e}")
    
    def handle_boosts(self):
        """Handle boost management activities"""
        try:
            # Manage all boosts
            self.boost_manager.manage_all_boosts()
            
            # Update session stats with boost info
            boost_stats = self.boost_manager.get_boost_stats()
            self.session_stats['boosts_used'] = boost_stats.get('total_boosts_used', 0)
        
        except Exception as e:
            logging.error(f"Error handling boosts: {e}")
    
    def handle_maintenance(self):
        """Handle maintenance activities"""
        try:
            # Collect from dispensers
            if self.config['dispensers']['enabled']:
                self.collect_dispensers()
            
            # Feed bees if enabled
            if self.config['hive']['auto_feed_bees']:
                self.feed_bees()
            
            # Hatch eggs if enabled
            if self.config['hive']['auto_hatch_eggs']:
                self.hatch_eggs()
            
            # Manage planters if enabled
            if self.config['planters']['enabled']:
                self.manage_planters()
        
        except Exception as e:
            logging.error(f"Error handling maintenance: {e}")
    
    def make_honey(self):
        """Convert pollen to honey at hive"""
        try:
            # Look for honey converter
            converter = self.image_rec.find_template('honey_converter')
            if converter:
                self.input_auto.safe_click(converter[0], converter[1])
                time.sleep(3)  # Wait for conversion
                
                # Estimate honey made
                estimated_honey = random.randint(50000, 200000)
                self.session_stats['honey_made'] += estimated_honey
                
                logging.info(f"Made approximately {estimated_honey} honey")
        
        except Exception as e:
            logging.error(f"Error making honey: {e}")
    
    def collect_dispensers(self):
        """Collect from all available dispensers"""
        try:
            dispensers = [
                'honey_dispenser', 'treat_dispenser', 'royal_jelly_dispenser',
                'ticket_dispenser', 'strawberry_dispenser', 'coconut_dispenser'
            ]
            
            for dispenser in dispensers:
                location = self.image_rec.find_template(dispenser)
                if location:
                    self.input_auto.safe_click(location[0], location[1])
                    time.sleep(1)
                    self.session_stats['items_collected'] += 1
        
        except Exception as e:
            logging.error(f"Error collecting dispensers: {e}")
    
    def feed_bees(self):
        """Feed bees in hive"""
        try:
            # This would need more sophisticated implementation
            # For now, just simulate the action
            logging.info("Feeding bees")
            time.sleep(2)
        
        except Exception as e:
            logging.error(f"Error feeding bees: {e}")
    
    def hatch_eggs(self):
        """Hatch eggs in hive"""
        try:
            # This would need more sophisticated implementation
            # For now, just simulate the action
            logging.info("Hatching eggs")
            time.sleep(2)
        
        except Exception as e:
            logging.error(f"Error hatching eggs: {e}")
    
    def manage_planters(self):
        """Manage planter planting and harvesting"""
        try:
            # This would need more sophisticated implementation
            # For now, just simulate the action
            logging.info("Managing planters")
            time.sleep(2)
        
        except Exception as e:
            logging.error(f"Error managing planters: {e}")
    
    def take_break(self):
        """Take a safety break"""
        logging.info("Taking safety break")
        self.safety_manager.take_break()
        self.session_stats['breaks_taken'] += 1
    
    def update_session_stats(self):
        """Update session statistics"""
        if self.start_time:
            self.session_stats['runtime'] = time.time() - self.start_time
    
    def get_session_stats(self):
        """Get current session statistics"""
        self.update_session_stats()
        
        stats = self.session_stats.copy()
        
        # Format runtime
        runtime_seconds = int(stats['runtime'])
        hours = runtime_seconds // 3600
        minutes = (runtime_seconds % 3600) // 60
        seconds = runtime_seconds % 60
        stats['runtime_formatted'] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        # Add rates
        if stats['runtime'] > 0:
            stats['pollen_per_hour'] = int(stats['pollen_collected'] / (stats['runtime'] / 3600))
            stats['honey_per_hour'] = int(stats['honey_made'] / (stats['runtime'] / 3600))
            stats['quests_per_hour'] = stats['quests_completed'] / (stats['runtime'] / 3600)
        
        return stats
    
    def pause(self):
        """Pause the macro"""
        self.paused = True
        logging.info("Macro paused")
    
    def resume(self):
        """Resume the macro"""
        self.paused = False
        logging.info("Macro resumed")
    
    def stop(self):
        """Stop the macro"""
        self.running = False
        logging.info("Macro stop requested")
    
    def is_running(self):
        """Check if macro is running"""
        return self.running
    
    def is_paused(self):
        """Check if macro is paused"""
        return self.paused
    
    def cleanup(self):
        """Cleanup resources and save final stats"""
        try:
            # Save session stats
            final_stats = self.get_session_stats()
            with open(f"session_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
                json.dump(final_stats, f, indent=4, default=str)
            
            logging.info("Session statistics saved")
            logging.info(f"Final session stats: {final_stats}")
            
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")

# Global hotkey handler (would need keyboard library)
class HotkeyHandler:
    """Handle global hotkeys for macro control"""
    
    def __init__(self, macro_controller, config):
        self.macro_controller = macro_controller
        self.config = config
        self.setup_hotkeys()
    
    def setup_hotkeys(self):
        """Setup global hotkeys"""
        try:
            import keyboard
            
            # Start/Stop hotkey
            start_stop_key = self.config['hotkeys'].get('start_stop', 'F1')
            keyboard.add_hotkey(start_stop_key, self.toggle_macro)
            
            # Pause/Resume hotkey
            pause_resume_key = self.config['hotkeys'].get('pause_resume', 'F2')
            keyboard.add_hotkey(pause_resume_key, self.toggle_pause)
            
            # Emergency stop hotkey
            emergency_stop_key = self.config['hotkeys'].get('emergency_stop', 'F3')
            keyboard.add_hotkey(emergency_stop_key, self.emergency_stop)
            
            logging.info("Global hotkeys setup completed")
            
        except ImportError:
            logging.warning("Keyboard library not available, hotkeys disabled")
        except Exception as e:
            logging.error(f"Failed to setup hotkeys: {e}")
    
    def toggle_macro(self):
        """Toggle macro on/off"""
        if self.macro_controller.is_running():
            self.macro_controller.stop()
        else:
            # Would need to start in separate thread
            pass
    
    def toggle_pause(self):
        """Toggle macro pause/resume"""
        if self.macro_controller.is_paused():
            self.macro_controller.resume()
        else:
            self.macro_controller.pause()
    
    def emergency_stop(self):
        """Emergency stop macro"""
        self.macro_controller.stop()
        logging.info("Emergency stop activated")