
def file_diff(from_pos: str, to_pos: str) -> int:
    return abs(ord(from_pos[0]) - ord(to_pos[0]))


def rank_diff(from_pos: str, to_pos: str) -> int:
    return abs(ord(from_pos[1]) - ord(to_pos[1]))


def move_sep(from_pos: str, to_pos: str) -> (int, int):
    return file_diff(from_pos, to_pos), rank_diff(from_pos, to_pos)


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
        return moved_by in [(0, 1), (0, 2)]

    def can_pawn_capture():
        return moved_by == (1, 1)

    return {"R": can_rook_move, "N": can_knight_move,  "B": can_bishop_move,
            "Q": can_queen_move, "K": can_king_move, "P": can_pawn_move,
            'C': can_pawn_capture}[piece.upper()]()
