class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def plant(self, x, y, plant):
        if self.grid[y][x] is None:
            self.grid[y][x] = Cell(plant)
            return True
        else:
            return False

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        else:
            return None  #Handle out of bounds

    def display(self):
        print("  " + " ".join(str(i) for i in range(self.width)))
        for i, row in enumerate(self.grid):
            row_str = f"{i} "
            for cell in row:
                if cell is None:
                    row_str += ". "
                else:
                    row_str += cell.plant.symbol + " "
            print(row_str)

    def tick(self, season):
        for row in self.grid:
            for cell in row:
                if cell and cell.plant:
                    cell.plant.grow(season)

class Cell:
    def __init__(self, plant=None):
        self.plant = plant