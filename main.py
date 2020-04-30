from sys import argv
#  K for king, Q for queen, R for rook, B for bishop, and N for knight
from_place = argv[1]  # a1
to_place = argv[2]
pieceToMove = " "  # default: pawn " "
if len(argv) == 4:
    pieceToMove = argv[3]

# all relative position possible
POSSIBLE_POS = {' ': [(0, 1), (1, 1), (1, -1)],  # pawn
                'N': [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)],
                'K': [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)],
                'R': [],
                'B': [],
                'Q': []}
for i in range(1, 9):
    POSSIBLE_POS['R'] += [(i, 0), (0, i), (0, -i), (-i, 0)]
    POSSIBLE_POS['B'] += [(i, i), (i, -i), (-i, -i), (-i, i)]
POSSIBLE_POS['Q'] = POSSIBLE_POS['B'] + POSSIBLE_POS['R']


def calcFileRank(pos: str) -> [int, int]:
    # FILE = ('', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
    FILE = " abcdefgh"
    return FILE.index(pos[0]), int(pos[1])


def checkValidMove(init_pos: str, final_pos: str, pieceToMove: str) -> bool:

    if final_pos[0] not in 'abcdefgh' or final_pos[1] not in '12345678':
        return False
    curr_file, curr_rank = calcFileRank(init_pos)
    final_file, final_rank = calcFileRank(final_pos)

    for relativePos in POSSIBLE_POS[pieceToMove.upper()]:

        if curr_file + relativePos[0] == final_file and curr_rank + relativePos[1] == final_rank:
            return True
    return False


print("a".index('a'))
# abs(curr_pos[0]- new_pos[0]), (curr_pos[0]- new_pos[0) in  [(1, 2), (2, 1)]
print(checkValidMove(from_place, to_place, pieceToMove))
