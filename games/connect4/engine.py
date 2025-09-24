"""
Connect-4 Game Engine
"""
ROWS = 6
COLS = 7
EMPTY = 0
PLAYER = 1
AI = 2

def create_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def is_valid_location(board, col):
    return 0 <= col < COLS and board[0][col] == EMPTY

def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return -1

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLS):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def winning_move(board, piece):
    # Check horizontal wins
    for c in range(COLS - 3):
        for r in range(ROWS):
            if (board[r][c] == piece and board[r][c+1] == piece and 
                board[r][c+2] == piece and board[r][c+3] == piece):
                return True

    # Check vertical wins
    for c in range(COLS):
        for r in range(ROWS - 3):
            if (board[r][c] == piece and board[r+1][c] == piece and 
                board[r+2][c] == piece and board[r+3][c] == piece):
                return True

    # Check positively sloped diagonals
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if (board[r][c] == piece and board[r+1][c+1] == piece and 
                board[r+2][c+2] == piece and board[r+3][c+3] == piece):
                return True

    # Check negatively sloped diagonals
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if (board[r][c] == piece and board[r-1][c+1] == piece and 
                board[r-2][c+2] == piece and board[r-3][c+3] == piece):
                return True

    return False

def is_terminal_node(board):
    return (winning_move(board, PLAYER) or 
            winning_move(board, AI) or 
            len(get_valid_locations(board)) == 0)

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER if piece == AI else AI
    
    piece_count = window.count(piece)
    empty_count = window.count(EMPTY)
    opp_count = window.count(opp_piece)
    
    if piece_count == 4:
        score += 100
    elif piece_count == 3 and empty_count == 1:
        score += 10
    elif piece_count == 2 and empty_count == 2:
        score += 2
        
    if opp_count == 3 and empty_count == 1:
        score -= 80
    elif opp_count == 2 and empty_count == 2:
        score -= 3
        
    return score

def score_position(board, piece):
    score = 0
    
    # Favor center column
    center_array = [board[i][COLS//2] for i in range(ROWS)]
    center_count = center_array.count(piece)
    score += center_count * 3
    
    # Score horizontal positions
    for r in range(ROWS):
        row_array = board[r]
        for c in range(COLS - 3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)
    
    # Score vertical positions
    for c in range(COLS):
        col_array = [board[i][c] for i in range(ROWS)]
        for r in range(ROWS - 3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)
    
    # Score positive diagonal positions
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)
    
    # Score negative diagonal positions
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)
    
    return score
