import pygame
import random

color_names = {
    -1: "blank",
    0: "red",
    1: "blue",
    2: "green",
    #3: "gray",
    4: "apricot",
    5: "pink",
    6: "purple"
}

color_values = [
    (255, 61, 61),   # 0
    (161, 242, 255), # 1
    (150, 255, 156), # 2
    #(189, 189, 189), # 3
    (255, 227, 161), # 4
    (255, 161, 161), # 5
    (164, 102, 255)  # 6
]

class Grid:
    values = []

    size = None
    size_pxl = None
    point_pxl = None
    border_color = None
    border_thickness_pxl = None

    cell_size_pxl = None
    spacing_pxl = None
    cell_colors = None

    total_score = None

    private_total_removed_cells = None

    def __init__(self, size, point_pxl, border_color, border_thickness_pxl, 
                cell_size_pxl, spacing_pxl, cell_colors, random_seed=None):
        if(random_seed):
            random.seed(random_seed)

        grid = []
        width, height = size
        for x in range(width):
            grid.append([])
            for y in range(height):
                random_value = random.randint(0, len(cell_colors)-1)
                grid[x].append(random_value)
        self.values = grid

        self.size = [*size]
        self.point_pxl = [*point_pxl]
        self.border_color = border_color
        self.border_thickness_pxl = border_thickness_pxl

        self.cell_size_pxl = [*cell_size_pxl]
        self.spacing_pxl = [*spacing_pxl]
        self.cell_colors = [*cell_colors]

        width_pxl = self.border_thickness_pxl * 2 \
                + (self.cell_size_pxl[0] + self.spacing_pxl[0]) * self.size[1] \
                - self.spacing_pxl[0]
        height_pxl = self.border_thickness_pxl * 2 \
                + (self.cell_size_pxl[1] + self.spacing_pxl[1]) * self.size[0] \
                - self.spacing_pxl[1]

        self.size_pxl = [width_pxl, height_pxl]

        self.total_score = 0

        self.private_total_removed_cells = 0

    def draw(self, screen):
        rect_border = pygame.Rect(self.point_pxl[0], self.point_pxl[1], 
                                    self.size_pxl[0], self.size_pxl[1])
        pygame.draw.rect(screen, self.border_color, rect_border)

        x_cur = self.border_thickness_pxl + self.point_pxl[0]
        y_cur = self.border_thickness_pxl + self.point_pxl[1]

        for row in self.values:
            x_cur = self.border_thickness_pxl + self.point_pxl[0]
            for cell in row:
                if cell != -1:
                    rect_cell = pygame.Rect(x_cur, y_cur, 
                                            self.cell_size_pxl[0], self.cell_size_pxl[1])
                    pygame.draw.rect(screen, self.cell_colors[cell], rect_cell)
                else:
                    pass

                #go to next cell's location
                x_cur += self.spacing_pxl[0] + self.cell_size_pxl[0]
            
            #go to next row
            y_cur += self.spacing_pxl[1] + self.cell_size_pxl[1]

    def remove_at(self, point):
        x, y = point

        if(self.values[x][y] == -1):
            return
        else:
            root_color = self.values[x][y]
            total_changed_cells = 1
            self.values[x][y] = -2

            ories = [[0, 1], [1, 0], [0, -1], [-1, 0]]
            # keep track
            last_moves = []

            while 1:
                moved = False
                # searching for the next movable cell
                for orie in ories:
                    if (0 <= x+orie[0] < self.size[0]) and (0 <= y+orie[1] < self.size[1]):
                        next_cell_value = self.values[x+orie[0]][y+orie[1]]

                        if (next_cell_value == root_color):
                            moved = True
                            x += orie[0]
                            y += orie[1]
                            last_moves.append(orie)
                            total_changed_cells += 1
                            self.values[x][y] = -2
                            break
                        elif (next_cell_value == -1):
                            moved = True
                            x += orie[0]
                            y += orie[1]
                            last_moves.append(orie)
                            self.values[x][y] = -2
                            break
                
                #if it moved
                if (moved):
                    continue
                #if it turn back the root and cant move
                elif (len(last_moves) == 0):
                    break
                # if cant move, it comes back the latest cell
                else:
                    self.values[x][y] = -2
                    latest_move = last_moves.pop()
                    x -= latest_move[0]
                    y -= latest_move[1]

        # reset all marked cells
        for x, row in enumerate(self.values):
            for y, cell in enumerate(row):
                if(self.values[x][y] == -2):
                    self.values[x][y] = -1

        self.private_total_removed_cells += total_changed_cells
        
        return total_changed_cells

    def reset_seed(self, random_seed):
        if(random_seed):
            random.seed(random_seed)

        grid = []
        width, height = self.size
        for x in range(width):
            grid.append([])
            for y in range(height):
                random_value = random.randint(0, len(self.cell_colors)-1)
                grid[x].append(random_value)

        self.values = grid

        self.total_score = 0

    def is_empty(self):
        return self.private_total_removed_cells >= (self.size[0] * self.size[1])

    def print_grid(self):
        for row in self.values:
            for cell in row:
                print(cell, end=' ')
            print()   

    def on_mouse_button_down(self, event):
        point_pxl = event.pos
        point = self.private_screen_point_to_cell_point(point_pxl)
        print(point)
        if(point):
            x, y = point
        else:
            return 0

        if(self.values[x][y] != -1):
            removed_cells_number = self.remove_at(point)

            self.total_score += self.private_get_scroce_from(removed_cells_number)
        else:
            return 0

    def private_screen_point_to_cell_point(self, point):
        x_mouse, y_mouse= point
        x, y = None, None

        x_mouse -= self.point_pxl[0] + self.border_thickness_pxl
        y = x_mouse // (self.cell_size_pxl[0] + self.spacing_pxl[0])
        x_mod = x_mouse % (self.cell_size_pxl[0] + self.spacing_pxl[0])

        if (x_mod >= self.cell_size_pxl[0]) or (not 0 <= y < self.size[1]):
            return None
        
        y_mouse -= self.point_pxl[1] + self.border_thickness_pxl
        x = y_mouse // (self.cell_size_pxl[1] + self.spacing_pxl[1])
        y_mod = y_mouse % (self.cell_size_pxl[1] + self.spacing_pxl[1])

        if (y_mod >= self.cell_size_pxl[1]) or (not 0 <= x < self.size[0]):
            return None

        return [x, y]

    def private_get_scroce_from(self, removed_cells_number):
        return int(removed_cells_number**1.5)


if __name__ == "__main__":
    my_grid = Grid(size=(32, 32), point_pxl=(5, 5), 
                border_color=(100, 100, 100), border_thickness_pxl=5, 
                cell_size_pxl=(16, 16), spacing_pxl=(0, 0),
                cell_colors=color_values, random_seed=180603)

    # print(my_grid.size)
    # print(my_grid.size_pxl)
    # print(my_grid.point_pxl)
    # print(my_grid.border_color)
    # print(my_grid.border_thickness_pxl)

    # print(my_grid.cell_size_pxl)
    # print(my_grid.spacing_pxl)
    # print(my_grid.cell_colors)