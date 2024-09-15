import turtle


rules = {
    'X': 'F+[[X]-X]-F[-FX]+X',
    'F': 'FF'
}

initial_word = 'X'

iterations = 7  # Can be adjusted


def generate_l_system(w, rules, iterations):
    for _ in range(iterations):
        new_w = ""
        # Apply rules in parallel
        for char in w:
            new_w += rules.get(char, char)  # Default to the character itself if no rule applies
        w = new_w
    return w


# Generate the L-system
final_word = generate_l_system(initial_word, rules, iterations)
print(final_word)


def draw_l_system(instructions, angle, length):
    stack = []
    for command in instructions:
        if command == 'F':
            turtle.forward(length)
        elif command == '+':
            turtle.right(angle)
        elif command == '-':
            turtle.left(angle)
        elif command == '[':
            stack.append((turtle.position(), turtle.heading()))
        elif command == ']':
            position, heading = stack.pop()
            turtle.penup()
            turtle.setposition(position)
            turtle.setheading(heading)
            turtle.pendown()


# Set up the turtle environment
turtle.setup(width=800, height=800)
turtle.speed(0)  # Set speed to fastest
turtle.tracer(500, 0)

turtle.penup()
turtle.goto(0, -350)  # Start near the bottom of the screen
turtle.pendown()
turtle.left(90)  # Orient the turtle to start pointing upwards

# Calculate length based on iterations to fit in the window
length = 15 / (2 ** (iterations // 2))  # Scaling factor calculation

# Draw the L-system
draw_l_system(final_word, 25, length)

turtle.update()
turtle.done()
