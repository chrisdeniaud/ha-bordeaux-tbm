# Bordeaux TBM for Home Assistant

Home Assistant integration for Bordeaux public transport (TBM) real-time information.

## Features
- Real-time arrival predictions for TBM trams and buses
- Configurable refresh interval
- Multiple predictions per stop

## Installation

### HACS Installation
1. Open HACS
2. Add custom repository: `chrisdeniaud/ha-bordeaux-tbm`
3. Install "Bordeaux TBM"
4. Restart Home Assistant

### Manual Installation
1. Download the latest release
2. Copy `custom_components/bordeaux_tbm` to your `config/custom_components` directory
3. Restart Home Assistant

## Configuration
Configuration is done via the UI:
1. Go to Configuration > Integrations
2. Click the + button
3. Search for "Bordeaux TBM"
4. Configure:
   - Line
   - Stop
   - Direction
   - Number of predictions
   - Update interval

## States and Attributes
- State: Next arrivals with delays
- Attributes: Detailed information for each predicted arrival
