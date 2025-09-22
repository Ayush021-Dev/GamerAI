"""
Minimax Algorithm with Alpha-Beta Pruning for Tic-Tac-Toe
Implements AI decision making with configurable difficulty levels.
"""

import random
from typing import Tuple, Optional
from .engine import TicTacToeEngine

class MinimaxAI:
    """AI player using minimax algorithm with alpha-beta pruning."""
    
    def __init__(self, difficulty: str = 'hard'):
        """
        Initialize AI with difficulty level.
        
        Args:
            difficulty: 'easy', 'medium', or 'hard'
        """
        self.difficulty = difficulty.lower()
        self.max_depth = self._get_max_depth()
        self.randomness = self._get_randomness()
    
    def _get_max_depth(self) -> int:
        """Get maximum search depth based on difficulty."""
        if self.difficulty == 'easy':
            return 1
        elif self.difficulty == 'medium':
            return 4
        else:  # hard
            return 9  # Full depth for 3x3 board
    
    def _get_randomness(self) -> float:
        """Get randomness factor for easy difficulty."""
        if self.difficulty == 'easy':
            return 0.3  # 30% chance of random move
        elif self.difficulty == 'medium':
            return 0.1  # 10% chance of random move
        else:  # hard
            return 0.0  # No randomness
    
    def get_best_move(self, engine: TicTacToeEngine, ai_player: str) -> Optional[Tuple[int, int]]:
        """Get the best move for the AI player."""
        available_moves = engine.get_available_moves()
        
        print(f"\n=== DIFFICULTY TEST DEBUG ===")
        print(f"🎯 Difficulty: {self.difficulty.upper()}")
        print(f"🔍 Max search depth: {self.max_depth}")
        print(f"🎲 Randomness factor: {self.randomness * 100}%")
        print(f"AI player: {ai_player}")
        print(f"Available moves: {available_moves}")
        print(f"Current board:")
        for i, row in enumerate(engine.board):
            print(f"  Row {i}: {row}")
        
        if not available_moves:
            print("No available moves!")
            return None
        
        # Check for randomness (Easy/Medium only)
        random_roll = random.random()
        print(f"🎲 Random roll: {random_roll:.3f} (threshold: {self.randomness:.3f})")
        
        if random_roll < self.randomness:
            random_move = random.choice(available_moves)
            print(f"🎲 USING RANDOM MOVE: {random_move} (due to {self.difficulty} difficulty)")
            print("=== END DIFFICULTY TEST ===\n")
            return random_move
        
        print(f"🧠 USING MINIMAX with depth limit: {self.max_depth}")
        
        best_move = None
        best_score = float('-inf')
        
        for i, (row, col) in enumerate(available_moves):
            print(f"\n📊 Evaluating move {i+1}/{len(available_moves)}: ({row}, {col})")
            
            # Create a copy of the engine to simulate the move
            temp_engine = engine.copy()
            temp_engine.make_move(row, col, ai_player)
            
            # Reset depth counter for each move evaluation
            self.depth_reached = 0  # We'll track this
            
            # Get score using minimax
            score = self._minimax(
                temp_engine, 
                depth=0, 
                is_maximizing=False,  # Next move will be opponent's
                alpha=float('-inf'), 
                beta=float('+inf'),
                ai_player=ai_player
            )
            
            print(f"📈 Move ({row}, {col}): Score = {score}, Max depth reached = {self.depth_reached}")
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
                print(f"⭐ NEW BEST MOVE: {best_move} with score: {best_score}")
        
        print(f"\n🏆 FINAL CHOICE: {best_move} with score: {best_score}")
        print(f"🎯 This was {self.difficulty.upper()} mode with max depth {self.max_depth}")
        print("=== END DIFFICULTY TEST ===\n")
        
        return best_move
    
    def _minimax(self, engine: TicTacToeEngine, depth: int, is_maximizing: bool, 
            alpha: float, beta: float, ai_player: str) -> int:
        """Minimax algorithm with alpha-beta pruning."""
        
        # Track the maximum depth we actually reach
        if hasattr(self, 'depth_reached'):
            self.depth_reached = max(self.depth_reached, depth)
        else:
            self.depth_reached = depth
        
        print(f"  {'  ' * depth}🔍 Depth {depth}: {'MAX' if is_maximizing else 'MIN'} player")
        
        # Terminal conditions
        if engine.is_terminal() or depth >= self.max_depth:
            score = engine.evaluate(ai_player)
            
            if depth >= self.max_depth:
                print(f"  {'  ' * depth}⛔ DEPTH LIMIT REACHED at {depth} (max: {self.max_depth})")
            else:
                print(f"  {'  ' * depth}🏁 Terminal state reached at depth {depth}")
            
            print(f"  {'  ' * depth}📊 Raw score: {score}")
            
            # Prefer faster wins and slower losses
            if score > 0:
                adjusted_score = score - depth
                print(f"  {'  ' * depth}⚡ Win bonus: {score} - {depth} = {adjusted_score}")
                return adjusted_score
            elif score < 0:
                adjusted_score = score + depth
                print(f"  {'  ' * depth}🐌 Loss penalty: {score} + {depth} = {adjusted_score}")
                return adjusted_score
            
            return score
        
        available_moves = engine.get_available_moves()
        
        if is_maximizing:
            max_eval = float('-inf')
            for i, (row, col) in enumerate(available_moves):
                print(f"  {'  ' * depth}🔴 MAX trying move {i+1}/{len(available_moves)}: ({row},{col})")
                
                temp_engine = engine.copy()
                temp_engine.make_move(row, col, ai_player)
                
                eval_score = self._minimax(
                    temp_engine, depth + 1, False, alpha, beta, ai_player
                )
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                print(f"  {'  ' * depth}📈 Move ({row},{col}): {eval_score}, running max: {max_eval}")
                
                # Alpha-beta pruning
                if beta <= alpha:
                    print(f"  {'  ' * depth}✂️  PRUNED remaining moves at depth {depth}")
                    break
            
            return max_eval
        
        else:  # Minimizing
            min_eval = float('+inf')
            opponent = 'O' if ai_player == 'X' else 'X'
            
            for i, (row, col) in enumerate(available_moves):
                print(f"  {'  ' * depth}🔵 MIN trying move {i+1}/{len(available_moves)}: ({row},{col})")
                
                temp_engine = engine.copy()
                temp_engine.make_move(row, col, opponent)
                
                eval_score = self._minimax(
                    temp_engine, depth + 1, True, alpha, beta, ai_player
                )
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                print(f"  {'  ' * depth}📉 Move ({row},{col}): {eval_score}, running min: {min_eval}")
                
                # Alpha-beta pruning
                if beta <= alpha:
                    print(f"  {'  ' * depth}✂️  PRUNED remaining moves at depth {depth}")
                    break
            
            return min_eval