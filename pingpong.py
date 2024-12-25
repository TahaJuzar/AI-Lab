import turtle
import random
import numpy as np

# Setup the game window
window = turtle.Screen()
window.title("Ping Pong Game with AI")
window.setup(width=800, height=600)
window.tracer(0)

# AI Paddle Class
class aipaddleright(turtle.Turtle):
    def _init_(self, *args, **kwargs):
        super(aipaddleright, self)._init_(*args, **kwargs)
        self.speed(0)  # Paddle speed
        self.shape("square")  # Paddle shape
        self.color("green")  # Paddle green color
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        self.goto(350, 0)
        self.array1as = 2 * np.random.random((5, 7)) - 1
        self.array3as = 2 * np.random.random((7, 3)) - 1

    def usebraintomove(self, ballpos):
        inputlayer = np.array([ballpos[0][0] * 1.5, ballpos[0][1] * 1.5, ballpos[1][0] / 400, ballpos[1][1] / 300, self.ycor() / 300])
        after1stlayer = self.sigmoid(np.dot(inputlayer, self.array1as))
        finalresults = self.softmax(np.dot(after1stlayer, self.array3as))
        return finalresults

    def move_ai(self, ballpos):
        probs = self.usebraintomove(ballpos)
        move_decision = random.uniform(0, 1)
        if move_decision <= probs[0]:  # Move up
            self.sety(min(self.ycor() + 10, 250))
        elif move_decision <= probs[0] + probs[1]:  # Move down
            self.sety(max(self.ycor() - 10, -250))

    @staticmethod
    def sigmoid(x):
        return np.maximum(0, x)

    @staticmethod
    def softmax(x):
        return np.exp(x) / np.sum(np.exp(x), axis=0)

# Left paddle controlled by the player
leftpaddle = turtle.Turtle()
leftpaddle.speed(0)
leftpaddle.shape("square")
leftpaddle.color("blue")
leftpaddle.shapesize(stretch_wid=5, stretch_len=1)
leftpaddle.penup()
leftpaddle.goto(-350, 0)

def godownleft():
    y = leftpaddle.ycor() - 20
    if y > -250:
        leftpaddle.sety(y)

def goupleft():
    y = leftpaddle.ycor() + 20
    if y < 250:
        leftpaddle.sety(y)

# Ball setup
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0, 0)
ballxdirection = random.uniform(-1.5, -0.5)
ballydirection = random.uniform(-1, 1)

# AI Paddle setup
ai_paddle = aipaddleright()

# Scores and Pen
player_1_score = 0
player_2_score = 0
pen = turtle.Turtle()
pen.speed(0)
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player 1: 0 Player 2: 0", align="center", font=("Courier", 24, "normal"))

# Key bindings
window.listen()
window.onkeypress(goupleft, 'w')  # Move up paddle to use w button
window.onkeypress(godownleft, 's')  # Move down paddle to use s button

# Game Loop
while True:
    window.update()
    ball.setx(ball.xcor() + ballxdirection * 2)  # Reduced from 5 to 2 ball speed
    ball.sety(ball.ycor() + ballydirection * 2)  # Reduced from 5 to 2 ball speed

    # Ball collision with top and bottom walls
    if ball.ycor() > 290 or ball.ycor() < -290:
        ballydirection *= -1

    # Ball collision with left paddle
    if (-360 < ball.xcor() < -340 and
            leftpaddle.ycor() - 50 < ball.ycor() < leftpaddle.ycor() + 50):
        ballxdirection *= -1

    # Ball collision with AI paddle
    if (340 < ball.xcor() < 360 and
            ai_paddle.ycor() - 50 < ball.ycor() < ai_paddle.ycor() + 50):
        ballxdirection *= -1

    # AI Paddle Movement
    ai_paddle.move_ai([[ballxdirection, ballydirection], [ball.xcor(), ball.ycor()]])

    # Ball out of bounds - scoring
    if ball.xcor() > 390:
        player_1_score += 1
        ball.goto(0, 0)
        ballxdirection = random.uniform(-1.5, -0.5)
        ballydirection = random.uniform(-1, 1)

    if ball.xcor() < -390:
        player_2_score += 1
        ball.goto(0, 0)
        ballxdirection = random.uniform(0.5, 1.5)
        ballydirection = random.uniform(-1, 1)

    # Update scores
    pen.clear()
    pen.write(f"Player 1: {player_1_score} Player 2: {player_2_score}", align="center", font=("Courier", 24, "normal"))
