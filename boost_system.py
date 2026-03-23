"""
BSS Pro Macro - Boost System Module
Smart boost management and optimization
"""

import time
import random
import logging
from datetime import datetime, timedelta
from core_systems import ImageRecognition, InputAutomation

class BoostManager:
    """Manage boost activation and optimization"""
    
    def __init__(self, image_rec, input_auto, game_state, config):
        self.image_rec = image_rec
        self.input_auto = input_auto
        self.game_state = game_state
        self.config = config
        
        self.boost_data = self._load_boost_data()
        self.active_boosts = {}
        self.boost_stats = {
            'total_boosts_used': 0,
            'field_dice_used': 0,
            'enzymes_used': 0,
            'glue_used': 0,
            'oil_used': 0,
            'glitter_used': 0
        }
    
    def _load_boost_data(self):
        """Load boost information and characteristics"""
        return {
            'field_dice': {
                'name': 'Field Dice',
                'duration': 15 * 60,  # 15 minutes
                'effect': 'x2 pollen from field tokens',
                'best_use': 'high_token_fields',
                'priority': 8,
                'cooldown': 60
            },
            'smooth_dice': {
                'name': 'Smooth Dice',
                'duration': 15 * 60,  # 15 minutes
                'effect': 'x2 pollen from field tokens, no field damage',
                'best_use': 'high_token_fields',
                'priority': 9,
                'cooldown': 60
            },
            'loaded_dice': {
                'name': 'Loaded Dice',
                'duration': 15 * 60,  # 15 minutes
                'effect': 'x2 pollen from field tokens, guaranteed rare tokens',
                'best_use': 'high_token_fields',
                'priority': 10,
                'cooldown': 60
            },
            'enzymes': {
                'name': 'Enzymes',
                'duration': 10 * 60,  # 10 minutes
                'effect': 'x2 pollen conversion rate',
                'best_use': 'farming_sessions',
                'priority': 7,
                'cooldown': 30
            },
            'oil': {
                'name': 'Oil',
                'duration': 30 * 60,  # 30 minutes
                'effect': 'x1.5 movement speed',
                'best_use': 'long_farming_sessions',
                'priority': 5,
                'cooldown': 120
            },
            'glue': {
                'name': 'Glue',
                'duration': 15 * 60,  # 15 minutes
                'effect': 'x1.25 pollen from tools',
                'best_use': 'tool_farming',
                'priority': 6,
                'cooldown': 60
            },
            'tropical_drink': {
                'name': 'Tropical Drink',
                'duration': 30 * 60,  # 30 minutes
                'effect': 'x1.5 blue pollen',
                'best_use': 'blue_fields',
                'priority': 4,
                'cooldown': 120
            },
            'strawberry': {
                'name': 'Strawberry',
                'duration': 30 * 60,  # 30 minutes
                'effect': 'x1.5 red pollen',
                'best_use': 'red_fields',
                'priority': 4,
                'cooldown': 120
            },
            'coconut': {
                'name': 'Coconut',
                'duration': 30 * 60,  # 30 minutes
                'effect': 'x1.5 white pollen',
                'best_use': 'white_fields',
                'priority': 4,
                'cooldown': 120
            },
            'glitter': {
                'name': 'Glitter',
                'duration': 15 * 60,  # 15 minutes
                'effect': 'x2 pollen from abilities',
                'best_use': 'ability_farming',
                'priority': 7,
                'cooldown': 60
            },
            'red_extract': {
                'name': 'Red Extract',
                'duration': 30 * 60,  # 30 minutes
                'effect': 'x1.25 red pollen, +critical chance',
                'best_use': 'red_fields',
                'priority': 6,
                'cooldown': 120
            },
            'blue_extract': {
                'name': 'Blue Extract',
                'duration': 30 * 60,  # 30 minutes
                'effect': 'x1.25 blue pollen, +focus',
                'best_use': 'blue_fields',
                'priority': 6,
                'cooldown': 120
            },
            'super_smoothie': {
                'name': 'Super Smoothie',
                'duration': 60 * 60,  # 60 minutes
                'effect': 'x1.5 all pollen, +energy',
                'best_use': 'long_sessions',
                'priority': 9,
                'cooldown': 240
            }
        }
    
    def check_boost_inventory(self):
        """Check available boosts in inventory"""
        available_boosts = {}
        
        # Open inventory
        if not self._open_inventory():
            return available_boosts
        
        # Scan for boosts
        for boost_type, boost_info in self.boost_data.items():
            count = self._count_boost_type(boost_type)
            if count > 0:
                available_boosts[boost_type] = {
                    'count': count,
                    'info': boost_info
                }
        
        self._close_inventory()
        return available_boosts
    
    def check_active_boosts(self):
        """Check currently active boosts"""
        active_boosts = {}
        
        # Look for boost indicators on screen
        for boost_type, boost_info in self.boost_data.items():
            boost_indicator = self.image_rec.find_template(f'active_{boost_type}')
            if boost_indicator:
                # Estimate remaining time (would need OCR for exact time)
                estimated_remaining = self._estimate_boost_remaining_time(boost_type)
                active_boosts[boost_type] = {
                    'remaining_time': estimated_remaining,
                    'info': boost_info
                }
        
        self.active_boosts = active_boosts
        return active_boosts
    
    def use_optimal_boosts(self, context='farming'):
        """Use optimal boosts based on current context"""
        if not self.config['boosts']['enabled']:
            return False
        
        logging.info(f"Checking optimal boosts for context: {context}")
        
        # Get available boosts
        available_boosts = self.check_boost_inventory()
        if not available_boosts:
            logging.info("No boosts available")
            return False
        
        # Get current active boosts
        active_boosts = self.check_active_boosts()
        
        # Determine optimal boosts for context
        optimal_boosts = self._get_optimal_boosts_for_context(context, available_boosts, active_boosts)
        
        # Use optimal boosts
        used_count = 0
        for boost_type in optimal_boosts:
            if self._use_boost(boost_type):
                used_count += 1
                self.boost_stats['total_boosts_used'] += 1
                self.boost_stats[f'{boost_type}_used'] = self.boost_stats.get(f'{boost_type}_used', 0) + 1
        
        if used_count > 0:
            logging.info(f"Used {used_count} boosts")
        
        return used_count > 0
    
    def manage_field_dice(self):
        """Smart field dice management"""
        if not self.config['boosts']['auto_use_field_dice']:
            return False
        
        # Check if field dice is already active
        if 'field_dice' in self.active_boosts or 'smooth_dice' in self.active_boosts or 'loaded_dice' in self.active_boosts:
            return False
        
        # Check current field for token density
        current_field = self.game_state.current_field
        if not current_field:
            return False
        
        token_density = self._estimate_field_token_density(current_field)
        
        # Use dice if token density is high enough
        if token_density >= self.config['boosts']['boost_threshold']:
            # Prioritize loaded dice > smooth dice > field dice
            dice_priority = ['loaded_dice', 'smooth_dice', 'field_dice']
            
            for dice_type in dice_priority:
                if self._has_boost(dice_type) and self._use_boost(dice_type):
                    logging.info(f"Used {dice_type} due to high token density in {current_field}")
                    return True
        
        return False
    
    def manage_enzymes(self):
        """Smart enzyme management"""
        if not self.config['boosts']['auto_use_enzymes']:
            return False
        
        # Check if enzymes already active
        if 'enzymes' in self.active_boosts:
            return False
        
        # Check bag fullness
        bag_fullness = self._estimate_bag_fullness()
        
        # Use enzymes if bag is getting full
        if bag_fullness >= 70:  # 70% full
            if self._has_boost('enzymes') and self._use_boost('enzymes'):
                logging.info("Used enzymes due to high bag fullness")
                return True
        
        return False
    
    def manage_glue(self):
        """Smart glue management"""
        if not self.config['boosts']['auto_use_glue']:
            return False
        
        # Check if glue already active
        if 'glue' in self.active_boosts:
            return False
        
        # Use glue during farming sessions
        if self._is_farming_session():
            if self._has_boost('glue') and self._use_boost('glue'):
                logging.info("Used glue for farming session")
                return True
        
        return False
    
    def manage_field_specific_boosts(self):
        """Manage field-specific boosts"""
        current_field = self.game_state.current_field
        if not current_field:
            return False
        
        # Determine field type
        field_type = self._get_field_type(current_field)
        
        # Use appropriate boost
        boost_used = False
        
        if field_type == 'red':
            if not self._has_active_boost(['strawberry', 'red_extract']):
                if self._has_boost('red_extract') and self._use_boost('red_extract'):
                    boost_used = True
                elif self._has_boost('strawberry') and self._use_boost('strawberry'):
                    boost_used = True
        
        elif field_type == 'blue':
            if not self._has_active_boost(['tropical_drink', 'blue_extract']):
                if self._has_boost('blue_extract') and self._use_boost('blue_extract'):
                    boost_used = True
                elif self._has_boost('tropical_drink') and self._use_boost('tropical_drink'):
                    boost_used = True
        
        elif field_type == 'white':
            if not self._has_active_boost(['coconut']):
                if self._has_boost('coconut') and self._use_boost('coconut'):
                    boost_used = True
        
        if boost_used:
            logging.info(f"Used field-specific boost for {field_type} field: {current_field}")
        
        return boost_used
    
    def _open_inventory(self):
        """Open inventory interface"""
        try:
            self.input_auto.safe_key_press('b')
            time.sleep(1)
            return True
        except Exception as e:
            logging.error(f"Failed to open inventory: {e}")
            return False
    
    def _close_inventory(self):
        """Close inventory interface"""
        try:
            self.input_auto.safe_key_press('esc')
            time.sleep(0.5)
        except Exception as e:
            logging.error(f"Failed to close inventory: {e}")
    
    def _count_boost_type(self, boost_type):
        """Count available boosts of specific type"""
        # This would use OCR or image recognition
        # For now, return simulated count
        return random.randint(0, 10)
    
    def _estimate_boost_remaining_time(self, boost_type):
        """Estimate remaining time for active boost"""
        # This would need OCR to read the actual timer
        # For now, return estimated time based on boost duration
        boost_info = self.boost_data.get(boost_type, {})
        return random.randint(60, boost_info.get('duration', 300))
    
    def _get_optimal_boosts_for_context(self, context, available_boosts, active_boosts):
        """Get optimal boosts for given context"""
        optimal_boosts = []
        
        if context == 'farming':
            # Prioritize farming boosts
            farming_boosts = ['field_dice', 'smooth_dice', 'loaded_dice', 'enzymes', 'glue', 'oil']
            for boost in farming_boosts:
                if boost in available_boosts and boost not in active_boosts:
                    optimal_boosts.append(boost)
                    break  # Only use one dice type at a time
        
        elif context == 'mob_hunting':
            # Prioritize combat boosts
            combat_boosts = ['oil', 'glitter']
            for boost in combat_boosts:
                if boost in available_boosts and boost not in active_boosts:
                    optimal_boosts.append(boost)
        
        elif context == 'quest_completion':
            # Prioritize general boosts
            quest_boosts = ['enzymes', 'oil', 'super_smoothie']
            for boost in quest_boosts:
                if boost in available_boosts and boost not in active_boosts:
                    optimal_boosts.append(boost)
        
        # Sort by priority
        optimal_boosts.sort(key=lambda x: self.boost_data.get(x, {}).get('priority', 0), reverse=True)
        
        return optimal_boosts[:3]  # Limit to 3 boosts at once
    
    def _use_boost(self, boost_type):
        """Use a specific boost"""
        try:
            logging.info(f"Using boost: {boost_type}")
            
            # Open inventory
            if not self._open_inventory():
                return False
            
            # Find and click boost
            boost_icon = self.image_rec.find_template(f'boost_{boost_type}')
            if not boost_icon:
                self._close_inventory()
                return False
            
            self.input_auto.safe_click(boost_icon[0], boost_icon[1])
            time.sleep(0.5)
            
            # Confirm use
            use_button = self.image_rec.find_template('use_boost_button')
            if use_button:
                self.input_auto.safe_click(use_button[0], use_button[1])
                time.sleep(1)
                
                self._close_inventory()
                
                # Add to active boosts
                self.active_boosts[boost_type] = {
                    'start_time': time.time(),
                    'duration': self.boost_data[boost_type]['duration']
                }
                
                return True
            
            self._close_inventory()
            return False
            
        except Exception as e:
            logging.error(f"Failed to use boost {boost_type}: {e}")
            return False
    
    def _has_boost(self, boost_type):
        """Check if boost is available in inventory"""
        # This would check inventory
        # For now, return random availability
        return random.random() > 0.3
    
    def _has_active_boost(self, boost_types):
        """Check if any of the specified boosts are active"""
        if isinstance(boost_types, str):
            boost_types = [boost_types]
        
        for boost_type in boost_types:
            if boost_type in self.active_boosts:
                return True
        
        return False
    
    def _estimate_field_token_density(self, field_name):
        """Estimate token density in field"""
        # This would analyze the field for tokens
        # For now, return estimated density based on field type
        high_token_fields = ['Sunflower Field', 'Dandelion Field', 'Blue Flower Field']
        medium_token_fields = ['Clover Field', 'Strawberry Field', 'Bamboo Field']
        
        if field_name in high_token_fields:
            return random.randint(70, 100)
        elif field_name in medium_token_fields:
            return random.randint(40, 70)
        else:
            return random.randint(10, 40)
    
    def _estimate_bag_fullness(self):
        """Estimate current bag fullness percentage"""
        # This would check bag status
        # For now, return random fullness
        return random.randint(20, 95)
    
    def _is_farming_session(self):
        """Check if currently in a farming session"""
        # This would check current activity
        # For now, assume we're always farming
        return True
    
    def _get_field_type(self, field_name):
        """Get the type (color) of a field"""
        red_fields = ['Strawberry Field', 'Rose Field', 'Mushroom Field']
        blue_fields = ['Blue Flower Field', 'Bamboo Field', 'Pine Tree Forest']
        white_fields = ['Sunflower Field', 'Dandelion Field', 'Coconut Field']
        
        if field_name in red_fields:
            return 'red'
        elif field_name in blue_fields:
            return 'blue'
        elif field_name in white_fields:
            return 'white'
        else:
            return 'mixed'
    
    def get_boost_stats(self):
        """Get boost usage statistics"""
        return self.boost_stats.copy()
    
    def get_active_boost_info(self):
        """Get information about currently active boosts"""
        active_info = {}
        current_time = time.time()
        
        for boost_type, boost_data in self.active_boosts.items():
            start_time = boost_data['start_time']
            duration = boost_data['duration']
            elapsed = current_time - start_time
            remaining = max(0, duration - elapsed)
            
            active_info[boost_type] = {
                'name': self.boost_data[boost_type]['name'],
                'remaining_time': remaining,
                'effect': self.boost_data[boost_type]['effect']
            }
        
        return active_info
    
    def cleanup_expired_boosts(self):
        """Remove expired boosts from active list"""
        current_time = time.time()
        expired_boosts = []
        
        for boost_type, boost_data in self.active_boosts.items():
            start_time = boost_data['start_time']
            duration = boost_data['duration']
            
            if current_time - start_time >= duration:
                expired_boosts.append(boost_type)
        
        for boost_type in expired_boosts:
            del self.active_boosts[boost_type]
            logging.info(f"Boost expired: {boost_type}")
    
    def manage_all_boosts(self):
        """Main boost management routine"""
        if not self.config['boosts']['enabled']:
            return
        
        logging.info("Starting boost management cycle")
        
        # Clean up expired boosts
        self.cleanup_expired_boosts()
        
        # Update active boosts
        self.check_active_boosts()
        
        # Manage specific boost types
        self.manage_field_dice()
        self.manage_enzymes()
        self.manage_glue()
        self.manage_field_specific_boosts()
        
        # Use optimal boosts based on current context
        current_context = 'farming'  # Would determine based on current activity
        self.use_optimal_boosts(current_context)