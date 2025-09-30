import tkinter as tk
import turtle
import time

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=30):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # Instantiate another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

        self.timer_start = time.time()
        self.score = 0

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=10):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        # TODO) You can do something here and follows.
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        self.runner.run_ai(self.chaser.pos())
        self.chaser.run_ai(self.runner.pos())
        now_timer = int(time.time() - self.timer_start)
        self.score = int(10*(time.time() - self.timer_start))
        # TODO) You can do something here and follows.
        is_catched = self.is_catched()
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'time : {now_timer}        score : {self.score}')
        
        if is_catched :
            self.drawer.setpos(-30, 30)
            self.drawer.write(f'game over\n\ntime : {now_timer}\n\nscore : {self.score}')
            self.ai_timer_msec = "inf"
        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=7):
        super().__init__(canvas)
        self.step_move = step_move

        # Register event handlers
        
        canvas.onkeypress(lambda: self.setheading(90), 'Up')
        canvas.onkeypress(lambda: self.setheading(270), 'Down')
        canvas.onkeypress(lambda: self.setheading(180), 'Left')
        canvas.onkeypress(lambda: self.setheading(0), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos):
        (x, y) = self.pos()
        if x < -360 or x > 360 or y < -360 or y > 360 :
            self.setheading(self.towards(0,0))
            self.forward(self.step_move)
        else : self.forward(self.step_move)

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=5):
        super().__init__(canvas)
        self.step_move = step_move

    def run_ai(self, opp_pos):
        (x, y) = opp_pos
        self.forward(self.step_move)
        self.setheading(self.towards(opp_pos))
        
        

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # TODO) Change the follows to your turtle if necessary
    runner = ManualMover(screen)
    chaser = RandomMover(screen)

    game = RunawayGame(screen, runner, chaser)
    game.start()
    screen.mainloop()
