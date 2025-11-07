from flask import Blueprint, render_template, request, jsonify, session
import random
from .minimax import MinimaxAI
from .engine import TicTacToeEngine
from . import tic_tac_toe_bp

# Note: The original file did not include the check_winner, is_board_full, 
# and get_smart_fallback_move utility functions, but they were implicitly 
# used in the original routes.py snippet. For a complete, working file, 
# I will include them here based on the functions provided in your prompt.

# --- UTILITY FUNCTIONS FROM YOUR PROMPT ---

def check_winner(board):
    """Check if there's a winner - works with None values"""
    # Check rows
    for row in board:
        if row[0] and row[0] == row[1] == row[2]:
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]
    
    # Check diagonals
    if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    
    if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    
    return None

def check_winner_internal(board):
    """Internal winner checker for string-based board."""
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != '':
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    
    return None

def is_board_full(board):
    """Check if board is full"""
    for row in board:
        for cell in row:
            if cell is None:
                return False
    return True

def get_smart_fallback_move(board):
    """Smart fallback AI that checks for wins and blocks."""
    # Convert None to empty string for easier processing
    b = []
    for row in board:
        b_row = []
        for cell in row:
            b_row.append(cell if cell is not None else '')
        b.append(b_row)
    
    # First, try to win
    for row in range(3):
        for col in range(3):
            if b[row][col] == '':
                b[row][col] = 'O'
                if check_winner_internal(b) == 'O':
                    return (row, col)
                b[row][col] = ''
    
    # Then, try to block opponent
    for row in range(3):
        for col in range(3):
            if b[row][col] == '':
                b[row][col] = 'X'
                if check_winner_internal(b) == 'X':
                    b[row][col] = ''
                    return (row, col)
                b[row][col] = ''
    
    # Take center if available
    if b[1][1] == '':
        return (1, 1)
    
    # Take corners
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for row, col in corners:
        if b[row][col] == '':
            return (row, col)
    
    # Take any remaining spot
    for row in range(3):
        for col in range(3):
            if b[row][col] == '':
                return (row, col)
    
    return None

# --- END UTILITY FUNCTIONS ---


@tic_tac_toe_bp.route('/play')
def play():
    return render_template('tic_tac_toe/play.html')

@tic_tac_toe_bp.route('/api/state')
def get_state():
    """Get current game state"""
    state = session.get('tic_tac_toe_state')
    
    if not state:
        # Return empty state if no game exists
        return jsonify({
            'success': True,
            'state': {
                'board': [[None, None, None], [None, None, None], [None, None, None]],
                'current_player': 'X',
                'game_over': False,
                'winner': None
            },
            'difficulty': 'medium',
            'game_mode': 'pve' # New: Default game mode
        })
    
    difficulty = session.get('tic_tac_toe_difficulty', 'medium')
    game_mode = session.get('tic_tac_toe_game_mode', 'pve') # New: Get game mode
    
    return jsonify({
        'success': True,
        'state': state,
        'difficulty': difficulty,
        'game_mode': game_mode # New: Return game mode
    })

@tic_tac_toe_bp.route('/api/new', methods=['POST'])
def new_game():
    """Start a new game"""
    data = request.get_json()
    difficulty = data.get('difficulty', 'medium')
    first_player = data.get('first_player', 'human')
    game_mode = data.get('game_mode', 'pve') # New: Get game mode
    
    # Determine the starting player
    # X is always the first player to start the board. 
    # In PVE, if 'ai' is first, current_player becomes 'O'.
    # In PVP, 'X' always starts.
    start_player = 'X'
    if game_mode == 'pve' and first_player == 'ai':
        start_player = 'O'
    
    # Initialize new game state
    state = {
        'board': [[None, None, None], [None, None, None], [None, None, None]],
        'current_player': start_player,
        'game_over': False,
        'winner': None
    }
    
    session['tic_tac_toe_state'] = state
    session['tic_tac_toe_difficulty'] = difficulty
    session['first_player'] = first_player
    session['tic_tac_toe_game_mode'] = game_mode # New: Store game mode
    
    return jsonify({
        'success': True,
        'state': state,
        # AI should only move if it's PVE mode AND the AI is the first player
        'ai_should_move': (game_mode == 'pve' and first_player == 'ai')
    })

@tic_tac_toe_bp.route('/api/move', methods=['POST'])
def make_move():
    """Handle player move"""
    data = request.get_json()
    row = data.get('row')
    col = data.get('col')
    
    state = session.get('tic_tac_toe_state')
    game_mode = session.get('tic_tac_toe_game_mode', 'pve') # New: Get game mode
    
    if not state:
        return jsonify({'success': False, 'error': 'No active game'})
    
    # Validate move
    if state['game_over']:
        return jsonify({'success': False, 'error': 'Game is over'})
    
    if state['board'][row][col] is not None:
        return jsonify({'success': False, 'error': 'Cell already occupied'})
    
    # Make move
    state['board'][row][col] = state['current_player']
    
    # Check for win/draw
    winner = check_winner(state['board'])
    if winner:
        state['winner'] = winner
        state['game_over'] = True
    elif is_board_full(state['board']):
        state['game_over'] = True
        state['winner'] = None
    else:
        # Switch players
        state['current_player'] = 'O' if state['current_player'] == 'X' else 'X'
        
        # New: If in PvP mode, we are done. Skip AI move.
        if game_mode == 'pvp':
            session['tic_tac_toe_state'] = state
            return jsonify({
                'success': True,
                'state': state,
                'ai_should_move': False
            })
            
    session['tic_tac_toe_state'] = state
    
    return jsonify({
        'success': True,
        'state': state
    })

@tic_tac_toe_bp.route('/api/ai-move', methods=['POST'])
def ai_move():
    """Handle AI move using minimax algorithm"""
    state = session.get('tic_tac_toe_state')
    difficulty = session.get('tic_tac_toe_difficulty', 'medium')
    game_mode = session.get('tic_tac_toe_game_mode', 'pve')
    
    print(f"\n=== AI MOVE DEBUG ===")
    print(f"Game Mode: {game_mode}, Difficulty: {difficulty}")
    print(f"Current state: {state}")
    
    if not state:
        return jsonify({'success': False, 'error': 'No active game'})
    
    if state['game_over'] or state['current_player'] != 'O' or game_mode == 'pvp': # Added pvp check as a safety
        return jsonify({'success': False, 'error': 'Not AI turn or incorrect mode'})
    
    try:
        # Create engine from current state
        engine = TicTacToeEngine()
        
        # Convert None to empty string for engine compatibility
        engine.board = []
        for row in state['board']:
            engine_row = []
            for cell in row:
                engine_row.append(cell if cell is not None else '')
            engine.board.append(engine_row)
        
        print(f"Engine board: {engine.board}")
        
        engine.current_player = 'O'
        engine.game_over = state['game_over']
        engine.winner = state['winner']
        
        # Get available moves
        available_moves = engine.get_available_moves()
        print(f"Available moves: {available_moves}")
        
        # Initialize AI with difficulty
        ai = MinimaxAI(difficulty)
        print(f"AI initialized with difficulty: {ai.difficulty}")
        print(f"AI max_depth: {ai.max_depth}")
        print(f"AI randomness: {ai.randomness}")
        
        # Get AI move
        ai_move = ai.get_best_move(engine, 'O')
        print(f"AI chose move: {ai_move}")
        
        if ai_move is None:
            print("AI returned None - no moves available")
            return jsonify({'success': False, 'error': 'No available moves'})
        
        ai_row, ai_col = ai_move
        
        # Make AI move
        state['board'][ai_row][ai_col] = 'O'
        
        # Check for win/draw
        winner = check_winner(state['board'])
        if winner:
            state['winner'] = winner
            state['game_over'] = True
        elif is_board_full(state['board']):
            state['game_over'] = True
            state['winner'] = None
        else:
            state['current_player'] = 'X'
        
        session['tic_tac_toe_state'] = state
        
        print(f"Final state after AI move: {state}")
        print("=== END AI MOVE DEBUG ===\n")
        
        return jsonify({
            'success': True,
            'state': state
        })
        
    except Exception as e:
        print(f"MINIMAX ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        # Fallback to simple smart AI
        print("Falling back to simple AI")
        ai_move = get_smart_fallback_move(state['board'])
        
        if ai_move is None:
            return jsonify({'success': False, 'error': 'No available moves'})
        
        ai_row, ai_col = ai_move
        state['board'][ai_row][ai_col] = 'O'
        
        # Check for win/draw
        winner = check_winner(state['board'])
        if winner:
            state['winner'] = winner
            state['game_over'] = True
        elif is_board_full(state['board']):
            state['game_over'] = True
            state['winner'] = None
        else:
            state['current_player'] = 'X'
        
        session['tic_tac_toe_state'] = state
        
        return jsonify({
            'success': True,
            'state': state
        })