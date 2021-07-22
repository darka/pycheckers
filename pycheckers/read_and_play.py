from pycheckers.game import initial_setup_board, square_number_to_pos
def read_checkers_pdn(filename: str):
    move_lines = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.rstrip()
            if not line.startswith('['):
                move_lines.append(line)
            if not line:
                break
    move_line = ' '.join(move_lines)

    moves = []
    tokens = move_line.split(' ')
    for token in tokens:
        if token in ('1-0', '0-1', '1/2-1/2'):
            continue
        elif '-' in token:
            moves_new = [int(x) for x in token.split('-')]
            moves.append(tuple(moves_new))
        elif 'x' in token:
            moves_new = [int(x) for x in token.split('x')]
            moves.append(tuple(moves_new))
    
    return moves


if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    moves = read_checkers_pdn(filename)
    print(moves)

    game = initial_setup_board()
    print(f'{game}\n')
    for move in moves:
        start = move[0]
        path = move[1:]
        start = square_number_to_pos(start)
        path = [square_number_to_pos(x) for x in path]
        game.move(start, path)
        print(f'{game}\n')
