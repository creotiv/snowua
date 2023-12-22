import curses
import random
import time
import math


template = "010101100010101001010101"


def draw_background(stdscr):
    height, width = stdscr.getmaxyx()

    for x in range(width):
        for y in range(height-1):
            s = (y*x + x) % len(template)
            stdscr.addstr(y,x, template[s],  curses.color_pair(236))


def draw_tree(stdscr):
    height, width = stdscr.getmaxyx()

    # ASCII art for the Christmas tree
    tree = [
        "              @              ",
        "             ***             ",
        "            *@*@*            ",
        "           @**@**@           ",
        "          *@***@**@          ",
        "         *@**@***@**         ",
        "        @*@***@**@**@        ",
        "       *@**@**@**@**@*       ",
        "             |||             ",
        "             |||             ",
        "                             ",
        "     З Новим 2024 Роком      ",
        "       Слава Україні!        ",
        "         //uah.fund          "
    ]
    tree_height = len(tree)
    tree_width = max(len(line) for line in tree)

    start_y = height // 2 - tree_height // 2
    start_x = width // 2 - tree_width // 2

    # Draw the tree
    for i, line in enumerate(tree):
        for j, char in enumerate(line):
            if char == '*':
                stdscr.addch(start_y + i, start_x + j, char, curses.color_pair(3))
            elif char == '@':
                color = random.choice([2, 10, 6, 7])  # Randomly choose a color for ornaments
                stdscr.addch(start_y + i, start_x + j, "*", curses.color_pair(color))
            elif char == '|':
                stdscr.addch(start_y + i, start_x + j, char, curses.color_pair(4))
            elif char != ' ': 
                stdscr.addch(start_y + i, start_x + j, char, curses.color_pair(7))


def main(stdscr):
    curses.curs_set(0)  
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    stdscr.nodelay(1)  
    height, width = stdscr.getmaxyx()

    snowflakes = ['.', '*', '+']

    total_flakes = height*width // 60
    
    # Initialize snowflakes with properties
    flakes = [{'orig_x': random.randint(0, width - 2),
               'y': random.randint(0, height - 1),
               'char': random.choice(snowflakes),
               'speed': random.uniform(0.6, 0.9),
               'angle': random.uniform(0, 2 * math.pi),
               'offset': 0} 
              for _ in range(total_flakes)]

    def update_snowflakes():
        for flake in flakes:
            # Update vertical position
            flake['y'] += flake['speed']
            if flake['y'] >= height:
                flake['y'] = 0
                flake['char'] = random.choice(snowflakes)
                flake['orig_x'] = random.randint(0, width - 2)
                flake['speed'] = random.uniform(0.6, 0.9)
                flake['angle'] = random.uniform(0, 2 * math.pi)

            # Update the angle for horizontal movement
            flake['angle'] += 0.05
            flake['offset'] = math.sin(flake['angle']) * 2 # Adjust amplitude

            # Draw the snowflake at the new position
            try:
                stdscr.addch(
                    int(flake['y']), int(flake['orig_x'] + flake['offset']), 
                    flake['char'], curses.A_DIM)
            except curses.error:
                pass

    # Main loop
    try:
        while True:
            draw_background(stdscr)
            draw_tree(stdscr)
            update_snowflakes()
            stdscr.refresh()
            time.sleep(0.05)

            # Break on keyboard event
            if stdscr.getch() != curses.ERR:
                break
    finally:
        curses.curs_set(1)


def run():
    curses.wrapper(main)

if __name__ == "__main__":
    run()
