import scene
from euclid import *
from scene import LightSet, Sphere
from math import floor

class Scene(scene.Scene):
    def __init__(self):
        super(Scene, self).__init__()
        lights = self.make_example_light()
        def texture_func(p):
            size = 2
            if int(floor(p.x * size) + floor(p.y * size)) % 2:
                return Vector3(1, 0, 0)
            else:
                return Vector3(0, 0, 1)
        self.objects = [
            Sphere(lights, Vector3(0, 0, 8.), 1,
                   texture=texture_func)]
        #lights.shadow_objects = self.objects

        for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0),
                     (1, 1)]:
            self.objects.append(
                Sphere(lights, Vector3(y, x, 7.7), 0.3))
        self.objects.reverse()
