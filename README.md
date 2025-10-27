# Ghana Robotics Competition 2025 — ORION V2

**MicroPython robot controller for the Ghana Robotics Competition (Engineers League, Smart City Builders Challenge).**
This repository contains the code, documentation, and build assets for **ORION V2**, a 4-wheel drive robot built with the Xplore Bot kit and a Raspberry Pi Pico brain. The robot supports a 30-second autonomous period (priority missions) and manual (Bluetooth) control for the remaining match time.

---

## Table of Contents

* [Project Overview](#project-overview)
* [Repository Structure](#repository-structure)
* [Quick Start (Flash & Run)](#quick-start--flash--run)
* [Hardware (Requirements & Pinout)](#hardware--requirements--pinout)
* [Software (Files & Usage)](#software--files--usage)
* [Autonomous and Manual Behaviors](#autonomous-and-manual-behaviors-high-level-overview)
* [Contributing](#contributing)
* [Troubleshooting](#troubleshooting)
* [License](#license)
* [Credits & Contact](#credits--contact)

---

## Project Overview

The **Smart City Builders Challenge** requires the robot to complete three core missions:

1. Fix a broken bridge (bridge pallets)
2. Build essential services (stack building blocks at specific sites)
3. Clean the city (collect rubbish balls into bins)

**Strategy Summary (Team Decision):**

* Prioritize **bridge repair** during autonomous mode (double points / avoid penalty)
* Use manual mode for building stacks (precision stacking)
* Use manual or autonomous rubbish collection as fallback / steady scoring

> For full design rationale, testing logs, and week-by-week notes, see [`docs/Engineering_Notebook.pdf`](docs/Engineering_Notebook.pdf).

---

## Repository Structure

```
├── README.md
├── LICENSE
├── docs/
│   ├── Engineering_Notebook.pdf
│   └── Game_Rules.pdf
├── src/
│   ├── main.py
│   ├── autonomous.py
│   └── utils.py
├── schemes/
│   └── wiring_diagram.png
├── models/
│   └── attachments/
├── photos/
│   ├── build/
│   └── final/
└── video/
    └── demo.mp4
```

---

## Quick Start — Flash & Run (Raspberry Pi Pico)

1. Install MicroPython firmware on your Pico (use Thonny or `esptool` for flashing).
2. Copy `src/main.py`, `src/utils.py`, and `src/autonomous.py` to the Pico root.
3. Power the robot — `main.py` will:

   * Wait for the **Start** button (`GPIO 2`)
   * Run the autonomous routine
   * Monitor UART for manual override (Bluetooth)
4. To test manual mode via Bluetooth:

   * Pair your phone or HC-05 module with the Pico.
   * Send one-character commands (`F`, `B`, `L`, `R`, `S`, `1`, `2`).

---

## Hardware — Requirements & Pinout

**Board:** Raspberry Pi Pico (MicroPython)

### Required Components

* **4x DC Motors** — Two front, two back (for drive control)
* **4x H-Bridge Motor Drivers (L298N or similar)** — One per motor pair, supports direction and PWM speed control
* **3x Servo Motors** —

  * Servo 1 (lifting mechanism): `GPIO 28`
  * Servo 2 (attachment): `GPIO 18`
  * Servo 3 (attachment): `GPIO 19`
* **Bluetooth Module (HC-05)** — Manual control via UART
* **Ultrasonic Sensor (HC-SR04)** — Optional; for distance measurement
* **Start Button** — `GPIO 2`, internal pull-up enabled
* **Battery Pack** — 7.4V (2S Li-ion or LiPo), powers Pico and drivers; ensure **common ground**

### Pin Mapping

#### Motor Control

* **Motor 1 (Left-Front)**

  * ENA (PWM): `GPIO 10`
  * IN1 (Forward): `GPIO 11`
  * IN2 (Backward): `GPIO 12`
* **Motor 2 (Right-Front)**

  * ENB (PWM): `GPIO 13`
  * IN1: `GPIO 14`
  * IN2: `GPIO 15`
* **Motor 3 (Left-Back)**

  * ENC (PWM): `GPIO 20`
  * IN1: `GPIO 17`
  * IN2: `GPIO 16`
* **Motor 4 (Right-Back)**

  * END (PWM): `GPIO 21`
  * IN1: `GPIO 19`
  * IN2: `GPIO 18`

#### Servo Control

* **Servo 1 (Lift Mechanism):** `GPIO 28`
* **Servo 2 (Attachment A):** `GPIO 18` *(shared with Motor 4 Backward pin)*
* **Servo 3 (Attachment B):** `GPIO 19` *(shared with Motor 4 Forward pin)*

> ⚠️ **Pin Conflict:** Motor 4 shares control pins with Servos 2 and 3. The firmware disables motor PWM during servo operation, then reinitializes motor pins afterward. See `disable_servos()`, `enable_servos()`, and `reinitialize_motor4()` in `utils.py`.

#### Other Peripherals

* **Start Button:** `GPIO 2` (internal pull-up)
* **UART / Bluetooth (HC-05):** UART0, `9600` baud

  * TX (Pico) → RX (HC-05)
  * RX (Pico) ← TX (HC-05)

---

## Software — Files & Usage

* **`src/utils.py`** — Hardware setup, motor & servo helpers, PWM control, and safety functions.
* **`src/autonomous.py`** — Autonomous mission logic (bridge repair, fallback routines).
* **`src/main.py`** — Main control loop: initialization, autonomous execution, UART override handling.

---

## Autonomous and Manual Behaviors (High-Level Overview)

### Autonomous Mode

* Runs for the first minute of the match.
* Executes pre-programmed actions with no manual input.
* **Primary:** Bridge repair for double points.
* **Fallback:** Rubbish collection if bridge repair fails.
* **Safety:** Conservative motor speeds; tune via `set_speed()` in `utils.py`.
* **Transition:** Switches to manual after completion or UART override.

### Manual Mode

* Controlled via Bluetooth UART commands for precision stacking and fine control.

#### Tasks

* **Building Assembly:** Stack blocks in order: foundation → middle → roof.
* **Rubbish Collection:** Manually pick and deposit rubbish.
* **Repositioning:** Minor movement adjustments.

#### Bluetooth Commands

| Command | Description         |
| ------- | ------------------- |
| `F`     | Move forward        |
| `B`     | Move backward       |
| `L`     | Turn left           |
| `R`     | Turn right          |
| `S`     | Stop motors         |
| `1`     | Servo down position |
| `2`     | Servo up position   |

### Manual Override

* Sending any UART command stops the autonomous routine and switches to manual control.
* Useful for real-time intervention if the robot misaligns or encounters obstacles.

> **Tip:** Pair Bluetooth before the match to ensure instant override availability.

---

## Contributing

1. Create a new branch: `git checkout -b feature/branch-name`
2. Keep commits atomic with clear messages.
3. Submit a PR to `main` with testing notes.

---

## Troubleshooting

* **Motors not responding:** Check PWM wiring and power supply.
* **Servos not moving:** Ensure motors are stopped and servos re-enabled.
* **Bluetooth not working:** Verify baud rate (9600) and TX/RX wiring.

---

## License

Licensed under the **MIT License**. See [`LICENSE`](LICENSE) for full text.

---

## Credits & Contact

Team **Orion** — University of Ghana, October 2025
**Contacts:**

* Ethan Nartey: Programmer — [ethan@example.com](mailto:ethan@example.com)
* Daniel K. D. Botchway: Designer — [daniel@example.com](mailto:daniel@example.com)
* Nelly Amewu: Builder — [neamewu@gmail.com](mailto:neamewu@gmail.com)
