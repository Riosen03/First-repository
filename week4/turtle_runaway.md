# 4주차 과제
# 변경사항에 대한 설명만 기재
# 해당 부분 위에 주석으로 설명

import tkinter as tk
# random 사용 안함(아래Randommover에 삭제 이유 기재)
import turtle
import time

class RunawayGame:
# catch 기준 반지름 50 -> 30 (30이 거의 거북이 사이즈와 일치)
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

# 타이머(timer) 및 스코어(score)를 위한 초기값 설정
        self.timer_start = time.time()
        self.score = 0

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

# 이동 기준 ai 타이머를 100 > 10으로 변경(두 거북이 모두 해당 타이머에 의존한 자동 이동)
    def start(self, init_dist=400, ai_timer_msec=10):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

# 아래에서 opp_heaing 부분 안쓰므로 삭제
    def step(self):
        self.runner.run_ai(self.chaser.pos())
        self.chaser.run_ai(self.runner.pos())

# 게임 시작 후 지난 시간을 int타입으로 casting, 점수는 해당 시간의 10배를 해서 int타입 변환
        now_timer = int(time.time() - self.timer_start)
        self.score = int(10*(time.time() - self.timer_start))
        
        is_catched = self.is_catched()
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)

# 잡혔는지는 플레이 중에는 별로 안중요하므로 삭제, 대신 시간과 점수를 갱신기재                                      ))))))))))))    1, 3) timer와 score 시스템 추가 
        self.drawer.write(f'time : {now_timer}        score : {self.score}')
        
# 잡혔는지 여부 확인 후 잡혔다면 중앙에 gameover표시와 함께 시간과 점수 표시, ai 타이머를 inf로 설정하여 두 거북이 모두 정지(이동X)
        if is_catched :
            self.drawer.setpos(-30, 30)
            self.drawer.write(f'game over\n\ntime : {now_timer}\n\nscore : {self.score}')
            self.ai_timer_msec = "inf"
 
        self.canvas.ontimer(self.step, self.ai_timer_msec)

# 직접 조작 거북이의 속도를 10 > 7로 조정(ai 타이머 시간을 내린것과 연계)
class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=7):
        super().__init__(canvas)
        self.step_move = step_move

# 방향키는 이동과 회전을 조금씩 하는 것 대신 방향키의 방향을 바라보도록 회전(해당 이유로 step_turn 사용 안하기 때문에 삭제)        
        canvas.onkeypress(lambda: self.setheading(90), 'Up')
        canvas.onkeypress(lambda: self.setheading(270), 'Down')
        canvas.onkeypress(lambda: self.setheading(180), 'Left')
        canvas.onkeypress(lambda: self.setheading(0), 'Right')
        canvas.listen()

# 벽 바깥으로 나가지 않도록 캔버스를 벗어나지 않게, 벗어났을시 원점(0,0)을 바라보고 이동하도록 변경(opp_heading은 안쓰니까 삭제)
    def run_ai(self, opp_pos):
        (x, y) = self.pos()
        if x < -360 or x > 360 or y < -360 or y > 360 :
            self.setheading(self.towards(0,0))
            self.forward(self.step_move)
        else : self.forward(self.step_move)

# 직접 조작 거북이의 속도를 10 > 5로 조정(ai 타이머 시간을 내린것, 자동추적과 연계)(마찬가지로 step_turn 삭제)     ))))))))))))     2) ai 시스템 수정(조작/ai 모두 일정부분 수정)
class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=5):
        super().__init__(canvas)
        self.step_move = step_move

# 항상 추적하는 runner turtle을 바라보도록 설정(opp_heading은 마찬가지로 삭제)
    def run_ai(self, opp_pos):
        (x, y) = opp_pos
        self.forward(self.step_move)
        self.setheading(self.towards(opp_pos))
        
        

if __name__ == '__main__':
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

# 내가 조작하는 거북이가 도망가는 쪽으로 전환
    runner = ManualMover(screen)
    chaser = RandomMover(screen)

    game = RunawayGame(screen, runner, chaser)
    game.start()
    screen.mainloop()
