"""
BSS Pro Macro - Mob System Module
Automated mob detection, fighting, and loot collection
"""

import time
import random
import logging
import math
from core_systems import ImageRecognition, InputAutomation, GameStateManager

class MobDetector:
    """Advanced mob detection and tracking system"""
    
    def __init__(self, image_rec):
        self.image_rec = image_rec
        self.mob_data = self._load_mob_data()
        self.detected_mobs = {}
        self.last_detection_time = 0
        
    def _load_mob_data(self):
        """Load mob information and characteristics"""
        return {
            'ladybug': {
                'name': 'Ladybug',
                'health': 100,
                'damage': 5,
                'speed': 'slow',
                'spawn_fields': ['Sunflower Field', 'Dandelion Field', 'Mushroom Field'],
                'loot': ['honey', 'treats', 'tickets'],
                'difficulty': 'easy',
                'respawn_time': 30
            },
            'rhinobeetle': {
                'name': 'Rhino Beetle',
                'health': 500,
                'damage': 15,
                'speed': 'medium',
                'spawn_fields': ['Blue Flower Field', 'Clover Field', 'Strawberry Field'],
                'loot': ['honey', 'treats', 'tickets', 'royal_jelly'],
                'difficulty': 'medium',
                'respawn_time': 120
            },
            'spider': {
                'name': 'Spider',
                'health': 200,
                'damage': 10,
                'speed': 'fast',
                'spawn_fields': ['Spider Field', 'Mushroom Field'],
                'loot': ['honey', 'treats', 'spider_silk'],
                'difficulty': 'medium',
                'respawn_time': 60
            },
            'mantis': {
                'name': 'Mantis',
                'health': 1000,
                'damage': 25,
                'speed': 'fast',
                'spawn_fields': ['Rose Field', 'Cactus Field'],
                'loot': ['honey', 'treats', 'tickets', 'enzymes'],
                'difficulty': 'hard',
                'respawn_time': 300
            },
            'scorpion': {
                'name': 'Scorpion',
                'health': 2000,
                'damage': 40,
                'speed': 'medium',
                'spawn_fields': ['Cactus Field', 'Rose Field'],
                'loot': ['honey', 'treats', 'tickets', 'stingers'],
                'difficulty': 'hard',
                'respawn_time': 600
            },
            'werewolf': {
                'name': 'Werewolf',
                'health': 5000,
                'damage': 60,
                'speed': 'very_fast',
                'spawn_fields': ['Pine Tree Forest'],
                'loot': ['honey', 'treats', 'tickets', 'moon_charms'],
                'difficulty': 'very_hard',
                'respawn_time': 1200
            },
            'tunnel_bear': {
                'name': 'Tunnel Bear',
                'health': 50000,
                'damage': 100,
                'speed': 'slow',
                'spawn_fields': ['Tunnel'],
                'loot': ['honey', 'treats', 'tickets', 'tunnel_bear_morph'],
                'difficulty': 'boss',
                'respawn_time': 3600
            }
        }
    
    def scan_for_mobs(self, current_field=None):
        """Scan current area for mobs"""
        current_time = time.time()
        if current_time - self.last_detection_time < 2.0:  # Don't scan too frequently
            return self.detected_mobs
        
        detected = {}
        
        for mob_type, mob_info in self.mob_data.items():
            # Check if mob can spawn in current field
            if current_field and current_field not in mob_info['spawn_fields']:
                continue
            
            # Look for mob on screen
            mob_locations = self.image_rec.find_multiple_templates(f"mob_{mob_type}")
            if mob_locations:
                detected[mob_type] = {
                    'locations': mob_locations,
                    'count': len(mob_locations),
                    'mob_info': mob_info,
                    'detection_time': current_time
                }
        
        self.detected_mobs = detected
        self.last_detection_time = current_time
        
        if detected:
            mob_names = [info['mob_info']['name'] for info in detected.values()]
            logging.info(f"Detected mobs: {', '.join(mob_names)}")
        
        return detected
    
    def get_priority_target(self, detected_mobs):
        """Get the highest priority mob to target"""
        if not detected_mobs:
            return None
        
        # Priority order: easy -> medium -> hard (for safety)
        priority_order = ['easy', 'medium', 'hard', 'very_hard', 'boss']
        
        for difficulty in priority_order:
            for mob_type, mob_data in detected_mobs.items():
                if mob_data['mob_info']['difficulty'] == difficulty:
                    # Return closest mob of this difficulty
                    closest_location = self._get_closest_location(mob_data['locations'])
                    return {
                        'type': mob_type,
                        'location': closest_location,
                        'info': mob_data['mob_info']
                    }
        
        return None
    
    def _get_closest_location(self, locations):
        """Get closest mob location to screen center"""
        screen_center = (640, 360)  # Assuming 1280x720 resolution
        
        min_distance = float('inf')
        closest_location = locations[0]
        
        for location in locations:
            distance = math.sqrt(
                (location[0] - screen_center[0]) ** 2 + 
                (location[1] - screen_center[1]) ** 2
            )
            if distance < min_distance:
                min_distance = distance
                closest_location = location
        
        return closest_location

class MobFighter:
    """Combat system for fighting mobs"""
    
    def __init__(self, image_rec, input_auto, config):
        self.image_rec = image_rec
        self.input_auto = input_auto
        self.config = config
        self.combat_patterns = self._load_combat_patterns()
        self.last_attack_time = 0
        
    def _load_combat_patterns(self):
        """Load combat patterns for different mob types"""
        return {
            'easy': {
                'approach': 'direct',
                'attack_pattern': ['click', 'click', 'click'],
                'dodge_pattern': ['s', 'a', 'w', 'd'],
                'attack_interval': 0.5
            },
            'medium': {
                'approach': 'cautious',
                'attack_pattern': ['click', 'dodge', 'click', 'click'],
                'dodge_pattern': ['s', 's', 'a', 'w'],
                'attack_interval': 0.7
            },
            'hard': {
                'approach': 'hit_and_run',
                'attack_pattern': ['click', 'dodge', 'dodge', 'click'],
                'dodge_pattern': ['s', 's', 's', 'a', 'a'],
                'attack_interval': 1.0
            },
            'very_hard': {
                'approach': 'kiting',
                'attack_pattern': ['click', 'dodge', 'dodge', 'dodge'],
                'dodge_pattern': ['s', 's', 's', 's'],
                'attack_interval': 1.5
            },
            'boss': {
                'approach': 'coordinated',
                'attack_pattern': ['click', 'dodge', 'dodge', 'dodge', 'dodge'],
                'dodge_pattern': ['s', 's', 's', 's', 's'],
                'attack_interval': 2.0
            }
        }
    
    def engage_mob(self, target_mob):
        """Engage and fight a specific mob"""
        mob_type = target_mob['type']
        mob_location = target_mob['location']
        mob_info = target_mob['info']
        
        logging.info(f"Engaging {mob_info['name']} at {mob_location}")
        
        # Get combat pattern for this mob difficulty
        pattern = self.combat_patterns[mob_info['difficulty']]
        
        # Approach the mob
        if not self._approach_mob(mob_location, pattern['approach']):
            return False
        
        # Fight the mob
        return self._fight_mob(mob_type, mob_location, pattern)
    
    def _approach_mob(self, mob_location, approach_type):
        """Approach mob using specified strategy"""
        if approach_type == 'direct':
            # Move directly to mob
            self.input_auto.move_mouse_smooth(mob_location[0], mob_location[1], 1.0)
            return True
        
        elif approach_type == 'cautious':
            # Approach slowly with pauses
            self.input_auto.move_mouse_smooth(mob_location[0], mob_location[1], 2.0)
            time.sleep(0.5)
            return True
        
        elif approach_type == 'hit_and_run':
            # Get close but maintain distance
            offset_x = mob_location[0] + random.randint(-50, 50)
            offset_y = mob_location[1] + random.randint(-50, 50)
            self.input_auto.move_mouse_smooth(offset_x, offset_y, 1.5)
            return True
        
        elif approach_type == 'kiting':
            # Maintain maximum attack distance
            offset_x = mob_location[0] + random.randint(-100, 100)
            offset_y = mob_location[1] + random.randint(-100, 100)
            self.input_auto.move_mouse_smooth(offset_x, offset_y, 1.0)
            return True
        
        elif approach_type == 'coordinated':
            # Complex approach pattern for bosses
            # Move in a spiral pattern
            for angle in range(0, 360, 45):
                radius = 80
                x = mob_location[0] + radius * math.cos(math.radians(angle))
                y = mob_location[1] + radius * math.sin(math.radians(angle))
                self.input_auto.move_mouse_smooth(x, y, 0.5)
                time.sleep(0.2)
            return True
        
        return False
    
    def _fight_mob(self, mob_type, mob_location, combat_pattern):
        """Fight mob using combat pattern"""
        max_fight_duration = 60  # Maximum fight time in seconds
        fight_start_time = time.time()
        
        while time.time() - fight_start_time < max_fight_duration:
            # Check if mob is still alive
            if not self._is_mob_alive(mob_type, mob_location):
                logging.info(f"Defeated {mob_type}")
                return True
            
            # Execute attack pattern
            for action in combat_pattern['attack_pattern']:
                if action == 'click':
                    self._attack_mob(mob_location)
                elif action == 'dodge':
                    self._dodge_attack(combat_pattern['dodge_pattern'])
                
                time.sleep(combat_pattern['attack_interval'])
                
                # Check if we need to stop fighting
                if not self._should_continue_fighting():
                    return False
        
        logging.warning(f"Fight with {mob_type} timed out")
        return False
    
    def _attack_mob(self, mob_location):
        """Perform attack on mob"""
        current_time = time.time()
        if current_time - self.last_attack_time < 0.3:  # Prevent spam clicking
            return
        
        # Click on mob location with slight randomization
        click_x = mob_location[0] + random.randint(-10, 10)
        click_y = mob_location[1] + random.randint(-10, 10)
        
        self.input_auto.safe_click(click_x, click_y)
        self.last_attack_time = current_time
    
    def _dodge_attack(self, dodge_pattern):
        """Execute dodge movement"""
        dodge_direction = random.choice(dodge_pattern)
        dodge_duration = random.uniform(0.3, 0.8)
        
        self.input_auto.safe_key_press(dodge_direction, hold_time=dodge_duration)
    
    def _is_mob_alive(self, mob_type, last_known_location):
        """Check if mob is still alive"""
        # Look for mob near last known location
        search_region = (
            last_known_location[0] - 100,
            last_known_location[1] - 100,
            200,
            200
        )
        
        mob_found = self.image_rec.find_template(f"mob_{mob_type}", region=search_region)
        return mob_found is not None
    
    def _should_continue_fighting(self):
        """Check if we should continue fighting"""
        # Check player health
        if self.image_rec.find_template('health_low'):
            logging.warning("Health low, retreating from combat")
            return False
        
        # Check if player is stuck
        # This would need more sophisticated detection
        
        return True

class LootCollector:
    """Collect loot dropped by defeated mobs"""
    
    def __init__(self, image_rec, input_auto):
        self.image_rec = image_rec
        self.input_auto = input_auto
        self.loot_types = ['honey', 'treats', 'tickets', 'royal_jelly', 'enzymes', 'stingers']
        
    def collect_nearby_loot(self, search_radius=100):
        """Collect all loot within search radius"""
        collected_items = []
        
        for loot_type in self.loot_types:
            loot_locations = self.image_rec.find_multiple_templates(f"loot_{loot_type}")
            
            for location in loot_locations:
                if self._is_within_radius(location, search_radius):
                    if self._collect_loot_item(location):
                        collected_items.append(loot_type)
        
        if collected_items:
            logging.info(f"Collected loot: {', '.join(collected_items)}")
        
        return collected_items
    
    def _is_within_radius(self, location, radius):
        """Check if location is within collection radius"""
        screen_center = (640, 360)
        distance = math.sqrt(
            (location[0] - screen_center[0]) ** 2 + 
            (location[1] - screen_center[1]) ** 2
        )
        return distance <= radius
    
    def _collect_loot_item(self, location):
        """Collect a specific loot item"""
        try:
            # Move to loot
            self.input_auto.move_mouse_smooth(location[0], location[1], 0.5)
            
            # Click to collect
            self.input_auto.safe_click(location[0], location[1])
            
            time.sleep(0.3)
            return True
        except Exception as e:
            logging.error(f"Failed to collect loot: {e}")
            return False

class MobManager:
    """Main mob management system"""
    
    def __init__(self, image_rec, input_auto, config, field_navigator):
        self.image_rec = image_rec
        self.input_auto = input_auto
        self.config = config
        self.field_navigator = field_navigator
        
        self.detector = MobDetector(image_rec)
        self.fighter = MobFighter(image_rec, input_auto, config)
        self.loot_collector = LootCollector(image_rec, input_auto)
        
        self.mob_stats = {
            'total_killed': 0,
            'kills_by_type': {},
            'loot_collected': {},
            'fight_duration_total': 0
        }
    
    def hunt_mobs_in_field(self, field_name, duration=300):
        """Hunt mobs in specified field for given duration"""
        if not self.config['mobs']['enabled']:
            return False
        
        logging.info(f"Starting mob hunting in {field_name} for {duration} seconds")
        
        # Navigate to field
        if not self.field_navigator.navigate_to_field(field_name):
            return False
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Scan for mobs
            detected_mobs = self.detector.scan_for_mobs(field_name)
            
            if detected_mobs:
                # Get priority target
                target = self.detector.get_priority_target(detected_mobs)
                
                if target and self._should_fight_mob(target):
                    # Fight the mob
                    fight_start = time.time()
                    success = self.fighter.engage_mob(target)
                    fight_duration = time.time() - fight_start
                    
                    if success:
                        # Update stats
                        self._update_kill_stats(target['type'], fight_duration)
                        
                        # Collect loot
                        collected_loot = self.loot_collector.collect_nearby_loot()
                        self._update_loot_stats(collected_loot)
                    
                    # Small delay before next scan
                    time.sleep(2)
            else:
                # No mobs found, wait a bit
                time.sleep(5)
        
        logging.info(f"Completed mob hunting in {field_name}")
        return True
    
    def _should_fight_mob(self, target_mob):
        """Determine if we should fight this mob"""
        mob_type = target_mob['type']
        mob_info = target_mob['info']
        
        # Check config settings
        if mob_type == 'ladybug' and not self.config['mobs']['kill_ladybugs']:
            return False
        if mob_type == 'rhinobeetle' and not self.config['mobs']['kill_rhinobeetles']:
            return False
        if mob_type == 'spider' and not self.config['mobs']['kill_spiders']:
            return False
        if mob_type == 'mantis' and not self.config['mobs']['kill_mantis']:
            return False
        if mob_type == 'scorpion' and not self.config['mobs']['kill_scorpions']:
            return False
        if mob_type == 'werewolf' and not self.config['mobs']['kill_werewolves']:
            return False
        
        # Check if mob is too difficult
        if mob_info['difficulty'] in ['boss'] and not self.config.get('advanced_combat', False):
            return False
        
        return True
    
    def _update_kill_stats(self, mob_type, fight_duration):
        """Update mob kill statistics"""
        self.mob_stats['total_killed'] += 1
        self.mob_stats['fight_duration_total'] += fight_duration
        
        if mob_type not in self.mob_stats['kills_by_type']:
            self.mob_stats['kills_by_type'][mob_type] = 0
        self.mob_stats['kills_by_type'][mob_type] += 1
    
    def _update_loot_stats(self, collected_loot):
        """Update loot collection statistics"""
        for loot_item in collected_loot:
            if loot_item not in self.mob_stats['loot_collected']:
                self.mob_stats['loot_collected'][loot_item] = 0
            self.mob_stats['loot_collected'][loot_item] += 1
    
    def get_mob_stats(self):
        """Get mob hunting statistics"""
        stats = self.mob_stats.copy()
        
        if stats['total_killed'] > 0:
            stats['average_fight_duration'] = stats['fight_duration_total'] / stats['total_killed']
        else:
            stats['average_fight_duration'] = 0
        
        return stats