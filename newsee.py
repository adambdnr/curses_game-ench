import sys
import curses
import random
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from curses import wrapper
import time


def main(stdscr):
    stdscr.clear()


def drawSnake(screen, snake):
    for pos in snake:
        screen.addch(pos[0], pos[1], '¤', curses.color_pair(1))

def growSnake(snake, direction):
    tail = snake[len(snake)-1][:]
    if direction == 0:
        tail[1] -= 1
    elif direction == 2:
        tail[1] += 1
    elif direction == 1:
        tail[0] -= 1
    elif direction == 3:
        tail[0] += 1

    snake.append(tail)
    return snake


def moveSnake(snake, direction):
    head = snake[0][:]
    if direction == 0:
        head[1] += 1
    elif direction == 2:
        head[1] -= 1
    elif direction == 1:
        head[0] += 1
    elif direction == 3:
        head[0] -= 1
    snake.insert(0, head)
    snake.pop()
    return snake


def menu(scr, maxyx):
    scr.clear()
    info1 = 'WELCOME TO OUR VERY OWN SNAKE GAME\n'
    info2 = 'You task is to collect te items apperaring on the screen'
    info3 = 'You can control the snake with the arrow keys'
    info4 = "PRESS 'S' TO START"
    info5 = "PRESS 'Q' TO QUIT TO THE TERMINAL"
    scr.addstr(maxyx[0]//2-4, maxyx[1]//2-len(info1)//2, info1, curses.A_BOLD + curses.A_BLINK)
    scr.addstr(maxyx[0]//2-2, maxyx[1]//2-len(info2)//2, info2)
    scr.addstr(maxyx[0]//2-1, maxyx[1]//2-len(info3)//2, info3)
    scr.addstr(maxyx[0]//2, maxyx[1]//2-len(info4)//2, info4)
    scr.addstr(maxyx[0]//2+1, maxyx[1]//2-len(info5)//2, info5)
    key = scr.getch()
    while True:
        key = scr.getch()
        if key == ord('s'):
            return True
        if key == ord('q'):
            scr.clear()
            scr.refresh()
            quit()

screen = curses.initscr()
curses.noecho()
maxyx = screen.getmaxyx()
curses.curs_set(0)
screen.keypad(1)
curses.start_color()


snake = [[maxyx[0]//2, maxyx[1]//2]]

a = random.randint(1, maxyx[0])
b = random.randint(1, maxyx[1])


over = False
direction = 0
screen.nodelay(1)
menu(screen, maxyx)
score = 0
while not over:
    screen.clear()
    screen.border()
    screen.addch(a, b, '*')
    drawSnake(screen, snake)
    action = screen.getch()

    if action == curses.KEY_UP and direction != 1:
        direction = 3
        snake = moveSnake(snake, 3)
    elif action == curses.KEY_DOWN and direction != 3:
        direction = 1
        snake = moveSnake(snake, 1)
    elif action == curses.KEY_RIGHT and direction != 2:
        direction = 0
        snake = moveSnake(snake, 0)
    elif action == curses.KEY_LEFT and direction != 0:
        direction = 2
        snake = moveSnake(snake, 2)
    else:
        snake = moveSnake(snake, direction)

    if curses.has_colors():
        curses.start_color()

    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_GREEN)

    if (a == snake[0][0]) and (b == snake[0][1]):

        a = random.randint(2, maxyx[0]-2)
        b = random.randint(2, maxyx[1]-2)

        screen.addch(a, b, '*')
        screen.refresh()

        snake = growSnake(snake, direction)
        score += 1
    time.sleep(0.1)

    if snake[0] in snake[1:]:
        over = True

    elif snake[0][0] == maxyx[0] - 1 or snake[0][1] == maxyx[1] - 1 or snake[0][0] == 0 or snake[0][1] == 0:
        over = True


screen.nodelay(0)
curses.curs_set(0)

screen.clear()
screen.refresh

message = ("Game Over (press any key to quit!). You have " +str(score)+ " points")
screen.addstr(maxyx[0]//2, maxyx[1]//2-len(message)//2, message, curses.A_BLINK + curses.A_BOLD)
screen.getch()

curses.endwin()
wrapper(main)
