import pygame
import random
import tkinter as tk
from tkinter import filedialog
from pygame.locals import *

def split_and_shuffle_image(image, rows, cols):
    piece_width = image.get_width() // cols
    piece_height = image.get_height() // rows
    pieces = []

    for row in range(rows):
        for col in range(cols):
            piece_rect = pygame.Rect(col * piece_width, row * piece_height, piece_width, piece_height)
            piece = image.subsurface(piece_rect).copy()
            pieces.append((piece, piece_rect))

    # Shuffle the positions of the pieces
    random_positions = [(x * piece_width, y * piece_height) for x in range(cols) for y in range(rows)]
    random.shuffle(random_positions)

    for i, piece in enumerate(pieces):
        piece[1].topleft = random_positions[i]

    return pieces

def main():
    pygame.init()

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return

    screen_width, screen_height = 800, 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('퍼즐 게임')

    image = pygame.image.load(file_path).convert()
    rows, cols = 3, 3
    pieces = split_and_shuffle_image(image, rows, cols)

    running = True
    selected_piece = None
    offset_x, offset_y = 0, 0

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                for piece, rect in pieces:
                    if rect.collidepoint(event.pos):
                        selected_piece = piece, rect
                        offset_x = rect.x - event.pos[0]
                        offset_y = rect.y - event.pos[1]
                        break
            elif event.type == MOUSEBUTTONUP:
                selected_piece = None
            elif event.type == MOUSEMOTION and selected_piece:
                piece, rect = selected_piece
                rect.x = event.pos[0] + offset_x
                rect.y = event.pos[1] + offset_y

        screen.fill((255, 255, 255))
        for piece, rect in pieces:
            screen.blit(piece, rect.topleft)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
