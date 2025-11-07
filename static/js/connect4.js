/**
 * Connect-4 Game JavaScript
 * Handles UI interactions and game logic for Connect-4
 */

class Connect4Game {
    constructor() {
        this.board = [];
        this.currentPlayer = 1;
        this.gameOver = false;
        this.winner = null;
        this.validMoves = [];
        this.scores = {
            human: 0,
            ai: 0,
            draws: 0
        };
        
        this.initializeGame();
        this.bindEvents();
        this.loadScores();
    }
    
    initializeGame() {
        this.createBoard();
        this.updateStatus("Choose difficulty and start a new game!");
    }
    
    createBoard() {
        const boardElement = document.getElementById('connect4-board');
        boardElement.innerHTML = '';
        
        // Create column headers for hover effect
        for (let col = 0; col < 7; col++) {
            const header = document.createElement('div');
            header.className = 'column-header';
            header.style.left = `${col * 68 + 8}px`;
            header.textContent = '↓';
            header.dataset.col = col;
            boardElement.appendChild(header);
        }
        
        // Create board cells
        for (let row = 0; row < 6; row++) {
            for (let col = 0; col < 7; col++) {
                const cell = document.createElement('div');
                cell.className = 'board-cell empty';
                cell.dataset.row = row;
                cell.dataset.col = col;
                cell.addEventListener('click', () => this.makeMove(col));
                boardElement.appendChild(cell);
            }
        }
    }
    
    bindEvents() {
        // New game button
        document.getElementById('new-game').addEventListener('click', () => {
            this.newGame();
        });
        
        // First player selection
        document.getElementById('you-first').addEventListener('click', () => {
            this.setFirstPlayer('human');
        });
        
        document.getElementById('ai-first').addEventListener('click', () => {
            this.setFirstPlayer('ai');
        });
        
        // Column hover effects
        document.addEventListener('mouseover', (e) => {
            if (e.target.classList.contains('column-header')) {
                const col = parseInt(e.target.dataset.col);
                this.highlightColumn(col, true);
            }
        });
        
        document.addEventListener('mouseout', (e) => {
            if (e.target.classList.contains('column-header')) {
                const col = parseInt(e.target.dataset.col);
                this.highlightColumn(col, false);
            }
        });
    }
    
    setFirstPlayer(player) {
        const youFirst = document.getElementById('you-first');
        const aiFirst = document.getElementById('ai-first');
        
        if (player === 'human') {
            youFirst.classList.add('active');
            aiFirst.classList.remove('active');
        } else {
            aiFirst.classList.add('active');
            youFirst.classList.remove('active');
        }
    }
    
    async newGame() {
        const difficulty = document.getElementById('difficulty').value;
        const firstPlayer = document.getElementById('ai-first').classList.contains('active') ? 'ai' : 'human';
        
        try {
            document.getElementById('new-game').disabled = true;
            this.updateStatus("Starting new game...");
            
            const response = await fetch('/connect4/api/new_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    difficulty: difficulty,
                    first_player: firstPlayer
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.updateGameState(data);
                if (data.ai_move !== undefined) {
                    this.animateMove(data.ai_move, -1);
                    this.updateStatus("Your turn! Click a column to drop your piece.");
                } else {
                    this.updateStatus("Your turn! Click a column to drop your piece.");
                }
            } else {
                this.updateStatus("Error starting game: " + data.error);
            }
        } catch (error) {
            console.error('Error starting new game:', error);
            this.updateStatus("Error starting game. Please try again.");
        } finally {
            document.getElementById('new-game').disabled = false;
        }
    }
    
    async makeMove(col) {
        if (this.gameOver || this.currentPlayer !== 1) {
            return;
        }
        
        if (!this.validMoves.includes(col)) {
            this.updateStatus("Invalid move! Column is full.");
            return;
        }
        
        try {
            this.updateStatus("Making your move...");
            
            const response = await fetch('/api/connect4/make_move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    col: col
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Animate human move
                this.animateMove(data.human_move, 1);
                
                // Update game state
                this.updateGameState(data);
                
                // Check if game is over after human move
                if (this.gameOver) {
                    this.handleGameEnd();
                    return;
                }
                
                // Animate AI move if it exists
                if (data.ai_move !== undefined) {
                    setTimeout(() => {
                        this.animateMove(data.ai_move, -1);
                        this.updateGameState(data);
                        
                        if (this.gameOver) {
                            this.handleGameEnd();
                        } else {
                            this.updateStatus("Your turn! Click a column to drop your piece.");
                        }
                    }, 600);
                    
                    this.updateStatus("AI is thinking...");
                }
            } else {
                this.updateStatus("Error: " + data.error);
            }
        } catch (error) {
            console.error('Error making move:', error);
            this.updateStatus("Error making move. Please try again.");
        }
    }
    
    animateMove(col, player) {
        // Find the row where the piece landed
        let row = -1;
        for (let r = 5; r >= 0; r--) {
            const cell = document.querySelector(`[data-row="${r}"][data-col="${col}"]`);
            if (cell.classList.contains('human') || cell.classList.contains('ai')) {
                row = r;
                break;
            }
        }
        
        if (row >= 0) {
            const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
            cell.classList.add('piece-drop', 'last-move');
            
            // Remove animation classes after animation completes
            setTimeout(() => {
                cell.classList.remove('piece-drop', 'last-move');
            }, 600);
        }
    }
    
    updateGameState(data) {
        this.board = data.board;
        this.currentPlayer = data.current_player;
        this.gameOver = data.game_over;
        this.winner = data.winner;
        this.validMoves = data.valid_moves || [];
        
        this.renderBoard();
        this.updateColumnHeaders();
    }
    
    renderBoard() {
        for (let row = 0; row < 6; row++) {
            for (let col = 0; col < 7; col++) {
                const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
                const value = this.board[row][col];
                
                cell.classList.remove('empty', 'human', 'ai', 'winning');
                
                if (value === 1) {
                    cell.classList.add('human');
                    cell.textContent = '🔴';
                } else if (value === -1) {
                    cell.classList.add('ai');
                    cell.textContent = '🟡';
                } else {
                    cell.classList.add('empty');
                    cell.textContent = '';
                }
            }
        }
    }
    
    updateColumnHeaders() {
        const headers = document.querySelectorAll('.column-header');
        headers.forEach((header, col) => {
            header.classList.remove('valid');
            if (this.validMoves.includes(col) && !this.gameOver && this.currentPlayer === 1) {
                header.classList.add('valid');
            }
        });
    }
    
    highlightColumn(col, highlight) {
        if (this.gameOver || this.currentPlayer !== 1 || !this.validMoves.includes(col)) {
            return;
        }
        
        // Find the top empty cell in the column
        for (let row = 0; row < 6; row++) {
            const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
            if (cell.classList.contains('empty')) {
                if (highlight) {
                    cell.style.background = 'rgba(231, 76, 60, 0.3)';
                } else {
                    cell.style.background = '';
                }
                break;
            }
        }
    }
    
    handleGameEnd() {
        if (this.winner === 1) {
            this.updateStatus("🎉 You won! Congratulations!");
            this.scores.human++;
        } else if (this.winner === -1) {
            this.updateStatus("🤖 AI won! Better luck next time!");
            this.scores.ai++;
        } else {
            this.updateStatus("🤝 It's a draw! Great game!");
            this.scores.draws++;
        }
        
        console.log("update score")
        this.saveScores();
        console.log("update score")
        this.updateScoreDisplay();
        
        // Highlight winning pieces if there's a winner
        if (this.winner !== 0) {
            this.highlightWinningPieces();
        }
    }
    
    highlightWinningPieces() {
        // This is a simplified version - you could implement actual winning line detection
        // For now, just add a subtle pulse to all pieces of the winning player
        const winningClass = this.winner === 1 ? 'human' : 'ai';
        const winningCells = document.querySelectorAll(`.${winningClass}`);
        
        winningCells.forEach(cell => {
            cell.classList.add('winning');
        });
    }
    
    updateStatus(message) {
        document.getElementById('game-status').textContent = message;
    }
    
    updateScoreDisplay() {
        document.getElementById('human-score').textContent = this.scores.human;
        document.getElementById('ai-score').textContent = this.scores.ai;
        document.getElementById('draws').textContent = this.scores.draws;
    }
    
    saveScores() {
        localStorage.setItem('connect4_scores', JSON.stringify(this.scores));
    }
    
    loadScores() {
        const saved = localStorage.getItem('connect4_scores');
        if (saved) {
            this.scores = JSON.parse(saved);
        }
        this.updateScoreDisplay();
    }
}

// Initialize the game when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new Connect4Game();
});