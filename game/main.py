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
    
    def __init__(self, color=(255, 0, 0), width=50, height=50):
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
        self.btn_up.rect.x, self.btn_up.rect.y = 100,  WIN_HEIGHT - 200
        self.btn_down.rect.x, self.btn_down.rect.y = 100,  WIN_HEIGHT - 100
        self.btn_left.rect.x, self.btn_left.rect.y = 50,  WIN_HEIGHT - 150
        self.btn_right.rect.x, self.btn_right.rect.y = 150,  WIN_HEIGHT - 150
        
        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.btn_up)
        self.buttons.add(self.btn_down)
        self.buttons.add(self.btn_left)
        self.buttons.add(self.btn_right)
        
    def btn_pressed(self, mouse_event):
        
        # check if left mouse is being pressed
        if pygame.mouse.get_pressed()[0]:
            x, y  = mouse_event.pos
            if self.btn_up.rect.collidepoint(x, y):
                return 'UP'
            elif self.btn_down.rect.collidepoint(x, y):
                return 'DOWN'
            elif self.btn_left.rect.collidepoint(x, y):
                return 'LEFT'
            elif self.btn_right.rect.collidepoint(x, y):
                return 'RIGHT'

# https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite
class Character(pygame.sprite.Sprite):
    """
    Basic generic character class
    """

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height):
       super(Character,  self).__init__()

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)
       
       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       
       self.speed = 5
       
    def move(self, joypad_direction):
        """
        move the character
        to be used along with Joypad.btn_pressed returns
        ('UP', 'DOWN' 'LEFT', 'RIGHT')
        """
        
        self.dx = 0
        self.dy = 0
        
        # check for horizontal move
        if joypad_direction == 'LEFT':
            self.dx = -self.speed
            self.rect.move_ip(-self.speed, 0)
        if joypad_direction == 'RIGHT':
            self.dx = +self.speed
            self.rect.move_ip(self.speed, 0)
            
        self.dx = 0
            
        # check for vertical move
        if joypad_direction == 'UP':
            self.dy = -self.speed
            self.rect.move_ip(0, -self.speed)
        if joypad_direction == 'DOWN':
            self.dy = +self.speed
            self.rect.move_ip(0, self.speed)
        self.dy = 0
       
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
    hero = Character((0, 0, 255), 5, 5)

    # On startup, load state saved by APP_WILLENTERBACKGROUND, and the delete
    # that state.
    x, y = load_state()
    delete_state()

    while True:

        ev = pygame.event.wait()
        
        # If not sleeping, draw the screen.
        if not sleeping:
            if ev.type == pygame.MOUSEMOTION or ev.type == pygame.MOUSEBUTTONDOWN or ev.type == pygame.TOUCH_MOUSEID:
                hero.move(joypad.btn_pressed(ev))
                
            screen.fill((0, 0, 0, 255))

            joypad.buttons.draw(screen)

            if x is not None:
                screen.blit(hero.image, (x, y))

            pygame.display.flip()
        
        x, y = hero.rect.x, hero.rect.y
        
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
    
