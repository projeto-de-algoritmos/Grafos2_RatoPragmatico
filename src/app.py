from tkinter import *
from PIL import ImageTk, Image
from box import Box
import board
import pygame
import sys


def show_lose_window(lose):
    root = Tk()
    root.geometry("500x500")
    root.title("Seu rato vai passar fome!")
    image = Image.open(lose)
    photo = ImageTk.PhotoImage(image)
    
    image_label = Label(root, image=photo)
    image_label.pack()
    
    text_label = Label(root, text="Seu rato vai passar fome!")
    text_label.pack()
    
    root.mainloop()
    
    

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
gato = pygame.image.load("assets/gato2.jpg")
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
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:
                if searching:
                    show_lose_window("assets/losegame.jpg")
                    searching = False

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
                    box.draw_square(window, (0, 255, 255),box_width,box_height)

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


main()
