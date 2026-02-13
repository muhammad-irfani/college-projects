import turtle

# Create a Turtle object
t = turtle.Turtle()
t.speed(5)

# --- Draw a filled circle ---
t.color("yellow")
t.begin_fill()
t.circle(100)       # Full circle with radius 100
t.end_fill()

# --- Move to position for the half moon ---
t.penup()
t.goto(50, 0)
t.pendown()

# --- Draw the half moon ---
t.color("black")
t.begin_fill()
t.circle(100)
t.end_fill()

# Hide turtle and finish
t.hideturtle()
turtle.done()
