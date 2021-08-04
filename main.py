
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
	def __init__(self, magnitude, speed, acceleration, max=250):
		self.magnitude = magnitude
		self.speed = speed
		self.acceleration = acceleration
		self.max = max

	def step(self, interval):
		self.magnitude += self.speed * interval + 0.5 * self.acceleration * interval ** 2
		self.speed += self.acceleration * interval
		if self.magnitude > self.max:
			self.magnitude = self.max


size = Vector(600, 600)
mid = Vector(size.x/2, size.y/2)


class Snake:
	def __init__(self, origin, position, angle, length, maxspeed=1000):
		self.origin = origin
		self.position = position
		self.angle = angle
		self.length = length
		self.ids = []

	def step(self, interval):
		self.position.step(interval)
		self.angle.step(interval)

	def cartesian(self):
		x = self.origin.x + math.sin(self.angle.magnitude) * self.position.magnitude
		y = self.origin.y + math.cos(self.angle.magnitude) * self.position.magnitude
		return x, y

	def draw(self, canvas, size):
		hsize = size * 0.5
		x, y = self.cartesian()
		self.ids.append(canvas.create_oval(x - hsize, y - hsize, x + hsize, y + hsize))
		if len(self.ids) >= self.length:
			canvas.delete(self.ids[-self.length])

	def jerk(self):
		var = uniform(-100, 100)
		change = -1 + 2 / (1 + math.e ** var)
		self.angle.magnitude += change/10


	def bounce(self, dimension):
		setattr(self.u, dimension, -getattr(self.u, dimension))


root = tk.Tk()
canvas = tk.Canvas(root, height=size.x, width=size.y)


s = Snake(mid, Property(0, 1, 0), Property(0.1, 0, 0), 30)
t = Snake(mid, Property(0, 0.1, 0), Property(0, 0.2, 0), 60)
u = Snake(mid, Property(0, 0.1, 0), Property(0, 0.3, 0), 60)


tostep = [s]

def repeat():
	for snake in tostep:
		snake.step(1)
		snake.jerk()
		snake.draw(canvas, 5)
	canvas.after(10, repeat)

canvas.after(10, repeat)

canvas.pack()
root.mainloop()
