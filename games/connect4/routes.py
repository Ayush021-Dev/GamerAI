"""
Connect-4 Flask Routes with Human vs Human Support
"""
from flask import render_template, request, jsonify, session
from . import connect4_bp
from .engine import *
from .minimax import get_best_move

@connect4_bp.route('/play')
def play():
    return render_template('connect4/play.html')

@connect4_bp.route('/connect4')
def connect4_game():
    session['connect4_board'] = create_board()
    session['connect4_game_over'] = False
    session['connect4_turn'] = PLAYER
    session['connect4_winner'] = None
    session['connect4_game_mode'] = 'ai'  # 'ai' or 'human'
    return render_template('connect4/play.html')

@connect4_bp.route('/api/make_move', methods=['POST'])
def make_move():
    try:
        data = request.get_json()
        col = int(data.get('column', -1))
        difficulty = data.get('difficulty', 'medium')
        game_mode = session.get('connect4_game_mode', 'ai')
        
        board = session.get('connect4_board', create_board())
        game_over = session.get('connect4_game_over', False)
        current_turn = session.get('connect4_turn', PLAYER)
        
        if game_over or not is_valid_location(board, col):
            return jsonify({
                'success': False, 
                'message': 'Invalid move or game is over'
            })
        
        # Current player move
        row = get_next_open_row(board, col)
        if row == -1:
            return jsonify({
                'success': False,
                'message': 'Column is full'
            })
        
        drop_piece(board, row, col, current_turn)
        
        # Check for win
        if winning_move(board, current_turn):
            session['connect4_board'] = board
            session['connect4_game_over'] = True
            winner = 'player' if current_turn == PLAYER else ('player2' if game_mode == 'human' else 'ai')
            session['connect4_winner'] = winner
            return jsonify({
                'success': True,
                'board': board,
                'winner': winner,
                'game_over': True,
                'message': f'{"Player 1" if current_turn == PLAYER else "Player 2"} wins!' if game_mode == 'human' else ('You win!' if winner == 'player' else 'AI wins!')
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
        
        # Human vs Human mode - just switch turns
        if game_mode == 'human':
            session['connect4_turn'] = AI if current_turn == PLAYER else PLAYER
            session['connect4_board'] = board
            next_player = 'Player 2' if current_turn == PLAYER else 'Player 1'
            return jsonify({
                'success': True,
                'board': board,
                'winner': None,
                'game_over': False,
                'message': f'{next_player}\'s turn',
                'current_turn': AI if current_turn == PLAYER else PLAYER
            })
        
        # AI mode - make AI move
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

@connect4_bp.route('/api/new_game', methods=['POST'])
def new_game():
    try:
        data = request.get_json()
        ai_first = data.get('ai_first', False)
        difficulty = data.get('difficulty', 'medium')
        game_mode = data.get('game_mode', 'ai')  # 'ai' or 'human'
        
        board = create_board()
        session['connect4_board'] = board
        session['connect4_game_over'] = False
        session['connect4_winner'] = None
        session['connect4_game_mode'] = game_mode
        session['connect4_turn'] = AI if ai_first else PLAYER
        
        response_data = {
            'success': True,
            'board': board,
            'ai_first': ai_first,
            'game_mode': game_mode,
            'current_turn': AI if ai_first else PLAYER,
            'message': 'Player 2\'s turn' if (game_mode == 'human' and ai_first) else ('Player 1\'s turn' if game_mode == 'human' else ('AI\'s turn' if ai_first else 'Your turn'))
        }
        
        # Only make AI move if in AI mode and AI goes first
        if game_mode == 'ai' and ai_first:
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