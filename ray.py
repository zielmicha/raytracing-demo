from draw import draw
import sys
import time

def main():
    name = sys.argv[1] if sys.argv[1:] else 'spheres'
    scene = __import__(name).Scene()
    scene.init()
    draw(scene.get_pixel, 'test', 640, 480)

if __name__ == '__main__':
    main()
