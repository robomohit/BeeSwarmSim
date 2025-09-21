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
        """Load field coordinates and navigation paths"""
        return {
            'Sunflower Field': {
                'hive_path': ['w', 'w', 'w'],
                'coordinates': (640, 400),
                'level': 'starter',
                'recommended_bees': 5
            },
            'Dandelion Field': {
                'hive_path': ['a', 'w', 'w'],
                'coordinates': (580, 350),
                'level': 'starter',
                'recommended_bees': 5
            },
            'Mushroom Field': {
                'hive_path': ['s', 'a', 'a'],
                'coordinates': (520, 450),
                'level': 'starter',
                'recommended_bees': 5
            },
            'Blue Flower Field': {
                'hive_path': ['d', 'w', 'w'],
                'coordinates': (700, 350),
                'level': 'starter',
                'recommended_bees': 10
            },
            'Clover Field': {
                'hive_path': ['d', 'd', 'w'],
                'coordinates': (760, 400),
                'level': 'starter',
                'recommended_bees': 10
            },
            'Strawberry Field': {
                'hive_path': ['a', 'a', 'w', 'w'],
                'coordinates': (480, 300),
                'level': 'intermediate',
                'recommended_bees': 15
            },
            'Bamboo Field': {
                'hive_path': ['w', 'w', 'w', 'w'],
                'coordinates': (640, 250),
                'level': 'intermediate',
                'recommended_bees': 15
            },
            'Spider Field': {
                'hive_path': ['s', 's', 'a', 'a'],
                'coordinates': (480, 550),
                'level': 'intermediate',
                'recommended_bees': 15
            },
            'Rose Field': {
                'hive_path': ['d', 'd', 'd', 'w'],
                'coordinates': (820, 350),
                'level': 'advanced',
                'recommended_bees': 20
            },
            'Pine Tree Forest': {
                'hive_path': ['w', 'w', 'w', 'w', 'w'],
                'coordinates': (640, 150),
                'level': 'advanced',
                'recommended_bees': 25
            },
            'Cactus Field': {
                'hive_path': ['s', 's', 's'],
                'coordinates': (640, 600),
                'level': 'advanced',
                'recommended_bees': 25
            },
            'Pumpkin Patch': {
                'hive_path': ['s', 's', 'd', 'd'],
                'coordinates': (780, 580),
                'level': 'advanced',
                'recommended_bees': 30
            },
            'Pineapple Patch': {
                'hive_path': ['a', 'a', 'a', 'w'],
                'coordinates': (420, 350),
                'level': 'expert',
                'recommended_bees': 35
            },
            'Stump Field': {
                'hive_path': ['a', 'a', 'a', 'a'],
                'coordinates': (380, 400),
                'level': 'expert',
                'recommended_bees': 35
            },
            'Coconut Field': {
                'hive_path': ['d', 'd', 'd', 'd'],
                'coordinates': (860, 400),
                'level': 'expert',
                'recommended_bees': 40
            },
            'Pepper Patch': {
                'hive_path': ['s', 's', 's', 'd'],
                'coordinates': (720, 620),
                'level': 'expert',
                'recommended_bees': 40
            },
            'Mountain Top Field': {
                'hive_path': ['w', 'w', 'w', 'w', 'w', 'w'],
                'coordinates': (640, 100),
                'level': 'master',
                'recommended_bees': 50
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
        
        logging.info(f"Navigating to {field_name}")
        
        # Execute movement sequence
        for direction in field_data['hive_path']:
            self.input_auto.safe_key_press(direction, hold_time=1.0)
            time.sleep(0.5)
        
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
        """Return to hive from any location"""
        logging.info("Returning to hive")
        
        # Method 1: Use E key (hive tool)
        if self.input_auto.safe_key_press('e'):
            time.sleep(3)
            if self._verify_at_hive():
                return True
        
        # Method 2: Use reset character position
        if self._reset_character_position():
            time.sleep(5)
            if self._verify_at_hive():
                return True
        
        # Method 3: Manual navigation using compass
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
    
    def _reset_character_position(self):
        """Reset character position using Roblox reset"""
        try:
            # Open Roblox menu (ESC)
            self.input_auto.safe_key_press('esc')
            time.sleep(1)
            
            # Look for reset button
            reset_button = self.image_rec.find_template('reset_button')
            if reset_button:
                self.input_auto.safe_click(reset_button[0], reset_button[1])
                time.sleep(1)
                
                # Confirm reset
                confirm_button = self.image_rec.find_template('confirm_reset')
                if confirm_button:
                    self.input_auto.safe_click(confirm_button[0], confirm_button[1])
                    return True
            
            # Close menu if reset failed
            self.input_auto.safe_key_press('esc')
            return False
        except Exception as e:
            logging.error(f"Failed to reset character position: {e}")
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