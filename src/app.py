from tkinter import *
from PIL import ImageTk, Image
from box import Box
import board
import pygame
import sys
import minorpath
from pygame import mixer


    
    

window_width = 900
window_height = 900

window = pygame.display.set_mode((window_width, window_height))

columns =  36
rows = 36

box_width = window_width // columns
box_height = window_height // rows

rato = pygame.image.load("assets/rato3.png")
queijo = pygame.image.load("assets/queijo2.png")
piso = pygame.image.load("assets/piso2.png")
gato = pygame.image.load("assets/gato2.png")
interrogacao = pygame.image.load("assets/interrogacao.png")


grid = []
queue = []
path = []


board.create_grid(columns, rows,grid)
board.set_neighbours(columns, rows, grid)
start_box = board.board_setup(grid,queue)


def main():
    begin_search = False
    target_box_set = False
    searching = True
    target_box = None

    mixer.init()
    mixer.music.load('assets/music.mp3')
    mixer.music.set_volume(0.1)
    mixer.music.play(-1)
    while True:
        
        for event in pygame.event.get():
            # Quit Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mouse Controls
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # Draw Wall
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True
                # Set Target
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3 and not target_box_set:
                    i = x // box_width
                    j = y // box_height
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True
            # Start Algorithm
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True

        if begin_search:
            searching= minorpath.dijikstra(queue,start_box, target_box, searching, path)
    
        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                #Background Color
                box.draw(window, piso,box_width,box_height)

                if box.queued:
                    #Queue image
                    box.draw(window, interrogacao,box_width,box_height)

                if box.visited:
                    #Visited Color
                    box.draw_square(window, (0, 150, 0),box_width,box_height)
                if box in path:
                    #Path Color
                    box.draw_square(window, (255, 255, 0),box_width,box_height)
                if box.start:
                    #Rat image
                    box.draw(window, rato,box_width,box_height)
                if box.wall:
                    #Cat Image
                    box.draw(window, gato,box_width,box_height)
                    #Cheese Image
                if box.target:
                    box.draw(window, queijo,box_width,box_height)
        
        pygame.display.flip()

        if path != []: 
            minorpath.show_win_window("assets/wingame.png")
            break
    
    


main()

         