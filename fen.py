import re
board_view = setup()


def setup():
    square = [y+x for x in "12345678" for y in "ABCDEFGH"]
    start = "RNBQKBNR" + "P" * 8 + " " * 32 + "p" * 8 + "rnbqkbnr"
    board_view = dict(zip(square, start))
    piece_view = {piece: [] for piece in "BKNPQRbknpqr"}
    for sq in board_view:
        piece = board_view[sq]
        if piece != " ":
            piece_view[piece].append(sq)
    # piece_view = locate_pieces(board_view)
    return board_view, piece_view


# def locate_pieces(board_view):
#     piece_view = {piece: [] for piece in "BKNPQRbknpqr"}
#     for sq in board_view:
#         piece = board_view[sq]
#         if piece != " ":
#             piece_view[piece].append(sq)
#     return piece_view

def moves_to_fen(board_view):
    pass


# def moves_on_board(moves):
#     board_view, piece_view = setup()
#     for move in moves:
#         board_view, piece_view = move_on_board(move, board_view, piece_view)
#     return board_view


# def move_on_board(move: [(str, str)], board_view, piece_view):
#     if move == '0-0' or move == 'o-o':
#         # piece_view['K'] == ''
#         pass

#     def default_move():
#         piece = move[0]
#         board_view[piece] = " "
#         board_view[move[-2:]] = piece
#     return board_view
    # def Qcastling():


# def locate_a_piece(board_view, piece):
#     piece_view = locate_pieces(board_view)
#     return piece_view[piece]


def pgn_to_moves(game_file: str) -> [str]:
    raw_pgn = " ".join([line.strip() for line in open(game_file)])

    comments_marked = raw_pgn.replace("{", "<").replace("}", ">")
    STRC = re.compile("<[^>]*>")
    comments_removed = STRC.sub(" ", comments_marked)

    STR_marked = comments_removed.replace("[", "<").replace("]", ">")
    str_removed = STRC.sub(" ", STR_marked)

    MOVE_NUM = re.compile("[1-9][0-9]* *\.")
    just_moves = [_.strip() for _ in MOVE_NUM.split(str_removed)]

    last_move = just_moves[-1]
    RESULT = re.compile("( *1 *- *0 *| *0 *- *1 *| *1/2 *- *1/2 *)")
    last_move = RESULT.sub("", last_move)
    # moves = just_moves[:-1] + [last_move]
    return [pre_process_a_move(move) for move in just_moves[:-1] if len(move) > 0]


def pre_process_a_move(move: str) -> (str, str):
    wmove, bmove = move.split()
    if wmove[0] in 'abcdefgh':
        wmove = "P" + wmove
    if bmove[0] in 'abcdefgh':
        bmove = "p" + bmove
    else:
        bmove = bmove.lower()

    return wmove, bmove


def pre_process_moves(moves: [str]) -> [(str, str)]:
    return [pre_process_a_move(move) for move in moves[-1]]


moves = pgn_to_moves("Morphy.pgn")
print(moves)

moves = moves_on_board(moves)
# print(setup())
