
""" furkan taha unal
     s22289
"""
import turtle
from turtle import *
import sys


def generate(n, result='[X]'):
    for _ in range(n):
        # rule #1
        result = result.replace('X', 'F+[[X]-X]-F[-FX]+X')
        # rule #2
        result = result.replace('F', 'FF')
    return result

def draw(cmds, size=2):
    stack = []
    for cmd in cmds:
        if cmd == 'F':
            turtle.forward(size)
        elif cmd == '-':
            turtle.left(25)
        elif cmd == '+':
            turtle.right(25)
        elif cmd == 'X':
            pass
        elif cmd == '[':
            stack.append((turtle.position(), turtle.heading()))
        elif cmd == ']':
            position, heading = stack.pop()
            turtle.penup()
            turtle.setposition(position)
            turtle.setheading(heading)
            turtle.pendown()
        else:
            raise ValueError('Unknown Cmd: {}'.format(ord(cmd)))
    turtle.update()


def setup():
    turtle.hideturtle()
    turtle.tracer(2500, 0)
    turtle.left(90)
    turtle.penup()
    turtle.goto(0, -turtle.window_height() / 2)
    turtle.pendown()
    turtle.color("brown")

setup()
plant = generate(7)
draw(plant, 1)
turtle.exitonclick()
