import random, sys, time, copy
import Imagenes
from pygame.locals import *
from Constantes import *
from Run import *

def main():
    pygame.init()
    while True:
        #run = run()
        if run() == False:
            break
if __name__ == '__main__':
    main()