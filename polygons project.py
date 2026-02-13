import turtle
import math

def polygon(t, length, sides):
    """Draws a regular polygon with the given number of sides and side length."""
    angle = 360 / sides
    for _ in range(sides):
        t.forward(length)
        t.right(angle)

def square(t, length):
    polygon(t, length, 4)

def hexagon(t, length):
    polygon(t, length, 6)

def circle(t, radius):
    """Draw a circle using 360 small steps as a polygon approximation."""
    for _ in range(360):
        t.forward(2 * math.pi * radius / 360)
        t.right(1)

if __name__ == "__main__":
    screen = turtle.Screen()
    t = turtle.Turtle()

    square(t, 100)
    t.penup()
    t.goto(-150, 0)
    t.pendown()
    hexagon(t, 80)
    t.penup()
    t.goto(150, 0)
    t.pendown()
    circle(t, 50)

    screen.mainloop()
