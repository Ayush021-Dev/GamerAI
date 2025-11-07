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
        this.gameMode = 'pve'; // New: Default to Player vs. Environment (Bot)
        this.scores = {
            human: 0,
            ai: 0,
            draw: 0
        };
        
        this.initializeElements();
        this.bindEvents();
        this.loadScores();
        this.loadGameState();
        this.updateUIMode(); // New: Initial UI update for mode
    }
    
    initializeElements() {
        // Toggle buttons for first player selection
        this.humanFirstBtn = document.getElementById('human-first-btn');
        this.aiFirstBtn = document.getElementById('ai-first-btn');
        
        // New: Game Mode Toggle
        this.pveModeBtn = document.getElementById('pve-mode-btn');
        this.pvpModeBtn = document.getElementById('pvp-mode-btn');

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
        
        // New: Game Mode listeners
        this.pveModeBtn.addEventListener('click', () => this.setGameMode('pve'));
        this.pvpModeBtn.addEventListener('click', () => this.setGameMode('pvp'));
        
        this.cells.forEach(cell => {
            cell.addEventListener('click', (e) => this.handleCellClick(e));
        });
    }

    // New method to handle game mode selection
    setGameMode(mode) {
        this.gameMode = mode;
        this.updateUIMode();
    }
    
    updateUIMode() {
        // Update button states
        this.pveModeBtn.classList.toggle('active', this.gameMode === 'pve');
        this.pvpModeBtn.classList.toggle('active', this.gameMode === 'pvp');
        
        // Show/Hide PVE-specific controls (First Player & Difficulty)
        const pveControls = document.getElementById('pve-controls');
        if (pveControls) {
            pveControls.style.display = this.gameMode === 'pve' ? 'flex' : 'none';
        }

        // Adjust score labels for PvP
        const humanLabel = document.getElementById('human-score-label');
        const aiLabel = document.getElementById('ai-score-label');

        if (this.gameMode === 'pvp') {
            humanLabel.textContent = 'Player 1 (X):';
            aiLabel.textContent = 'Player 2 (O):';
        } else {
            humanLabel.textContent = 'You (X):';
            aiLabel.textContent = 'Bot (O):';
        }
        
        // Reset game on mode change for clean state
        this.startNewGame(false);
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
                this.gameMode = data.game_mode || 'pve'; // New: Load game mode
                this.updateUIMode(); // New: Update UI based on loaded mode
                
                // If it's AI's turn and game is not over, make AI move (only in PVE)
                if (this.gameMode === 'pve' && !this.gameOver && this.currentPlayer === 'O') {
                    setTimeout(() => this.makeAIMove(), 500);
                }
            } else {
                // No existing game, show initial message
                this.updateStatus("Choose mode/difficulty and start a new game!");
                this.showTurnIndicator(false);
            }
        } catch (error) {
            console.error('Failed to load game state:', error);
            this.updateStatus("Choose mode/difficulty and start a new game!");
            this.showTurnIndicator(false);
        }
    }
    
    async startNewGame(updateServer = true) { // Optional parameter to skip server call
        try {
            this.showLoading(false);
            
            // If skipping server update (e.g., on mode switch), reset locally
            if (!updateServer) {
                this.board = Array(3).fill(null).map(() => Array(3).fill(null));
                this.currentPlayer = 'X';
                this.gameOver = false;
                this.winner = null;
                this.renderBoard();
                this.updateStatus(this.gameMode === 'pvp' ? "Player 1 (X)'s turn! Click any cell." : "Choose mode/settings and start a new game!");
                this.showTurnIndicator(this.gameMode === 'pvp');
                return;
            }

            const response = await fetch('/tic-tac-toe/api/new', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    difficulty: this.difficulty,
                    first_player: this.firstPlayerValue,
                    game_mode: this.gameMode // New: Pass game mode
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.updateGameState(data.state);
                
                if (this.gameMode === 'pve' && data.ai_should_move) {
                    this.updateStatus("Bot goes first...");
                    setTimeout(() => this.makeAIMove(), 500);
                } else {
                    const message = this.gameMode === 'pvp' 
                        ? "Player 1 (X)'s turn! Click any cell."
                        : "Your turn! Click any cell to make your move.";
                    this.updateStatus(message);
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
        console.log('Bot turn:', this.isAITurn); // Debug
        
        if (this.gameOver || (this.gameMode === 'pve' && this.isAITurn)) { // Check AI turn only in PVE
            console.log('Returning early - game over or Bot turn (PVE mode)'); // Debug
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
            this.showLoading(true, 'Processing move...');
            
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
                    // Decide next step based on game mode
                    if (this.gameMode === 'pve') {
                        // PVE: AI's turn
                        setTimeout(() => this.makeAIMove(), 300);
                    } else {
                        // PVP: Next human player's turn
                        const nextPlayerText = this.currentPlayer === 'X' ? 'Player 1 (X)' : 'Player 2 (O)';
                        this.updateStatus(`${nextPlayerText}'s turn! Click any cell.`);
                        this.showTurnIndicator(true);
                    }
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
        if (this.gameOver || this.currentPlayer !== 'O' || this.gameMode !== 'pve') { // New: check game mode
            return;
        }
        
        this.isAITurn = true;
        
        try {
            this.showLoading(true, 'Bot is thinking...');
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
                this.showError(data.error || 'Bot move failed');
            }
        } catch (error) {
            this.showError('Network error. Please try again.');
            console.error('Bot move error:', error);
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
        
        let humanText = this.gameMode === 'pvp' ? 'Player 1 (X)' : 'You';
        let aiText = this.gameMode === 'pvp' ? 'Player 2 (O)' : 'Bot';

        if (this.winner === 'X') {
            this.updateStatus(`🎉 ${humanText} won! Great job!`, 'winner');
            this.scores.human++;
        } else if (this.winner === 'O') {
            this.updateStatus(`🏆 ${aiText} wins!`, 'winner');
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
            let playerText;
            if (this.gameMode === 'pvp') {
                playerText = this.currentPlayer === 'X' ? 'Player 1 (X)\'s turn' : 'Player 2 (O)\'s turn';
            } else {
                playerText = this.currentPlayer === 'X' ? 'Your turn' : 'Bot\'s turn';
            }
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
    // New code to handle score label elements when the game mode changes
    const scoreBoard = document.querySelector('.score-board');
    if (scoreBoard) {
        let humanLabel = scoreBoard.querySelector('#human-score-label');
        if (!humanLabel) {
            humanLabel = document.createElement('span');
            humanLabel.id = 'human-score-label';
            humanLabel.className = 'label';
            scoreBoard.children[0].prepend(humanLabel); // Assuming structure
        }

        let aiLabel = scoreBoard.querySelector('#ai-score-label');
        if (!aiLabel) {
            aiLabel = document.createElement('span');
            aiLabel.id = 'ai-score-label';
            aiLabel.className = 'label';
            scoreBoard.children[1].prepend(aiLabel); // Assuming structure
        }
    }
    
    new TicTacToeGame();
});