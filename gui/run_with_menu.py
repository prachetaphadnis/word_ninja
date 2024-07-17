import pygame

from gui.run import init_screen, run, SCREEN_WIDTH, SCREEN_HEIGHT, load_translations
from gui.utils import Button

IMAGE = "gui/images/button.png"

def menu():
    screen = init_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
    spanish_button = Button(IMAGE, SCREEN_WIDTH-100, SCREEN_HEIGHT-40, "Spanish", "es")
    german_button = Button(IMAGE, SCREEN_WIDTH-500, SCREEN_HEIGHT-40, "German", "de")
    french_button = Button(IMAGE, SCREEN_WIDTH-300, SCREEN_HEIGHT-40, "French", "fr")
    buttons = [spanish_button, german_button, french_button]
    in_game=True

    background = pygame.image.load("gui/images/menu_background.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    while in_game:
        screen.blit(background, (0, 0))

        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.checkForInput(mouse, run, (screen, load_translations(button.lang, level="easy")))

        for button in buttons:
            button.update(screen)
            button.changeColor(mouse)

        pygame.display.update() 


if __name__ == "__main__":
    menu()