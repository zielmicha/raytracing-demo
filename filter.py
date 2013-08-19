import pygame
import sys
import struct
import os

w = 640
h = 480

def main():
    pygame.init()
    screen = pygame.display.set_mode((w,h))

    _unpack = struct.unpack
    for y in xrange(h):
        for x in xrange(w):
            color = _unpack('BBB', sys.stdin.read(3))
            screen.set_at((x, y), color)
        if y % 10 == 0:
            pygame.display.flip()

    pygame.display.flip()
    pygame.image.save(screen, 'test.png')
    while True:
        ev = pygame.event.wait()
        if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and
                                      ev.key in (pygame.K_ESCAPE,
                                                 pygame.K_q)):
            os._exit(0)

if __name__ == '__main__':
    try:
        main()
    except:
        pass
