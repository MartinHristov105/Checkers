from src.piece import *
import pygame

def test_piece_calc_pos():
    piece = Piece(1, 1, RED, 100)
    piece.calc_pos()
    assert piece.x == 150 and piece.y == 150

def test_piece_move():
    piece = Piece(1, 1, RED, 100)
    piece.move(2, 2)
    assert piece.row == 2 and piece.col == 2