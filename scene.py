from __future__ import division
from euclid import *
from math import atan2, asin

PLANE_DIST = 1
CENTER = Vector3(0.5, 0.5, 0)

class Scene(object):
    def __init__(self):
        self.objects = []
        self.camera = Vector3(0, 0, -3.)
        self._blocks = None

    def make_example_light(self):
        lights = LightSet()
        lights.ambient = Vector3(0.01, 0.01, 0.01)
        lights.add_point(Vector3(10, 10, -3.), Vector3(1, 1, 1))
        lights.add_point(self.camera, Vector3(0., 0., 0.1))

        lights.add_diffuse(Vector3(0.5, -1, 1).normalized(),
                           Vector3(0.5, 0.1, 0.))
        return lights

    def _trace_pixel(self, a, b):
        v = Vector3()
        dist = None
        for obj in self._find_objects(a, b):
            color, pos = obj.draw(a, b)
            if color:
                mdist = abs(pos - a)
                if not dist or mdist < dist:
                    dist = mdist
                    v = color
        return v

    def _find_objects(self, a, b):
        return self.objects

    def make_blocks(self):
        pass

    def get_pixel(self, x, y):
        if not self._blocks:
            self.make_blocks()
        b = Vector3(x, y, 0)
        v = self._trace_pixel(self.camera, b)
        v.x = min(max(v.x, 0), 1)
        v.y = min(max(v.y, 0), 1)
        v.z = min(max(v.z, 0), 1)

        return v

class LightSet(object):
    def __init__(self):
        self.point = []
        self.diffuse = []
        self.ambient = Vector3()
        self.shadow_objects = None

    def add_point(self, src, color=Vector3(1, 1, 1)):
        self.point.append((src, color))

    def add_diffuse(self, src, color=Vector3(1, 1, 1)):
        self.diffuse.append((src, color))

    def make_light(self, x, normal):
        color = Vector3()
        for light_src, light_color in self.point:
            light = max(-(x - light_src).normalized().dot(normal), 0)
            if not self.is_obscured(light_src, x):
                color += light_color * light

        for light_dir, light_color in self.diffuse:
            light_src = x + light_dir * 100 # TODO: constant
            light = max(light_dir.normalized().dot(normal), 0)
            if not self.is_obscured(light_src, x):
                color += light_color * light

        color += self.ambient
        return color

    def is_obscured(self, src, dest):
        if not self.shadow_objects:
            return False
        for obj in self.shadow_objects:
            x, normal = obj.intersect(src, dest)
            if x is not None:
                v2 = (src - dest)
                t = vec_div((x - dest), v2)
                if t > 0.01 and t < 0.9999:
                    return True
        return False

def vec_div(a, b):
    avg = []
    if abs(b.x) > 0.01:
        avg.append(a.x / b.x)
    if abs(b.y) > 0.01:
        avg.append(a.y / b.y)
    if abs(b.z) > 0.01:
        avg.append(a.z / b.z)
    return sum(avg) / len(avg)

class Object(object):
    def draw(self, a, b):
        x, normal = self.intersect(a, b)
        if x is not None:
            return self.make_color(x, normal), x
        else:
            return None, None

    def make_color(self, x, normal):
        # TODO:
        # reflected_dir = -2dot(ligth_dir, n)*n  + light_dir
        color = self.lightset.make_light(x, normal)
        return color

class TexturedObject(Object):
    def make_color(self, x, n):
        if self.normal_texture:
            tex_x = self.texture_mapping(x, n)
            n = self.normal_texture(tex_x, n).normalized()
        color = Object.make_color(self, x, n)
        if self.texture:
            tex_x = self.texture_mapping(x, n)
            tex_color = self.texture(tex_x)
            color = texture_mul(tex_color, color)
        return color

class Sphere(TexturedObject):
    def __init__(self, lightset, center, r, texture=None):
        self.c = center
        self.r = r
        self.lightset = lightset
        r_vec = Vector3(self.r, self.r, self.r)
        self.bbox = self.c - r_vec, self.c + r_vec
        self.texture = texture
        self.normal_texture = None

    def intersect(self, a, b):
        c = self.c
        r = self.r

        A = (b - a).magnitude_squared()
        B = (b - a).dot(a - c) * 2
        C = (a - c).magnitude_squared() - r ** 2

        delta = B ** 2 - 4 * A * C

        if delta >= 0:
            t = (-delta ** 0.5 - B) / (2 * A)
            x = (b - a) * t + a
            normal = (x - c).normalized()
            return x, normal
        else:
            return None, None

    def texture_mapping(self, p, n):
        q = p - self.c
        return Vector2(asin(q.y / self.r),
                       atan2(q.z, q.x))

class Triangle(TexturedObject):
    def __init__(self, lightset, p1, p2, p3, texture=None,
                 normal_texture=None):
        self.lightset = lightset
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.n = (p1 - p2).cross(p1 - p3).normalized()
        self.texture = texture
        self.normal_texture = normal_texture
        self.bbox = make_bbox([self.p1, self.p2, self.p3])

    def intersect(self, a, b):
        p1 = self.p1
        p2 = self.p2
        p3 = self.p3
        n = self.n

        h1 = (p1 - a).dot(n)
        h2 = n.dot(b - a)
        if h2 == 0:
            return None, None

        t = h1 / h2
        if t < 0:
            return None, None

        x = (b - a) * t + a

        r0 = (p1 - x).cross(p2 - x).dot(n)
        r1 = (p2 - x).cross(p3 - x).dot(n)
        r2 = (p3 - x).cross(p1 - x).dot(n)

        if r0 < 0 or r1 < 0 or r2 < 0:
            return None, None

        return x, n

def texture_mul(a, b):
    return Vector3(a.x * b.x, a.y * b.y, a.z * b.z)

def texture_mapping(x, n):
    return Vector2(x.x, x.y) # TODO!!!

def make_bbox(points):
    return Vector3(max( p.x for p in points ),
                   max( p.y for p in points ),
                   max( p.z for p in points )), \
        Vector3(min( p.x for p in points ),
                min( p.y for p in points ),
                min( p.z for p in points ))

class Texture(object):
    def __init__(self, image, mapped_size):
        self.mapped_size = mapped_size
        self.image = image

    def __call__(self, p):
        x = p.x / self.mapped_size.x
        y = p.y / self.mapped_size.y
        x %= 1
        y %= 1
        color = self.image.get_at(int(x * self.image.w),
                                  int(y * self.image.h))
        return Vector3(color[0] / 256., color[1] / 256.,
                       color[2] / 256.)

class MergedTexture(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self, p):
        return self.a(p) + self.b(p)
