from lib import *
from sphere import Sphere
from numpy import tan
from math import pi

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)


class Raytracer(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.clear()

  def clear(self):
    self.pixels = [
      [BLACK for x in range(self.width)]
      for y in range(self.height)
    ]

  def write(self, filename):
    writebmp(filename, self.width, self.height, self.pixels)

  def display(self, filename='out.bmp'):
    self.write(filename)

    try:
      from wand.image import Image
      from wand.display import display

      with Image(filename=filename) as image:
        display(image)
    except ImportError:
      pass  # do nothing if no wand is installed

  def point(self, x, y, c = None):
    try:
      self.pixels[y][x] = c or self.current_color
    except:
      pass

  def cast_ray(self, orig, direction, sphere):
    if sphere.ray_intersect(orig, direction):
      return color(255, 0, 0)
    else:
      return color(0, 0, 255)

  def render(self, sphere):
    fov = int(pi/2)
    for y in range(self.height):
      for x in range(self.width):
        i =  (2*(x + 0.5)/self.width - 1)*tan(fov/2)*self.width/self.height
        j = -(2*(y + 0.5)/self.height - 1)*tan(fov/2)
        # x = int(x)
        # y = int(y)
        # print(x, y)
        direction = norm(V3(i, j, -1))
        self.pixels[y][x] = self.cast_ray(V3(0,0,0), direction, sphere)

  def silly_render(self):
    for x in range(self.width):
      for y in range(self.height):
        r = int((x/self.width)*255) if x/self.width < 1 else 1
        g = int((y/self.height)*255) if y/self.height < 1 else 1
        b = 0
        self.pixels[y][x] = color(r, g, b)

r = Raytracer(1000, 1000)
s = Sphere(V3(-3, 0, -16), 2)
r.render(s)
r.display()