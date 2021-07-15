#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import numpy as np
import os
import chess

import pathlib


ROOT = pathlib.Path(__file__).resolve().parent
PIECES_DIR = os.path.join(ROOT, "pieces")


def get_chessboard_pattern(nb_squares=8):
    """Generate a 2d array nb_squares* nb_squares
    with zeros and ones representing a chessboard.
    The pattern is the one of the standard chessboard.

    Args:
        nb_squares (int): nb of squares per side.
            Defaults to 8

    Returns:
        np.ndarray: binary representation of the chessboard.
            Ones denote the dark squares.
            Zeros denote the light squares.
    """
    x = np.zeros((nb_squares, nb_squares), dtype=int)
    x[1::2, ::2] = 1
    x[::2, 1::2] = 1
    return x


def fen_to_array(fen):
    """Transform a FEN representation to a two
    dimensional numpy array representing the chess
    board with the pieces positions as strings.

    Args:
        fen (str): fen representation of a chessboard

    Returns:
        np.ndarray: 2d representation of array and pieces
    """
    ascii_fen = chess.Board(fen).__str__()
    ascii_fen = ascii_fen.split("\n")
    array_fen = np.array([row.split(" ") for row in ascii_fen])
    return array_fen


def create_empty_board(board_size=480, nb_squares=8,
                       light_color=(255, 253, 208), dark_color=(76, 153, 0)):
    """Generate PIL image of a chessboard.

    Args:
        board_size (int): image width and height (in pixels). Should be
            divisible by nb_squares. Defaults to 480.
        nb_squares (int, optional): nb of squares per side. Defaults to 8.
        light_color (tuple, optional): RGB color for light squares.
            Defaults to (255, 253, 208).
        dark_color (tuple, optional): RGB color for dark squares.
            Defaults to (76, 153, 0).

    Raises:
        ValueError: if the board_size is not divisible by nb_squares

    Returns:
        PIL.Image: empty chessboard image
    """
    if board_size % nb_squares != 0:
        raise ValueError(
            f"Board size must be divisible by {nb_squares}. Got {board_size}.")
    board = Image.new('RGB', (board_size, board_size), light_color)
    square_size = int(board_size/nb_squares)
    dark_square = Image.new('RGB', (square_size, square_size), dark_color)

    chessboard_pattern = get_chessboard_pattern(nb_squares)
    for i in range(nb_squares):
        for j in range(nb_squares):
            is_dark = chessboard_pattern[i][j]
            if is_dark:
                top_left = [j * square_size, i * square_size]
                bottom_right = [(j+1) * square_size, (i+1) * square_size]
                board.paste(dark_square, box=(*top_left, *bottom_right))
    return board


def load_pieces_images(dir_path, extension="png"):
    """Load all chess pieces images in a dict.
    The pieces names are:
    ["B", "K", "N", "P", "Q", "R"] for
    [bishop, king, knight, pawn, queen, rook]

    For the white pieces names are uppercase. For the
    black pieces names are lowercase.

    Pieces should be organized as follows in the directory
    dir_path:

    <dir_path>
        |
        |--- white
        |        |
        |        |- "B.<extension>"
        |        |- "K.<extension>"
        |        |- ...
        |        |_ "R.<extension>"
        |
        |____ black
                |
                |- "b.<extension>"
                |- "k.<extension>"
                |- ...
                |_ "r.<extension>"

    Args:
        dir_path (str): directory where pieces images are saved
        extension (str, optional): image files extensions. Defaults to "png".

    Returns:
        dict: mapping of piece name to PIL.Image of the piece
    """
    white_pieces = ["B", "K", "N", "P", "Q", "R"]
    black_pieces = [name.lower() for name in white_pieces]

    pieces_names = white_pieces + black_pieces

    pieces = {}
    for piece in pieces_names:
        color = "black"
        if piece.isupper():
            color = "white"
        piece_file_path = os.path.join(
            dir_path, color,
            f"{piece.lower()}.{extension}"
        )
        piece_img = Image.open(piece_file_path)
        piece_img = piece_img.convert('RGBA')
        pieces[piece] = piece_img
    return pieces


def draw_pieces(board_img, pieces, board_array, nb_squares=8):
    """Draw pieces on an empty chessboard.

    Args:
        board_img (PIL.Image): empty chessboard image
        pieces (dict): mapping of piece name to PIL.Image of the piece.
            Images must have transparency as background.
        board_array (np.ndarray): 2d representation of array and pieces
        nb_squares (int, optional): nb of squares on a side of the chessboard.
            Defaults to 8.

    Raises:
        ValueError: if the board_size is not divisible by nb_squares

    Returns:
        PIL.Image: chess board with pieces placed as specified in
            board_array
    """
    board_size = board_img.size[0]
    if board_size % nb_squares != 0:
        raise ValueError(
            f"Board size must be divisible by {nb_squares}. Got {board_size}.")
    square_size = int(board_size/nb_squares)
    for i in range(len(board_array)):
        for j in range(len(board_array)):
            piece = board_array[i, j]
            if piece != ".":
                piece_img = pieces[piece]
                top_left = (j * square_size, i * square_size)
                board_img.paste(piece_img, box=top_left, mask=piece_img)
    return board_img


def transform_fen_pil(fen, board_size=480, light_color=(255, 253, 208),
                      dark_color=(76, 153, 0), pieces_ext="png",
                      pieces_path=PIECES_DIR):
    """Convert a FEN representation to a PIL image.

    Args:
        fen (str): Forsyth–Edwards Notation of chessboard position i.e:
            "r1b1kb1r/pp2pppp/1qn2n2/3p4/3P1B2/1N3N2/PPP2PPP/R2QKB1R"
        board_size (int): image width and height (in pixels). Should be
            divisible by nb_squares. Defaults to 480.
        light_color (tuple, optional): RGB color for light squares.
            Defaults to (255, 253, 208).
        dark_color (tuple, optional): RGB color for dark squares.
            Defaults to (76, 153, 0).
        pieces_ext (str, optional): file extension of chess piece images.
            Defaults to "png".
        pieces_path (str, optional): path where chess piece images are saved.
            Default images are provided. To use yours, provide the path to a
            directory structured as follows:
            <pieces_path>
                |
                |--- white
                |        |
                |        |- "b.<extension>"
                |        |- "k.<extension>"
                |        |- ...
                |        |_ "r.<extension>"
                |
                |____ black
                        |
                        |- "b.<extension>"
                        |- "k.<extension>"
                        |- ...
                        |_ "r.<extension>"

            Defaults to PIECES_DIR.

    Returns:
        PIL.Image: image representation of input fen
    """

    board = create_empty_board(
        board_size=board_size,
        nb_squares=8,
        light_color=light_color,
        dark_color=dark_color
    )
    pieces = load_pieces_images(
        pieces_path, extension=pieces_ext)
    board_array = fen_to_array(fen)
    board = draw_pieces(board, pieces, board_array)
    return board
