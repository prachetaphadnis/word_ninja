import pygame
import time
import random

# == GUI ====================
# screen
background_color = ("white")

# word box
WORD_BOX_WITDH = 100
WORD_BOX_HEIGHT = 100
TEXT_SIZE = 20
color_text = ("black")
color_word_box = ("yellow")

NEW_WORD_BOX_EVERY = 2000
FPS = 60

# ===========================

pygame.init()
clock = pygame.time.Clock()

new_word_box_event = pygame.USEREVENT + 1
pygame.time.set_timer(new_word_box_event, NEW_WORD_BOX_EVERY)
        
class WordBox(pygame.sprite.Sprite):
    def __init__(self, text, color_text, x, y):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create a text box and fill with color
       self.font = pygame.font.SysFont("Arial", TEXT_SIZE)
       self.textSurf = self.font.render(text, 1, color_text)
       self.image = pygame.Surface([WORD_BOX_WITDH, WORD_BOX_HEIGHT])
       self.image.fill(color_word_box)
       W = self.textSurf.get_width()
       H = self.textSurf.get_height()
       self.image.blit(self.textSurf, [WORD_BOX_WITDH/2 - W, WORD_BOX_HEIGHT/2 - H/2])

       # Update position of word box
       self.rect = self.image.get_rect()
       self.rect.center = (x, y)

    def update(self):
        self.rect.move_ip(0, 2)


def draw_word_box(words):
    x = random.choice([100, 200, 300, 400])
    word = WordBox("NEW", color_text, x, 0)
    words.add(word)
    return words


def run():
    # Set up the drawing window
    screen = pygame.display.set_mode([500, 500])
    pygame.display.set_caption("Word Ninja")

    words = pygame.sprite.Group()

    running = True
    while running:
        clock.tick(FPS)
        
        # TODO: fetch transcriptions
        # TODO: match/score function

        screen.fill(background_color)
        words.update()
        words.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == new_word_box_event:
                words = draw_word_box(words)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run()

