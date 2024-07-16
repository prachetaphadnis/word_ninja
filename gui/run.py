import pygame
import threading
import time
import random
from main import SMTranscribe, QUEUE
from pathlib import Path


from gui.utils import yaml_file_to_dict

# == GUI ====================
# screen
SCREEN_COLOR = (59, 108, 160)
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# word box
WORD_BOX_WITDH = 100
WORD_BOX_HEIGHT = 100
TEXT_FONT_SIZE = 20
TEXT_COLOR = "black"
WORD_BOX_COLOR = "yellow"

NEW_WORD_BOX_EVERY = 100
FPS = 60

TRANSLATIONS_PATH = "en_es.yaml"

# ===========================

pygame.init()
clock = pygame.time.Clock()

new_word_box_event = pygame.USEREVENT + 1
pygame.time.set_timer(new_word_box_event, NEW_WORD_BOX_EVERY)

class WordBox(pygame.sprite.Sprite):
    def __init__(self, text: str, translation: str, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)

        self.translation = text
        self.text = translation
        self.text_color = TEXT_COLOR
        self.text_font_size = TEXT_FONT_SIZE
        self.word_box_width = WORD_BOX_WITDH
        self.word_box_height = WORD_BOX_HEIGHT
        self.word_box_color = WORD_BOX_COLOR

        # top left x, y coordinates
        self.init_x = x
        self.init_y = y

        # state
        self.hit = False
        self.miss = False

        # init sprite (box with text)
        self._init_sprite()

    def _init_sprite(self):
        # image surface
        # self.image = pygame.Surface([self.word_box_width, self.word_box_height])
        # self.image.fill(self.word_box_color)

        # parachute surface
        self.image = pygame.image.load(Path('gui/images/parachute.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # text surface
        font = pygame.font.SysFont("Arial", self.text_font_size, bold = True)
        self.text_surface = font.render(self.text, 1, self.text_color)       
        W = self.text_surface.get_width()
        H = self.text_surface.get_height()

        # image surface + text surface
        # self.image.blit(self.text_surface, [self.word_box_width/2 - W/2, self.word_box_height/2 - H/2])
        self.image.blit(self.text_surface, [self.word_box_width/2 - W/2, self.word_box_height - 25])

        # Update position of word box
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.init_x, self.init_y)

    def update(self):
        self.rect.move_ip(0, 2)
        if self.rect.bottom > SCREEN_HEIGHT and not self.hit:
            # self.image.fill("red")
            self.image = pygame.image.load(Path('gui/images/explosion.png')).convert_alpha()
            self.image = pygame.transform.scale(self.image, (100, 100))
            self.miss = True

    def update_text(self):
        font = pygame.font.SysFont("Arial", self.text_font_size, bold = True)
        self.text_surface = font.render(self.translation, 1, self.text_color)       
        W = self.text_surface.get_width()
        H = self.text_surface.get_height()
        self.image.blit(self.text_surface, [self.word_box_width/2 - W/2, self.word_box_height/2 - H/2])


def update_word_boxes(word_box_group: pygame.sprite.Group, translations: dict):
    new_random_word = random.choice(list(translations.keys()))
    x = random.choice([0, 100, 200, 300, 400])
    word_box = WordBox(new_random_word, translations[new_random_word], x, 0)
    word_box_group.add(word_box)


def init_screen(width: int, height: int):
    screen = pygame.display.set_mode([width, height])
    pygame.display.set_caption("Word Ninja")
    return screen


def update_score(word_box_group):
    score = 0
    for word_box in word_box_group:
        if word_box.miss:
            score -= 1
        if word_box.hit:
            score += 2
    return score


def load_translations():
    return yaml_file_to_dict(TRANSLATIONS_PATH)


def display_time(screen, seconds_left: int):
    font = pygame.font.SysFont("Arial", 36, bold = True)
    timer_text = font.render(f"Time Left: {seconds_left}", True, "black")
    screen.blit(timer_text, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 50))


def display_score(screen, score: int):
    font = pygame.font.SysFont("Arial", 36, bold = True)
    score_text = font.render(f'Score: {score}', True, "black")
    screen.blit(score_text, (10, SCREEN_HEIGHT-50))


def run():
    translations = load_translations()
    screen = init_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
    word_box_group = pygame.sprite.Group()

    background_img = pygame.image.load('gui/images/background.jpg')

    score = 0
    running = True
    start_ticks = pygame.time.get_ticks()  # Start timer

    transcriber = SMTranscribe()
    thread = threading.Thread(target=transcriber.run)
    thread.start()

    word = ""

    while running:
        clock.tick(FPS)

        # Calculate time left
        seconds_left = (60000 - (pygame.time.get_ticks() - start_ticks)) // 1000
        if seconds_left <= 0:
            running = False  # End the game when the timer reaches 0

        try:
            word = QUEUE.get(block=False)
        except:
            word = word

        for word_box in word_box_group:
            if word == word_box.translation:
                fish_img = pygame.image.load('gui/images/fish.png').convert_alpha()
                word_box.image = pygame.transform.scale(fish_img, (100, 100))
                word_box.update_text()
                word_box.hit = True

        screen.fill(SCREEN_COLOR)
        screen.blit(background_img, (0, 0))
        word_box_group.update()
        word_box_group.draw(screen)

        score = update_score(word_box_group)

        display_score(screen, score)
        display_time(screen, seconds_left)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == new_word_box_event:
                update_word_boxes(word_box_group, translations)

    time.sleep(3)
    pygame.quit()


if __name__ == "__main__":
    run()
