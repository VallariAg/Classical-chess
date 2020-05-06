import re
from sys import argv
# modules
import validMoves
import pgnToMoves
import movesToFen
# pawn_capture_name = 'C'
WHITE, BLACK = 'w', 'b'
pgnFile = argv[1]
moves = pgnToMoves.pgn_to_moves(pgnFile)
board_view = pgnToMoves.setup()
# board_view -> {'A1': 'R', 'A2': 'B', ...}


# -- MOVE INFO -- (PIECE, FROM, TO)
def get_from_pos(piece, from_pos_hint, to_pos):
    piece_view = pgnToMoves.locate_pieces(board_view)  # NEEDS BOARD_VIEW

    if from_pos_hint == '':
        return [_ for _ in piece_view[piece] if validMoves.check_move(piece, _, to_pos)][0]
    else:
        return [_ for _ in piece_view[piece] if validMoves.check_move(piece, _, to_pos) and from_pos_hint in _][0]


def get_move_info(move):
    PATTERN = re.compile(
        "(?P<piece>.)(?P<from_pos_hint>[a-h]*[1-8]*)(?P<to_go>[a-h][1-8])")
    move_dict = PATTERN.match(move).groupdict()
    piece, from_pos_hint, to_pos = move_dict['piece'], move_dict['from_pos_hint'], move_dict['to_go']
    from_pos = get_from_pos(piece, from_pos_hint, to_pos)
    return piece, from_pos, to_pos
# ------------------


# -- MOVES PIECES -- (gives changes in board_view)
def move_piece(move):
    piece, from_pos, to_pos = get_move_info(move)
    return {from_pos: ' ', to_pos: piece}


def make_pawn_move(move):

    # if is_enpassant(move):
    # return pawn_capture(move)
    if is_capture(move):
        return pawn_capture(move)

    elif is_pawn_promotion(move):
        return pawn_promotion(move)
    else:
        return move_piece(move)
# -------------


def pawn_capture(move):
    pawn_capture_name = 'c' if move.lower() == move else 'C'
    move = pawn_capture_name + move[1:]
    move = move.replace('x', '')
    piece, from_pos, to_pos = get_move_info(move)
    piece = 'p' if piece == 'c' else 'P'
    return {from_pos: ' ', to_pos: piece}


def pawn_promotion(move):
    from_pos, promoted_to_piece = move.split('=')
    return {from_pos: promoted_to_piece}


def castle(move):
    return {'o-o': {'e8': ' ', 'g8': 'k', 'h8': ' ', 'f8': 'r'},
            'O-O': {'e1': ' ', 'g1': 'K', 'h1': ' ', 'f1': 'R'},
            'o-o-o': {'e8': ' ', 'c8': 'k', 'a8': ' ', 'd8': 'r'},
            'O-O-O': {'e1': ' ', 'c1': 'K', 'a1': ' ', 'd1': 'R'}}[move]


# -- IDENTIFY MOVES --


def is_pawn_promotion(move):
    return '=' in move


def is_two_step(from_pos, to_pos):
    return validMoves.move_sep(from_pos, to_pos) == (0, 2)


def is_castling(move):
    return move in ["o-o", 'o-o-o', 'O-O-O', 'O-O']


def is_pawn_capture(from_pos, to_pos):
    return validMoves.move_sep(from_pos, to_pos) == (1, 1)


def is_capture(move):
    return 'x' in move


def is_pawn_move(move):
    return move[0] in ['p', 'P']


def is_check(move):
    return move[-1] == '+'
# -------------


def make_move(move):
    if is_check(move):
        move = move[:-1]
    if is_capture(move) and not is_pawn_move(move):
        move = move.replace('x', '')
    if is_pawn_move(move):
        board_changes = make_pawn_move(move)
    elif is_castling(move):
        board_changes = castle(move)
    else:
        board_changes = move_piece(move)
    return board_changes


def move_to_fen(COLOR, move):
    if move is not "":
        board_changes = make_move(
            move)
        board_view.update(board_changes)  # BOARD VIEW USED
        return movesToFen.board_to_fen(board_view)
    return ""


for (fullmove, (wmove, bmove)) in enumerate(moves):

    fen = move_to_fen('b', wmove)
    print(fen)
    fen = move_to_fen('w', bmove)
    print(fen)
