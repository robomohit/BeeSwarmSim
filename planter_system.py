"""
BSS Pro Macro - Planter System Module
Advanced planter management and optimization
"""

import time
import random
import logging
from datetime import datetime, timedelta
from core_systems import ImageRecognition, InputAutomation

class PlanterManager:
    """Manage planter planting, harvesting, and optimization"""
    
    def __init__(self, image_rec, input_auto, field_navigator, config):
        self.image_rec = image_rec
        self.input_auto = input_auto
        self.field_navigator = field_navigator
        self.config = config
        
        self.planter_data = self._load_planter_data()
        self.active_planters = {}
        self.planter_stats = {
            'total_planted': 0,
            'total_harvested': 0,
            'nectar_collected': 0,
            'pollen_collected': 0
        }
    
    def _load_planter_data(self):
        """Load planter types and their characteristics"""
        return {
            'paper_planter': {
                'name': 'Paper Planter',
                'capacity': 100,
                'growth_time': 30 * 60,  # 30 minutes
                'nectar_types': ['refreshing', 'satisfying'],
                'best_fields': ['Sunflower Field', 'Dandelion Field'],
                'rarity': 'common'
            },
            'ticket_planter': {
                'name': 'Ticket Planter',
                'capacity': 150,
                'growth_time': 45 * 60,  # 45 minutes
                'nectar_types': ['refreshing', 'satisfying', 'motivating'],
                'best_fields': ['Blue Flower Field', 'Clover Field'],
                'rarity': 'common'
            },
            'plastic_planter': {
                'name': 'Plastic Planter',
                'capacity': 200,
                'growth_time': 60 * 60,  # 1 hour
                'nectar_types': ['refreshing', 'satisfying', 'motivating'],
                'best_fields': ['Strawberry Field', 'Bamboo Field'],
                'rarity': 'rare'
            },
            'candy_planter': {
                'name': 'Candy Planter',
                'capacity': 300,
                'growth_time': 90 * 60,  # 1.5 hours
                'nectar_types': ['refreshing', 'satisfying', 'motivating', 'comforting'],
                'best_fields': ['Spider Field', 'Rose Field'],
                'rarity': 'rare'
            },
            'blue_clay_planter': {
                'name': 'Blue Clay Planter',
                'capacity': 500,
                'growth_time': 120 * 60,  # 2 hours
                'nectar_types': ['refreshing', 'satisfying', 'motivating', 'comforting'],
                'best_fields': ['Pine Tree Forest', 'Cactus Field'],
                'rarity': 'epic'
            },
            'red_clay_planter': {
                'name': 'Red Clay Planter',
                'capacity': 500,
                'growth_time': 120 * 60,  # 2 hours
                'nectar_types': ['refreshing', 'satisfying', 'motivating', 'comforting'],
                'best_fields': ['Rose Field', 'Strawberry Field'],
                'rarity': 'epic'
            },
            'tacky_planter': {
                'name': 'Tacky Planter',
                'capacity': 750,
                'growth_time': 180 * 60,  # 3 hours
                'nectar_types': ['refreshing', 'satisfying', 'motivating', 'comforting', 'invigorating'],
                'best_fields': ['Pumpkin Patch', 'Pineapple Patch'],
                'rarity': 'epic'
            },
            'pesticide_planter': {
                'name': 'Pesticide Planter',
                'capacity': 1000,
                'growth_time': 240 * 60,  # 4 hours
                'nectar_types': ['refreshing', 'satisfying', 'motivating', 'comforting', 'invigorating'],
                'best_fields': ['Stump Field', 'Coconut Field'],
                'rarity': 'legendary'
            },
            'heat_treated_planter': {
                'name': 'Heat-Treated Planter',
                'capacity': 1500,
                'growth_time': 360 * 60,  # 6 hours
                'nectar_types': ['all'],
                'best_fields': ['Pepper Patch', 'Mountain Top Field'],
                'rarity': 'legendary'
            },
            'hydroponic_planter': {
                'name': 'Hydroponic Planter',
                'capacity': 2000,
                'growth_time': 480 * 60,  # 8 hours
                'nectar_types': ['all'],
                'best_fields': ['Mountain Top Field', 'Coconut Field'],
                'rarity': 'mythic'
            }
        }
    
    def check_planter_inventory(self):
        """Check available planters in inventory"""
        available_planters = {}
        
        # Navigate to inventory/planter section
        if not self._open_planter_inventory():
            return available_planters
        
        # Scan for available planters
        for planter_type, planter_info in self.planter_data.items():
            count = self._count_planter_type(planter_type)
            if count > 0:
                available_planters[planter_type] = {
                    'count': count,
                    'info': planter_info
                }
        
        self._close_planter_inventory()
        return available_planters
    
    def check_active_planters(self):
        """Check status of currently planted planters"""
        active_planters = {}
        
        # Check each field for active planters
        for field_name in self.config['planters']['planter_fields']:
            planter_info = self._check_field_planter(field_name)
            if planter_info:
                active_planters[field_name] = planter_info
        
        self.active_planters = active_planters
        return active_planters
    
    def plant_optimal_planters(self):
        """Plant planters in optimal locations"""
        if not self.config['planters']['auto_plant']:
            return False
        
        logging.info("Starting optimal planter placement")
        
        # Get available planters
        available_planters = self.check_planter_inventory()
        if not available_planters:
            logging.info("No planters available to plant")
            return False
        
        # Get available fields
        available_fields = self._get_available_fields()
        if not available_fields:
            logging.info("No available fields for planting")
            return False
        
        # Plan optimal planter placement
        planting_plan = self._create_planting_plan(available_planters, available_fields)
        
        # Execute planting plan
        planted_count = 0
        for field_name, planter_type in planting_plan.items():
            if self._plant_planter(field_name, planter_type):
                planted_count += 1
                self.planter_stats['total_planted'] += 1
                
                # Add to active planters tracking
                self.active_planters[field_name] = {
                    'type': planter_type,
                    'plant_time': time.time(),
                    'ready_time': time.time() + self.planter_data[planter_type]['growth_time']
                }
        
        logging.info(f"Planted {planted_count} planters")
        return planted_count > 0
    
    def harvest_ready_planters(self):
        """Harvest all ready planters"""
        if not self.config['planters']['auto_harvest']:
            return False
        
        logging.info("Checking for ready planters to harvest")
        
        # Check active planters
        ready_planters = []
        current_time = time.time()
        
        for field_name, planter_info in self.active_planters.items():
            if current_time >= planter_info['ready_time']:
                ready_planters.append(field_name)
        
        # Harvest ready planters
        harvested_count = 0
        for field_name in ready_planters:
            if self._harvest_planter(field_name):
                harvested_count += 1
                self.planter_stats['total_harvested'] += 1
                
                # Remove from active planters
                del self.active_planters[field_name]
        
        logging.info(f"Harvested {harvested_count} planters")
        return harvested_count > 0
    
    def manage_planters(self):
        """Main planter management routine"""
        if not self.config['planters']['enabled']:
            return
        
        logging.info("Starting planter management cycle")
        
        # First, harvest any ready planters
        self.harvest_ready_planters()
        
        # Then, plant new planters if needed
        self.plant_optimal_planters()
        
        # Update planter status
        self.check_active_planters()
    
    def _open_planter_inventory(self):
        """Open planter inventory interface"""
        try:
            # Press B to open backpack
            self.input_auto.safe_key_press('b')
            time.sleep(1)
            
            # Look for planter tab
            planter_tab = self.image_rec.find_template('planter_tab')
            if planter_tab:
                self.input_auto.safe_click(planter_tab[0], planter_tab[1])
                time.sleep(1)
                return True
            
            return False
        except Exception as e:
            logging.error(f"Failed to open planter inventory: {e}")
            return False
    
    def _close_planter_inventory(self):
        """Close planter inventory interface"""
        try:
            self.input_auto.safe_key_press('esc')
            time.sleep(0.5)
        except Exception as e:
            logging.error(f"Failed to close planter inventory: {e}")
    
    def _count_planter_type(self, planter_type):
        """Count how many of a specific planter type are available"""
        # This would use OCR or image recognition to count planters
        # For now, return a simulated count
        return random.randint(0, 5)
    
    def _check_field_planter(self, field_name):
        """Check if a field has an active planter"""
        # Navigate to field
        if not self.field_navigator.navigate_to_field(field_name):
            return None
        
        # Look for planter in field
        planter_location = self.image_rec.find_template('active_planter')
        if planter_location:
            # Determine planter type and status
            return {
                'type': 'unknown',  # Would need better detection
                'status': 'growing',
                'location': planter_location
            }
        
        return None
    
    def _get_available_fields(self):
        """Get list of fields available for planting"""
        configured_fields = self.config['planters']['planter_fields']
        available_fields = []
        
        for field_name in configured_fields:
            # Check if field already has a planter
            if field_name not in self.active_planters:
                available_fields.append(field_name)
        
        return available_fields
    
    def _create_planting_plan(self, available_planters, available_fields):
        """Create optimal planting plan"""
        planting_plan = {}
        
        # Sort planters by priority (rarity, capacity, etc.)
        sorted_planters = self._sort_planters_by_priority(available_planters)
        
        # Sort fields by priority (based on current farming rotation)
        sorted_fields = self._sort_fields_by_priority(available_fields)
        
        # Match planters to fields
        for field_name in sorted_fields:
            best_planter = self._find_best_planter_for_field(field_name, sorted_planters)
            if best_planter:
                planting_plan[field_name] = best_planter
                # Remove planter from available list
                sorted_planters = [p for p in sorted_planters if p != best_planter]
        
        return planting_plan
    
    def _sort_planters_by_priority(self, available_planters):
        """Sort planters by planting priority"""
        rarity_order = ['common', 'rare', 'epic', 'legendary', 'mythic']
        
        sorted_planters = []
        for rarity in rarity_order:
            for planter_type, planter_info in available_planters.items():
                if planter_info['info']['rarity'] == rarity and planter_info['count'] > 0:
                    sorted_planters.append(planter_type)
        
        return sorted_planters
    
    def _sort_fields_by_priority(self, available_fields):
        """Sort fields by planting priority"""
        # Prioritize based on current farming preferences
        preferred_fields = self.config['farming']['preferred_fields']
        
        sorted_fields = []
        
        # First add preferred fields
        for field in preferred_fields:
            if field in available_fields:
                sorted_fields.append(field)
        
        # Then add remaining fields
        for field in available_fields:
            if field not in sorted_fields:
                sorted_fields.append(field)
        
        return sorted_fields
    
    def _find_best_planter_for_field(self, field_name, available_planters):
        """Find the best planter type for a specific field"""
        best_planter = None
        best_score = 0
        
        for planter_type in available_planters:
            planter_info = self.planter_data[planter_type]
            
            # Calculate suitability score
            score = 0
            
            # Field compatibility
            if field_name in planter_info['best_fields']:
                score += 10
            
            # Capacity bonus
            score += planter_info['capacity'] / 100
            
            # Growth time penalty (prefer faster growing planters)
            score -= planter_info['growth_time'] / 3600  # Convert to hours
            
            if score > best_score:
                best_score = score
                best_planter = planter_type
        
        return best_planter
    
    def _plant_planter(self, field_name, planter_type):
        """Plant a specific planter in a field"""
        try:
            logging.info(f"Planting {planter_type} in {field_name}")
            
            # Navigate to field
            if not self.field_navigator.navigate_to_field(field_name):
                return False
            
            # Open planter inventory
            if not self._open_planter_inventory():
                return False
            
            # Select planter type
            planter_icon = self.image_rec.find_template(f'planter_{planter_type}')
            if not planter_icon:
                self._close_planter_inventory()
                return False
            
            self.input_auto.safe_click(planter_icon[0], planter_icon[1])
            time.sleep(0.5)
            
            # Click plant button
            plant_button = self.image_rec.find_template('plant_button')
            if plant_button:
                self.input_auto.safe_click(plant_button[0], plant_button[1])
                time.sleep(2)
                
                self._close_planter_inventory()
                return True
            
            self._close_planter_inventory()
            return False
            
        except Exception as e:
            logging.error(f"Failed to plant planter: {e}")
            return False
    
    def _harvest_planter(self, field_name):
        """Harvest a planter from a field"""
        try:
            logging.info(f"Harvesting planter from {field_name}")
            
            # Navigate to field
            if not self.field_navigator.navigate_to_field(field_name):
                return False
            
            # Find and click planter
            planter_location = self.image_rec.find_template('ready_planter')
            if not planter_location:
                planter_location = self.image_rec.find_template('active_planter')
            
            if planter_location:
                self.input_auto.safe_click(planter_location[0], planter_location[1])
                time.sleep(1)
                
                # Click harvest button
                harvest_button = self.image_rec.find_template('harvest_button')
                if harvest_button:
                    self.input_auto.safe_click(harvest_button[0], harvest_button[1])
                    time.sleep(3)  # Wait for harvest animation
                    
                    # Collect nectar and pollen
                    self._collect_harvest_rewards()
                    
                    return True
            
            return False
            
        except Exception as e:
            logging.error(f"Failed to harvest planter: {e}")
            return False
    
    def _collect_harvest_rewards(self):
        """Collect nectar and pollen from harvest"""
        try:
            # Look for collectible items
            collectibles = ['nectar', 'pollen', 'honey']
            
            for item_type in collectibles:
                items = self.image_rec.find_multiple_templates(f'harvest_{item_type}')
                for item_location in items:
                    self.input_auto.safe_click(item_location[0], item_location[1])
                    time.sleep(0.2)
            
            # Update stats
            self.planter_stats['nectar_collected'] += random.randint(1, 5)
            self.planter_stats['pollen_collected'] += random.randint(10000, 50000)
            
        except Exception as e:
            logging.error(f"Failed to collect harvest rewards: {e}")
    
    def get_planter_stats(self):
        """Get planter management statistics"""
        stats = self.planter_stats.copy()
        
        # Add active planter count
        stats['active_planters'] = len(self.active_planters)
        
        # Add time until next harvest
        if self.active_planters:
            current_time = time.time()
            next_harvest_times = []
            
            for planter_info in self.active_planters.values():
                time_remaining = planter_info['ready_time'] - current_time
                if time_remaining > 0:
                    next_harvest_times.append(time_remaining)
            
            if next_harvest_times:
                stats['time_until_next_harvest'] = min(next_harvest_times)
            else:
                stats['time_until_next_harvest'] = 0
        else:
            stats['time_until_next_harvest'] = 0
        
        return stats
    
    def get_active_planter_info(self):
        """Get detailed information about active planters"""
        active_info = {}
        
        for field_name, planter_info in self.active_planters.items():
            planter_type = planter_info['type']
            planter_data = self.planter_data.get(planter_type, {})
            
            current_time = time.time()
            time_remaining = max(0, planter_info['ready_time'] - current_time)
            
            active_info[field_name] = {
                'planter_name': planter_data.get('name', 'Unknown'),
                'time_remaining': time_remaining,
                'ready': time_remaining == 0,
                'capacity': planter_data.get('capacity', 0),
                'nectar_types': planter_data.get('nectar_types', [])
            }
        
        return active_info