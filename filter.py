import pygame
import sys
import struct
import os
import time

w = int(sys.argv[1])
h = int(sys.argv[2])

def main():
    pygame.init()
    screen = pygame.display.set_mode((w,h))
    start = time.time()

    _unpack = struct.unpack
    for _ in xrange(h):
        y, = _unpack('I', sys.stdin.read(4))
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
