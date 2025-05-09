import heapq
import time
import tracemalloc
import tkinter as tk
from itertools import product
import random
from TESTCASE import test_cases

# === Heuristic and DFS Algorithm === #
def get_hint(line):
    hints = []
    count = 0
    for cell in line:
        if cell == '#':
            count += 1
        elif count > 0:
            hints.append(count)
            count = 0
    if count > 0:
        hints.append(count)
    return hints if hints else [0]
# Heuristic Algorithm
def heuristic(grid, row_hints, col_hints):
    score = 0
    for i in range(len(grid)):
        if get_hint(grid[i]) != row_hints[i]:
            score += 1
    for j in range(len(grid[0])):
        col = [grid[i][j] for i in range(len(grid))]
        if get_hint(col) != col_hints[j]:
            score += 1
    return score

def get_neighbors(grid):
    neighbors = []
    size = len(grid)
    for i in range(size):
        for j in range(size):
            new_grid = [row[:] for row in grid]
            new_grid[i][j] = '#' if new_grid[i][j] == '.' else '.'
            neighbors.append(new_grid)
    return neighbors

def greedy_search(grid, row_hints, col_hints):
    tracemalloc.start()
    start_time = time.time()

    pq = []
    heapq.heappush(pq, (heuristic(grid, row_hints, col_hints), grid))
    visited = set()
    state_list = []
    state_count = 0  

    while pq:
        h, current_grid = heapq.heappop(pq)
        state_count += 1
        state_list.append([row[:] for row in current_grid])

        if heuristic(current_grid, row_hints, col_hints) == 0:
            end_time = time.time() 
            current, peak = tracemalloc.get_traced_memory() 
            tracemalloc.stop()
            print(f"##############################################")
            print(f"Greedy Search - Time: {end_time - start_time:.4f} seconds")
            print(f"Greedy Search - Memory Usage: {current / 10**6:.4f} MB")
            print(f"Greedy Search - State Count: {len(state_list)}")
            return state_list, True

        state_tuple = tuple(tuple(row) for row in current_grid)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        for neighbor in get_neighbors(current_grid):
            new_h = heuristic(neighbor, row_hints, col_hints)
            heapq.heappush(pq, (new_h, neighbor))

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"##############################################")    
    print(f"Greedy Search - Time: {end_time - start_time:.4f} seconds")
    print(f"Greedy Search - Memory Usage: {current / 10**6:.4f} MB")
    print(f"Greedy Search - State Count: {len(state_list)}")
    return state_list, False

# DFS Algorithm
def generate_row(size, hint):
    def valid_row(row):
        return get_hint(row) == hint
    
    return [list(row) for row in product(['.', '#'], repeat=size) if valid_row(row)]

def is_valid(grid, row_hints, col_hints):
    for i in range(len(grid)):
        if get_hint(grid[i]) != row_hints[i]:
            return False
    
    for j in range(len(grid[0])):
        col = [grid[i][j] for i in range(len(grid))]
        if get_hint(col) != col_hints[j]:
            return False
    
    return True

def dfs(grid, row_hints, col_hints, row=0, state_list=[]):
    if row == len(grid):
        if is_valid(grid, row_hints, col_hints) == True:
            return True
        return False
    for row_perm in generate_row(len(grid), row_hints[row]):
        grid[row] = row_perm
        state_list.append([row[:] for row in grid])
        if dfs(grid, row_hints, col_hints, row + 1, state_list):
            return True
    return False

def solve_nonogram_dfs(row_hints, col_hints, size):
    grid = [['.' for _ in range(size)] for _ in range(size)]
    state_list = []

    tracemalloc.start()
    start_time = time.time() 
    
    dfs(grid, row_hints, col_hints, state_list=state_list)
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"##############################################")
    print(f"DFS - Time: {end_time - start_time:.4f} seconds")
    print(f"DFS - Memory Usage: {current / 10**6:.4f} MB")
    print(f"DFS - State Count: {len(state_list)}")
    
    return state_list

# === UI === #
class NonogramApp:
    def __init__(self, root):

        input = random.choice(test_cases)
        size = input[0]
        row_hints = input[1]
        col_hints = input[2]

        self.file = open("output.txt", "w")
        self.input = input
        self.root = root
        self.size = size
        self.row_hints = row_hints
        self.col_hints = col_hints
        self.cell_size = 50
        self.hint_offset = 100
        self.grid = [['.' for _ in range(size)] for _ in range(size)]
        self.state_list = []
        self.current_state_idx = 0

        self.canvas = tk.Canvas(root, width=self.cell_size * (10), height=self.cell_size * (10), bg="gray")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.toggle_cell)

        self.btn_heuristic = tk.Button(root, text="Heuristic", command=self.start_heuristic)
        self.btn_heuristic.pack(side=tk.LEFT, padx=10)

        self.btn_dfs = tk.Button(root, text="DFS", command=self.start_dfs)
        self.btn_dfs.pack(side=tk.LEFT, padx=10)

        self.btn_reset = tk.Button(root, text="Reset", command=self.reset_grid)
        self.btn_reset.pack(side=tk.RIGHT, padx=10)

        self.btn_reset = tk.Button(root, text="New Puzzel", command=self.new_puzzel)
        self.btn_reset.pack(side=tk.RIGHT, padx=10)

        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for i, hints in enumerate(self.row_hints):
            hint_text = "  ".join(map(str, hints))
            self.canvas.create_text(80, self.hint_offset + i * self.cell_size + 25, text=hint_text, font=("Arial", 15), anchor="e")
        for j, hints in enumerate(self.col_hints):
            hint_text = "\n".join(map(str, hints))
            self.canvas.create_text(self.hint_offset + j * self.cell_size + 25, 80, text=hint_text, font=("Arial", 15), anchor="s")
        for i in range(self.size):
            for j in range(self.size):
                color = "black" if self.grid[i][j] == '#' else "white"
                x1 = self.hint_offset + j * self.cell_size
                y1 = self.hint_offset + i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
    
        if self.check_completion():
            self.canvas.create_text(self.hint_offset + self.size * self.cell_size / 2, self.hint_offset + self.size * self.cell_size / 2, 
                                    text="Hoàn thành!", font=("Arial", 20, "bold"), fill="green")


    def toggle_cell(self, event):
        j = (event.x - self.hint_offset) // self.cell_size
        i = (event.y - self.hint_offset) // self.cell_size
        if 0 <= i < self.size and 0 <= j < self.size:
            self.grid[i][j] = '#' if self.grid[i][j] == '.' else '.'
            self.draw_grid()

    def check_completion(self):
        return all(get_hint(self.grid[i]) == self.row_hints[i] for i in range(self.size)) and \
               all(get_hint([self.grid[i][j] for i in range(self.size)]) == self.col_hints[j] for j in range(self.size))
    
    def start_heuristic(self):
        self.state_list, _ = greedy_search(self.grid, self.row_hints, self.col_hints)
        self.animate_states_heuristic()

    def start_dfs(self):
        self.state_list = solve_nonogram_dfs(self.row_hints, self.col_hints, self.size)
        self.animate_states_dfs()

    def animate_states_dfs(self):
        if self.current_state_idx < len(self.state_list):
            self.grid = self.state_list[self.current_state_idx]

            for row in self.state_list[self.current_state_idx]:
                self.file.write(" ".join(row) + "\n")
            self.file.write("\n")

            self.current_state_idx += 1
            self.draw_grid()
            self.root.after(20, self.animate_states_dfs)

    def animate_states_heuristic(self):
        if self.current_state_idx < len(self.state_list):
            self.grid = self.state_list[self.current_state_idx]

            
            for r in self.state_list[self.current_state_idx]:
                self.file.write(" ".join(r) + "\n")
            self.file.write("\n")

            self.current_state_idx += 1
            self.draw_grid()
            self.root.after(100, self.animate_states_heuristic)

    def reset_grid(self):
        self.grid = [['.' for _ in range(self.size)] for _ in range(self.size)]
        self.current_state_idx = 0
        self.draw_grid()

    def new_puzzel(self):
        input = random.choice(test_cases)
        while self.input == input:
            input = random.choice(test_cases)
        self.input = input
        self.size = input[0]
        self.row_hints = input[1]
        self.col_hints = input[2]

        self.grid = [['.' for _ in range(self.size)] for _ in range(self.size)]
        self.current_state_idx = 0
        self.draw_grid()

root = tk.Tk()
root.title("Nonograms")
app = NonogramApp(root)
root.mainloop()
