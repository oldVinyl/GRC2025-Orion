# GHANA ROBOTICS COMPETITION 2025 ROBOT CONTROLLER

A MicroPython-based robot controller for a 4-wheel drive robot with servo attachments for the 2025 edition of the Ghana Robotics Competition. The robot supports both autonomous navigation and Bluetooth-controlled manual operation.

## Features

- **Dual Operation Modes**
  - Autonomous mode with pre-programmed navigation routines
  - Manual control via UART/Bluetooth communication
  
- **4-Motor Drive System**
  - Independent control of 4 DC motors with PWM speed control
  - Directional movement: forward, backward, left, right, and stop
  
- **Servo Control**
  - Dual servo motors for additional mechanical functions
  - Up/down positioning and alternating movement patterns
  
- **Manual Override**
  - Seamlessly switch from autonomous to manual mode during operation
  - Real-time command processing via UART

## Hardware Requirements

- Raspberry Pi Pico (or compatible MicroPython board)
- 4x DC motors with H-bridge motor drivers
- 4x PWM motor controllers
- 2x Servo motors
- Bluetooth/UART module
- Start button (connected to GPIO 2)
- Appropriate power supply

## Pin Configuration

### Motors
- **Motor 1:** ENA (GPIO 10), Forward (GPIO 11), Backward (GPIO 12)
- **Motor 2:** ENB (GPIO 13), Forward (GPIO 14), Backward (GPIO 15)
- **Motor 3:** ENC (GPIO 20), Forward (GPIO 17), Backward (GPIO 16)
- **Motor 4:** END (GPIO 21), Forward (GPIO 19), Backward (GPIO 18)

### Servos
- **Servo 1:** GPIO 28 (lifting mechanism)
- **Servo 2:** GPIO 18 (shared with Motor 4 backward pin)
- **Servo 3:** GPIO 19 (shared with Motor 4 forward pin)

**Note:** Servos 2 and 3 share pins with Motor 4. The `utils.py` module automatically manages these conflicts by disabling servo PWM when motors are in use and reinitializing motor pins after servo operations.

### Other
- **Start Button:** GPIO 2 (with pull-up)
- **UART:** UART0, 9600 baud

## Core Functions (from utils.py)

### Motor Control
- `set_speed(speed)` - Set PWM duty cycle for all motors (0-65535)
- `forward()` - Move robot forward
- `backward()` - Move robot backward
- `left()` - Turn robot left
- `right()` - Turn robot right
- `stop()` - Stop all motors

### Servo Control
- `servo_up()` - Raise servos 2 & 3 to up position
- `servo_down()` - Lower servos 2 & 3 to down position
- `servo_open()` - Open servo 1 (lifting mechanism)
- `servo_close()` - Close servo 1 (lifting mechanism)
- `enable_servos()` - Initialize servo PWM on shared pins
- `disable_servos()` - Disable servo PWM to allow motor operation

### Autonomous Functions
- `red_autonomous_behavior()` - Execute pre-programmed autonomous routine
- `check_manual_override()` - Check for incoming UART commands
- `timed_sleep_with_override(duration)` - Sleep with ability to detect manual override

## Project Structure

```
GRC_25/
├── main.py       - Main robot controller and operation loop
├── utils.py      - Hardware utilities and motor/servo control functions
├── README.md     - This file
└── requirements.txt
```

### File Descriptions

- **main.py**: Main program that handles the operation loop, mode switching between autonomous and manual control, and processes Bluetooth commands
- **utils.py**: Contains all hardware initialization, motor control functions, servo operations, and autonomous behavior routines

## Installation

1. Install MicroPython firmware on your Raspberry Pi Pico
2. Upload **all project files** to your Pico's root directory:
   - `main.py` - Main robot controller
   - `utils.py` - Hardware utilities and control functions
   
   **Important:** Both files must be uploaded to the Pico for the robot to function properly. The `main.py` file imports functions from `utils.py`.

3. Connect your hardware according to the pin configuration below
4. The robot will automatically run `main.py` on power-up (if configured as boot.py or main.py)

## Usage

### Autonomous Mode

The robot starts in autonomous mode by default. Press the start button to begin:

1. Press the physical start button (GPIO 2)
2. Wait 3 seconds for initialization
3. Robot executes pre-programmed autonomous behavior

The autonomous routine includes:
- Forward navigation
- Right turns
- Speed adjustments for precision
- Automatic stop upon completion

### Manual Control

Send commands via Bluetooth/UART connection:

| Command | Action |
|---------|--------|
| `F` | Move forward |
| `B` | Move backward |
| `L` | Turn left |
| `R` | Turn right |
| `S` | Stop |
| `1` | Servo down position |
| `2` | Servo up position |

### Manual Override

During autonomous mode, send any command via UART to immediately switch to manual control mode.

## Troubleshooting

- **Motors not responding:** Check PWM connections and power supply
- **Servos not moving:** Ensure motors are stopped and servos are enabled
- **Bluetooth commands not working:** Verify UART baud rate (9600) and connection

## License

This project is provided as-is for educational and competition purposes.

## Contributing

Feel free to modify and adapt this code for your specific robot configuration and requirements.
