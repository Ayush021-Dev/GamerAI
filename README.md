```markdown
# Flask Game Hub

A modular web-based gaming platform built with Flask (Python) and vanilla JavaScript. The hub allows easy addition of new games through a pluggable module system.

## Features

- 🎮 **Modular Architecture**: Easy to add new games
- 🧠 **Smart AI**: Minimax algorithm with alpha-beta pruning
- 📱 **Responsive Design**: Works on desktop and mobile
- ⚡ **Fast & Lightweight**: Vanilla JavaScript, no frameworks
- 🎯 **Multiple Difficulties**: Easy, Medium, and Hard AI levels
- 📊 **Score Tracking**: Persistent score tracking
- 🎨 **Modern UI**: Clean, professional interface with animations

## Currently Available Games

### Tic-Tac-Toe ✓
- Complete implementation with AI opponent
- Three difficulty levels:
  - **Easy**: Random moves mixed with basic strategy
  - **Medium**: Moderate lookahead with some randomness
  - **Hard**: Perfect play using full minimax depth
- Score tracking and game statistics
- Smooth animations and responsive design

### Connect-4 (Coming Soon)
- Framework ready for implementation
- Placeholder card visible in dashboard

## Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Clone or download the project**
```bash
# Create project directory
mkdir game_hub && cd game_hub
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Open your browser**
Navigate to `http://localhost:5000`

## Project Structure

```
game_hub/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings  
├── requirements.txt            # Python dependencies
├── games/                      # Game modules
│   └── tic_tac_toe/           # Tic-Tac-Toe module
│       ├── engine.py          # Game logic & rules
│       ├── minimax.py         # AI algorithm
│       └── blueprint.py       # Flask routes
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── dashboard.html         # Main dashboard
│   └── tic_tac_toe/
│       └── play.html          # Game interface
└── static/                    # CSS/JS assets
    ├── css/
    └── js/
```

## API Endpoints

### Tic-Tac-Toe API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/tic-tac-toe/api/new` | POST | Start new game |
| `/tic-tac-toe/api/move` | POST | Make human move |
| `/tic-tac-toe/api/ai-move` | POST | Get AI move |
| `/tic-tac-toe/api/state` | GET | Get current state |

### API Response Format

```javascript
// New game response
{
  "success": true,
  "state": {
    "board": [["", "", ""], ["", "", ""], ["", "", ""]],
    "current_player": "X",
    "game_over": false,
    "winner": null
  },
  "difficulty": "medium"
}

// Move response  
{
  "success": true,
  "state": { /* updated game state */ }
}

// AI move response
{
  "success": true,
  "move": {"row": 1, "col": 1},
  "state": { /* updated game state */ }
}
```
