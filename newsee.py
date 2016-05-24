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
        screen.addch(pos[0], pos[1], '#')


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


screen = curses.initscr()
curses.noecho()
maxyx = screen.getmaxyx()
curses.curs_set(0)
screen.keypad(1)

snake = [[maxyx[0]//2, maxyx[1]//2]]

a = random.randint(1, maxyx[0])
b = random.randint(1, maxyx[1])


over = False
direction = 0
screen.nodelay(1)

while not over:
    screen.clear()

    screen.addch(a, b, '&')
    drawSnake(screen, snake)
    screen.refresh()
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

    if (a == snake[0][0]) and (b == snake[0][1]):

        a = random.randint(1, maxyx[0]-1)
        b = random.randint(1, maxyx[1]-1)

        screen.addch(a, b, '&')
        screen.refresh()

        snake = growSnake(snake, direction)
    time.sleep(0.1)

    if snake[0][0] == maxyx[0] or snake[0][1] == maxyx[1] or snake[0][0] == 0 or snake[0][1] == 0:
        over = True

screen.nodelay(0)
curses.curs_set(1)

string = 'Game Over (press any key to quit!)'
screen.addstr(maxyx[0]//2, maxyx[1]//2-len(string)//2, string)
screen.getch()

curses.endwin()
wrapper(main)
