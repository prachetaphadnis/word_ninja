# Simple pygame program

# Import and initialize the pygame library
import pygame
import time
pygame.init()



background_color = (255, 255, 255)
text_color = (0, 0, 0)

def display_text(word):
    screen.fill(background_color)  # Clear screen
    font = pygame.font.Font(None, 26)
    text_surface = font.render(word, True, text_color)
    screen.blit(text_surface, (20, 20))
    pygame.display.flip()


english_to_spanish = { "hello": "hola", "goodbye": "adiós", "please": "por favor", "thank you": "gracias", "yes": "sí","no": "no", "man": "hombre", "woman": "mujer", "boy": "niño", "girl": "niña", "food": "comida", "water": "agua","house": "casa", "car": "coche", "school": "escuela", "book": "libro", "dog": "perro", "cat": "gato", "friend (masc)": "amigo","family": "familia" }

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

# Run until the user asks to quit
running = True
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for word in english_to_spanish.keys():
        # Fill the background with white
        screen.fill(background_color)
        display_text(word)
        time.sleep(2)


# Done! Time to quit.
pygame.quit()


