/**
 * Tic-Tac-Toe Frontend Logic
 * Handles UI interactions and API communication
 */

class TicTacToeGame {
    constructor() {
        this.board = null;
        this.currentPlayer = 'X';
        this.gameOver = false;
        this.winner = null;
        this.difficulty = 'medium';
        this.isAITurn = false;
        this.firstPlayerValue = 'human'; // Default value for toggle
        this.scores = {
            human: 0,
            ai: 0,
            draw: 0
        };
        
        this.initializeElements();
        this.bindEvents();
        this.loadScores();
        this.loadGameState();
    }
    
    initializeElements() {
        // Toggle buttons for first player selection
        this.humanFirstBtn = document.getElementById('human-first-btn');
        this.aiFirstBtn = document.getElementById('ai-first-btn');
        
        this.difficultySelect = document.getElementById('difficulty-select');
        this.newGameBtn = document.getElementById('new-game-btn');
        this.statusMessage = document.getElementById('status-message');
        this.turnIndicator = document.getElementById('turn-indicator');
        this.gameBoard = document.getElementById('game-board');
        this.loadingOverlay = document.getElementById('loading-overlay');
        this.cells = document.querySelectorAll('.cell');
        
        // Score elements
        this.humanScoreEl = document.getElementById('human-score');
        this.aiScoreEl = document.getElementById('ai-score');
        this.drawScoreEl = document.getElementById('draw-score');
    }
    
    bindEvents() {
        this.newGameBtn.addEventListener('click', () => this.startNewGame());
        this.difficultySelect.addEventListener('change', (e) => {
            this.difficulty = e.target.value;
        });
        
        // Add toggle button event listeners
        this.humanFirstBtn.addEventListener('click', () => this.setFirstPlayer('human'));
        this.aiFirstBtn.addEventListener('click', () => this.setFirstPlayer('ai'));
        
        this.cells.forEach(cell => {
            cell.addEventListener('click', (e) => this.handleCellClick(e));
        });
    }
    
    // New method to handle toggle button selection
    setFirstPlayer(player) {
        this.firstPlayerValue = player;
        
        // Update button states
        this.humanFirstBtn.classList.toggle('active', player === 'human');
        this.aiFirstBtn.classList.toggle('active', player === 'ai');
    }
    
    async loadGameState() {
        try {
            const response = await fetch('/tic-tac-toe/api/state');
            const data = await response.json();
            
            console.log('Loaded game state:', data); // Debug
            
            if (data.success && data.state.board) {
                this.updateGameState(data.state);
                this.difficulty = data.difficulty || 'medium';
                this.difficultySelect.value = this.difficulty;
                
                // If it's AI's turn and game is not over, make AI move
                if (!this.gameOver && this.currentPlayer === 'O') {
                    setTimeout(() => this.makeAIMove(), 500);
                }
            } else {
                // No existing game, show initial message
                this.updateStatus("Choose difficulty and start a new game!");
                this.showTurnIndicator(false);
            }
        } catch (error) {
            console.error('Failed to load game state:', error);
            this.updateStatus("Choose difficulty and start a new game!");
            this.showTurnIndicator(false);
        }
    }
    
    async startNewGame() {
        try {
            this.showLoading(false);
            
            const response = await fetch('/tic-tac-toe/api/new', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    difficulty: this.difficulty,
                    first_player: this.firstPlayerValue // Use toggle value instead of select
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.updateGameState(data.state);
                
                if (data.ai_should_move) {
                    this.updateStatus("AI goes first...");
                    setTimeout(() => this.makeAIMove(), 500);
                } else {
                    this.updateStatus("Your turn! Click any cell to make your move.");
                    this.showTurnIndicator(true);
                }
            }
        } catch (error) {
            this.showError('Network error. Please try again.');
            console.error('Start new game error:', error);
        } finally {
            this.hideLoading();
        }
    }
    
    async handleCellClick(event) {
        console.log('Cell clicked!'); // Debug
        console.log('Game over:', this.gameOver); // Debug
        console.log('AI turn:', this.isAITurn); // Debug
        
        if (this.gameOver || this.isAITurn) {
            console.log('Returning early - game over or AI turn'); // Debug
            return;
        }
        
        const cell = event.target;
        const row = parseInt(cell.dataset.row);
        const col = parseInt(cell.dataset.col);
        
        console.log('Cell row:', row, 'col:', col); // Debug
        console.log('Cell classes:', cell.className); // Debug
        console.log('Cell content:', cell.textContent); // Debug
        console.log('Current board state:', this.board); // Debug
        
        // Check if cell is already occupied
        if (cell.classList.contains('occupied')) {
            console.log('Cell has occupied class'); // Debug
            return;
        }
        
        // Also check the board state
        if (this.board && this.board[row] && this.board[row][col]) {
            console.log('Cell is occupied in board state:', this.board[row][col]); // Debug
            return;
        }
        
        try {
            this.showLoading(true, 'Processing your move...');
            
            const response = await fetch('/tic-tac-toe/api/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ row, col })
            });
            
            const data = await response.json();
            console.log('Server response:', data); // Debug
            
            if (data.success) {
                this.updateGameState(data.state);
                
                if (this.gameOver) {
                    this.handleGameEnd();
                } else {
                    // AI's turn
                    setTimeout(() => this.makeAIMove(), 300);
                }
            } else {
                this.showError(data.error || 'Invalid move');
            }
        } catch (error) {
            this.showError('Network error. Please try again.');
            console.error('Make move error:', error);
        } finally {
            this.hideLoading();
        }
    }
    
    async makeAIMove() {
        if (this.gameOver || this.currentPlayer !== 'O') {
            return;
        }
        
        this.isAITurn = true;
        
        try {
            this.showLoading(true, 'AI is thinking...');
            this.gameBoard.classList.add('ai-thinking');
            
            // Add a small delay to make AI thinking more visible
            await new Promise(resolve => setTimeout(resolve, 500));
            
            const response = await fetch('/tic-tac-toe/api/ai-move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.updateGameState(data.state);
                
                if (this.gameOver) {
                    this.handleGameEnd();
                } else {
                    this.updateStatus("Your turn! Click any cell to make your move.");
                    this.showTurnIndicator(true);
                }
            } else {
                this.showError(data.error || 'AI move failed');
            }
        } catch (error) {
            this.showError('Network error. Please try again.');
            console.error('AI move error:', error);
        } finally {
            this.isAITurn = false;
            this.gameBoard.classList.remove('ai-thinking');
            this.hideLoading();
        }
    }
    
    updateGameState(state) {
        this.board = state.board;
        this.currentPlayer = state.current_player;
        this.gameOver = state.game_over;
        this.winner = state.winner;
        
        this.renderBoard();
    }
    
    renderBoard() {
        console.log('Rendering board:', this.board); // Debug
        
        this.cells.forEach((cell, index) => {
            const row = Math.floor(index / 3);
            const col = index % 3;
            const cellValue = this.board ? this.board[row][col] : null;
            
            console.log(`Cell [${row}][${col}]: "${cellValue}"`); // Debug
            
            // Clear previous classes
            cell.className = 'cell';
            cell.textContent = cellValue || '';
            
            if (cellValue) {
                cell.classList.add('occupied');
                cell.classList.add(cellValue.toLowerCase());
            }
            
            if (this.gameOver && !this.isAITurn) {
                cell.classList.add('disabled');
            }
        });
        
        // Highlight winning cells if there's a winner
        if (this.winner && this.gameOver) {
            this.highlightWinningCells();
        }
    }
    
    highlightWinningCells() {
        const winPatterns = [
            // Rows
            [[0,0], [0,1], [0,2]],
            [[1,0], [1,1], [1,2]],
            [[2,0], [2,1], [2,2]],
            // Columns
            [[0,0], [1,0], [2,0]],
            [[0,1], [1,1], [2,1]],
            [[0,2], [1,2], [2,2]],
            // Diagonals
            [[0,0], [1,1], [2,2]],
            [[0,2], [1,1], [2,0]]
        ];
        
        for (const pattern of winPatterns) {
            const [pos1, pos2, pos3] = pattern;
            const val1 = this.board[pos1[0]][pos1[1]];
            const val2 = this.board[pos2[0]][pos2[1]];
            const val3 = this.board[pos3[0]][pos3[1]];
            
            if (val1 && val1 === val2 && val2 === val3) {
                // Highlight winning cells
                pattern.forEach(pos => {
                    const cellIndex = pos[0] * 3 + pos[1];
                    this.cells[cellIndex].classList.add('winning');
                });
                break;
            }
        }
    }
    
    handleGameEnd() {
        this.showTurnIndicator(false);
        
        if (this.winner === 'X') {
            this.updateStatus("🎉 You won! Great job!", 'winner');
            this.scores.human++;
        } else if (this.winner === 'O') {
            this.updateStatus("🤖 AI wins! Better luck next time.", 'winner');
            this.scores.ai++;
        } else {
            this.updateStatus("🤝 It's a draw! Well played!", 'draw');
            this.scores.draw++;
        }
        
        this.updateScoreDisplay();
        this.saveScores();
    }
    
    updateStatus(message, className = '') {
        this.statusMessage.textContent = message;
        this.statusMessage.className = 'status-message';
        
        if (className) {
            this.statusMessage.classList.add(className);
        }
    }
    
    showTurnIndicator(show) {
        this.turnIndicator.style.display = show ? 'flex' : 'none';
        
        if (show) {
            const playerText = this.currentPlayer === 'X' ? 'Your turn' : 'AI\'s turn';
            this.turnIndicator.querySelector('.current-player').textContent = playerText;
        }
    }
    
    showLoading(show, message = 'Loading...') {
        if (show) {
            this.loadingOverlay.style.display = 'flex';
            this.loadingOverlay.querySelector('p').textContent = message;
        } else {
            this.loadingOverlay.style.display = 'none';
        }
    }
    
    hideLoading() {
        this.showLoading(false);
    }
    
    showError(message) {
        this.updateStatus(`❌ ${message}`);
        console.error(message);
    }
    
    updateScoreDisplay() {
        this.humanScoreEl.textContent = this.scores.human;
        this.aiScoreEl.textContent = this.scores.ai;
        this.drawScoreEl.textContent = this.scores.draw;
    }
    
    saveScores() {
        localStorage.setItem('tic_tac_toe_scores', JSON.stringify(this.scores));
    }
    
    loadScores() {
        try {
            const saved = localStorage.getItem('tic_tac_toe_scores');
            if (saved) {
                this.scores = { ...this.scores, ...JSON.parse(saved) };
                this.updateScoreDisplay();
            }
        } catch (error) {
            console.error('Failed to load scores:', error);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new TicTacToeGame();
});