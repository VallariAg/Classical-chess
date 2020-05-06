import re


def file_diff(from_pos: str, to_pos: str) -> int:
    return abs(ord(from_pos[0]) - ord(to_pos[0]))


def rank_diff(from_pos: str, to_pos: str) -> int:
    return abs(ord(from_pos[1]) - ord(to_pos[1]))


def move_sep(from_pos: str, to_pos: str) -> (int, int):
    return file_diff(from_pos, to_pos), rank_diff(from_pos, to_pos),


def check_move(piece: str, from_pos: str, to_pos: str) -> bool:
    BOARD = [x + y for x in "ABCDEFGH" for y in "12345678"]

    fp = from_pos.strip().upper()
    tp = to_pos.strip().upper()
    if fp == tp or fp not in BOARD or tp not in BOARD:
        return False
    moved_by = move_sep(fp, tp)

    def can_rook_move():
        return moved_by[0] == 0 or moved_by[1] == 0

    def can_knight_move():
        return moved_by in [(1, 2), (2, 1)]

    def can_bishop_move():
        return moved_by[0] == moved_by[1]

    def can_queen_move():
        return can_rook_move() or can_bishop_move()

    def can_king_move():
        return moved_by in [(0, 1), (1, 0), (1, 1)]

    def can_pawn_move():
        return (moved_by in [(0, 1), (0, 2)]) or (moved_by in [(1, 1)])

    return {"R": can_rook_move, "N": can_knight_move,  "B": can_bishop_move,
            "Q": can_queen_move, "K": can_king_move, "P": can_pawn_move}[piece]()


def setup():
    square = [y+x for x in "12345678" for y in "ABCDEFGH"]
    start = "RNBQKBNR" + "P" * 8 + " " * 32 + "p" * 8 + "rnbqkbnr"
    board_view = dict(zip(square, start))
    # piece_view = locate_pieces(board_view)
    return board_view


def locate_pieces(board_view):
    piece_view = {piece: [] for piece in "BKNPQRbknpqr"}
    for sq in board_view:
        piece = board_view[sq]
        if piece != " ":
            piece_view[piece].append(sq)
    return piece_view


def pattern_match(pattern, move):
    return pattern.match(move)


def get_move_info(move):
    MOVE_PATTERNS = [re.compile("(?P<piece>.)(?P<to_go>[a-h][1-8])"),
                     # --- DISAMBIGUITY MOVES ---
                     re.compile(
        "(?P<piece>.)(?P<from_pos>[a-h])(?P<to_go>[a-h][1-8])"),
        re.compile(
        "(?P<piece>.)(?P<from_pos>[1-8])(?P<to_go>[a-h][1-8])"),
        re.compile(
        "(?P<piece>.)(?P<from_pos>[a-h][1-8])(?P<to_go>[a-h][1-8])"),
        # ---
        re.compile('(?P<to_go>[a-h][1-8])=(?P<pass_to_piece>.)'),
    ]

    for pattern in MOVE_PATTERNS:
        pattern_result = pattern_match(pattern, move)
        if pattern_result is not None:
            return pattern_result.groupdict()
    return {}


def moves_on_board(moves):
    board_view = setup()

    def castling(move):
        if move == move.lower():  # black
            rank, king, rook = '8', 'k', 'r'
        else:
            rank, king, rook = '1', 'K', 'R'
        if move.lower() == 'o-o':  # king side
            board_view['E' + rank] = board_view['H' + rank] = " "
            board_view['G' + rank] = king
            board_view['F' + rank] = rook
        elif move.lower() == 'o-o-o':
            board_view['E' + rank] = board_view['A' + rank] = " "
            board_view['C' + rank] = king
            board_view['D' + rank] = rook
        return board_view

    def move_on_board(move):
        piece_view = locate_pieces(board_view)
        # active color
        if move == move.lower():  # black
            active_color = 'b'
        else:
            active_color = 'w'
        # print(piece_view)

        # capture
        move = move.replace("x", "")
        # castling
        if move.lower() in['o-o', 'o-o-o']:
            return castling(move)
        # is check
        if (move[-1] == '+'):
            move = move[:-1]

        from_pos = ""
        move_info = get_move_info(move)

        piece = move_info['piece']
        to_pos = move_info['to_go'].upper()

        # get from_pos of piece
        for pos in piece_view[piece]:
            if check_move(piece.upper(), pos, to_pos) == True:
                if 'from_pos' in move_info.keys():
                    from_pos = move_info['from_pos'].upper()
                    if (from_pos == pos or from_pos == pos[0] or from_pos == pos[1]):
                        from_pos = pos
                        break
                else:
                    from_pos = pos
                    break

        board_view[from_pos] = " "
        board_view[to_pos] = piece
        return board_view

    for (wmove, bmove) in moves:
        board_view = move_on_board(wmove)
        board_view = move_on_board(bmove)
        # board_view = board[0]
    return board_to_fen(board_view)


def board_to_fen(board):
    board_list = list(board.values())
    rank_list = []

    for i in range(8):
        this_rank = "".join(board_list[i * 8:(i*8) + 8])
        SPACES = (re.findall(' {1,8}', this_rank))
        print(SPACES, this_rank.replace(' ', '+'))
        for space in SPACES:
            # space = space.replace(' ', '+')
            this_rank = this_rank.replace(space, str(len(space)))
        rank_list += [this_rank]
    return ' / '.join(rank_list)
# print(check_move('Q', 'e3', 'e4'))
# print(piece_view)
# def rank_same(move):
# SAME_RANK_PATTERN = re.compile("(.)([a-h])([a-h][1-8])")
# print(SAME_RANK_PATTERN.match('Nda8').groups())
# if (SAME_RANK_PATTERN.match('Nda8'):
# print("a")
# print(piece_view)
# board_view, piece_view = (default_move('Rab1'))
# print(piece_view)
# board_view, piece_view = (default_move('Rdg8'))
# board_view, piece_view = (default_move('Rdg8'))
