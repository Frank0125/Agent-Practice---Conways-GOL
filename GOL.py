import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Genera el grid de size dims, y de forma aleatoria pone cuales 
# celdas estan vivas o no al inicio
def create_grid(dims, alive_probability=0.2, seed=None):
    if seed:
        np.random.seed(seed)
    return np.random.choice([False, True], size=dims, p=[1 - alive_probability, alive_probability])

# Contador de los vecinos vivos dentro del area alrededor de la celda
def count_alive_neighbors(grid, x, y):
    neighborhood = grid[max(0, x-1):x+2, max(0, y-1):y+2]
    alive_neighbors = np.sum(neighborhood) - grid[x, y]
    return alive_neighbors

def step(grid):
    new_grid = grid.copy()
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            alive_neighbors = count_alive_neighbors(grid, x, y)
            if grid[x, y] and rules[0] <= alive_neighbors <= rules[3]: 
               new_grid[x, y] = True
            elif not grid[x, y] and rules[2] <= alive_neighbors <= rules[3]:
                new_grid[x, y] = True
            else:
                new_grid[x,y] = False
    return new_grid

# Actualiza la ventana con las nuevas posiciones de las celdas
def update(img, grid, rules):
    new_grid = step(grid, rules)
    img.set_data(new_grid)
    grid[:] = new_grid[:] 
    return [img]

# Variables de inicio
rules = (3, 10, 1, 6) # (D, S, R, O)
dims = (50, 50)
alive_probability = 0.2
seed = 313

grid = create_grid(dims, alive_probability, seed)

fig, ax = plt.subplots()
img = ax.imshow(grid, cmap='gray', interpolation='nearest')

ani = animation.FuncAnimation(fig, update, fargs=(img, grid, rules), frames=60, interval=100, save_count=50)

plt.show()
