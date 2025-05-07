# Combat Tracker

A GUI application for managing combat encounters in tabletop role-playing games.

## Features

- Character management with customizable fields
- Initiative tracking and round counting
- Character templates for quick creation
- Health tracking and quick edit functionality
- Session management for saving and loading combat states
- Character copying functionality
- Modern and intuitive user interface

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)
- Pillow >= 10.0.0

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/combat_tracker.git
   cd combat_tracker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python combat_tracker.py
```

## Project Structure

- `combat_tracker.py`: Main application entry point
- `GUI/`: Contains all GUI-related components
  - `components/`: Modular GUI components
    - `character_list.py`: Character list view and management
    - `character_details.py`: Character details panel
    - `templates_screen.py`: Template management interface
    - And more specialized components
- `character/`: Character-related logic
- `saves/`: Directory for saved combat states
