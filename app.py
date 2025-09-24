"""
Main Flask Application
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template

# Create Flask app
app = Flask(__name__)
app.secret_key = 'kzdnfsneksnoefsdnfsdnfsinfj'

# Import and register blueprints
try:
    from games.connect4 import connect4_bp
    app.register_blueprint(connect4_bp)
    print("Connect-4 blueprint registered successfully!")
except ImportError as e:
    print(f"Error importing connect4 blueprint: {e}")

try:
    from games.tic_tac_toe import tic_tac_toe_bp
    app.register_blueprint(tic_tac_toe_bp)
    print("TicTacToe blueprint registered successfully!")
except ImportError as e:
    print(f"Error importing TicTacToe blueprint: {e}")

@app.route('/')
def dashboard():
    """Main dashboard showing available games."""
    games = [
        {
            'name': 'Tic-Tac-Toe',
            'description': 'Classic 3x3 grid game with AI opponent',
            'url': '/tic-tac-toe/play',
            'available': True
        },
        {
            'name': 'Connect-4',
            'description': 'Drop pieces to connect four in a row',
            'url': '/connect4/play',
            'available': True
        }
    ]
    return render_template('dashboard.html', games=games)

if __name__ == '__main__':
    print("Starting Flask application...")
    print(f"Python path: {sys.path[0]}")
    print(f"Current directory: {os.getcwd()}")
    app.run(debug=True, host='0.0.0.0', port=5000)
