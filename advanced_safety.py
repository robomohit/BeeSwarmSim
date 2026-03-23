"""
BSS Pro Macro - Advanced Safety Module
Enhanced safety features and anti-detection mechanisms
"""

import time
import random
import logging
import threading
import psutil
import os
import hashlib
from datetime import datetime, timedelta
from core_systems import ImageRecognition, InputAutomation

class AdvancedSafetyManager:
    """Advanced safety management with multiple detection layers"""
    
    def __init__(self, config):
        self.config = config
        self.safety_enabled = config['general']['safety_enabled']
        
        # Safety monitoring
        self.last_activity_time = time.time()
        self.activity_pattern = []
        self.break_schedule = []
        self.emergency_triggers = []
        
        # Detection avoidance
        self.behavior_randomizer = BehaviorRandomizer(config)
        self.pattern_breaker = PatternBreaker()
        self.activity_monitor = ActivityMonitor()
        
        # System monitoring
        self.system_monitor = SystemMonitor()
        self.process_monitor = ProcessMonitor()
        
        # Initialize safety systems
        self.initialize_safety_systems()
    
    def initialize_safety_systems(self):
        """Initialize all safety systems"""
        if not self.safety_enabled:
            logging.warning("Safety features are disabled!")
            return
        
        # Generate random break schedule
        self.generate_break_schedule()
        
        # Setup emergency triggers
        self.setup_emergency_triggers()
        
        # Start monitoring threads
        self.start_monitoring_threads()
        
        logging.info("Advanced safety systems initialized")
    
    def generate_break_schedule(self):
        """Generate randomized break schedule"""
        current_time = time.time()
        session_duration = 8 * 3600  # 8 hours max session
        
        # Generate breaks throughout the session
        break_count = random.randint(3, 8)
        
        for i in range(break_count):
            # Random break time within session
            break_time = current_time + random.uniform(
                i * (session_duration / break_count),
                (i + 1) * (session_duration / break_count)
            )
            
            # Random break duration
            break_duration = random.uniform(
                self.config['safety']['break_duration_min'],
                self.config['safety']['break_duration_max']
            )
            
            self.break_schedule.append({
                'time': break_time,
                'duration': break_duration,
                'type': 'scheduled',
                'taken': False
            })
        
        logging.info(f"Generated {break_count} scheduled breaks")
    
    def setup_emergency_triggers(self):
        """Setup emergency stop triggers"""
        self.emergency_triggers = [
            {'type': 'mouse_corner', 'active': True},
            {'type': 'key_combo', 'keys': ['ctrl', 'alt', 'del'], 'active': True},
            {'type': 'process_monitor', 'active': True},
            {'type': 'system_resource', 'active': True},
            {'type': 'time_limit', 'limit': 10 * 3600, 'active': True}  # 10 hour limit
        ]
    
    def start_monitoring_threads(self):
        """Start background monitoring threads"""
        if not self.safety_enabled:
            return
        
        # System monitoring thread
        system_thread = threading.Thread(target=self.system_monitoring_loop, daemon=True)
        system_thread.start()
        
        # Activity monitoring thread
        activity_thread = threading.Thread(target=self.activity_monitoring_loop, daemon=True)
        activity_thread.start()
        
        # Emergency monitoring thread
        emergency_thread = threading.Thread(target=self.emergency_monitoring_loop, daemon=True)
        emergency_thread.start()
    
    def check_safety_conditions(self):
        """Check all safety conditions"""
        if not self.safety_enabled:
            return True
        
        # Check emergency triggers
        if self.check_emergency_triggers():
            return False
        
        # Check scheduled breaks
        if self.check_scheduled_breaks():
            return False
        
        # Check system resources
        if not self.check_system_resources():
            return False
        
        # Check activity patterns
        if not self.check_activity_patterns():
            return False
        
        return True
    
    def check_emergency_triggers(self):
        """Check for emergency stop conditions"""
        for trigger in self.emergency_triggers:
            if not trigger['active']:
                continue
            
            if trigger['type'] == 'mouse_corner':
                if self.check_mouse_corner_trigger():
                    logging.critical("Emergency stop: Mouse corner trigger")
                    return True
            
            elif trigger['type'] == 'key_combo':
                if self.check_key_combo_trigger(trigger['keys']):
                    logging.critical("Emergency stop: Key combination trigger")
                    return True
            
            elif trigger['type'] == 'process_monitor':
                if self.check_process_monitor_trigger():
                    logging.critical("Emergency stop: Process monitor trigger")
                    return True
            
            elif trigger['type'] == 'system_resource':
                if self.check_system_resource_trigger():
                    logging.critical("Emergency stop: System resource trigger")
                    return True
            
            elif trigger['type'] == 'time_limit':
                if self.check_time_limit_trigger(trigger['limit']):
                    logging.critical("Emergency stop: Time limit reached")
                    return True
        
        return False
    
    def check_mouse_corner_trigger(self):
        """Check if mouse is in corner (failsafe)"""
        try:
            import pyautogui
            x, y = pyautogui.position()
            screen_width, screen_height = pyautogui.size()
            
            # Check corners
            corner_threshold = 5
            corners = [
                (0, 0),  # Top-left
                (screen_width - 1, 0),  # Top-right
                (0, screen_height - 1),  # Bottom-left
                (screen_width - 1, screen_height - 1)  # Bottom-right
            ]
            
            for corner_x, corner_y in corners:
                if abs(x - corner_x) <= corner_threshold and abs(y - corner_y) <= corner_threshold:
                    return True
            
            return False
        except:
            return False
    
    def check_key_combo_trigger(self, keys):
        """Check if emergency key combination is pressed"""
        try:
            import keyboard
            return all(keyboard.is_pressed(key) for key in keys)
        except:
            return False
    
    def check_process_monitor_trigger(self):
        """Check for suspicious processes"""
        try:
            suspicious_processes = [
                'cheatengine', 'processhacker', 'wireshark', 'fiddler',
                'debugger', 'ida', 'ollydbg', 'x64dbg'
            ]
            
            for proc in psutil.process_iter(['name']):
                proc_name = proc.info['name'].lower()
                if any(suspicious in proc_name for suspicious in suspicious_processes):
                    logging.warning(f"Suspicious process detected: {proc_name}")
                    return True
            
            return False
        except:
            return False
    
    def check_system_resource_trigger(self):
        """Check system resource usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            
            # Stop if system is under heavy load
            if cpu_percent > 90 or memory_percent > 95:
                logging.warning(f"High system resource usage: CPU {cpu_percent}%, RAM {memory_percent}%")
                return True
            
            return False
        except:
            return False
    
    def check_time_limit_trigger(self, limit_seconds):
        """Check if time limit has been reached"""
        runtime = time.time() - self.last_activity_time
        return runtime >= limit_seconds
    
    def check_scheduled_breaks(self):
        """Check if a scheduled break is due"""
        current_time = time.time()
        
        for break_info in self.break_schedule:
            if not break_info['taken'] and current_time >= break_info['time']:
                logging.info("Scheduled break is due")
                self.take_scheduled_break(break_info)
                return True
        
        return False
    
    def take_scheduled_break(self, break_info):
        """Take a scheduled break"""
        logging.info(f"Taking scheduled break for {break_info['duration']:.0f} seconds")
        
        # Mark break as taken
        break_info['taken'] = True
        
        # Add some randomization to break duration
        actual_duration = break_info['duration'] * random.uniform(0.8, 1.2)
        
        # Sleep for break duration
        time.sleep(actual_duration)
        
        logging.info("Scheduled break completed")
    
    def check_system_resources(self):
        """Check if system resources are adequate"""
        try:
            # Check available memory
            memory = psutil.virtual_memory()
            if memory.percent > 90:
                logging.warning("High memory usage detected")
                return False
            
            # Check CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > 85:
                logging.warning("High CPU usage detected")
                return False
            
            # Check disk space
            disk = psutil.disk_usage('/')
            if disk.percent > 95:
                logging.warning("Low disk space detected")
                return False
            
            return True
        except:
            # If we can't check resources, assume it's safe
            return True
    
    def check_activity_patterns(self):
        """Check for suspicious activity patterns"""
        # This would analyze activity patterns for bot-like behavior
        # For now, just return True
        return True
    
    def system_monitoring_loop(self):
        """Background system monitoring loop"""
        while True:
            try:
                # Monitor system health
                self.system_monitor.update()
                
                # Check for system anomalies
                if self.system_monitor.detect_anomalies():
                    logging.warning("System anomalies detected")
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logging.error(f"System monitoring error: {e}")
                time.sleep(60)
    
    def activity_monitoring_loop(self):
        """Background activity monitoring loop"""
        while True:
            try:
                # Monitor activity patterns
                self.activity_monitor.record_activity()
                
                # Analyze patterns
                if self.activity_monitor.detect_bot_patterns():
                    logging.warning("Bot-like activity patterns detected")
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logging.error(f"Activity monitoring error: {e}")
                time.sleep(30)
    
    def emergency_monitoring_loop(self):
        """Background emergency monitoring loop"""
        while True:
            try:
                # Quick emergency checks
                if self.check_mouse_corner_trigger():
                    logging.critical("Emergency stop triggered by mouse position")
                    # Would trigger emergency stop
                
                time.sleep(0.5)  # Check very frequently
                
            except Exception as e:
                logging.error(f"Emergency monitoring error: {e}")
                time.sleep(5)

class BehaviorRandomizer:
    """Randomize behavior to avoid detection"""
    
    def __init__(self, config):
        self.config = config
        self.randomization_enabled = config['general']['randomization_enabled']
    
    def randomize_timing(self, base_time):
        """Add randomization to timing"""
        if not self.randomization_enabled:
            return base_time
        
        variance = self.config['safety']['pause_randomization']
        return base_time * random.uniform(1 - variance, 1 + variance)
    
    def randomize_position(self, x, y):
        """Add randomization to click positions"""
        if not self.randomization_enabled:
            return x, y
        
        variance = self.config['safety']['click_randomization'] * 10
        new_x = x + random.uniform(-variance, variance)
        new_y = y + random.uniform(-variance, variance)
        
        return int(new_x), int(new_y)
    
    def randomize_movement(self, duration):
        """Add randomization to movement duration"""
        if not self.randomization_enabled:
            return duration
        
        variance = self.config['safety']['movement_randomization']
        return duration * random.uniform(1 - variance, 1 + variance)
    
    def should_take_micro_break(self):
        """Randomly decide if a micro break should be taken"""
        if not self.randomization_enabled:
            return False
        
        # 5% chance of micro break
        return random.random() < 0.05
    
    def get_micro_break_duration(self):
        """Get random micro break duration"""
        return random.uniform(0.5, 3.0)

class PatternBreaker:
    """Break repetitive patterns to avoid detection"""
    
    def __init__(self):
        self.action_history = []
        self.pattern_threshold = 5
    
    def record_action(self, action):
        """Record an action for pattern analysis"""
        self.action_history.append({
            'action': action,
            'timestamp': time.time()
        })
        
        # Keep only recent history
        cutoff_time = time.time() - 300  # 5 minutes
        self.action_history = [
            a for a in self.action_history 
            if a['timestamp'] > cutoff_time
        ]
    
    def should_break_pattern(self):
        """Check if pattern should be broken"""
        if len(self.action_history) < self.pattern_threshold:
            return False
        
        # Check for repetitive patterns
        recent_actions = [a['action'] for a in self.action_history[-self.pattern_threshold:]]
        
        # If all recent actions are the same, break pattern
        if len(set(recent_actions)) == 1:
            return True
        
        return False
    
    def get_pattern_break_action(self):
        """Get an action to break the current pattern"""
        break_actions = [
            'random_mouse_movement',
            'brief_pause',
            'check_stats',
            'look_around',
            'micro_break'
        ]
        
        return random.choice(break_actions)

class ActivityMonitor:
    """Monitor activity patterns for bot detection"""
    
    def __init__(self):
        self.activity_log = []
        self.bot_indicators = 0
        self.human_indicators = 0
    
    def record_activity(self):
        """Record current activity"""
        activity = {
            'timestamp': time.time(),
            'mouse_position': self.get_mouse_position(),
            'active_window': self.get_active_window(),
            'cpu_usage': self.get_cpu_usage()
        }
        
        self.activity_log.append(activity)
        
        # Keep only recent activity
        cutoff_time = time.time() - 3600  # 1 hour
        self.activity_log = [
            a for a in self.activity_log 
            if a['timestamp'] > cutoff_time
        ]
    
    def detect_bot_patterns(self):
        """Detect bot-like patterns in activity"""
        if len(self.activity_log) < 10:
            return False
        
        # Check for too-regular timing
        if self.check_regular_timing():
            self.bot_indicators += 1
        
        # Check for inhuman precision
        if self.check_inhuman_precision():
            self.bot_indicators += 1
        
        # Check for lack of idle time
        if self.check_lack_of_idle():
            self.bot_indicators += 1
        
        # Reset indicators periodically
        if time.time() % 3600 < 60:  # Every hour
            self.bot_indicators = max(0, self.bot_indicators - 1)
        
        return self.bot_indicators > 3
    
    def check_regular_timing(self):
        """Check for too-regular timing patterns"""
        if len(self.activity_log) < 5:
            return False
        
        intervals = []
        for i in range(1, len(self.activity_log)):
            interval = self.activity_log[i]['timestamp'] - self.activity_log[i-1]['timestamp']
            intervals.append(interval)
        
        # Check if intervals are too similar
        if len(intervals) > 0:
            avg_interval = sum(intervals) / len(intervals)
            variance = sum((i - avg_interval) ** 2 for i in intervals) / len(intervals)
            
            # If variance is too low, it might be a bot
            return variance < 0.1
        
        return False
    
    def check_inhuman_precision(self):
        """Check for inhuman precision in actions"""
        # This would check for pixel-perfect clicks, etc.
        # For now, return False
        return False
    
    def check_lack_of_idle(self):
        """Check for lack of idle time"""
        # Humans take breaks, bots don't
        # This would check for continuous activity
        return False
    
    def get_mouse_position(self):
        """Get current mouse position"""
        try:
            import pyautogui
            return pyautogui.position()
        except:
            return (0, 0)
    
    def get_active_window(self):
        """Get active window title"""
        try:
            import pyautogui
            window = pyautogui.getActiveWindow()
            return window.title if window else "Unknown"
        except:
            return "Unknown"
    
    def get_cpu_usage(self):
        """Get current CPU usage"""
        try:
            return psutil.cpu_percent()
        except:
            return 0

class SystemMonitor:
    """Monitor system health and anomalies"""
    
    def __init__(self):
        self.baseline_metrics = {}
        self.current_metrics = {}
        self.anomaly_threshold = 2.0  # Standard deviations
    
    def update(self):
        """Update system metrics"""
        try:
            self.current_metrics = {
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_io': psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else {},
                'network_io': psutil.net_io_counters()._asdict() if psutil.net_io_counters() else {},
                'process_count': len(psutil.pids()),
                'timestamp': time.time()
            }
            
            # Update baseline if not set
            if not self.baseline_metrics:
                self.baseline_metrics = self.current_metrics.copy()
                
        except Exception as e:
            logging.error(f"System metrics update failed: {e}")
    
    def detect_anomalies(self):
        """Detect system anomalies"""
        if not self.baseline_metrics or not self.current_metrics:
            return False
        
        anomalies = []
        
        # Check CPU usage
        if self.current_metrics['cpu_percent'] > 90:
            anomalies.append("High CPU usage")
        
        # Check memory usage
        if self.current_metrics['memory_percent'] > 90:
            anomalies.append("High memory usage")
        
        # Check process count
        baseline_processes = self.baseline_metrics.get('process_count', 0)
        current_processes = self.current_metrics.get('process_count', 0)
        
        if current_processes > baseline_processes * 1.5:
            anomalies.append("High process count")
        
        return len(anomalies) > 0

class ProcessMonitor:
    """Monitor running processes for security"""
    
    def __init__(self):
        self.baseline_processes = set()
        self.suspicious_processes = [
            'cheatengine', 'processhacker', 'wireshark', 'fiddler',
            'debugger', 'ida', 'ollydbg', 'x64dbg', 'autohotkey'
        ]
        
        self.update_baseline()
    
    def update_baseline(self):
        """Update baseline process list"""
        try:
            self.baseline_processes = set()
            for proc in psutil.process_iter(['name']):
                self.baseline_processes.add(proc.info['name'].lower())
        except Exception as e:
            logging.error(f"Process baseline update failed: {e}")
    
    def check_new_processes(self):
        """Check for new processes since baseline"""
        try:
            current_processes = set()
            for proc in psutil.process_iter(['name']):
                current_processes.add(proc.info['name'].lower())
            
            new_processes = current_processes - self.baseline_processes
            
            # Check for suspicious new processes
            suspicious_new = []
            for proc_name in new_processes:
                if any(suspicious in proc_name for suspicious in self.suspicious_processes):
                    suspicious_new.append(proc_name)
            
            return suspicious_new
            
        except Exception as e:
            logging.error(f"Process check failed: {e}")
            return []
    
    def is_roblox_running(self):
        """Check if Roblox is still running"""
        try:
            for proc in psutil.process_iter(['name']):
                if 'roblox' in proc.info['name'].lower():
                    return True
            return False
        except:
            return True  # Assume it's running if we can't check