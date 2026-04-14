import time

def display_map(map_data, current_pos):
    for x, row in enumerate(map_data):
        display_row = ""
        for y, cell in enumerate(row):
            if (y, x) == current_pos:
                display_row += display_row[:1] + "*"  # SnowPlow
            else:
                display_row += cell
        print(display_row)
    print("\nUse f, b, l, r to move:")

def move(map_data, current_pos, direction):
    y, x = current_pos
    if direction == 'f' and x > 0 and map_data[x - 1][y] != '##':
        x -= 1
    elif direction == 'b' and x < len(map_data) - 1 and map_data[x + 1][y] != '##':
        x += 1
    elif direction == 'l' and y > 0 and map_data[x][y-1] != '|| ':
        y -= 1
    elif direction == 'r' and y < len(map_data[0]) - 1 and map_data[x][y + 1] != '||':
        y += 1
    return (y, x)
