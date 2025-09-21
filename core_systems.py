"""
BSS Pro Macro - Core Systems Module
Advanced Bee Swarm Simulator automation with image recognition and safety features
"""

import cv2
import numpy as np
import pyautogui
import time
import random
import threading
import logging
from PIL import Image, ImageGrab
import json
import os
import sys
import keyboard
import psutil

# Configure PyAutoGUI settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

class ImageRecognition:
    """Advanced image recognition system for BSS automation"""
    
    def __init__(self):
        self.confidence_threshold = 0.8
        self.template_cache = {}
        self.screen_region = None
        
    def load_template(self, template_name):
        """Load and cache template images"""
        template_path = f"templates/{template_name}.png"
        if template_name not in self.template_cache:
            if os.path.exists(template_path):
                template = cv2.imread(template_path, cv2.IMREAD_COLOR)
                self.template_cache[template_name] = template
                return template
            else:
                logging.warning(f"Template {template_name} not found")
                return None
        return self.template_cache[template_name]
    
    def capture_screen(self, region=None):
        """Capture screen or specific region"""
        if region:
            screenshot = ImageGrab.grab(bbox=region)
        else:
            screenshot = ImageGrab.grab()
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    def find_template(self, template_name, region=None, confidence=None):
        """Find template on screen using OpenCV template matching"""
        if confidence is None:
            confidence = self.confidence_threshold
            
        template = self.load_template(template_name)
        if template is None:
            return None
            
        screen = self.capture_screen(region)
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        
        locations = np.where(result >= confidence)
        if len(locations[0]) > 0:
            # Return the best match
            max_loc = cv2.minMaxLoc(result)[3]
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            
            # Adjust for region offset
            if region:
                center_x += region[0]
                center_y += region[1]
                
            return (center_x, center_y)
        return None
    
    def find_multiple_templates(self, template_name, region=None, confidence=None):
        """Find multiple instances of a template"""
        if confidence is None:
            confidence = self.confidence_threshold
            
        template = self.load_template(template_name)
        if template is None:
            return []
            
        screen = self.capture_screen(region)
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        
        locations = np.where(result >= confidence)
        matches = []
        h, w = template.shape[:2]
        
        for pt in zip(*locations[::-1]):
            center_x = pt[0] + w // 2
            center_y = pt[1] + h // 2
            
            if region:
                center_x += region[0]
                center_y += region[1]
                
            matches.append((center_x, center_y))
            
        return matches
    
    def wait_for_template(self, template_name, timeout=30, region=None):
        """Wait for template to appear on screen"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            location = self.find_template(template_name, region)
            if location:
                return location
            time.sleep(0.5)
        return None

class InputAutomation:
    """Safe input automation with randomization"""
    
    def __init__(self, config):
        self.config = config
        self.last_action_time = 0
        self.action_delay_base = 0.1
        
    def safe_click(self, x, y, button='left', clicks=1):
        """Click with randomization and safety checks"""
        if not self._is_safe_to_act():
            return False
            
        # Add randomization to click position
        if self.config['safety']['click_randomization'] > 0:
            rand_x = random.uniform(-self.config['safety']['click_randomization'] * 10,
                                  self.config['safety']['click_randomization'] * 10)
            rand_y = random.uniform(-self.config['safety']['click_randomization'] * 10,
                                  self.config['safety']['click_randomization'] * 10)
            x += int(rand_x)
            y += int(rand_y)
        
        try:
            pyautogui.click(x, y, button=button, clicks=clicks)
            self._add_random_delay()
            return True
        except Exception as e:
            logging.error(f"Click failed: {e}")
            return False
    
    def safe_key_press(self, key, hold_time=None):
        """Press key with randomization"""
        if not self._is_safe_to_act():
            return False
            
        try:
            if hold_time:
                pyautogui.keyDown(key)
                time.sleep(hold_time + random.uniform(-0.1, 0.1))
                pyautogui.keyUp(key)
            else:
                pyautogui.press(key)
            self._add_random_delay()
            return True
        except Exception as e:
            logging.error(f"Key press failed: {e}")
            return False
    
    def safe_type(self, text, interval=0.1):
        """Type text with randomization"""
        if not self._is_safe_to_act():
            return False
            
        try:
            for char in text:
                pyautogui.typewrite(char)
                time.sleep(interval + random.uniform(-0.05, 0.05))
            return True
        except Exception as e:
            logging.error(f"Typing failed: {e}")
            return False
    
    def move_mouse_smooth(self, x, y, duration=1.0):
        """Move mouse smoothly with randomization"""
        if not self._is_safe_to_act():
            return False
            
        try:
            # Add some randomization to movement
            if self.config['safety']['movement_randomization'] > 0:
                rand_factor = self.config['safety']['movement_randomization']
                duration += random.uniform(-duration * rand_factor, duration * rand_factor)
                duration = max(0.1, duration)  # Ensure minimum duration
            
            pyautogui.moveTo(x, y, duration=duration)
            return True
        except Exception as e:
            logging.error(f"Mouse movement failed: {e}")
            return False
    
    def _is_safe_to_act(self):
        """Check if it's safe to perform an action"""
        # Check if BSS window is active
        try:
            active_window = pyautogui.getActiveWindow()
            if active_window and "Roblox" not in active_window.title:
                logging.warning("Roblox window not active")
                return False
        except:
            pass
        
        # Check minimum delay between actions
        current_time = time.time()
        if current_time - self.last_action_time < self.action_delay_base:
            time.sleep(self.action_delay_base - (current_time - self.last_action_time))
        
        self.last_action_time = time.time()
        return True
    
    def _add_random_delay(self):
        """Add random delay after actions"""
        if self.config['safety']['pause_randomization'] > 0:
            delay = random.uniform(0, self.config['safety']['pause_randomization'])
            time.sleep(delay)

class GameStateManager:
    """Manage game state and detection"""
    
    def __init__(self, image_recognition):
        self.image_rec = image_recognition
        self.current_field = None
        self.hive_full = False
        self.player_position = None
        self.last_state_check = 0
        
    def detect_current_field(self):
        """Detect which field the player is currently in"""
        fields = {
            'sunflower': 'Sunflower Field',
            'dandelion': 'Dandelion Field',
            'mushroom': 'Mushroom Field',
            'blue_flower': 'Blue Flower Field',
            'clover': 'Clover Field',
            'strawberry': 'Strawberry Field',
            'bamboo': 'Bamboo Field',
            'pineapple': 'Pineapple Patch',
            'spider': 'Spider Field',
            'rose': 'Rose Field',
            'cactus': 'Cactus Field',
            'pumpkin': 'Pumpkin Patch',
            'pine_tree': 'Pine Tree Forest',
            'stump': 'Stump Field',
            'coconut': 'Coconut Field',
            'pepper': 'Pepper Patch',
            'mountain_top': 'Mountain Top Field'
        }
        
        for field_key, field_name in fields.items():
            if self.image_rec.find_template(f"field_{field_key}"):
                self.current_field = field_name
                return field_name
        
        self.current_field = None
        return None
    
    def check_bag_full(self):
        """Check if bag is full"""
        bag_full_indicator = self.image_rec.find_template("bag_full")
        self.hive_full = bag_full_indicator is not None
        return self.hive_full
    
    def check_player_health(self):
        """Check player health status"""
        return self.image_rec.find_template("health_low") is None
    
    def detect_mobs(self):
        """Detect mobs in current area"""
        mobs = {}
        mob_types = ['ladybug', 'rhinobeetle', 'spider', 'mantis', 'scorpion', 'werewolf']
        
        for mob_type in mob_types:
            locations = self.image_rec.find_multiple_templates(f"mob_{mob_type}")
            if locations:
                mobs[mob_type] = locations
                
        return mobs
    
    def detect_collectibles(self):
        """Detect collectible items"""
        collectibles = {}
        item_types = ['token', 'honey', 'pollen', 'treat', 'ticket']
        
        for item_type in item_types:
            locations = self.image_rec.find_multiple_templates(f"item_{item_type}")
            if locations:
                collectibles[item_type] = locations
                
        return collectibles
    
    def update_state(self):
        """Update all game state information"""
        current_time = time.time()
        if current_time - self.last_state_check < 1.0:  # Don't update too frequently
            return
            
        self.detect_current_field()
        self.check_bag_full()
        self.last_state_check = current_time

class SafetyManager:
    """Manage safety features and anti-detection"""
    
    def __init__(self, config):
        self.config = config
        self.last_break_time = time.time()
        self.break_due = False
        self.emergency_stop = False
        self.pause_requested = False
        
    def should_take_break(self):
        """Check if it's time for a break"""
        if not self.config['safety']['break_interval_min']:
            return False
            
        current_time = time.time()
        time_since_break = current_time - self.last_break_time
        
        break_interval = random.uniform(
            self.config['safety']['break_interval_min'],
            self.config['safety']['break_interval_max']
        )
        
        return time_since_break >= break_interval
    
    def take_break(self):
        """Take a randomized break"""
        break_duration = random.uniform(
            self.config['safety']['break_duration_min'],
            self.config['safety']['break_duration_max']
        )
        
        logging.info(f"Taking break for {break_duration:.1f} seconds")
        time.sleep(break_duration)
        self.last_break_time = time.time()
    
    def check_emergency_conditions(self):
        """Check for emergency stop conditions"""
        # Check if failsafe position is triggered
        if pyautogui.position() == (0, 0):
            self.emergency_stop = True
            return True
            
        # Check if specific key combinations are pressed
        if keyboard.is_pressed('ctrl+alt+del'):
            self.emergency_stop = True
            return True
            
        return False
    
    def is_safe_to_continue(self):
        """Check if it's safe to continue macro operations"""
        if self.emergency_stop:
            return False
            
        if self.pause_requested:
            return False
            
        if self.check_emergency_conditions():
            return False
            
        return True

class Logger:
    """Advanced logging system"""
    
    def __init__(self, log_file="bss_macro.log"):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_action(self, action, details=""):
        """Log macro actions"""
        self.logger.info(f"Action: {action} - {details}")
    
    def log_error(self, error, details=""):
        """Log errors"""
        self.logger.error(f"Error: {error} - {details}")
    
    def log_warning(self, warning, details=""):
        """Log warnings"""
        self.logger.warning(f"Warning: {warning} - {details}")