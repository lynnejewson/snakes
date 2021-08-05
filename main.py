
import tkinter as tk
from random import uniform
import math


def safedivide(x, y, max=10000000):
	if y == 0:
		return max
	else:
		return x/y


class Vector:
	def __init__(self, x, y):
		self.x, self.y = x, y


class Property:
	def __init__(self, magnitude, speed, acceleration, bounce=True, min=0, max=600):
		self.magnitude = magnitude
		self.speed = speed
		self.acceleration = acceleration
		self.min, self.max = min, max
		self.bounce = bounce

	def step(self, interval):
		self.magnitude += self.speed * interval + 0.5 * self.acceleration * interval ** 2
		self.speed += self.acceleration * interval
		if self.bounce:
			self.check_bounce()
		else:
			self.check_stop()

	def check_bounce(self):
		if self.magnitude >= self.max:
			self.speed = -self.speed
		elif self.magnitude <= self.min:
			self.speed = -self.speed

	def check_stop(self):
		if self.magnitude >= self.max:
			self.magnitude = self.max
		elif self.magnitude <= self.min:
			self.magnitude = self.min


class Snake:
	def __init__(self, x, y, length, maxspeed=1000, colour='black'):
		self.x, self.y = x, y
		self.properties = (self.x, self.y)
		self.colour = colour
		self.maxspeed = maxspeed
		self.length = length
		self.ids = []

	def step(self, interval):
		for i in self.properties:
			i.step(interval)

	def draw(self, canvas, size):
		hsize = size * 0.5
		x, y = self.x.magnitude, self.y.magnitude
		self.ids.append(canvas.create_oval(x - hsize, y - hsize, x + hsize, y + hsize, outline=self.colour))
		if len(self.ids) >= self.length:
			canvas.delete(self.ids[-self.length])

	def jerk(self):
		for i in [self.x, self.y]:
			i.acceleration = uniform(-1, 1)


canvas_size = Vector(600, 600)
canvas_centre = Vector(canvas_size.x/2, canvas_size.y/2)

root = tk.Tk()
canvas = tk.Canvas(root, height=canvas_size.x, width=canvas_size.y)


a = Snake(Property(250, 3, 0), Property(250, 2, 0), 20)
b = Snake(Property(250, 0.1, 0), Property(0, 0.2, 0), 20)
c = Snake(Property(250, 0.1, 0), Property(0, 0.3, 0), 20)


tostep = (a, )


def repeat():
	for snake in tostep:
		snake.step(1)
		snake.jerk()
		snake.draw(canvas, 5)
	canvas.after(10, repeat)

canvas.after(10, repeat)

canvas.pack()
root.mainloop()
