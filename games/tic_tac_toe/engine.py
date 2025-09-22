"""
Tic-Tac-Toe Game Engine
Handles game state, rules validation, and win condition checking.
"""

from typing import List, Optional, Tuple, Dict
import copy

class TicTacToeEngine:
    """Main game engine for Tic-Tac-Toe logic."""
    
    def __init__(self):
        """Initialize a new game."""
        self.reset_game()
    
    def reset_game(self) -> None:
        """Reset the game to initial state."""
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # X always starts
        self.game_over = False
        self.winner = None
    
    def get_state(self) -> Dict:
        """Get current game state as dictionary."""
        return {
            'board': self.board,
            'current_player': self.current_player,
            'game_over': self.game_over,
            'winner': self.winner
        }
    
    def set_state(self, state: Dict) -> None:
        """Set game state from dictionary."""
        self.board = state['board']
        self.current_player = state['current_player']
        self.game_over = state['game_over']
        self.winner = state['winner']
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """Check if a move is valid."""
        if self.game_over:
            return False
        if row < 0 or row >= 3 or col < 0 or col >= 3:
            return False
        return self.board[row][col] == ''
    
    def make_move(self, row: int, col: int, player: str = None) -> bool:
        """
        Make a move on the board.
        Returns True if move was successful, False otherwise.
        """
        if player is None:
            player = self.current_player
            
        if not self.is_valid_move(row, col):
            return False
        
        self.board[row][col] = player
        
        # Check for win or draw
        self.winner = self._check_winner()
        if self.winner or self._is_board_full():
            self.game_over = True
        else:
            # Switch players
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        return True
    
    def get_available_moves(self) -> List[Tuple[int, int]]:
        """Get list of available moves as (row, col) tuples."""
        moves = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    moves.append((row, col))
        return moves
    
    def _check_winner(self) -> Optional[str]:
        """Check if there's a winner. Returns 'X', 'O', or None."""
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != '':
                return row[0]
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return self.board[0][col]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]
        
        return None
    
    def _is_board_full(self) -> bool:
        """Check if the board is full."""
        for row in self.board:
            for cell in row:
                if cell == '':
                    return False
        return True
    
    def is_terminal(self) -> bool:
        """Check if the game is in a terminal state."""
        return self.game_over
    
    def evaluate(self, player: str) -> int:
        """
        Evaluate the board position for the given player.
        Returns: +10 if player wins, -10 if opponent wins, 0 for draw/ongoing.
        """
        winner = self._check_winner()
        if winner == player:
            return 10
        elif winner is not None:  # Opponent wins
            return -10
        return 0  # Draw or ongoing game
    
    def copy(self):
        """Create a deep copy of the game engine."""
        new_engine = TicTacToeEngine()
        new_engine.board = copy.deepcopy(self.board)
        new_engine.current_player = self.current_player
        new_engine.game_over = self.game_over
        new_engine.winner = self.winner
        return new_engine