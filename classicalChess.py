import re
from sys import argv
# modules
import validMoves
import pgnToMoves
import movesToFen
# PAWN_CAPTURE = 'C'
WHITE, BLACK = 'w', 'b'
# CASTLING = {'K': }
pgnFile = argv[1]
CASTLING_AVAILIBILTY, EN_PASSANT, HALFMOVE = 'KQkq', ('-', '-'), 0
moves = pgnToMoves.pgn_to_moves(pgnFile)
board_view = pgnToMoves.setup()
# board -> {'A1': 'R', 'A2': 'B', ...}


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
# -------------


# -- MOVES PIECES -- (gives changes in board_view)
def move_piece(move):
    piece, from_pos, to_pos = get_move_info(move)
    return {from_pos: ' ', to_pos: piece}


def make_pawn_move(move):
    global HALFMOVE, EN_PASSANT
    HALFMOVE = 0

    if is_enpassant(move):
        global EN_PASSANT
        EN_PASSANT = ('-', '-')
        return pawn_capture(move).update({EN_PASSANT[1]: " "})
    elif is_capture(move):
        return pawn_capture(move)

    elif is_pawn_promotion(move):
        return pawn_promotion(move)
    else:
        piece, from_pos, to_pos = get_move_info(move)
        if is_two_step(from_pos, to_pos):
            return make_enpassant(piece, from_pos, to_pos)
        if EN_PASSANT[1] == from_pos:
            EN_PASSANT = ('-', '-')
        return {from_pos: ' ', to_pos: piece}
# -------------


def pawn_capture(move):
    PAWN_CAPTURE = 'c' if move.lower() == move else 'C'
    move = PAWN_CAPTURE + move[1:]
    move = move.replace('x', '')
    piece, from_pos, to_pos = get_move_info(move)
    piece = 'p' if piece == 'c' else 'P'
    return {from_pos: ' ', to_pos: piece}


def make_enpassant(piece, from_pos, to_pos):
    global EN_PASSANT
    add_rank = 1 if piece is 'P' else -1
    EN_PASSANT = (from_pos[0] + str(int(from_pos[1]) + add_rank), to_pos)
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


def is_enpassant(move):
    pawn = 'p' if move == move.lower() else 'P'
    return move[-2:] == EN_PASSANT[0] and EN_PASSANT[1] == pawn


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
        global HALFMOVE
        HALFMOVE = 0
    if is_pawn_move(move):
        board_changes = make_pawn_move(move)
    elif is_castling(move):
        board_changes = castle(move)
    else:
        board_changes = move_piece(move)
    return board_changes


def move_to_fen(COLOR, move):
    global HALFMOVE
    HALFMOVE += 1
    if move is not "":
        board_changes = make_move(
            move)
        board_view.update(board_changes)  # BOARD VIEW USED
        fen = movesToFen.get_full_fen(
            board_view, COLOR, CASTLING_AVAILIBILTY, EN_PASSANT[0], HALFMOVE, fullmove + 1)
        return fen
    return ""


for (fullmove, (wmove, bmove)) in enumerate(moves):

    fen = move_to_fen('b', wmove)
    print(fen)
    fen = move_to_fen('w', bmove)
    print(fen)
