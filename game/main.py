# Allow pygame_sdl2 to be imported as pygame.
import pygame_sdl2
pygame_sdl2.import_as_pygame()

import pygame
import os

WIN_WIDTH = 1280 # in pixel
WIN_HEIGHT = 720 # in pixel
SCREEN_SIZE = ((WIN_WIDTH, WIN_HEIGHT))

class Button(pygame.sprite.Sprite):
    """
    Button for Joypad object.
    """
    
    def __init__(self, color=(255, 0, 0), width=25, height=25):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       
       self.image = pygame.Surface([width, height])
       self.image.fill(color)
       
       self.rect = self.image.get_rect()

class Joypad(object):
    """
    Joypad object.
    """
    def __init__(self):
        self.btn_up = Button()
        self.btn_down = Button()
        self.btn_left = Button()
        self.btn_right = Button()
        self.btn_up.rect.x, self.btn_up.rect.y = 50,  WIN_HEIGHT - 100
        self.btn_down.rect.x, self.btn_down.rect.y = 50,  WIN_HEIGHT - 50
        self.btn_left.rect.x, self.btn_left.rect.y = 25,  WIN_HEIGHT - 75
        self.btn_right.rect.x, self.btn_right.rect.y = 75,  WIN_HEIGHT - 75
        
        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.btn_up)
        self.buttons.add(self.btn_down)
        self.buttons.add(self.btn_left)
        self.buttons.add(self.btn_right)
        
    def btn_pressed(self):
        
        ev = pygame.event.wait()
        # check if left mouse is being pressed
        if pygame.mouse.get_pressed()[0]:
            x, y  = ev.pos
            if self.btn_up.rect.collidepoint(x, y):
                print('UP')
            elif self.btn_down.rect.collidepoint(x, y):
                print('DOWN')
            elif self.btn_left.rect.collidepoint(x, y):
                print('LEFT')
            elif self.btn_right.rect.collidepoint(x, y):
                print('RIGHT')

def save_state(x, y):
    """
    Saves the game state.
    """

    with open("state.txt", "w") as f:
        f.write("{} {}".format(x, y))

def load_state():
    try:
        with open("state.txt", "r") as f:
            x, y = f.read().split()
            x = int(x)
            y = int(y)

        return x, y
    except:
        return None, None

def delete_state():

    if os.path.exists("state.txt"):
        os.unlink("state.txt")


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_SIZE))
    
    sleeping = False
    
    joypad = Joypad()

    # On startup, load state saved by APP_WILLENTERBACKGROUND, and the delete
    # that state.
    x, y = load_state()
    delete_state()

    while True:

        # If not sleeping, draw the screen.
        if not sleeping:
            screen.fill((0, 0, 0, 255))

            joypad.buttons.draw(screen)

            if x is not None:
                #screen.blit(icon, (x - icon_w / 2, y - icon_h / 2))
                pass

            pygame.display.flip()

        ev = pygame.event.wait()

        joypad.btn_pressed()
        # Pygame quit.
        if ev.type == pygame.QUIT:
            break

        # Android back key.
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_AC_BACK:
            break

        elif ev.type == pygame.APP_WILLENTERBACKGROUND:
            # The app is about to go to sleep. It should save state, cancel
            # any timers, and stop drawing the screen until an APP_DIDENTERFOREGROUND
            # event shows up.

            save_state(x, y)

            sleeping = True

        elif ev.type == pygame.APP_DIDENTERFOREGROUND:
            # The app woke back up. Delete the saved state (we don't need it),
            # restore any times, and start drawing the screen again.

            delete_state()
            sleeping = False

            # For now, we have to re-open the window when entering the
            # foreground.
            screen = pygame.display.set_mode((SCREEN_SIZE))


if __name__ == "__main__":
    main()
    
