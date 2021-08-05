
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


class LimitedVariable:
	def __init__(self, val, *conditions):
		self._val = val
		self.conditions = conditions

	@property
	def val(self):
		return self._val
	
	@val.setter
	def val(self, new):
		valid = True
		for c in self.conditions:
			if not c(new):
				valid = False
		if valid:
			self._val = new


class Property:
	def __init__(self, magnitude, speed, acceleration, bounce=True, min=0, max=600):
		self.magnitude = magnitude
		self.speed = speed
		self.acceleration = acceleration
		self.min, self.max = min, max
		self.bounce = bounce

	def step(self, interval):
		self.magnitude.val += self.speed.val * interval + 0.5 * self.acceleration.val * interval ** 2
		self.speed.val += self.acceleration.val * interval

	
class Snake:
	def __init__(self, **chosen_properties):
		possible_property_keys = ['x', 'y', 'z', 'length', 'maxspeed', 'colour']
		min_s = lambda x: x > 50
		min_v = lambda x: x > -10
		min_a = lambda x: x > -5
		max_s = lambda x: x < 550
		max_v = lambda x: x < 10
		max_a = lambda x: x < 5
		default_properties = {
			'x': Property(LimitedVariable(250, min_s, max_s), LimitedVariable(0, min_v, max_v), LimitedVariable(0, min_a, max_a)),
			'y': Property(LimitedVariable(250, min_s, max_s), LimitedVariable(0, min_v, max_v), LimitedVariable(0, min_a, max_a)),
			'z': Property(LimitedVariable(250, min_s, max_s), LimitedVariable(0, min_v, max_v), LimitedVariable(0, min_a, max_a)),
			'length': 20,
			'maxspeed': 1000,
			'colour': 'black'
		}

		for p in possible_property_keys:
			if p in chosen_properties:
				setattr(self, p, chosen_properties[p])
			else:
				setattr(self, p, default_properties[p])

		self.properties = (self.x, self.y, self.z)
		self.ids = []

	def step(self, interval):
		for i in self.properties:
			i.step(interval)

	def draw(self, canvas, size):
		x, y, z = self.x.magnitude.val, self.y.magnitude.val, self.z.magnitude.val
		size = z
		hsize = size * 0.05
		self.ids.append(canvas.create_oval(x - hsize, y - hsize, x + hsize, y + hsize, outline=self.colour))
		if len(self.ids) >= self.length:
			canvas.delete(self.ids[-self.length])

	def jerk(self):
		for i in [self.x, self.y, self.z]:
			i.acceleration.val = uniform(-1, 1)


canvas_size = Vector(600, 600)
canvas_centre = Vector(canvas_size.x/2, canvas_size.y/2)

root = tk.Tk()
canvas = tk.Canvas(root, height=canvas_size.x, width=canvas_size.y)


a = Snake()
b = Snake()
c = Snake()

tostep = (a, b, c)

i = 0

def repeat(i):
	i += 1
	for snake in tostep:
		snake.step(1)
		if i%10 == 0:
			snake.jerk()
		print(snake.x.acceleration.val, snake.y.acceleration.val, snake.z.acceleration.val)
		snake.draw(canvas, 5)
	canvas.after(10, lambda: repeat(i))

canvas.after(10, lambda: repeat(i))

canvas.pack()
root.mainloop()
