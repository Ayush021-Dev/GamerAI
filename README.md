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

## Adding New Games

### 1. Create Game Module Structure

```bash
mkdir games/your_game_name
touch games/your_game_name/__init__.py
touch games/your_game_name/engine.py
touch games/your_game_name/minimax.py  # if AI needed
touch games/your_game_name/blueprint.py
```

### 2. Implement Game Engine

```python
# games/your_game_name/engine.py
class YourGameEngine:
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
        # Initialize game state
        pass
    
    def get_state(self):
        # Return current state as dict
        return {}
    
    def is_valid_move(self, move):
        # Validate move
        return True
    
    def make_move(self, move):
        # Apply move and update state
        return True
    
    def is_terminal(self):
        # Check if game is over
        return False
    
    def evaluate(self, player):
        # Evaluate position for AI
        return 0
```

### 3. Create Flask Blueprint

```python
# games/your_game_name/blueprint.py
from flask import Blueprint, render_template, request, jsonify

your_game_bp = Blueprint('your_game', __name__)

@your_game_bp.route('/play')
def play():
    return render_template('your_game/play.html')

@your_game_bp.route('/api/new', methods=['POST'])
def new_game():
    # Implement new game logic
    pass

# Add other API endpoints...
```

### 4. Register Blueprint

```python
# app.py
from games.your_game_name.blueprint import your_game_bp

app.register_blueprint(your_game_bp, url_prefix='/your-game-name')
```

### 5. Create Templates and Assets

- Add HTML template in `templates/your_game_name/`
- Add CSS in `static/css/`  
- Add JavaScript in `static/js/`

### 6. Update Dashboard

Add your game to the games list in `app.py`:

```python
games = [
    {
        'name': 'Your Game',
        'description': 'Game description',
        'url': '/your-game-name/play',
        'available': True,
        'image': 'data:image/svg+xml;base64,...'
    }
    # ... other games
]
```

## Development Tips

### Code Style
- Follow PEP8 for Python code
- Use meaningful variable names
- Add docstrings to functions and classes
- Comment complex logic

### Testing
- Test API endpoints with tools like Postman
- Test responsive design on different screen sizes
- Verify game logic with edge cases

### Performance
- Minimize API calls in frontend
- Use efficient algorithms for game logic
- Optimize AI search depth based on game complexity

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure all `__init__.py` files exist
2. **Template not found**: Check template paths in render_template()
3. **API errors**: Verify JSON request format and error handling
4. **Session issues**: Make sure Flask secret key is set

### Debug Mode
Set `FLASK_DEBUG=True` environment variable for detailed error messages.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

---

## Changelog

### v1.0.0
- Initial release with Tic-Tac-Toe
- Modular architecture implemented
- AI with multiple difficulty levels
- Responsive web interface
- Score tracking system