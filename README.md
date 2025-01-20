# Memory Games Arcade

A Django-based web application featuring three engaging memory games to test and improve your cognitive skills.

## Games Available

### 1. Number Sequence Memory
- **Description**: Test your memory by remembering and clicking numbers in the correct sequence.
- **Gameplay**: 
  - Numbers are displayed briefly and then hidden
  - Click the numbers in the same order they were shown
  - Start with 4 numbers and progress up to 10
  - Each level adds 2 more numbers to remember
  - Make a mistake, and you start over
- **Features**:
  - Progressive difficulty (5 levels)
  - Visual feedback for correct/incorrect sequences
  - Celebration animation on completion

### 2. Color Pairs Memory
- **Description**: Classic card-matching memory game with colorful pairs.
- **Gameplay**:
  - Find matching pairs of colored cards
  - Start with 4 cards (2 pairs) and progress up to 10 cards (5 pairs)
  - Cards flip back if no match is found
  - Complete the level to progress
- **Features**:
  - 4 levels of increasing difficulty
  - Smooth card flip animations
  - Color-coded feedback
  - Progress tracking
  - Winner celebration with fireworks

### 3. Directional Memory
- **Description**: Remember and replicate sequences of directional arrows.
- **Gameplay**:
  - Watch the sequence of arrows (↑, →, ↓, ←)
  - Replicate the sequence using the arrow buttons
  - Start with 3 arrows and progress up to 5
  - Wrong sequence requires starting over
- **Features**:
  - Real-time feedback with color-coded slots
  - Status messages for game state
  - Progressive difficulty (3 levels)
  - Visual feedback for correct/incorrect moves
  - Sequence replay on mistakes

## Technical Features
- Built with Django web framework
- Modern UI using Tailwind CSS
- Responsive design for all screen sizes
- HTMX for smooth interactions
- Session-based game state management
- Clean and modular code structure

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Visit `http://localhost:8000` in your browser

## Dependencies
- Django 5.1.5
- HTMX
- Tailwind CSS
- Font Awesome

## Contributing
Feel free to submit issues and enhancement requests!

## License
This project is licensed under the MIT License - see the LICENSE file for details. 
