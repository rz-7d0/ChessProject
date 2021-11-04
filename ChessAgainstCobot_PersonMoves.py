import rtde_control
import rtde_io
import rtde_receive
import chess.engine
import chess
from functions import *


# constants
IP = "10.202.237.200"
FIELD_WIDTH_X = 0.054  # in mm
FIELD_WIDTH_Y = 0.0542  # in mm
KING_SIZE = 98/1000  # needs to be adjusted
ORIGIN = [0.373, -0.425, 0.06775, 2.835, -1.223, 0.005]  # needs to be adjusted
SUBSTITUTE_BOX_WHITE = [0.251, -0.271, 0.165, ORIGIN[3], ORIGIN[4], ORIGIN[5]]
SUBSTITUTE_BOX_BLACK = [0.251, -0.166, 0.165, ORIGIN[3], ORIGIN[4], ORIGIN[5]]

skill_level = int(input("Auf welcher Schwierigkeitsstufe möchtest du spielen? (Im Bereich [0, 20], wobei 20\n"
                    "das höchste Rating ist.)\n"
                    "Schwierigkeitsstufe: "))

chess_engine = r"C:\Users\uie48291\Downloads\stockfish_14.1_win_x64_popcnt\stockfish_14.1_win_x64_popcnt.exe"


# origin is at the bottom left corner of the A1 square

# INITIALIZATION OF COBOT AND BOARD
rtde_c = rtde_control.RTDEControlInterface(IP)
rtde_io_ = rtde_io.RTDEIOInterface(IP)
rtde_r = rtde_receive.RTDEReceiveInterface(IP)
board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(chess_engine)
engine.configure({"Skill Level": skill_level})


moves, capture, en_passant, promotion, kingside_castle, queenside_castle, i, zug_uci = [], [], [], [], [], [], 0, ""

color_input = input("Willst du weiß oder schwarz sein?\n").lower()

if color_input == "weiß":
    color = True
else:
    color = False

while not board.is_game_over():

    if i == 0:
        print("Das akzeptierte Format ist die Bewegung der Figur vom Startfeld \n"
              "zum Endfeld des Zuges (Beispiel: e2e4). Wenn das Spiel vorbei ist gebe Game Over \n"
              "zum Stoppen des Programms ein.\n")

    if board.turn == color:
        zug_uci = input("Zug: ").lower()

        if zug_uci == "game over":
            break
        else:
            move = chess.Move.from_uci(zug_uci)

    else:
        result = engine.play(board, chess.engine.Limit(time=1))
        move = result.move
        zug_uci = board.uci(result.move)
        print(zug_uci)

        if not color:
            substitute_box = SUBSTITUTE_BOX_BLACK
        else:
            substitute_box = SUBSTITUTE_BOX_WHITE

        if board.is_en_passant(move):
            en_passant_move(rtde_c, rtde_r, rtde_io_, KING_SIZE, ORIGIN, zug_uci[:2],
                            zug_uci[2:], white=not color,
                            substitute_box=substitute_box)
        elif board.is_capture(move):
            capture_piece(rtde_c, rtde_r, rtde_io_, KING_SIZE, ORIGIN, zug_uci[:2],
                          zug_uci[2:], substitute_box=substitute_box)
        elif board.is_kingside_castling(move):
            kingside_castling_move(rtde_c, rtde_r, rtde_io_, KING_SIZE, ORIGIN, white=not color)
        elif board.is_queenside_castling(move):
            queenside_castling_move(rtde_c, rtde_r, rtde_io_, KING_SIZE, ORIGIN, white=not color)
        elif move.promotion is not None:
            promoting_move(rtde_c, rtde_r, rtde_io_, KING_SIZE, ORIGIN, zug_uci[:2],
                           zug_uci[2:])
        else:
            move_piece(rtde_c, rtde_r, rtde_io_, KING_SIZE, ORIGIN, zug_uci[:2],
                       zug_uci[2:])
        rtde_c.moveL(SUBSTITUTE_BOX_WHITE, 1, 0.3)

    capture.append(board.is_capture(move))
    moves.append(move)
    en_passant.append(board.is_en_passant(move))
    kingside_castle.append(board.is_kingside_castling(move))
    queenside_castle.append(board.is_queenside_castling(move))

    if str(move.promotion) == "None":
        promotion.append([False, move.promotion])
    else:
        promotion.append([True, move.promotion])

    board.push(move)

    i += 1

print(board)
print(capture)

