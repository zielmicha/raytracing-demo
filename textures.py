import scene
from euclid import *
from scene import LightSet, Triangle, Sphere

class Scene(scene.Scene):
    def __init__(self):
        super(Scene, self).__init__()
        lights = self.make_example_light()
        lights.add_diffuse(Vector3(0, 1, 0),
                           Vector3(0, 0, 1))

        def tex_color(x):
            X = 0.3
            if (x.x % (X*2)) < X != (x.y % (X*2)) < X:
                return Vector3(0, 0, 1)
            else:
                return Vector3(1, 1, 1)

        d = 50
        S = 13
        self.objects += self.make_tetrahedron(
            lights,
            Vector3(-2, -3, d),
            Vector3(2, -3, d),
            Vector3(0, -3, d - S*2),
            Vector3(0, 2, d - S),
            tex_color,
        )

        self.objects += [
            Sphere(lights, Vector3(0.5, 0, 29), 0.3)
        ]

    def make_tetrahedron(self, light, a, b, c, d, texture):
        return [
            Triangle(light, a, b, c, texture),
            Triangle(light, a, b, d, texture),
            Triangle(light, a, c, d, texture),
            Triangle(light, b, c, d, texture),
            ]
