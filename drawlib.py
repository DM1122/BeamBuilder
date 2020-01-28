# cross section visualizer using turtle graphics

import turtle
import veclib

size = [1000,500]
scl = 1                    # every meter represents scl pixels
pen = 1
vel = 10
axes = [1,1]


tim = turtle.Turtle()


def setup():
    tim.shape('classic')
    tim.color('black')
    tim.pensize(pen)
    tim.speed(vel)
    
    screen = turtle.Screen()
    screen.setup(width=size[0], height=size[1], startx=None, starty=None)
    #screen.title('Truss ')


def draw_axes():
    tim.penup()
    tim.home()
    
    # x-axis
    tim.pendown()
    tim.backward(axes[0]*scl)
    tim.forward(axes[0]*scl)
    tim.forward(axes[0]*scl)
    tim.home()

    # y-axis
    tim.setheading(90)
    tim.backward(axes[1]*scl)
    tim.forward(axes[1]*scl)
    tim.forward(axes[1]*scl)
    tim.home()

    tim.penup()


def draw_section(section):
    tim.penup()
    tim.goto(veclib.scal(section.pos,scl))
    tim.dot(5,'blue')

    tim.penup()


    corner = [section.pos[0]-section.b/2, section.pos[1]-section.h/2]

    tim.goto(veclib.scal(corner,scl))
    tim.pendown()
    tim.setheading(90)
    tim.forward(section.h*scl)
    tim.setheading(0)
    tim.forward(section.b*scl)
    tim.setheading(270)
    tim.forward(section.h*scl)
    tim.setheading(180)
    tim.forward(section.b*scl)

    tim.penup()

def draw_com(struct):
    tim.penup()
    tim.goto(veclib.scal(struct.com,scl))
    tim.dot(5,'red')


def hide():
    tim.hideturtle()


if __name__ == '__main__':
    setup()
    draw_axes()


    input("Press Enter to continue...")