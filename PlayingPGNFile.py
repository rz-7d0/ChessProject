import rtde_control
import rtde_io
import rtde_receive
from functions import *

# constants
IP = "10.202.237.200"
FIELD_WIDTH_X = 0.054  # in mm
FIELD_WIDTH_Y = 0.0542  # in mm
KING_SIZE = 98/1000  # needs to be adjusted
ORIGIN = [0.373, -0.425, 0.06775, 2.835, -1.223, 0.005]  # needs to be adjusted
SUBSTITUTE_BOX_WHITE = [0.251, -0.271, 0.165, ORIGIN[3], ORIGIN[4], ORIGIN[5]]
SUBSTITUTE_BOX_BLACK = [0.251, -0.166, 0.165, ORIGIN[3], ORIGIN[4], ORIGIN[5]]
chess_pgn = "Jahrhunderpartie.pgn"
# "hallo.pgn", "Fischer_spassky.pgn", "test2.pgn", "Jahrhundertpartie.pgn", "A02.pgn"

# origin is at the bottom left corner of the A1 square

rtde_c = rtde_control.RTDEControlInterface(IP)
rtde_io_ = rtde_io.RTDEIOInterface(IP)
rtde_r = rtde_receive.RTDEReceiveInterface(IP)

for i in range(len(read_chess_game_uci(chess_pgn))):
    if is_white_colored_piece(chess_pgn)[i]:
        substitute_box = SUBSTITUTE_BOX_BLACK
    else:
        substitute_box = SUBSTITUTE_BOX_WHITE

    if is_en_passant_move(chess_pgn)[i]:
        en_passant_move(rtde_c, rtde_r, rtde_io_, KING_SIZE, ORIGIN, read_chess_game_uci(chess_pgn)[i][:2],
                        read_chess_game_uci(chess_pgn)[i][2:], white=is_white_colored_piece(chess_pgn)[i],
                        substitute_box=substitute_box)
    elif is_capturing_move(chess_pgn)[i]:
        capture_piece(rtde_c, rtde_r, rtde_io_, KING_SIZE, ORIGIN, read_chess_game_uci(chess_pgn)[i][:2],
                      read_chess_game_uci(chess_pgn)[i][2:], substitute_box=substitute_box)
    elif is_kingside_castling_move(chess_pgn)[i]:
        kingside_castling_move(rtde_c, rtde_r, rtde_io_, KING_SIZE, ORIGIN, white=is_white_colored_piece(chess_pgn)[i])
    elif is_queenside_castling_move(chess_pgn)[i]:
        queenside_castling_move(rtde_c, rtde_r, rtde_io_, KING_SIZE, ORIGIN, white=is_white_colored_piece(chess_pgn)[i])
    elif is_promotion_move(chess_pgn)[i][0]:
        promoting_move(rtde_c, rtde_r, rtde_io_, KING_SIZE, ORIGIN, read_chess_game_uci(chess_pgn)[i][:2],
                       read_chess_game_uci(chess_pgn)[i][2:])
    else:
        move_piece(rtde_c, rtde_r, rtde_io_, KING_SIZE, ORIGIN, read_chess_game_uci(chess_pgn)[i][:2],
                   read_chess_game_uci(chess_pgn)[i][2:])
