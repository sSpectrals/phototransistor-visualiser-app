# phototransistor-visualiser-app

_A real-time sensor monitoring tool for phototransistors_

<div style="display: flex; gap: 10px;">
  <img src="images/app_screenshot.jpg" alt="App Screenshot" width="300" style="height: auto;">
  <img src="images/robot_on_line.jpg" alt="Robot on Line"  width="300" style="height: 300px; object-fit: cover; transform: rotate(-90deg);">
</div>

## 📖 Table of Contents

- [Abstract](#Abstract)
- [Features](#Features)
- [Open-Source](#open-source)
- [How to Use](#How-to-use)
- [Customization](#Customization)
- [Installation](#installation)
- [Credits](#Credits)

## Abstract

For my robotics team Roboticus, we needed a better way to monitor **32 phototransistor sensors** while detecting a white line. Simply reading raw serial values was inefficient so we built this real-time visualizer to:  
✔ Clearly display which sensors are triggered  
✔ Optimize debugging with instant visual feedback

## Open-Source

The original project was designed specifically for the sensors and components used in the football robot for Roboticus. The goal now is to make the application universally usable for a wider audience and allowing wider customization.

Would you like to help with this project? Feel free to make a pull request!

## Features

- Live 2D representation of sensor positions
- Color-coded coordinates representing activation
  - <strong style="color:#FF0000">Red</strong>: sensor triggered
  - <strong style="color:#3950FF">Blue</strong>: sensor not triggered
  - <strong style="color:#FFFF00">Yellow</strong>: sensor deactivated
- COM port selection when reading data

## How to use

1. Adjust the arduino code to your liking. Take a look at [customization](#Customization)
1. Upload the arduino code to your microprocessor
1. Calibrate the coordinates.json for the visual in case of any specific shape of a pcb
1. Run the python code while the microprocessor is powered
1. Select the correct COM port
1. Enjoy the visual feedback

## Customization

- main.py
  - Give coordinates for each sensor to match a specific shape if necessary (i.e. of a PCB)
  - Give each sensor a label on the graph (i.e an ID to do something very specific).
- visualisation.ino
  - Allow use of a multiplexer if required
  - Allow use of EEPROM to receive values if required

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/sSpectrals/phototransistor-visualizer.git
   ```

2. **Install dependencies:**:

   ```bash
   pip install -r docs/requirements.txt
   ```

## Credits

Developed by Edgar Mamikonian as part of Roboticus Robotics Team
