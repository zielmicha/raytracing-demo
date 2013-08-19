from euclid import *

PLANE_DIST = 1
CENTER = Vector3(0.5, 0.5, 0)

class Scene(object):
    def __init__(self):
        #lights.ambient = Vector3(0.03, 0.03, 0.03)
        self.camera = Vector3(0, 0, -3.)

        lights = LightSet()
        #lights.add_point(Vector3(10, 10, -3.), Vector3(0.3, 0., 0.))
        lights.add_point(self.camera, Vector3(0., 0.2, 0))
        lights.add_diffuse(Vector3(0.5, -1, 1).normalized(),
                           Vector3(0.5, 0.1, 0.))
        self.objects = [Sphere(lights)]

    def get_pixel(self, x, y):
        v = Vector3()
        for obj in self.objects:
            v += obj.draw(self.camera, x, y)

        v.x = min(max(v.x, 0), 1)
        v.y = min(max(v.y, 0), 1)
        v.z = min(max(v.z, 0), 1)

        return v

class LightSet(object):
    def __init__(self):
        self.point = []
        self.diffuse = []
        self.ambient = Vector3()

    def add_point(self, src, color=Vector3(1, 1, 1)):
        self.point.append((src, color))

    def add_diffuse(self, src, color=Vector3(1, 1, 1)):
        self.diffuse.append((src, color))

class Sphere(object):
    def __init__(self, lightset):
        self.c = Vector3(0, 0, 8.)
        self.r = 1
        self.lightset = lightset

    def draw(self, a, x, y):
        b = Vector3(x, y, 0)
        c = self.c
        r = self.r

        A = (b - a).magnitude_squared()
        B = (b - a).dot(a - c) * 2
        C = (a - c).magnitude_squared() - r ** 2

        delta = B ** 2 - 4 * A * C

        if delta >= 0:
            t = (delta ** 0.5 - B) / (2 * A)
            x = (b - a) * t + a
            normal = (x - c).normalized()
            color = Vector3()
            for light_src, light_color in self.lightset.point:
                light = max((x - light_src).normalized().dot(normal), 0)
                color += light_color * light

            for light_src, light_color in self.lightset.diffuse:
                light = max((light_src).dot(normal), 0)
                color += light_color * light

            color += self.lightset.ambient
            return color
        else:
            return Vector3(0, 0, -delta / 10000)
