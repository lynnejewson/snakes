
import tkinter as tk
from random import uniform


def safedivide(x, y, max=10000000):
	if y == 0:
		return max
	else:
		return x/y


class Vector:
	def __init__(self, x, y):
		self.x, self.y = x, y


size = Vector(600, 600)
mid = Vector(size.x/2, size.y/2)


class Snake:
	def __init__(self, s, u, length):
		self.s = s
		self.u = u
		self.length = length
		self.ids = []

	def step(self, interval):
		for d in ['x', 'y']:
			change = getattr(self.u, d) * interval
			setattr(self.s, d, getattr(self.s, d) + change)

	def draw(self, canvas, size):
		hsize = size * 0.5
		self.ids.append(canvas.create_oval(self.s.x - hsize, self.s.y - hsize, self.s.x + hsize, self.s.y + hsize))
		if len(self.ids) >= self.length:
			canvas.delete(self.ids[-self.length])

	def jerk(self):
		u_change_x, u_change_y = uniform(-0.1, 0.1), uniform(-0.1, 0.1)
		self.u.x += u_change_x
		self.u.y += u_change_y

	def bounce(self, dimension):
		setattr(self.u, dimension, -getattr(self.u, dimension))


root = tk.Tk()
canvas = tk.Canvas(root, height=size.x, width=size.y)


s = Snake(mid, Vector(0, 0.5), 60)
t = Snake(Vector(100, 100), Vector(-0.2, 0), 40)
u = Snake(Vector(400, 500), Vector(0, 0), 55)

tostep = [s, t, u]

def repeat():
	for snake in tostep:
		snake.step(1)
		snake.jerk()
		snake.draw(canvas, 5)
		for i in ['x', 'y']:
			position = getattr(snake.s, i)
			if position <= 0 or position >= getattr(size, i):
				snake.bounce(i)
	canvas.after(5, repeat)

canvas.after(5, repeat)

canvas.pack()
root.mainloop()
