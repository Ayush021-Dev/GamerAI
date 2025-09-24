"""
Connect-4 Minimax Algorithm with Alpha-Beta Pruning
"""
import math
import random
from .engine import *

def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI))
    
    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations) if valid_locations else 0
        
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = [row[:] for row in board]
            drop_piece(b_copy, row, col, AI)
            
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            
            if new_score > value:
                value = new_score
                column = col
            
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        
        return column, value
    
    else:
        value = math.inf
        column = random.choice(valid_locations) if valid_locations else 0
        
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = [row[:] for row in board]
            drop_piece(b_copy, row, col, PLAYER)
            
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            
            if new_score < value:
                value = new_score
                column = col
            
            beta = min(beta, value)
            if alpha >= beta:
                break
        
        return column, value

def get_best_move(board, difficulty='medium'):
    depth_map = {
        'easy': 2,
        'medium': 4,
        'hard': 6
    }
    
    depth = depth_map.get(difficulty, 4)
    valid_locations = get_valid_locations(board)
    
    if not valid_locations:
        return None
    
    if difficulty == 'easy' and random.random() < 0.3:
        return random.choice(valid_locations)
    
    col, _ = minimax(board, depth, -math.inf, math.inf, True)
    return col if col is not None else random.choice(valid_locations)
