## app.py
"""
Flask Game Hub - Main Application
A modular game platform with pluggable game modules.
"""

from flask import Flask, render_template
from games.tic_tac_toe.blueprint import tic_tac_toe_bp

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Register game blueprints
    app.register_blueprint(tic_tac_toe_bp, url_prefix='/tic-tac-toe')
    
    @app.route('/')
    def dashboard():
        """Main dashboard showing available games."""
        games = [
            {
                'name': 'Tic-Tac-Toe',
                'description': 'Classic 3x3 grid game with AI opponent',
                'url': '/tic-tac-toe/play',
                'available': True,
                'image': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iIzMzNzNkYyIvPjx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjI0IiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+WCBPPC90ZXh0Pjwvc3ZnPg=='
            },
            {
                'name': 'Connect-4',
                'description': 'Drop pieces to connect four in a row',
                'url': '#',
                'available': False,
                'image': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iIzZiNzI4MCIvPjx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE2IiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+U29vbjwvdGV4dD48L3N2Zz4='
            }
        ]
        return render_template('dashboard.html', games=games)
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return render_template('dashboard.html', error="Page not found"), 404
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
