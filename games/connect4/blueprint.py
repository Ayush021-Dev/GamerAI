"""
Connect-4 Flask Blueprint
Handles HTTP routes and game session management.
"""

from flask import render_template, request, jsonify, session
from . import bp  # Import bp from current package
from .engine import *
from .minimax import get_best_move
import copy

@bp.route('/connect4')
def connect4_game():
    """Main Connect-4 game page."""
    # Initialize new game session
    session['connect4_board'] = create_board()
    session['connect4_game_over'] = False
    session['connect4_turn'] = PLAYER
    session['connect4_winner'] = None
    
    return render_template('connect4/play.html')

@bp.route('/connect4/make_move', methods=['POST'])
def make_move():
    """Handle player move and AI response."""
    try:
        data = request.get_json()
        col = int(data.get('column', -1))
        difficulty = data.get('difficulty', 'medium')
        
        # Get current game state
        board = session.get('connect4_board', create_board())
        game_over = session.get('connect4_game_over', False)
        
        if game_over or not is_valid_location(board, col):
            return jsonify({
                'success': False, 
                'message': 'Invalid move or game is over'
            })
        
        # Make player move
        row = get_next_open_row(board, col)
        if row == -1:
            return jsonify({
                'success': False,
                'message': 'Column is full'
            })
        
        drop_piece(board, row, col, PLAYER)
        
        # Check for player win
        if winning_move(board, PLAYER):
            session['connect4_board'] = board
            session['connect4_game_over'] = True
            session['connect4_winner'] = 'player'
            return jsonify({
                'success': True,
                'board': board,
                'winner': 'player',
                'game_over': True,
                'message': 'You win!'
            })
        
        # Check for draw
        if len(get_valid_locations(board)) == 0:
            session['connect4_board'] = board
            session['connect4_game_over'] = True
            session['connect4_winner'] = 'draw'
            return jsonify({
                'success': True,
                'board': board,
                'winner': 'draw',
                'game_over': True,
                'message': 'It\'s a draw!'
            })
        
        # Make AI move
        ai_col = get_best_move(board, difficulty)
        if ai_col is not None:
            ai_row = get_next_open_row(board, ai_col)
            if ai_row != -1:
                drop_piece(board, ai_row, ai_col, AI)
                
                # Check for AI win
                if winning_move(board, AI):
                    session['connect4_board'] = board
                    session['connect4_game_over'] = True
                    session['connect4_winner'] = 'ai'
                    return jsonify({
                        'success': True,
                        'board': board,
                        'winner': 'ai',
                        'game_over': True,
                        'ai_move': ai_col,
                        'message': 'AI wins!'
                    })
                
                # Check for draw after AI move
                if len(get_valid_locations(board)) == 0:
                    session['connect4_board'] = board
                    session['connect4_game_over'] = True
                    session['connect4_winner'] = 'draw'
                    return jsonify({
                        'success': True,
                        'board': board,
                        'winner': 'draw',
                        'game_over': True,
                        'ai_move': ai_col,
                        'message': 'It\'s a draw!'
                    })
        
        # Save game state and continue
        session['connect4_board'] = board
        return jsonify({
            'success': True,
            'board': board,
            'winner': None,
            'game_over': False,
            'ai_move': ai_col,
            'message': 'Your turn'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        })

@bp.route('/api/new_game', methods=['POST'])
def new_game():
    """Start a new Connect-4 game."""
    try:
        data = request.get_json()
        ai_first = data.get('ai_first', False)
        difficulty = data.get('difficulty', 'medium')
        
        # Initialize new game
        board = create_board()
        session['connect4_board'] = board
        session['connect4_game_over'] = False
        session['connect4_winner'] = None
        session['connect4_turn'] = AI if ai_first else PLAYER
        
        response_data = {
            'success': True,
            'board': board,
            'ai_first': ai_first,
            'message': 'AI\'s turn' if ai_first else 'Your turn'
        }
        
        # Make AI first move if needed
        if ai_first:
            ai_col = get_best_move(board, difficulty)
            if ai_col is not None:
                ai_row = get_next_open_row(board, ai_col)
                drop_piece(board, ai_row, ai_col, AI)
                session['connect4_board'] = board
                response_data['board'] = board
                response_data['ai_move'] = ai_col
                response_data['message'] = 'Your turn'
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        })

@bp.route('/connect4/get_board', methods=['GET'])
def get_board():
    """Get current board state."""
    board = session.get('connect4_board', create_board())
    game_over = session.get('connect4_game_over', False)
    winner = session.get('connect4_winner', None)
    
    return jsonify({
        'success': True,
        'board': board,
        'game_over': game_over,
        'winner': winner
    })

@bp.route('/connect4/hint', methods=['POST'])
def get_hint():
    """Get a hint for the best move."""
    try:
        data = request.get_json()
        difficulty = data.get('difficulty', 'medium')
        
        board = session.get('connect4_board', create_board())
        
        if session.get('connect4_game_over', False):
            return jsonify({
                'success': False,
                'message': 'Game is over'
            })
        
        hint_col = get_best_move(board, difficulty)
        
        return jsonify({
            'success': True,
            'hint_column': hint_col,
            'message': f'Try column {hint_col + 1}' if hint_col is not None else 'No valid moves'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        })
