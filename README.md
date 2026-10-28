# Converto

![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

A desktop unit and currency converter built with Python and CustomTkinter. Unit conversions work offline, while currency conversion requires an internet connection.

![Converto Default](Screenshot_default.png)
![Converto Currency](Screenshot_Currency.png)
![Converto Input Validation](Screenshot_invalid.png)

## Features

- **11 conversion categories:** Currency, length, mass, volume, temperature, energy, power, pressure, speed, digital storage, and data transfer speed.
- **Live exchange rates:** Fetches current currency rates online.
- **Dark UI:** CustomTkinter interface with the Anthropic Sans Display font.
- **Windows DPI support:** Scales the interface for different display settings.

## Installation

### Run the executable

Download `Converto.exe` from the [Releases](https://github.com/toluoguntayo/Converto/releases) page and run it.

### Run from source

1. Install Python and clone this repository.
2. Install the dependencies:

   ```bash
   pip install customtkinter requests
   ```

3. Run the application:

   ```bash
   python main.py
   ```

## Usage

1. Select a conversion category.
2. Choose the source and target units.
3. Enter a value.
4. Click **Convert** to see the result.

## Technologies

- Python
- CustomTkinter
- Requests

## License

This project is licensed under the [MIT License](LICENSE).
