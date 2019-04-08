from lib import *
from sphere import *
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
    self.light = None
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
    material, intersect = self.scene_intersect(orig, direction)

    if material is None:
      return self.background_color

    light_dir = norm(sub(self.light.position, intersect.point))
    intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal))

    reflection = reflect(light_dir, intersect.normal)
    specular_intensity = self.light.intensity * (
      max(0, -dot(reflection, direction))**material.spec
    )

    diffuse = (
      int(material.diffuse[2] * intensity * material.albedo[0]),
      int(material.diffuse[1] * intensity * material.albedo[0]),
      int(material.diffuse[0] * intensity * material.albedo[0]),
    )

    specular = (
      int(255 * specular_intensity * material.albedo[1]),
      int(255 * specular_intensity * material.albedo[1]),
      int(255 * specular_intensity * material.albedo[1])
    )

    return color(
      diffuse[0] + specular[0] if diffuse[0] + specular[0] < 255 else 255,
      diffuse[1] + specular[1] if diffuse[1] + specular[1] < 255 else 255,
      diffuse[2] + specular[2] if diffuse[2] + specular[2] < 255 else 255
    )

  def scene_intersect(self, orig, direction):
    zbuffer = float('inf')

    material = None
    intersect = None

    for obj in self.scene:
      hit = obj.ray_intersect(orig, direction)
      if hit is not None:
        if hit.distance < zbuffer:
          zbuffer = hit.distance
          material = obj.material
          intersect = hit

    return material, intersect

  def render(self):
    fov = int(pi/2)
    for y in range(self.height):
      for x in range(self.width):
        i =  (2*(x + 0.5)/self.width - 1) * tan(fov/2) * self.width/self.height
        j =  (2*(y + 0.5)/self.height - 1) * tan(fov/2)
        direction = norm(V3(i, j, -1))
        self.pixels[y][x] = self.cast_ray(V3(0,0,0), direction)


ivory = Material(diffuse=color(100, 100, 80), albedo=(0.6,  0.3), spec=50)
rubber = Material(diffuse=color(80, 0, 0), albedo=(0.9,  0.1), spec=10)


r = Raytracer(1000, 1000)

r.light = Light(
  position=V3(-20, 20, 20),
  intensity=1.5
)

r.background_color = color(50, 50, 200)

r.scene = [
  Sphere(V3(0, -1.5, -10), 1.5, ivory),
  Sphere(V3(-2, -1, -12), 2, rubber),
  Sphere(V3(1, 1, -8), 1.7, rubber),
  Sphere(V3(0, 5, -20), 5, ivory)
]
r.render()
r.write('out.bmp')