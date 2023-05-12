from box import Box

def create_grid(columns, rows,grid):
    for i in range(columns):
        arr = []
        for j in range(rows):
            arr.append(Box(i, j))
        grid.append(arr)
    
def set_neighbours(columns, rows, grid):
    for i in range(columns):
        for j in range(rows):
            grid[i][j].set_neighbours(columns, rows, grid)

def board_setup(grid,queue):
    start_box = grid[0][0]
    start_box.start = True
    start_box.visited = True
    queue.append(start_box)
    
    return start_box