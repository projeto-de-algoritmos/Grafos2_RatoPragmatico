from tkinter import messagebox, Tk
import pygame
import sys

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


class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None

    def draw(self, win, image):    
        win.blit(image, (self.x * box_width, self.y * box_height))
    
    def draw_square(self, win, color):
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width-2, box_height-2))

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


# Create Grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

# Set Neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()

start_box = grid[0][0]
start_box.start = True
start_box.visited = True
queue.append(start_box)


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
                    Tk().wm_withdraw()
                    messagebox.showinfo("Seu rato vai passar fome", "Não há caminho para o queijo")
                    searching = False

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                #Background Color
                box.draw(window, piso)

                if box.queued:
                    #Queue image
                    box.draw(window, interrogacao)

                if box.visited:
                    #Visited Color
                    box.draw_square(window, (0, 150, 0))
                if box in path:
                    #Path Color
                    box.draw_square(window, (0, 255, 255))

                if box.start:
                    #Rat image
                    box.draw(window, rato)
                if box.wall:
                    #Cat Image
                    box.draw(window, gato)
                    #Cheese Image
                if box.target:
                    box.draw(window, queijo)

        pygame.display.flip()


main()
