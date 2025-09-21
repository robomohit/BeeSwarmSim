"""
BSS Pro Macro - Quest System Module
Automated quest completion for all NPCs
"""

import time
import random
import logging
from core_systems import ImageRecognition, InputAutomation

class QuestManager:
    """Manage all quest-related activities"""
    
    def __init__(self, image_rec, input_auto, field_navigator):
        self.image_rec = image_rec
        self.input_auto = input_auto
        self.field_navigator = field_navigator
        self.quest_npcs = self._load_quest_npcs()
        self.active_quests = {}
        
    def _load_quest_npcs(self):
        """Load quest NPC information"""
        return {
            'black_bear': {
                'name': 'Black Bear',
                'location': 'hive',
                'navigation': [],
                'quest_types': ['collect_pollen', 'kill_mobs', 'collect_items'],
                'rewards': ['honey', 'tickets', 'treats']
            },
            'brown_bear': {
                'name': 'Brown Bear',
                'location': 'brown_bear_area',
                'navigation': ['d', 'd', 's'],
                'quest_types': ['collect_pollen', 'field_specific'],
                'rewards': ['honey', 'tickets', 'treats']
            },
            'polar_bear': {
                'name': 'Polar Bear',
                'location': 'polar_bear_area',
                'navigation': ['a', 'a', 'w', 'w'],
                'quest_types': ['collect_pollen', 'defeat_snowbear'],
                'rewards': ['honey', 'tickets', 'treats', 'snowflakes']
            },
            'panda_bear': {
                'name': 'Panda Bear',
                'location': 'bamboo_field',
                'navigation': ['w', 'w', 'w', 'w'],
                'quest_types': ['bamboo_tokens', 'collect_pollen'],
                'rewards': ['honey', 'tickets', 'treats']
            },
            'science_bear': {
                'name': 'Science Bear',
                'location': 'science_lab',
                'navigation': ['d', 'd', 'd', 'w'],
                'quest_types': ['experiments', 'collect_items'],
                'rewards': ['honey', 'tickets', 'science_materials']
            },
            'mother_bear': {
                'name': 'Mother Bear',
                'location': 'mother_bear_area',
                'navigation': ['a', 'a', 'a', 's'],
                'quest_types': ['family_quests', 'collect_pollen'],
                'rewards': ['honey', 'tickets', 'treats', 'mother_bear_morph']
            },
            'gifted_bucko_bee': {
                'name': 'Gifted Bucko Bee',
                'location': 'blue_flower_field',
                'navigation': ['d', 'w', 'w'],
                'quest_types': ['blue_pollen', 'blue_field_tokens'],
                'rewards': ['blue_extracts', 'tickets']
            },
            'gifted_riley_bee': {
                'name': 'Gifted Riley Bee',
                'location': 'sunflower_field',
                'navigation': ['w', 'w', 'w'],
                'quest_types': ['red_pollen', 'red_field_tokens'],
                'rewards': ['red_extracts', 'tickets']
            }
        }
    
    def check_all_quests(self):
        """Check all available quests from all NPCs"""
        logging.info("Checking all available quests")
        available_quests = {}
        
        for npc_id, npc_data in self.quest_npcs.items():
            quests = self.check_npc_quests(npc_id)
            if quests:
                available_quests[npc_id] = quests
        
        return available_quests
    
    def check_npc_quests(self, npc_id):
        """Check quests from a specific NPC"""
        if npc_id not in self.quest_npcs:
            logging.error(f"Unknown NPC: {npc_id}")
            return None
        
        npc_data = self.quest_npcs[npc_id]
        
        # Navigate to NPC
        if not self._navigate_to_npc(npc_id):
            logging.warning(f"Failed to navigate to {npc_data['name']}")
            return None
        
        # Interact with NPC
        if not self._interact_with_npc(npc_id):
            logging.warning(f"Failed to interact with {npc_data['name']}")
            return None
        
        # Read quest information
        quests = self._read_quest_dialog(npc_id)
        
        # Close dialog
        self._close_quest_dialog()
        
        return quests
    
    def accept_quest(self, npc_id, quest_id):
        """Accept a quest from an NPC"""
        if not self._navigate_to_npc(npc_id):
            return False
        
        if not self._interact_with_npc(npc_id):
            return False
        
        # Look for accept button
        accept_button = self.image_rec.find_template('quest_accept_button')
        if accept_button:
            self.input_auto.safe_click(accept_button[0], accept_button[1])
            time.sleep(1)
            
            # Add to active quests
            if npc_id not in self.active_quests:
                self.active_quests[npc_id] = []
            self.active_quests[npc_id].append(quest_id)
            
            logging.info(f"Accepted quest from {self.quest_npcs[npc_id]['name']}")
            self._close_quest_dialog()
            return True
        
        self._close_quest_dialog()
        return False
    
    def complete_quest(self, npc_id, quest_data):
        """Complete a specific quest"""
        logging.info(f"Attempting to complete quest for {self.quest_npcs[npc_id]['name']}")
        
        quest_type = quest_data.get('type', 'unknown')
        
        if quest_type == 'collect_pollen':
            return self._complete_pollen_quest(quest_data)
        elif quest_type == 'kill_mobs':
            return self._complete_mob_quest(quest_data)
        elif quest_type == 'collect_items':
            return self._complete_item_quest(quest_data)
        elif quest_type == 'field_specific':
            return self._complete_field_quest(quest_data)
        else:
            logging.warning(f"Unknown quest type: {quest_type}")
            return False
    
    def turn_in_quest(self, npc_id):
        """Turn in completed quest to NPC"""
        if not self._navigate_to_npc(npc_id):
            return False
        
        if not self._interact_with_npc(npc_id):
            return False
        
        # Look for turn in button
        turn_in_button = self.image_rec.find_template('quest_turn_in_button')
        if turn_in_button:
            self.input_auto.safe_click(turn_in_button[0], turn_in_button[1])
            time.sleep(2)
            
            # Remove from active quests
            if npc_id in self.active_quests:
                self.active_quests[npc_id] = []
            
            logging.info(f"Turned in quest to {self.quest_npcs[npc_id]['name']}")
            self._close_quest_dialog()
            return True
        
        self._close_quest_dialog()
        return False
    
    def _navigate_to_npc(self, npc_id):
        """Navigate to specific NPC"""
        npc_data = self.quest_npcs[npc_id]
        
        # Return to hive first
        if not self.field_navigator.return_to_hive():
            return False
        
        # Navigate to NPC location
        if npc_data['navigation']:
            for direction in npc_data['navigation']:
                self.input_auto.safe_key_press(direction, hold_time=1.0)
                time.sleep(0.5)
        
        # Verify we reached the NPC
        return self._verify_npc_location(npc_id)
    
    def _verify_npc_location(self, npc_id):
        """Verify we're at the correct NPC location"""
        npc_template = f"npc_{npc_id}"
        location = self.image_rec.find_template(npc_template)
        return location is not None
    
    def _interact_with_npc(self, npc_id):
        """Interact with NPC to open quest dialog"""
        # Look for NPC
        npc_location = self.image_rec.find_template(f"npc_{npc_id}")
        if not npc_location:
            return False
        
        # Click on NPC
        self.input_auto.safe_click(npc_location[0], npc_location[1])
        time.sleep(1)
        
        # Verify dialog opened
        return self.image_rec.find_template('quest_dialog') is not None
    
    def _read_quest_dialog(self, npc_id):
        """Read quest information from dialog"""
        quests = []
        
        # This would normally use OCR to read quest text
        # For now, we'll simulate quest detection
        quest_indicators = [
            'quest_collect_pollen',
            'quest_kill_mobs',
            'quest_collect_items',
            'quest_field_specific'
        ]
        
        for indicator in quest_indicators:
            if self.image_rec.find_template(indicator):
                quest_data = self._parse_quest_from_indicator(indicator)
                if quest_data:
                    quests.append(quest_data)
        
        return quests
    
    def _parse_quest_from_indicator(self, indicator):
        """Parse quest data from visual indicator"""
        # This would normally extract specific requirements
        # For now, return generic quest data
        if 'pollen' in indicator:
            return {
                'type': 'collect_pollen',
                'amount': 1000000,  # Example amount
                'field': 'any',
                'time_limit': 3600
            }
        elif 'mobs' in indicator:
            return {
                'type': 'kill_mobs',
                'mob_type': 'any',
                'amount': 10,
                'time_limit': 1800
            }
        elif 'items' in indicator:
            return {
                'type': 'collect_items',
                'item_type': 'tokens',
                'amount': 50,
                'time_limit': 2400
            }
        elif 'field' in indicator:
            return {
                'type': 'field_specific',
                'field': 'Sunflower Field',
                'amount': 500000,
                'time_limit': 1800
            }
        
        return None
    
    def _close_quest_dialog(self):
        """Close quest dialog"""
        # Look for close button
        close_button = self.image_rec.find_template('dialog_close_button')
        if close_button:
            self.input_auto.safe_click(close_button[0], close_button[1])
        else:
            # Try ESC key
            self.input_auto.safe_key_press('esc')
        
        time.sleep(0.5)
    
    def _complete_pollen_quest(self, quest_data):
        """Complete pollen collection quest"""
        required_amount = quest_data.get('amount', 1000000)
        field_requirement = quest_data.get('field', 'any')
        
        logging.info(f"Completing pollen quest: {required_amount} pollen from {field_requirement}")
        
        # Select appropriate field
        if field_requirement == 'any':
            field = 'Sunflower Field'  # Default field
        else:
            field = field_requirement
        
        # Farm the required field
        return self.field_navigator.navigate_to_field(field)
    
    def _complete_mob_quest(self, quest_data):
        """Complete mob killing quest"""
        mob_type = quest_data.get('mob_type', 'any')
        amount = quest_data.get('amount', 10)
        
        logging.info(f"Completing mob quest: Kill {amount} {mob_type}")
        
        # Navigate to field with target mobs
        if mob_type == 'ladybug' or mob_type == 'any':
            field = 'Sunflower Field'
        elif mob_type == 'spider':
            field = 'Spider Field'
        else:
            field = 'Sunflower Field'  # Default
        
        return self.field_navigator.navigate_to_field(field)
    
    def _complete_item_quest(self, quest_data):
        """Complete item collection quest"""
        item_type = quest_data.get('item_type', 'tokens')
        amount = quest_data.get('amount', 50)
        
        logging.info(f"Completing item quest: Collect {amount} {item_type}")
        
        # Navigate to best field for item collection
        field = 'Sunflower Field'  # Default field for token collection
        return self.field_navigator.navigate_to_field(field)
    
    def _complete_field_quest(self, quest_data):
        """Complete field-specific quest"""
        field = quest_data.get('field', 'Sunflower Field')
        amount = quest_data.get('amount', 500000)
        
        logging.info(f"Completing field quest: {amount} pollen from {field}")
        
        return self.field_navigator.navigate_to_field(field)

class QuestTracker:
    """Track quest progress and completion"""
    
    def __init__(self):
        self.quest_progress = {}
        self.completed_quests = {}
        self.quest_history = []
        
    def start_tracking_quest(self, npc_id, quest_data):
        """Start tracking a quest"""
        quest_key = f"{npc_id}_{quest_data.get('type', 'unknown')}"
        self.quest_progress[quest_key] = {
            'npc_id': npc_id,
            'quest_data': quest_data,
            'start_time': time.time(),
            'progress': 0,
            'completed': False
        }
        
        logging.info(f"Started tracking quest: {quest_key}")
    
    def update_quest_progress(self, quest_key, progress):
        """Update quest progress"""
        if quest_key in self.quest_progress:
            self.quest_progress[quest_key]['progress'] = progress
            
            # Check if quest is completed
            quest_data = self.quest_progress[quest_key]['quest_data']
            required_amount = quest_data.get('amount', 100)
            
            if progress >= required_amount:
                self.complete_quest(quest_key)
    
    def complete_quest(self, quest_key):
        """Mark quest as completed"""
        if quest_key in self.quest_progress:
            quest_info = self.quest_progress[quest_key]
            quest_info['completed'] = True
            quest_info['completion_time'] = time.time()
            
            # Move to completed quests
            self.completed_quests[quest_key] = quest_info
            
            # Add to history
            self.quest_history.append({
                'quest_key': quest_key,
                'completion_time': time.time(),
                'duration': time.time() - quest_info['start_time']
            })
            
            logging.info(f"Completed quest: {quest_key}")
    
    def get_active_quests(self):
        """Get all active (incomplete) quests"""
        return {k: v for k, v in self.quest_progress.items() if not v['completed']}
    
    def get_completed_quests(self):
        """Get all completed quests"""
        return self.completed_quests
    
    def get_quest_statistics(self):
        """Get quest completion statistics"""
        total_quests = len(self.quest_history)
        if total_quests == 0:
            return {}
        
        total_duration = sum(q['duration'] for q in self.quest_history)
        average_duration = total_duration / total_quests
        
        return {
            'total_completed': total_quests,
            'total_duration': total_duration,
            'average_duration': average_duration,
            'active_quests': len(self.get_active_quests())
        }