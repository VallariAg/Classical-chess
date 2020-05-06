import re


def board_to_fen(board):
    board_list = list(board.values())
    rank_list = []

    for i in range(8):
        this_rank = "".join(board_list[i * 8:(i*8) + 8])
        SPACES = (re.findall(' {1,8}', this_rank))
        print(SPACES)
        for space in SPACES:
            # space = space.replace(' ', '+')
            print(space.replace(' ', '+'))
            this_rank = this_rank.replace(space, str(len(space)))
        rank_list += [this_rank]
    return ' / '.join(reversed(rank_list))


def get_full_fen(board, a_color, castling_availability, en_pessant, halfmove, fullmove):
    return board_to_fen(board), a_color, castling_availability, en_pessant, halfmove, fullmove
    # piece, from_pos, destination = get_move_info(move)
    # board_changes = {'R': make_rook_move, 'r': make_rook_move,
    #                  'K': make_king_move, 'k': make_king_move,
    #                  'Q': make_queen_move, 'q': make_queen_move,
    #                  #  'P': make_pawn_move, 'p': make_pawn_move,
    #                  'B': make_bishop_move, 'b': make_bishop_move,
    #                  'N': make_knight_move, 'n': make_knight_move,
    #                  }[piece](COLOR, from_pos, destination)
