from lib import *
from sphere import Sphere, Material
from numpy import tan
from math import pi

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)


class Raytracer(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.background_color = color(0, 0, 0)
    self.scene = []
    self.clear()

  def clear(self):
    self.pixels = [
      [self.background_color for x in range(self.width)]
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

  def cast_ray(self, orig, direction):
    material = self.scene_intersect(orig, direction)

    if material is None:
      return self.background_color
    else:
      return material.diffuse

  def scene_intersect(self, orig, direction):
    zbuffer = float('inf')

    material = None
    for obj in self.scene:
      intersect = obj.ray_intersect(orig, direction)
      if intersect is not None:
        if intersect.distance < zbuffer:  # infront of the zbuffer
          zbuffer = intersect.distance
          material = obj.material

    return material

  def render(self):
    fov = int(pi/2)
    for y in range(self.height):
      for x in range(self.width):
        i =  (2*(x + 0.5)/self.width - 1) * tan(fov/2) * self.width/self.height
        j =  (2*(y + 0.5)/self.height - 1) * tan(fov/2)
        direction = norm(V3(i, j, -1))
        self.pixels[y][x] = self.cast_ray(V3(0,0,0), direction)


ivory = Material(diffuse=color(100, 100, 80))
rubber = Material(diffuse=color(80, 0, 0))


r = Raytracer(1000, 1000)
r.scene = [
  Sphere(V3(0, -1.5, -10), 1.5, ivory),
  Sphere(V3(-2, -1, -12), 2, rubber),
  Sphere(V3(1, 1, -8), 1.7, rubber),
  Sphere(V3(0, 5, -20), 5, ivory)
]
r.render()
r.write('out.bmp')