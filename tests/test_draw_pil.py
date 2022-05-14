import pytest
import numpy as np
from PIL import Image

from fen2pil import draw


def test_get_chessboard_pattern():
    pattern = draw.get_chessboard_pattern(
        nb_squares=8
    )
    expected_pattern = np.array([
        [
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0]
        ]
    ])
    assert (pattern == expected_pattern).all()


def test_fen_to_array():
    fen = "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQ1RK1 w Qkq - 0 1"
    pos_array = draw.fen_to_array(fen)

    expected = np.array([
        ['r', '.', 'b', 'q', 'k', 'b', '.', 'r'],
        ['p', 'p', 'p', 'p', '.', 'p', 'p', 'p'],
        ['.', '.', 'n', '.', '.', 'n', '.', '.'],
        ['.', '.', '.', '.', 'p', '.', '.', '.'],
        ['.', '.', 'B', '.', 'P', '.', '.', '.'],
        ['.', '.', '.', 'P', '.', 'N', '.', '.'],
        ['P', 'P', 'P', '.', '.', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', '.', 'R', 'K', '.']
    ])
    assert (pos_array == expected).all()


def test_create_empty_board():
    board = draw.create_empty_board(
        board_size=8,
        nb_squares=4,
        light_color=(255, 255, 255),
        dark_color=(0, 0, 0)
    )
    board = np.array(board)

    # white cells
    assert (board[:2, :2] == [255, 255, 255]).all()
    assert (board[4:6, :2] == [255, 255, 255]).all()
    assert (board[2:4, 2:4] == [255, 255, 255]).all()
    assert (board[2:4, 6:8] == [255, 255, 255]).all()
    assert (board[6:8, 2:4] == [255, 255, 255]).all()
    assert (board[6:8, 6:8] == [255, 255, 255]).all()
    assert (board[:2, 4:6] == [255, 255, 255]).all()
    assert (board[4:6, 4:6] == [255, 255, 255]).all()

    # all the rest is black
    assert np.sum(board) == 32*255


def test_create_empty_board(tmp_path):
    pieces = draw.load_pieces_images(
        dir_path=draw.PIECES_DIR
    )
    pieces_names = {
        "B", "K", "N", "P", "Q", "R",
        "b", "k", "n", "p", "q", "r"}

    assert pieces_names.difference(set(pieces.keys())) == set()


def test_draw_pieces():
    board = np.zeros((8, 8, 3), dtype=np.uint8)

    board[:2, :2] = [255, 255, 255]
    board[4:6, :2] = [255, 255, 255]
    board[2:4, 2:4] = [255, 255, 255]
    board[2:4, 6:8] = [255, 255, 255]
    board[6:8, 2:4] = [255, 255, 255]
    board[6:8, 6:8] = [255, 255, 255]
    board[:2, 4:6] = [255, 255, 255]
    board[4:6, 4:6] = [255, 255, 255]

    black_rook = np.zeros((2, 2, 3), dtype=np.uint8)
    black_rook[:] = [0, 255, 0]

    white_king = np.zeros((2, 2, 3), dtype=np.uint8)
    white_king[:] = [255, 0, 0]

    black_pawn = np.zeros((2, 2, 3), dtype=np.uint8)
    black_pawn[:] = [0, 0, 255]

    white_pawn = np.zeros((2, 2, 3), dtype=np.uint8)
    white_pawn[:] = [255, 0, 255]

    pieces = {}

    pieces["r"] = black_rook
    pieces["K"] = white_king
    pieces["p"] = black_pawn
    pieces["P"] = white_pawn

    pieces = {
        k: Image.fromarray(
            v).convert('RGBA')
        for k, v in pieces.items()
    }

    board_array = np.array(
        [
            ["r", ".", ".", "."],
            [".", "p", ".", "p"],
            ["P", ".", ".", "."],
            [".", ".", "K", "."]
        ]
    )

    board_img = Image.fromarray(board)

    img_pieces = draw.draw_pieces(
        board_img=board_img,
        pieces=pieces,
        board_array=board_array,
        nb_squares=4
    )

    img_pieces = img_pieces.convert("RGB")
    img_pieces = np.array(img_pieces)

    assert (img_pieces[:2, :2] == black_rook).all()
    assert (img_pieces[4:6, :2] == white_pawn).all()
    assert (img_pieces[2:4, 2:4] == black_pawn).all()
    assert (img_pieces[2:4, 6:8] == black_pawn).all()
    assert (img_pieces[6:8, 4:6] == white_king).all()


def test_draw_pieces_black_perspective():
    board = np.zeros((8, 8, 3), dtype=np.uint8)

    board[:2, :2] = [255, 255, 255]
    board[4:6, :2] = [255, 255, 255]
    board[2:4, 2:4] = [255, 255, 255]
    board[2:4, 6:8] = [255, 255, 255]
    board[6:8, 2:4] = [255, 255, 255]
    board[6:8, 6:8] = [255, 255, 255]
    board[:2, 4:6] = [255, 255, 255]
    board[4:6, 4:6] = [255, 255, 255]

    black_rook = np.zeros((2, 2, 3), dtype=np.uint8)
    black_rook[:] = [0, 255, 0]

    white_king = np.zeros((2, 2, 3), dtype=np.uint8)
    white_king[:] = [255, 0, 0]

    black_pawn = np.zeros((2, 2, 3), dtype=np.uint8)
    black_pawn[:] = [0, 0, 255]

    white_pawn = np.zeros((2, 2, 3), dtype=np.uint8)
    white_pawn[:] = [255, 0, 255]

    pieces = {}

    pieces["r"] = black_rook
    pieces["K"] = white_king
    pieces["p"] = black_pawn
    pieces["P"] = white_pawn

    pieces = {
        k: Image.fromarray(
            v).convert('RGBA')
        for k, v in pieces.items()
    }

    board_array = np.array(
        [
            # ["r", ".", ".", "."],
            # [".", "p", ".", "p"],
            # ["P", ".", ".", "."],
            # [".", ".", "K", "."]
            [".", "K", ".", "."],
            [".", ".", ".", "P"],
            ["p", ".", "p", "."],
            [".", ".", ".", "r"]
        ]
    )

    board_img = Image.fromarray(board)

    img_pieces = draw.draw_pieces(
        board_img=board_img,
        pieces=pieces,
        board_array=board_array,
        nb_squares=4,
        perspective=1
    )

    img_pieces = img_pieces.convert("RGB")
    img_pieces = np.array(img_pieces)

    assert (img_pieces[:2, :2] == black_rook).all()
    assert (img_pieces[4:6, :2] == white_pawn).all()
    assert (img_pieces[2:4, 2:4] == black_pawn).all()
    assert (img_pieces[2:4, 6:8] == black_pawn).all()
    assert (img_pieces[6:8, 4:6] == white_king).all()


def test_transform_fen_pil():
    fen = "r1b1kb1r/pp2pppp/1qn2n2/3p4/3P1B2/1N3N2/PPP2PPP/R2QKB1R"

    img = draw.transform_fen_pil(
        fen,
        board_size=480)

    assert img.size == (480, 480)
