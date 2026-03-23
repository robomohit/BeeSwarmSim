# BSS Pro Macro v1.0.0

**Advanced Bee Swarm Simulator Automation Tool**

A comprehensive, feature-rich automation macro for Bee Swarm Simulator with advanced safety features, intelligent automation, and a modern GUI interface.

## 🚀 Features

### Core Automation
- **Advanced Field Navigation**: Precise hive-to-field navigation using BSS mechanics (E key hive tool + character reset)
- **Smart Field Farming**: Intelligent field rotation with optimized pollen collection patterns
- **Quest System**: Automated quest completion for all NPCs (Black Bear, Brown Bear, Polar Bear, etc.)
- **Mob Hunting**: Smart mob detection and elimination with loot collection
- **Planter Management**: Automated planter planting, harvesting, and optimization
- **Boost Management**: Intelligent boost usage based on context and efficiency
- **Hive Management**: Auto bee feeding, egg hatching, and honey conversion
- **Dispenser Collection**: Automated collection from all game dispensers

### Safety & Anti-Detection
- **Advanced Randomization**: Movement, timing, and click position randomization
- **Pattern Breaking**: Intelligent pattern detection and breaking to avoid bot-like behavior
- **Break System**: Randomized break scheduling with configurable intervals
- **Emergency Stops**: Multiple failsafe mechanisms including mouse corner trigger
- **System Monitoring**: Real-time system resource and process monitoring
- **Activity Analysis**: Bot pattern detection and prevention

### User Interface
- **Modern GUI**: Intuitive tabbed interface with real-time statistics
- **Live Monitoring**: Real-time activity logs and performance metrics
- **Configuration Management**: Easy settings import/export with presets
- **Statistics Tracking**: Comprehensive session and historical statistics
- **Hotkey Support**: Global hotkeys for macro control

### Technical Features
- **Image Recognition**: Advanced OpenCV-based game state detection
- **Multi-threading**: Smooth operation with background monitoring
- **Error Handling**: Robust error recovery and logging system
- **Performance Optimization**: Efficient resource usage and minimal impact
- **Modular Design**: Extensible architecture for easy customization

## 📋 Requirements

### System Requirements
- **OS**: Windows 10/11 (64-bit recommended)
- **Python**: 3.7 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB free space
- **Display**: 1280x720 minimum resolution

### Software Requirements
- Roblox (latest version)
- Bee Swarm Simulator
- Python 3.7+
- All dependencies (auto-installed via requirements.txt)

## 🛠️ Installation

### Option 1: Automatic Installation
1. Download all files to a folder
2. Run `install.bat` (Windows) or `python install.py`
3. Follow the on-screen instructions

### Option 2: Manual Installation
1. Install Python 3.7+ from [python.org](https://python.org)
2. Download/clone this repository
3. Open command prompt in the macro folder
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Quick Start

### GUI Mode (Recommended)
1. Run `python bss_pro_macro.py`
2. Configure settings in the GUI tabs
3. Click "Start Macro" to begin automation
4. Monitor progress in real-time

### Console Mode
1. Run `python bss_pro_macro.py --console`
2. Macro will run with default settings
3. Press Ctrl+C to stop

### First Time Setup
1. **Configure Fields**: Select your preferred farming fields
2. **Set Quest NPCs**: Enable desired quest NPCs
3. **Adjust Safety**: Configure break intervals and randomization
4. **Test Run**: Start with a short test session

## 🗺️ Field Navigation System

### How Navigation Works
The macro uses BSS's built-in mechanics for efficient field navigation:

1. **Hive Return**: Uses E key (Hive Tool) to instantly return to hive
2. **Character Reset**: Falls back to Roblox character reset if E key fails
3. **Precise Paths**: Pre-calculated movement sequences for each field
4. **Smart Movement**: Automatic jumping on ramps and obstacles

### Supported Fields
All 17 BSS fields are supported with optimized paths:

**Starter Fields:** Sunflower, Dandelion, Mushroom, Blue Flower, Clover
**Intermediate:** Strawberry, Bamboo, Spider
**Advanced:** Rose, Pine Tree, Cactus, Pumpkin
**Expert:** Pineapple, Stump, Coconut, Pepper
**Master:** Mountain Top

### Navigation Features
- **E Key Integration**: Uses BSS's hive tool for instant return
- **Roblox Reset Backup**: Character reset as failsafe method
- **Timed Movement**: Precise movement durations for each field
- **Obstacle Handling**: Automatic jumping for ramps and barriers
- **Path Verification**: Confirms arrival at target field

## ⚙️ Configuration

### Main Settings
- **Farming**: Field selection, rotation, timing
- **Quests**: NPC selection, auto-accept settings
- **Mobs**: Mob types to hunt, detection timeout
- **Planters**: Auto-plant/harvest, field selection
- **Boosts**: Smart boost usage, thresholds
- **Safety**: Randomization, breaks, emergency stops

### Hotkeys (Default)
- `F1`: Start/Stop Macro
- `F2`: Pause/Resume
- `F3`: Emergency Stop
- `F4`: Show/Hide GUI

### Safety Settings
- **Break Intervals**: 30-60 minutes (randomized)
- **Break Duration**: 2-5 minutes (randomized)
- **Movement Randomization**: 30% variance
- **Click Randomization**: 20% variance
- **Emergency Stops**: Multiple failsafe triggers

## 📊 Statistics & Monitoring

### Real-time Monitoring
- Current activity and status
- Active boosts and timers
- Quest progress tracking
- System resource usage

### Session Statistics
- Runtime and efficiency metrics
- Pollen/honey collection rates
- Quest completion counts
- Mob kills and loot collected
- Planter management stats

### Performance Metrics
- Actions per minute
- Error rates and recovery
- System impact monitoring
- Safety trigger activations

## 🛡️ Safety & Legal

### Safety Features
- **Anti-Detection**: Advanced randomization and pattern breaking
- **System Monitoring**: Resource usage and anomaly detection
- **Emergency Stops**: Multiple failsafe mechanisms
- **Break System**: Human-like break patterns
- **Activity Analysis**: Bot behavior prevention

### Legal Notice
- Use at your own risk and discretion
- Follow Roblox Terms of Service
- This tool is for educational purposes
- No warranty or guarantee provided
- Users are responsible for their account safety

### Best Practices
- Start with short test sessions
- Monitor system resources
- Use reasonable break intervals
- Don't run 24/7 continuously
- Keep backup saves of progress

## 🔧 Troubleshooting

### Common Issues

**Macro won't start**
- Check Roblox is running
- Verify BSS is loaded
- Check Python dependencies
- Review error logs

**Image recognition issues**
- Ensure correct screen resolution
- Check game graphics settings
- Verify template images exist
- Adjust confidence thresholds

**Performance problems**
- Close unnecessary programs
- Check system resources
- Reduce randomization settings
- Lower image quality settings

**Safety triggers activating**
- Check mouse position
- Review system resources
- Verify no debugging tools
- Check break schedules

### Getting Help
1. Check the troubleshooting section
2. Review log files for errors
3. Verify configuration settings
4. Test with minimal settings

## 📁 File Structure

```
BSS_Pro_Macro/
├── bss_pro_macro.py          # Main application
├── main_controller.py        # Core macro controller
├── core_systems.py          # Core automation systems
├── field_system.py          # Field navigation & farming
├── quest_system.py          # Quest management
├── mob_system.py            # Mob hunting system
├── planter_system.py        # Planter management
├── boost_system.py          # Boost optimization
├── gui_interface.py         # GUI interface
├── advanced_safety.py       # Safety features
├── config.json              # Configuration file
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── templates/              # Image templates
├── logs/                   # Log files
└── screenshots/            # Debug screenshots
```

## 🔄 Updates & Maintenance

### Version History
- **v1.0.0**: Initial release with full feature set

### Future Updates
- Enhanced image recognition
- Additional quest NPCs
- Mobile device support
- Cloud configuration sync
- Advanced statistics

### Maintenance
- Regular dependency updates
- Template image updates
- Configuration optimizations
- Performance improvements

## 🤝 Contributing

This project is open for improvements and contributions:
- Bug reports and fixes
- Feature suggestions
- Code optimizations
- Documentation improvements

## 📞 Support

For support and questions:
- Check the troubleshooting section
- Review configuration guides
- Examine log files for errors
- Test with minimal settings

## ⚠️ Disclaimer

This macro is provided "as-is" without warranty. Users assume all risks associated with automation tools. Always follow game terms of service and use responsibly. The developers are not responsible for any account actions or consequences.

---

**BSS Pro Macro v1.0.0** - Advanced Bee Swarm Simulator Automation
*Created with advanced AI assistance for educational purposes*
