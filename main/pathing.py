
import sys
import time
import os
import math


# ROTATED (90 deg CW): SO MAP IS A [T]
# New Width: 16.0m
# New Height: 7.0m (4m main + 3m garage)
MAP_WIDTH_M = 16.0
MAP_HEIGHT_M = 7.0
RESOLUTION = 0.25  # meters per cell

# Grid Dimensions
COLS = int(MAP_WIDTH_M / RESOLUTION)
ROWS = int(MAP_HEIGHT_M / RESOLUTION)


def rotate_point(x, y):
    return (y, 7.0 - x)

DEFAULT_POINTS = {
    1: rotate_point(4, 7.5),
    2: rotate_point(2.25, 7.5),
    3: rotate_point(2.25, 3.25),
    4: rotate_point(1.75, 3.25),
    5: rotate_point(1.75, 12.75),
    6: rotate_point(2.25, 12.75),
    7: rotate_point(2.25, 8.5),
    8: rotate_point(4, 8.5),
}

def get_grid_pos(x, y):
    col = int(x / RESOLUTION)
    row = int((MAP_HEIGHT_M - y) / RESOLUTION) # Invert Y for terminal display
    return max(0, min(COLS - 1, col)), max(0, min(ROWS - 1, row))

def interpolate_linear_path(p1, p2, step_size=0.25):
    x1, y1 = p1
    x2, y2 = p2
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    steps = int(dist / step_size)
    if steps == 0: return [p2]
    
    path = []
    for i in range(steps + 1):
        t = i / steps
        path.append((x1 + t * (x2 - x1), y1 + t * (y2 - y1)))
    return path

def draw_map(plow_pos, points):
    grid = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    
    # Draw boundaries and zones 
    for r in range(ROWS):
        for c in range(COLS):
            x = c * RESOLUTION
            y = MAP_HEIGHT_M - (r * RESOLUTION)
            
            # Map back to original coordinates to check zones
            # x_orig = 7.0 - y
            # y_orig = x
            orig_x = 7.0 - y
            orig_y = x
            
            # Main horizontal boundaries (Original vertical 0m and 4m)
            if (abs(orig_x - 0.0) < 0.1 or abs(orig_x - 4.0) < 0.1) and (0 <= orig_y <= 16):
                grid[r][c] = "-"
            
            # Main vertical boundaries (Original horizontal 0m and 16m)
            if (abs(orig_y - 0.0) < 0.1 or abs(orig_y - 16.0) < 0.1) and (orig_x <= 4):
                grid[r][c] = "|"
            
            # Garage area (4m to 7m, 5.5m to 10.5m)
            if 4 < orig_x <= 7 and 5.5 <= orig_y <= 10.5:
                if abs(orig_y - 5.5) < 0.1 or abs(orig_y - 10.5) < 0.1:
                    grid[r][c] = "|"
                if abs(orig_x - 7.0) < 0.1:
                    grid[r][c] = "-"
            
           # Central path markers (dots)
            if 1.5 <= orig_x <= 2.5 and 3 <= orig_y <= 13:
                if grid[r][c] == " ":
                    grid[r][c] = "."

    #mark the points 1-8
    for pid, pos in points.items():
        c, r = get_grid_pos(*pos)
        grid[r][c] = str(pid)

    # Mark plow position (X)
    pc, pr = get_grid_pos(*plow_pos)
    grid[pr][pc] = "X"

    # Render to string
    output = []
    output.append("+" + "-" * COLS + "+")
    for row in grid:
        output.append("|" + "".join(row) + "|")
    output.append("+" + "-" * COLS + "+")
    output.append(f"Plow Location: ({plow_pos[0]:.2f}m, {plow_pos[1]:.2f}m)")
    return "\n".join(output)

def get_user_points():
    return DEFAULT_POINTS

def get_single_key():
    if os.name == 'nt':
        import msvcrt
        return msvcrt.getwch().lower()
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch.lower()


def clamp_position(x, y):
    x = max(0.0, min(MAP_WIDTH_M, x))
    y = max(0.0, min(MAP_HEIGHT_M, y))
    return x, y


def interactive_pause(position, points, step_size=0.25):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("SnowPlow Rotated Simulation - PAUSED")
        print(draw_map(position, points))
        print("\nUse WASD to move one step. Press R to resume or Q to quit.")
        key = get_single_key()
        if key == 'w':
            position = clamp_position(position[0], position[1] + step_size)
        elif key == 's':
            position = clamp_position(position[0], position[1] - step_size)
        elif key == 'a':
            position = clamp_position(position[0] - step_size, position[1])
        elif key == 'd':
            position = clamp_position(position[0] + step_size, position[1])
        elif key == 'r':
            return position, True
        elif key == 'q':
            return position, False


def map_main():
    points = get_user_points()
    velocity = 1.0 # meters per second
    step_size = 0.25

    try:
        input("\nPress Enter to start the simulation...\n(Press Ctrl+C during the run to pause and use WASD override.)")

        for waypoint_index in range(1, 8):
            target = points[waypoint_index + 1]
            current = points[waypoint_index]
            segment_path = interpolate_linear_path(current, target, step_size=step_size)
            index = 0
            while index < len(segment_path):
                current = segment_path[index]
                os.system('cls' if os.name == 'nt' else 'clear')
                print("SnowPlow Rotated Simulation")
                print(draw_map(current, points))
                print("\nPress Ctrl+C to pause and enter WASD override.")
                time_per_step = step_size / velocity
                try:
                    time.sleep(time_per_step)
                except KeyboardInterrupt:
                    current, keep_running = interactive_pause(current, points, step_size)
                    if not keep_running:
                        print("\nSimulation stopped.")
                        return
                    segment_path = interpolate_linear_path(current, target, step_size=step_size)
                    index = 0
                    continue
                index += 1

        print("\nSimulation Complete: Points 1 to 8 reached.")
    except KeyboardInterrupt:
        print("\nSimulation stopped.")






