import scene
from euclid import *
from math import *
from scene import LightSet, Triangle, Sphere, Texture, MergedTexture
from draw import Image

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

        img = Image.load('linux.jpg')
        tex_img = Texture(img, Vector2(2, -2))

        d = 50
        S = 13
        self.objects += self.make_tetrahedron(
            lights,
            Vector3(-2, -3, d),
            Vector3(2, -3, d),
            Vector3(0, -3, d - S*2),
            Vector3(0, 2, d - S),
            texture=tex_img,
        )

        self.objects += [
            Sphere(lights, Vector3(0.5, 0, 29), 0.3)
        ]

    def make_tetrahedron(self, light, a, b, c, d, **kwargs):
        return [
            Triangle(light, a, b, c, **kwargs),
            Triangle(light, a, b, d, **kwargs),
            Triangle(light, a, c, d, **kwargs),
            Triangle(light, b, c, d, **kwargs),
            ]
