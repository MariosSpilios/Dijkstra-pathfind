# coding=utf-8

from tkinter import *
import tkinter as tk
# import math
# import sys
import random
import os
# import time
import heapq

WINDOW_WIDTH: int = 1160
WINDOW_HEIGHT: int = 920
WHITE = "lightblue"
BLACK = "black"
RED = "red"
GREEN = "green"
PURPLE = "purple"

main_window = Tk()

def on_closing(*args) -> None:
    main_window.destroy()

main_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
main_window.geometry("+100+50")
main_window.resizable(False, False)
main_window.protocol("WM_DELETE_WINDOW", on_closing)
main_window.title("PATHFIND WITH DIJKSTRA")
main_window.__setitem__("bg", BLACK)


def generate_random_rgb_color():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    hex_color = "#{:02x}{:02x}{:02x}".format(red, green, blue)

    return hex_color

class Cube:

    cubes: int = 0
    dx: int = 0
    dy: int = 0
    grid_x: int = 0
    grid_y: int = 0
    point: int = 0
    start_point: int = 0
    start_point_grid_pos: tuple[int, int] = (0, 0)
    cube_width: int = 20

    def __init__(self, master=main_window) -> None:

        self.id: int = Cube.cubes + 1
        Cube.cubes += 1

        self.cube = Frame(master=master, width=Cube.cube_width, height=Cube.cube_width, background=random.choice([WHITE, WHITE, BLACK]))
        self.cube.place(x=Cube.dx, y=Cube.dy)

        self.grid_pos: tuple[int, int] = (Cube.grid_y, Cube.grid_x)

        Cube.dx += Cube.cube_width
        Cube.grid_x += 1
        if (Cube.dx >= WINDOW_WIDTH):
            Cube.dy += Cube.cube_width
            Cube.grid_y += 1
            Cube.dx = 0
            Cube.grid_x = 0

    def pos_info(self, *args) -> tuple[int, int]:
        return (int(self.cube.place_info()['x']), int(self.cube.place_info()['y']))


    def change_color(self, color: str, *args) -> None:
        self.cube.__setitem__("background", color)


    def set_destination_point(self, *args) -> None:
        if Cube.point != 0:
            for cube in cubes:
                if cube.id == Cube.point:
                    cube.change_color(WHITE)

        Cube.point = self.id
        self.cube.__setitem__("background", RED)

    def set_start_point(self, *args) -> None:
        if Cube.start_point != 0:
            for cube in cubes:
                if cube.id == Cube.start_point:
                    cube.change_color(WHITE)

        Cube.start_point = self.id
        Cube.start_point_grid_pos = self.grid_pos
        self.cube.__setitem__("background", GREEN)


    def get_color(self, *args) -> str:
        return self.cube.__getitem__("background")
    
    def kill_yourself(self, *args) -> None:
        self.cube.destroy()

cubes: list[Cube] = [Cube() for i in range((WINDOW_WIDTH // Cube.cube_width) * (WINDOW_HEIGHT // Cube.cube_width))]

def draw_wall(event) -> None:
    for cube in cubes:
        cube_pos: tuple[int, int] = cube.pos_info()

        if ((cube_pos[0] < event.x) and cube_pos[0] + Cube.cube_width > event.x) and ((cube_pos[1] < event.y) and cube_pos[1] + Cube.cube_width > event.y):
            
            cube.change_color(BLACK)
            break

def generate_random_pattern(*args) -> None:
    clear_wall()

    for cube in cubes:
        cube.change_color(random.choice([WHITE, WHITE, BLACK]))

def clear_wall(*args) -> None:
    for cube in cubes:
        cube.change_color(WHITE)
        Cube.point = 0
        Cube.start_point = 0
        Cube.start_point_grid_pos = (0, 0)

def set_end_point(event) -> None:
    for cube in cubes:
        cube_pos: tuple[int, int] = cube.pos_info()
        
        if ((cube_pos[0] < event.x) and cube_pos[0] + Cube.cube_width > event.x) and ((cube_pos[1] < event.y) and cube_pos[1] + Cube.cube_width > event.y):
            cube.set_destination_point()
            break

def set_start_point(event) -> None:
    for cube in cubes:
        cube_pos: tuple[int, int] = cube.pos_info()

        if ((cube_pos[0] < event.x) and cube_pos[0] + Cube.cube_width > event.x) and ((cube_pos[1] < event.y) and cube_pos[1] + Cube.cube_width > event.y):
            cube.set_start_point()
            break

grid: list[list] = []

def create_logic_grid(*args) -> None:
    os.system("cls")
    grid.clear()
    new_line: list[int] = []
    total_lines: int = 1

    for cube in cubes:
        if cube.id == total_lines * WINDOW_WIDTH // Cube.cube_width:
            if cube.get_color() == BLACK:
                new_line.append(1)
            elif cube.get_color() == WHITE:
                new_line.append(0)
            elif cube.get_color() == RED:
                new_line.append(2)
            elif cube.get_color() == GREEN:
                new_line.append(3)
            elif cube.get_color() == PURPLE:
                new_line.append(0)
            grid.append(new_line[:])
            new_line.clear()
            total_lines += 1
        else:
            if cube.get_color() == BLACK:
                new_line.append(1)
            elif cube.get_color() == WHITE:
                new_line.append(0)
            elif cube.get_color() == RED:
                new_line.append(2)
            elif cube.get_color() == GREEN:
                new_line.append(3)
            elif cube.get_color() == PURPLE:
                new_line.append(0)
    draw_path()

def dijkstra(matrix):
    rows = WINDOW_HEIGHT // Cube.cube_width
    cols = WINDOW_WIDTH // Cube.cube_width
    start = Cube.start_point_grid_pos
    destination = None

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 2:
                destination = (i, j)
                break
        if destination:
            break
    
    if not destination:
        return "Destination point not found"

    distances = {start: 0}
    visited = set()
    heap = [(0, start)]
    path = {}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while heap:

        (distance, current) = heapq.heappop(heap)
        visited.add(current)
        
        if current == destination:

            path_list = []
            while current in path:
                path_list.append(current)
                current = path[current]
            path_list.append(start)
            path_list.reverse()
            return path_list
        
        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and matrix[neighbor[0]][neighbor[1]] != 1 and neighbor not in visited:
                new_distance = distance + 1
                if neighbor not in distances or new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(heap, (new_distance, neighbor))
                    path[neighbor] = current

    return "No path found"

def draw_path(*args) -> None:
    path = dijkstra(grid)

    for cube in cubes:
        if cube.get_color() == PURPLE:
            cube.change_color(WHITE)

    if path == "No path found":
        print(f"{path}")
    else:
        for grid_pos in path[1:len(path)-1]:
            for cube in cubes:
                if cube.grid_pos == grid_pos:
                    cube.change_color(PURPLE)

if __name__ == "__main__":

    main_window.bind("<c>", draw_wall)
    main_window.bind("<x>", clear_wall)
    main_window.bind("<z>", set_end_point)
    main_window.bind("<s>", create_logic_grid)
    main_window.bind("<a>", set_start_point)
    main_window.bind("<f>", generate_random_pattern)
    main_window.mainloop()