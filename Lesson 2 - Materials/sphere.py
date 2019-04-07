from lib import *

WHITE = color(255, 255, 255)

class Material(object):
  def __init__(self, diffuse=WHITE):
    self.diffuse = diffuse


class Intersect(object):
  def __init__(self, distance):
    self.distance = distance

class Sphere(object):
  def __init__(self, center, radius, material):
    self.center = center
    self.radius = radius
    self.material = material

  def ray_intersect(self, orig, direction):
    L = sub(self.center, orig)
    tca = dot(L, direction)
    l = length(L)
    d2 = l**2 - tca**2
    if d2 > self.radius**2:
      return None
    thc = (self.radius**2 - d2)**1/2
    t0 = tca - thc
    t1 = tca + thc
    if t0 < 0:
      t0 = t1
    if t0 < 0:
      return None

    return Intersect(
      distance=t0
    )