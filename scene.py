from euclid import *

PLANE_DIST = 1
CENTER = Vector3(0.5, 0.5, 0)

class Scene(object):
    def __init__(self):
        lights = LightSet()
        lights.point.append(Vector3(2, 2, -3.))
        self.objects = [Sphere(lights)]

    def get_pixel(self, x, y):
        v = Vector3()
        for obj in self.objects:
            v += obj.draw(x, y)

        return v

class LightSet(object):
    def __init__(self):
        self.point = []

class Sphere(object):
    def __init__(self, lightset):
        self.a = Vector3(0, 0, -3.)
        self.c = Vector3(0, 0, 8.)
        self.r = 1
        self.lightset = lightset

    def draw(self, x, y):
        a = self.a
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
            intensity = 0
            for light_src in self.lightset.point:
                light = normal.dot(light_src)
                intensity += light
            return Vector3(1, 1, 1) * max(0, min(1, intensity))
        else:
            return Vector3(0, 0, -delta / 10000)
