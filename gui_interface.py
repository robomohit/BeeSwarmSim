"""
BSS Pro Macro - GUI Interface Module
Modern and user-friendly graphical interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import threading
import time
import logging
from PIL import Image, ImageTk
import os

class MacroGUI:
    """Main GUI class for the BSS Pro Macro"""
    
    def __init__(self, config, macro_controller):
        self.config = config
        self.macro_controller = macro_controller
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.load_config_to_gui()
        self.running = False
        
    def setup_window(self):
        """Setup main window properties"""
        self.root.title("BSS Pro Macro v1.0.0 - Advanced Bee Swarm Simulator Automation")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Set window icon if available
        try:
            if os.path.exists("icon.ico"):
                self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom colors
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#F18F01',
            'warning': '#C73E1D',
            'background': '#F5F5F5',
            'text': '#333333'
        }
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Create main notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_main_tab()
        self.create_farming_tab()
        self.create_quest_tab()
        self.create_mob_tab()
        self.create_advanced_tab()
        self.create_stats_tab()
        self.create_logs_tab()
        
        # Create control panel at bottom
        self.create_control_panel()
    
    def create_main_tab(self):
        """Create main control tab"""
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text="Main Control")
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Macro Status", padding=10)
        status_frame.pack(fill='x', padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Status: Stopped", font=('Arial', 12, 'bold'))
        self.status_label.pack()
        
        self.runtime_label = ttk.Label(status_frame, text="Runtime: 00:00:00")
        self.runtime_label.pack()
        
        # Quick actions
        actions_frame = ttk.LabelFrame(main_frame, text="Quick Actions", padding=10)
        actions_frame.pack(fill='x', padx=10, pady=5)
        
        button_frame = ttk.Frame(actions_frame)
        button_frame.pack()
        
        self.start_button = ttk.Button(button_frame, text="Start Macro", command=self.start_macro,
                                     style='success.TButton')
        self.start_button.pack(side='left', padx=5)
        
        self.pause_button = ttk.Button(button_frame, text="Pause", command=self.pause_macro,
                                     state='disabled')
        self.pause_button.pack(side='left', padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_macro,
                                    state='disabled', style='warning.TButton')
        self.stop_button.pack(side='left', padx=5)
        
        # Current activity
        activity_frame = ttk.LabelFrame(main_frame, text="Current Activity", padding=10)
        activity_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.activity_text = scrolledtext.ScrolledText(activity_frame, height=15, state='disabled')
        self.activity_text.pack(fill='both', expand=True)
        
        # Progress bars
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding=10)
        progress_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(progress_frame, text="Overall Progress:").pack(anchor='w')
        self.overall_progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.overall_progress.pack(fill='x', pady=2)
        
        ttk.Label(progress_frame, text="Current Task:").pack(anchor='w')
        self.task_progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.task_progress.pack(fill='x', pady=2)
    
    def create_farming_tab(self):
        """Create farming configuration tab"""
        farming_frame = ttk.Frame(self.notebook)
        self.notebook.add(farming_frame, text="Farming")
        
        # Create scrollable frame
        canvas = tk.Canvas(farming_frame)
        scrollbar = ttk.Scrollbar(farming_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Farming settings
        general_frame = ttk.LabelFrame(scrollable_frame, text="General Settings", padding=10)
        general_frame.pack(fill='x', padx=10, pady=5)
        
        self.farming_enabled = tk.BooleanVar()
        ttk.Checkbutton(general_frame, text="Enable Farming", variable=self.farming_enabled).pack(anchor='w')
        
        self.field_rotation_enabled = tk.BooleanVar()
        ttk.Checkbutton(general_frame, text="Enable Field Rotation", variable=self.field_rotation_enabled).pack(anchor='w')
        
        # Field selection
        fields_frame = ttk.LabelFrame(scrollable_frame, text="Field Selection", padding=10)
        fields_frame.pack(fill='x', padx=10, pady=5)
        
        self.field_vars = {}
        fields = [
            "Sunflower Field", "Dandelion Field", "Mushroom Field", "Blue Flower Field",
            "Clover Field", "Strawberry Field", "Bamboo Field", "Pineapple Patch",
            "Spider Field", "Rose Field", "Cactus Field", "Pumpkin Patch",
            "Pine Tree Forest", "Stump Field", "Coconut Field", "Pepper Patch",
            "Mountain Top Field"
        ]
        
        # Create field checkboxes in columns
        cols = 3
        for i, field in enumerate(fields):
            row = i // cols
            col = i % cols
            
            if col == 0:
                field_row_frame = ttk.Frame(fields_frame)
                field_row_frame.pack(fill='x', pady=2)
            
            var = tk.BooleanVar()
            self.field_vars[field] = var
            ttk.Checkbutton(field_row_frame, text=field, variable=var).pack(side='left', padx=10)
        
        # Timing settings
        timing_frame = ttk.LabelFrame(scrollable_frame, text="Timing Settings", padding=10)
        timing_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(timing_frame, text="Collect Time (min):").pack(anchor='w')
        self.collect_time_min = tk.StringVar()
        ttk.Entry(timing_frame, textvariable=self.collect_time_min, width=10).pack(anchor='w', pady=2)
        
        ttk.Label(timing_frame, text="Collect Time (max):").pack(anchor='w')
        self.collect_time_max = tk.StringVar()
        ttk.Entry(timing_frame, textvariable=self.collect_time_max, width=10).pack(anchor='w', pady=2)
        
        ttk.Label(timing_frame, text="Hive Return Threshold (%):").pack(anchor='w')
        self.hive_return_threshold = tk.StringVar()
        ttk.Entry(timing_frame, textvariable=self.hive_return_threshold, width=10).pack(anchor='w', pady=2)
    
    def create_quest_tab(self):
        """Create quest configuration tab"""
        quest_frame = ttk.Frame(self.notebook)
        self.notebook.add(quest_frame, text="Quests")
        
        # Quest settings
        general_frame = ttk.LabelFrame(quest_frame, text="General Settings", padding=10)
        general_frame.pack(fill='x', padx=10, pady=5)
        
        self.quests_enabled = tk.BooleanVar()
        ttk.Checkbutton(general_frame, text="Enable Quest System", variable=self.quests_enabled).pack(anchor='w')
        
        self.auto_accept_quests = tk.BooleanVar()
        ttk.Checkbutton(general_frame, text="Auto Accept Quests", variable=self.auto_accept_quests).pack(anchor='w')
        
        # NPC settings
        npc_frame = ttk.LabelFrame(quest_frame, text="NPC Settings", padding=10)
        npc_frame.pack(fill='x', padx=10, pady=5)
        
        self.npc_vars = {}
        npcs = [
            ("Black Bear", "black_bear_enabled"),
            ("Brown Bear", "brown_bear_enabled"),
            ("Polar Bear", "polar_bear_enabled"),
            ("Panda Bear", "panda_bear_enabled"),
            ("Science Bear", "science_bear_enabled"),
            ("Mother Bear", "mother_bear_enabled")
        ]
        
        for npc_name, var_name in npcs:
            var = tk.BooleanVar()
            self.npc_vars[var_name] = var
            ttk.Checkbutton(npc_frame, text=f"Enable {npc_name} Quests", variable=var).pack(anchor='w')
        
        # Quest progress
        progress_frame = ttk.LabelFrame(quest_frame, text="Quest Progress", padding=10)
        progress_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview for quest display
        columns = ('NPC', 'Quest', 'Progress', 'Status')
        self.quest_tree = ttk.Treeview(progress_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.quest_tree.heading(col, text=col)
            self.quest_tree.column(col, width=150)
        
        quest_scrollbar = ttk.Scrollbar(progress_frame, orient='vertical', command=self.quest_tree.yview)
        self.quest_tree.configure(yscrollcommand=quest_scrollbar.set)
        
        self.quest_tree.pack(side='left', fill='both', expand=True)
        quest_scrollbar.pack(side='right', fill='y')
    
    def create_mob_tab(self):
        """Create mob fighting configuration tab"""
        mob_frame = ttk.Frame(self.notebook)
        self.notebook.add(mob_frame, text="Mob Fighting")
        
        # Mob settings
        general_frame = ttk.LabelFrame(mob_frame, text="General Settings", padding=10)
        general_frame.pack(fill='x', padx=10, pady=5)
        
        self.mobs_enabled = tk.BooleanVar()
        ttk.Checkbutton(general_frame, text="Enable Mob Fighting", variable=self.mobs_enabled).pack(anchor='w')
        
        ttk.Label(general_frame, text="Mob Detection Timeout (seconds):").pack(anchor='w')
        self.mob_detection_timeout = tk.StringVar()
        ttk.Entry(general_frame, textvariable=self.mob_detection_timeout, width=10).pack(anchor='w', pady=2)
        
        # Mob type settings
        mob_types_frame = ttk.LabelFrame(mob_frame, text="Mob Types", padding=10)
        mob_types_frame.pack(fill='x', padx=10, pady=5)
        
        self.mob_type_vars = {}
        mob_types = [
            ("Ladybugs", "kill_ladybugs"),
            ("Rhino Beetles", "kill_rhinobeetles"),
            ("Spiders", "kill_spiders"),
            ("Mantis", "kill_mantis"),
            ("Scorpions", "kill_scorpions"),
            ("Werewolves", "kill_werewolves")
        ]
        
        for mob_name, var_name in mob_types:
            var = tk.BooleanVar()
            self.mob_type_vars[var_name] = var
            ttk.Checkbutton(mob_types_frame, text=f"Kill {mob_name}", variable=var).pack(anchor='w')
        
        # Mob statistics
        stats_frame = ttk.LabelFrame(mob_frame, text="Mob Statistics", padding=10)
        stats_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview for mob stats
        columns = ('Mob Type', 'Kills', 'Loot Collected', 'Avg Fight Time')
        self.mob_stats_tree = ttk.Treeview(stats_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.mob_stats_tree.heading(col, text=col)
            self.mob_stats_tree.column(col, width=150)
        
        mob_stats_scrollbar = ttk.Scrollbar(stats_frame, orient='vertical', command=self.mob_stats_tree.yview)
        self.mob_stats_tree.configure(yscrollcommand=mob_stats_scrollbar.set)
        
        self.mob_stats_tree.pack(side='left', fill='both', expand=True)
        mob_stats_scrollbar.pack(side='right', fill='y')
    
    def create_advanced_tab(self):
        """Create advanced settings tab"""
        advanced_frame = ttk.Frame(self.notebook)
        self.notebook.add(advanced_frame, text="Advanced")
        
        # Safety settings
        safety_frame = ttk.LabelFrame(advanced_frame, text="Safety Settings", padding=10)
        safety_frame.pack(fill='x', padx=10, pady=5)
        
        self.safety_enabled = tk.BooleanVar()
        ttk.Checkbutton(safety_frame, text="Enable Safety Features", variable=self.safety_enabled).pack(anchor='w')
        
        self.randomization_enabled = tk.BooleanVar()
        ttk.Checkbutton(safety_frame, text="Enable Randomization", variable=self.randomization_enabled).pack(anchor='w')
        
        # Randomization settings
        rand_frame = ttk.LabelFrame(advanced_frame, text="Randomization Settings", padding=10)
        rand_frame.pack(fill='x', padx=10, pady=5)
        
        settings = [
            ("Movement Randomization:", "movement_randomization"),
            ("Click Randomization:", "click_randomization"),
            ("Pause Randomization:", "pause_randomization")
        ]
        
        self.rand_vars = {}
        for label, var_name in settings:
            ttk.Label(rand_frame, text=label).pack(anchor='w')
            var = tk.StringVar()
            self.rand_vars[var_name] = var
            ttk.Entry(rand_frame, textvariable=var, width=10).pack(anchor='w', pady=2)
        
        # Break settings
        break_frame = ttk.LabelFrame(advanced_frame, text="Break Settings", padding=10)
        break_frame.pack(fill='x', padx=10, pady=5)
        
        break_settings = [
            ("Break Interval Min (seconds):", "break_interval_min"),
            ("Break Interval Max (seconds):", "break_interval_max"),
            ("Break Duration Min (seconds):", "break_duration_min"),
            ("Break Duration Max (seconds):", "break_duration_max")
        ]
        
        self.break_vars = {}
        for label, var_name in break_settings:
            ttk.Label(break_frame, text=label).pack(anchor='w')
            var = tk.StringVar()
            self.break_vars[var_name] = var
            ttk.Entry(break_frame, textvariable=var, width=10).pack(anchor='w', pady=2)
        
        # Hotkey settings
        hotkey_frame = ttk.LabelFrame(advanced_frame, text="Hotkey Settings", padding=10)
        hotkey_frame.pack(fill='x', padx=10, pady=5)
        
        hotkey_settings = [
            ("Start/Stop:", "start_stop"),
            ("Pause/Resume:", "pause_resume"),
            ("Emergency Stop:", "emergency_stop"),
            ("Show/Hide GUI:", "show_hide_gui")
        ]
        
        self.hotkey_vars = {}
        for label, var_name in hotkey_settings:
            frame = ttk.Frame(hotkey_frame)
            frame.pack(fill='x', pady=2)
            
            ttk.Label(frame, text=label).pack(side='left')
            var = tk.StringVar()
            self.hotkey_vars[var_name] = var
            ttk.Entry(frame, textvariable=var, width=10).pack(side='right')
    
    def create_stats_tab(self):
        """Create statistics tab"""
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="Statistics")
        
        # Overall stats
        overall_frame = ttk.LabelFrame(stats_frame, text="Overall Statistics", padding=10)
        overall_frame.pack(fill='x', padx=10, pady=5)
        
        self.stats_labels = {}
        stats = [
            "Total Runtime:", "Pollen Collected:", "Honey Made:", "Quests Completed:",
            "Mobs Killed:", "Items Collected:", "Fields Visited:", "Average Session Time:"
        ]
        
        for i, stat in enumerate(stats):
            row = i // 2
            col = i % 2
            
            if col == 0:
                stat_row_frame = ttk.Frame(overall_frame)
                stat_row_frame.pack(fill='x', pady=2)
            
            label = ttk.Label(stat_row_frame, text=f"{stat} 0")
            label.pack(side='left', padx=20)
            self.stats_labels[stat.replace(":", "")] = label
        
        # Performance metrics
        performance_frame = ttk.LabelFrame(stats_frame, text="Performance Metrics", padding=10)
        performance_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Graph placeholder (would need matplotlib for real graphs)
        self.performance_text = scrolledtext.ScrolledText(performance_frame, height=20, state='disabled')
        self.performance_text.pack(fill='both', expand=True)
    
    def create_logs_tab(self):
        """Create logs tab"""
        logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(logs_frame, text="Logs")
        
        # Log controls
        controls_frame = ttk.Frame(logs_frame)
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(controls_frame, text="Clear Logs", command=self.clear_logs).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Save Logs", command=self.save_logs).pack(side='left', padx=5)
        
        # Log level selection
        ttk.Label(controls_frame, text="Log Level:").pack(side='left', padx=10)
        self.log_level = tk.StringVar(value="INFO")
        log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        ttk.Combobox(controls_frame, textvariable=self.log_level, values=log_levels, width=10).pack(side='left')
        
        # Log display
        self.log_text = scrolledtext.ScrolledText(logs_frame, state='disabled')
        self.log_text.pack(fill='both', expand=True, padx=10, pady=5)
    
    def create_control_panel(self):
        """Create bottom control panel"""
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Left side - Config controls
        left_frame = ttk.Frame(control_frame)
        left_frame.pack(side='left')
        
        ttk.Button(left_frame, text="Load Config", command=self.load_config).pack(side='left', padx=5)
        ttk.Button(left_frame, text="Save Config", command=self.save_config).pack(side='left', padx=5)
        ttk.Button(left_frame, text="Reset Config", command=self.reset_config).pack(side='left', padx=5)
        
        # Right side - Info
        right_frame = ttk.Frame(control_frame)
        right_frame.pack(side='right')
        
        ttk.Label(right_frame, text="BSS Pro Macro v1.0.0 - Created by Claude").pack()
    
    def load_config_to_gui(self):
        """Load configuration values to GUI elements"""
        # Farming settings
        self.farming_enabled.set(self.config['farming']['enabled'])
        self.field_rotation_enabled.set(self.config['farming']['field_rotation_enabled'])
        self.collect_time_min.set(str(self.config['farming']['collect_time_min']))
        self.collect_time_max.set(str(self.config['farming']['collect_time_max']))
        self.hive_return_threshold.set(str(self.config['farming']['hive_return_threshold']))
        
        # Field selection
        preferred_fields = self.config['farming']['preferred_fields']
        for field, var in self.field_vars.items():
            var.set(field in preferred_fields)
        
        # Quest settings
        self.quests_enabled.set(self.config['quests']['enabled'])
        self.auto_accept_quests.set(self.config['quests']['auto_accept_quests'])
        
        for var_name, var in self.npc_vars.items():
            var.set(self.config['quests'].get(var_name, False))
        
        # Mob settings
        self.mobs_enabled.set(self.config['mobs']['enabled'])
        self.mob_detection_timeout.set(str(self.config['mobs']['mob_detection_timeout']))
        
        for var_name, var in self.mob_type_vars.items():
            var.set(self.config['mobs'].get(var_name, False))
        
        # Safety settings
        self.safety_enabled.set(self.config['general']['safety_enabled'])
        self.randomization_enabled.set(self.config['general']['randomization_enabled'])
        
        # Randomization settings
        for var_name, var in self.rand_vars.items():
            var.set(str(self.config['safety'].get(var_name, 0)))
        
        # Break settings
        for var_name, var in self.break_vars.items():
            var.set(str(self.config['safety'].get(var_name, 0)))
        
        # Hotkey settings
        for var_name, var in self.hotkey_vars.items():
            var.set(self.config['hotkeys'].get(var_name, ''))
    
    def save_config_from_gui(self):
        """Save GUI values to configuration"""
        # Farming settings
        self.config['farming']['enabled'] = self.farming_enabled.get()
        self.config['farming']['field_rotation_enabled'] = self.field_rotation_enabled.get()
        self.config['farming']['collect_time_min'] = int(self.collect_time_min.get() or 45)
        self.config['farming']['collect_time_max'] = int(self.collect_time_max.get() or 90)
        self.config['farming']['hive_return_threshold'] = int(self.hive_return_threshold.get() or 95)
        
        # Field selection
        preferred_fields = []
        for field, var in self.field_vars.items():
            if var.get():
                preferred_fields.append(field)
        self.config['farming']['preferred_fields'] = preferred_fields
        
        # Quest settings
        self.config['quests']['enabled'] = self.quests_enabled.get()
        self.config['quests']['auto_accept_quests'] = self.auto_accept_quests.get()
        
        for var_name, var in self.npc_vars.items():
            self.config['quests'][var_name] = var.get()
        
        # Mob settings
        self.config['mobs']['enabled'] = self.mobs_enabled.get()
        self.config['mobs']['mob_detection_timeout'] = int(self.mob_detection_timeout.get() or 30)
        
        for var_name, var in self.mob_type_vars.items():
            self.config['mobs'][var_name] = var.get()
        
        # Safety settings
        self.config['general']['safety_enabled'] = self.safety_enabled.get()
        self.config['general']['randomization_enabled'] = self.randomization_enabled.get()
        
        # Randomization settings
        for var_name, var in self.rand_vars.items():
            self.config['safety'][var_name] = float(var.get() or 0)
        
        # Break settings
        for var_name, var in self.break_vars.items():
            self.config['safety'][var_name] = int(var.get() or 0)
        
        # Hotkey settings
        for var_name, var in self.hotkey_vars.items():
            self.config['hotkeys'][var_name] = var.get()
    
    def start_macro(self):
        """Start the macro"""
        if not self.running:
            self.save_config_from_gui()
            self.running = True
            
            # Update UI
            self.start_button.config(state='disabled')
            self.pause_button.config(state='normal')
            self.stop_button.config(state='normal')
            self.status_label.config(text="Status: Running")
            self.overall_progress.start()
            
            # Start macro in separate thread
            self.macro_thread = threading.Thread(target=self.run_macro_thread)
            self.macro_thread.daemon = True
            self.macro_thread.start()
            
            self.log_message("Macro started")
    
    def pause_macro(self):
        """Pause/resume the macro"""
        if self.running:
            if self.macro_controller.is_paused():
                self.macro_controller.resume()
                self.pause_button.config(text="Pause")
                self.status_label.config(text="Status: Running")
                self.log_message("Macro resumed")
            else:
                self.macro_controller.pause()
                self.pause_button.config(text="Resume")
                self.status_label.config(text="Status: Paused")
                self.log_message("Macro paused")
    
    def stop_macro(self):
        """Stop the macro"""
        if self.running:
            self.running = False
            self.macro_controller.stop()
            
            # Update UI
            self.start_button.config(state='normal')
            self.pause_button.config(state='disabled', text="Pause")
            self.stop_button.config(state='disabled')
            self.status_label.config(text="Status: Stopped")
            self.overall_progress.stop()
            
            self.log_message("Macro stopped")
    
    def run_macro_thread(self):
        """Run macro in separate thread"""
        try:
            self.macro_controller.run(self.config)
        except Exception as e:
            self.log_message(f"Macro error: {str(e)}", "ERROR")
        finally:
            self.running = False
            # Reset UI in main thread
            self.root.after(0, self.stop_macro)
    
    def load_config(self):
        """Load configuration from file"""
        filename = filedialog.askopenfilename(
            title="Load Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.config = json.load(f)
                self.load_config_to_gui()
                self.log_message(f"Configuration loaded from {filename}")
                messagebox.showinfo("Success", "Configuration loaded successfully!")
            except Exception as e:
                self.log_message(f"Failed to load config: {str(e)}", "ERROR")
                messagebox.showerror("Error", f"Failed to load configuration: {str(e)}")
    
    def save_config(self):
        """Save configuration to file"""
        filename = filedialog.asksaveasfilename(
            title="Save Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.save_config_from_gui()
                with open(filename, 'w') as f:
                    json.dump(self.config, f, indent=4)
                self.log_message(f"Configuration saved to {filename}")
                messagebox.showinfo("Success", "Configuration saved successfully!")
            except Exception as e:
                self.log_message(f"Failed to save config: {str(e)}", "ERROR")
                messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
    
    def reset_config(self):
        """Reset configuration to defaults"""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all settings to defaults?"):
            try:
                with open('config.json', 'r') as f:
                    self.config = json.load(f)
                self.load_config_to_gui()
                self.log_message("Configuration reset to defaults")
                messagebox.showinfo("Success", "Configuration reset successfully!")
            except Exception as e:
                self.log_message(f"Failed to reset config: {str(e)}", "ERROR")
                messagebox.showerror("Error", f"Failed to reset configuration: {str(e)}")
    
    def log_message(self, message, level="INFO"):
        """Add message to log display"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        
        # Also add to activity text if it's an important message
        if level in ["INFO", "WARNING", "ERROR"]:
            self.activity_text.config(state='normal')
            self.activity_text.insert(tk.END, log_entry)
            self.activity_text.see(tk.END)
            self.activity_text.config(state='disabled')
    
    def clear_logs(self):
        """Clear log display"""
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        
        self.activity_text.config(state='normal')
        self.activity_text.delete(1.0, tk.END)
        self.activity_text.config(state='disabled')
    
    def save_logs(self):
        """Save logs to file"""
        filename = filedialog.asksaveasfilename(
            title="Save Logs",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                messagebox.showinfo("Success", "Logs saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save logs: {str(e)}")
    
    def update_stats(self, stats):
        """Update statistics display"""
        for stat_name, value in stats.items():
            if stat_name in self.stats_labels:
                self.stats_labels[stat_name].config(text=f"{stat_name}: {value}")
    
    def update_quest_progress(self, quests):
        """Update quest progress display"""
        # Clear existing items
        for item in self.quest_tree.get_children():
            self.quest_tree.delete(item)
        
        # Add quest data
        for quest_id, quest_data in quests.items():
            self.quest_tree.insert('', 'end', values=(
                quest_data.get('npc', 'Unknown'),
                quest_data.get('name', 'Unknown Quest'),
                f"{quest_data.get('progress', 0)}%",
                quest_data.get('status', 'Active')
            ))
    
    def update_mob_stats(self, mob_stats):
        """Update mob statistics display"""
        # Clear existing items
        for item in self.mob_stats_tree.get_children():
            self.mob_stats_tree.delete(item)
        
        # Add mob stats
        for mob_type, stats in mob_stats.items():
            self.mob_stats_tree.insert('', 'end', values=(
                mob_type.replace('_', ' ').title(),
                stats.get('kills', 0),
                stats.get('loot_collected', 0),
                f"{stats.get('avg_fight_time', 0):.1f}s"
            ))
    
    def run(self):
        """Start the GUI main loop"""
        self.root.mainloop()
    
    def close(self):
        """Close the GUI"""
        if self.running:
            self.stop_macro()
        self.root.destroy()