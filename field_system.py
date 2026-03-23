"""
BSS Pro Macro - Field System Module
Advanced field navigation, farming, and pollen collection
"""

import time
import random
import logging
from core_systems import ImageRecognition, InputAutomation, GameStateManager

class FieldNavigator:
    """Navigate between different fields efficiently"""
    
    def __init__(self, image_rec, input_auto):
        self.image_rec = image_rec
        self.input_auto = input_auto
        self.field_coordinates = self._load_field_coordinates()
        self.current_field = None
        
    def _load_field_coordinates(self):
        """Load field coordinates and navigation paths from hive"""
        return {
            'Sunflower Field': {
                'hive_path': [('w', 2.0)],  # (key, duration) - Walk straight forward for 2 seconds
                'coordinates': (640, 400),
                'level': 'starter',
                'recommended_bees': 5,
                'description': 'Straight forward from hive'
            },
            'Dandelion Field': {
                'hive_path': [('a', 0.8), ('w', 1.5)],  # Turn left, then forward
                'coordinates': (580, 350),
                'level': 'starter',
                'recommended_bees': 5,
                'description': 'Left from hive, then forward'
            },
            'Mushroom Field': {
                'hive_path': [('s', 0.5), ('a', 0.8), ('w', 1.2)],  # Back, left, forward
                'coordinates': (520, 450),
                'level': 'starter',
                'recommended_bees': 5,
                'description': 'Behind hive to the left'
            },
            'Blue Flower Field': {
                'hive_path': [('d', 0.8), ('w', 2.0)],  # Right, then forward
                'coordinates': (700, 350),
                'level': 'starter',
                'recommended_bees': 10,
                'description': 'Right from hive, then forward'
            },
            'Clover Field': {
                'hive_path': [('d', 1.2), ('w', 1.5)],  # Further right, then forward
                'coordinates': (760, 400),
                'level': 'starter',
                'recommended_bees': 10,
                'description': 'Far right from hive'
            },
            'Strawberry Field': {
                'hive_path': [('a', 1.5), ('w', 2.5)],  # Left, then long forward walk
                'coordinates': (480, 300),
                'level': 'intermediate',
                'recommended_bees': 15,
                'description': 'Left from hive, up the ramp'
            },
            'Bamboo Field': {
                'hive_path': [('w', 4.0)],  # Long walk straight forward
                'coordinates': (640, 250),
                'level': 'intermediate',
                'recommended_bees': 15,
                'description': 'Straight forward from hive, up ramps'
            },
            'Spider Field': {
                'hive_path': [('s', 1.0), ('a', 1.5), ('w', 1.0)],  # Back, left, forward
                'coordinates': (480, 550),
                'level': 'intermediate',
                'recommended_bees': 15,
                'description': 'Behind and left of hive'
            },
            'Rose Field': {
                'hive_path': [('d', 2.0), ('w', 2.5)],  # Far right, then forward
                'coordinates': (820, 350),
                'level': 'advanced',
                'recommended_bees': 20,
                'description': 'Far right from hive, up ramps'
            },
            'Pine Tree Forest': {
                'hive_path': [('w', 6.0)],  # Very long walk forward
                'coordinates': (640, 150),
                'level': 'advanced',
                'recommended_bees': 25,
                'description': 'Straight forward, up multiple ramps'
            },
            'Cactus Field': {
                'hive_path': [('s', 2.5)],  # Walk backwards/south
                'coordinates': (640, 600),
                'level': 'advanced',
                'recommended_bees': 25,
                'description': 'Behind hive, down ramps'
            },
            'Pumpkin Patch': {
                'hive_path': [('s', 1.5), ('d', 1.5), ('w', 1.0)],  # Back, right, forward
                'coordinates': (780, 580),
                'level': 'advanced',
                'recommended_bees': 30,
                'description': 'Behind and right of hive'
            },
            'Pineapple Patch': {
                'hive_path': [('a', 2.5), ('w', 2.0)],  # Far left, then forward
                'coordinates': (420, 350),
                'level': 'expert',
                'recommended_bees': 35,
                'description': 'Far left from hive, up ramps'
            },
            'Stump Field': {
                'hive_path': [('a', 3.0), ('w', 1.5)],  # Very far left, then forward
                'coordinates': (380, 400),
                'level': 'expert',
                'recommended_bees': 35,
                'description': 'Far left of hive, hidden area'
            },
            'Coconut Field': {
                'hive_path': [('d', 3.0), ('w', 2.0)],  # Very far right, then forward
                'coordinates': (860, 400),
                'level': 'expert',
                'recommended_bees': 40,
                'description': 'Far right of hive, up multiple ramps'
            },
            'Pepper Patch': {
                'hive_path': [('s', 2.0), ('d', 1.5), ('w', 1.5)],  # Back, right, forward
                'coordinates': (720, 620),
                'level': 'expert',
                'recommended_bees': 40,
                'description': 'Behind hive, right side, down ramps'
            },
            'Mountain Top Field': {
                'hive_path': [('w', 8.0)],  # Extremely long walk forward
                'coordinates': (640, 100),
                'level': 'master',
                'recommended_bees': 50,
                'description': 'Straight forward, up all ramps to the top'
            }
        }
    
    def navigate_to_field(self, field_name):
        """Navigate to a specific field from hive"""
        if field_name not in self.field_coordinates:
            logging.error(f"Unknown field: {field_name}")
            return False
        
        # First, ensure we're at the hive
        if not self.return_to_hive():
            return False
        
        field_data = self.field_coordinates[field_name]
        
        logging.info(f"Navigating to {field_name}: {field_data['description']}")
        
        # Execute movement sequence with proper timing
        for movement in field_data['hive_path']:
            if isinstance(movement, tuple):
                # New format: (key, duration)
                direction, duration = movement
                logging.info(f"Moving {direction} for {duration} seconds")
                
                # For longer movements (ramps), add jumping to help navigation
                if duration >= 2.0:
                    self._move_with_jumping(direction, duration)
                else:
                    self.input_auto.safe_key_press(direction, hold_time=duration)
                
                time.sleep(0.3)  # Brief pause between movements
            else:
                # Legacy format: just key (1 second default)
                logging.info(f"Moving {movement} for 1.0 seconds")
                self.input_auto.safe_key_press(movement, hold_time=1.0)
                time.sleep(0.3)
        
        # Verify we reached the field
        time.sleep(2)
        if self._verify_field_arrival(field_name):
            self.current_field = field_name
            logging.info(f"Successfully reached {field_name}")
            return True
        else:
            logging.warning(f"Failed to reach {field_name}, trying alternative route")
            return self._try_alternative_navigation(field_name)
    
    def return_to_hive(self):
        """Return to hive from any location using BSS mechanics"""
        logging.info("Returning to hive")
        
        # Method 1: Use E key (Hive Tool) - Primary method in BSS
        logging.info("Using E key (Hive Tool) to return to hive")
        if self.input_auto.safe_key_press('e'):
            time.sleep(4)  # Wait for teleport animation
            if self._verify_at_hive():
                logging.info("Successfully returned to hive using E key")
                return True
        
        # Method 2: Use Roblox character reset (ESC menu method)
        logging.info("E key failed, trying character reset")
        if self._reset_character_roblox():
            time.sleep(6)  # Wait for respawn
            if self._verify_at_hive():
                logging.info("Successfully returned to hive using character reset")
                return True
        
        # Method 3: Manual walk back (last resort)
        logging.info("Reset failed, attempting manual navigation")
        return self._navigate_to_hive_manually()
    
    def _verify_field_arrival(self, field_name):
        """Verify that we've arrived at the correct field"""
        # Look for field-specific visual indicators
        field_key = field_name.lower().replace(' ', '_').replace('field', '').replace('patch', '').replace('forest', '').strip('_')
        
        # Check for field name UI element
        if self.image_rec.find_template(f"field_name_{field_key}"):
            return True
        
        # Check for field-specific visual elements
        if self.image_rec.find_template(f"field_visual_{field_key}"):
            return True
        
        # Check for field-specific flowers/objects
        if self.image_rec.find_template(f"flower_{field_key}"):
            return True
        
        return False
    
    def _verify_at_hive(self):
        """Verify that we're at the hive"""
        hive_indicators = ['hive_entrance', 'honey_dispenser', 'royal_jelly_dispenser']
        
        for indicator in hive_indicators:
            if self.image_rec.find_template(indicator):
                return True
        
        return False
    
    def _reset_character_roblox(self):
        """Reset character using Roblox ESC menu (returns to spawn/hive)"""
        try:
            logging.info("Opening Roblox menu to reset character")
            
            # Open Roblox menu (ESC)
            self.input_auto.safe_key_press('esc')
            time.sleep(1.5)
            
            # Look for reset character button in menu
            reset_button = self.image_rec.find_template('reset_character_button')
            if reset_button:
                logging.info("Found reset character button, clicking...")
                self.input_auto.safe_click(reset_button[0], reset_button[1])
                time.sleep(1)
                
                # Look for confirmation dialog
                confirm_reset = self.image_rec.find_template('confirm_reset_button')
                if confirm_reset:
                    logging.info("Confirming character reset...")
                    self.input_auto.safe_click(confirm_reset[0], confirm_reset[1])
                    return True
                else:
                    # Try alternative confirmation (some Roblox versions)
                    self.input_auto.safe_key_press('enter')  # Confirm with Enter
                    return True
            else:
                # Alternative method: Try R key (some Roblox versions)
                logging.info("Reset button not found, trying R key shortcut")
                self.input_auto.safe_key_press('esc')  # Close menu first
                time.sleep(0.5)
                self.input_auto.safe_key_press('r')  # R key for reset in some versions
                time.sleep(1)
                
                # Confirm if dialog appears
                self.input_auto.safe_key_press('enter')
                return True
            
        except Exception as e:
            logging.error(f"Failed to reset character: {e}")
            # Try to close any open menus
            self.input_auto.safe_key_press('esc')
            return False
    
    def _navigate_to_hive_manually(self):
        """Navigate to hive manually using directional keys"""
        # This is a fallback method
        logging.info("Attempting manual navigation to hive")
        
        # Try moving in different directions to find the hive
        directions = ['s', 'a', 'w', 'd']
        for direction in directions:
            for _ in range(5):
                self.input_auto.safe_key_press(direction, hold_time=1.0)
                time.sleep(0.5)
                
                if self._verify_at_hive():
                    return True
        
        return False
    
    def _move_with_jumping(self, direction, duration):
        """Move in direction with periodic jumping to help with ramps/obstacles"""
        logging.info(f"Moving {direction} with jumping for {duration} seconds")
        
        # Break movement into segments with jumping
        segments = int(duration / 0.8)  # Jump every 0.8 seconds approximately
        segment_duration = duration / max(segments, 1)
        
        for i in range(segments):
            # Move for a segment
            self.input_auto.safe_key_press(direction, hold_time=segment_duration * 0.7)
            
            # Jump to help with ramps/obstacles
            if i < segments - 1:  # Don't jump on the last segment
                self.input_auto.safe_key_press('space')
                time.sleep(0.1)
        
        # Final movement segment if needed
        remaining_time = duration - (segments * segment_duration * 0.7)
        if remaining_time > 0.1:
            self.input_auto.safe_key_press(direction, hold_time=remaining_time)
    
    def _try_alternative_navigation(self, field_name):
        """Try alternative navigation method"""
        # Use click-based navigation if available
        field_data = self.field_coordinates[field_name]
        
        try:
            # Try clicking directly on field coordinate
            self.input_auto.safe_click(field_data['coordinates'][0], field_data['coordinates'][1])
            time.sleep(2)
            
            if self._verify_field_arrival(field_name):
                self.current_field = field_name
                return True
        except Exception as e:
            logging.error(f"Alternative navigation failed: {e}")
        
        return False

class PollenCollector:
    """Advanced pollen collection system"""
    
    def __init__(self, image_rec, input_auto, game_state):
        self.image_rec = image_rec
        self.input_auto = input_auto
        self.game_state = game_state
        self.collection_patterns = self._load_collection_patterns()
        
    def _load_collection_patterns(self):
        """Load optimized collection patterns for each field"""
        return {
            'default': {
                'pattern': 'spiral',
                'movements': ['w', 'd', 's', 'a'],
                'duration': 2.0
            },
            'large_field': {
                'pattern': 'zigzag',
                'movements': ['w', 'd', 's', 'a', 'w', 'a', 's', 'd'],
                'duration': 1.5
            },
            'small_field': {
                'pattern': 'circle',
                'movements': ['w', 'd', 's', 'a'],
                'duration': 1.0
            }
        }
    
    def collect_pollen_in_field(self, field_name, duration=60):
        """Collect pollen in specified field for given duration"""
        logging.info(f"Starting pollen collection in {field_name} for {duration} seconds")
        
        start_time = time.time()
        collection_time = 0
        
        # Select appropriate collection pattern
        pattern = self._select_collection_pattern(field_name)
        
        while collection_time < duration:
            # Check if bag is full
            if self.game_state.check_bag_full():
                logging.info("Bag is full, returning to hive")
                return 'bag_full'
            
            # Execute collection movement
            self._execute_collection_pattern(pattern)
            
            # Collect any visible tokens/items
            self._collect_nearby_items()
            
            # Check for mobs and handle them
            mobs = self.game_state.detect_mobs()
            if mobs:
                self._handle_mobs(mobs)
            
            collection_time = time.time() - start_time
            
            # Random micro-breaks
            if random.random() < 0.1:  # 10% chance
                time.sleep(random.uniform(1, 3))
        
        logging.info(f"Completed pollen collection in {field_name}")
        return 'completed'
    
    def _select_collection_pattern(self, field_name):
        """Select optimal collection pattern for field"""
        large_fields = ['Mountain Top Field', 'Pine Tree Forest', 'Coconut Field']
        small_fields = ['Mushroom Field', 'Strawberry Field']
        
        if field_name in large_fields:
            return self.collection_patterns['large_field']
        elif field_name in small_fields:
            return self.collection_patterns['small_field']
        else:
            return self.collection_patterns['default']
    
    def _execute_collection_pattern(self, pattern):
        """Execute the collection movement pattern"""
        for movement in pattern['movements']:
            # Add randomization to movement duration
            duration = pattern['duration'] + random.uniform(-0.3, 0.3)
            duration = max(0.5, duration)  # Minimum duration
            
            self.input_auto.safe_key_press(movement, hold_time=duration)
            
            # Random pause between movements
            if random.random() < 0.3:  # 30% chance
                time.sleep(random.uniform(0.1, 0.5))
    
    def _collect_nearby_items(self):
        """Collect nearby tokens and items"""
        collectibles = self.game_state.detect_collectibles()
        
        for item_type, locations in collectibles.items():
            for location in locations[:3]:  # Limit to 3 closest items
                # Move towards item
                self.input_auto.move_mouse_smooth(location[0], location[1], 0.5)
                self.input_auto.safe_click(location[0], location[1])
                time.sleep(0.2)
    
    def _handle_mobs(self, mobs):
        """Handle mobs encountered during collection"""
        # For now, just avoid them by moving away
        for mob_type, locations in mobs.items():
            if locations:
                logging.info(f"Detected {mob_type}, moving away")
                # Move in opposite direction
                self.input_auto.safe_key_press('s', hold_time=1.0)
                time.sleep(0.5)
                break

class FieldManager:
    """Manage field selection and rotation"""
    
    def __init__(self, config, navigator, collector):
        self.config = config
        self.navigator = navigator
        self.collector = collector
        self.field_rotation_index = 0
        self.field_stats = {}
        
    def get_next_field(self):
        """Get the next field in rotation"""
        if not self.config['farming']['field_rotation_enabled']:
            # Return preferred field
            preferred_fields = self.config['farming']['preferred_fields']
            return preferred_fields[0] if preferred_fields else 'Sunflower Field'
        
        # Rotate through preferred fields
        preferred_fields = self.config['farming']['preferred_fields']
        if not preferred_fields:
            preferred_fields = ['Sunflower Field']
        
        field = preferred_fields[self.field_rotation_index % len(preferred_fields)]
        self.field_rotation_index += 1
        
        return field
    
    def farm_field(self, field_name):
        """Farm a specific field completely"""
        logging.info(f"Starting farming sequence for {field_name}")
        
        # Navigate to field
        if not self.navigator.navigate_to_field(field_name):
            logging.error(f"Failed to navigate to {field_name}")
            return False
        
        # Calculate collection time
        collect_time = random.uniform(
            self.config['farming']['collect_time_min'],
            self.config['farming']['collect_time_max']
        )
        
        # Collect pollen
        result = self.collector.collect_pollen_in_field(field_name, collect_time)
        
        # Update field stats
        if field_name not in self.field_stats:
            self.field_stats[field_name] = {'visits': 0, 'total_time': 0}
        
        self.field_stats[field_name]['visits'] += 1
        self.field_stats[field_name]['total_time'] += collect_time
        
        # Return to hive if bag is full or farming complete
        if result == 'bag_full' or result == 'completed':
            return self.navigator.return_to_hive()
        
        return True
    
    def get_field_stats(self):
        """Get farming statistics"""
        return self.field_stats