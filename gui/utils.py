import yaml
import os
import pygame


def yaml_file_to_dict(translations_dir: os.PathLike, lang: str, level: str) -> dict:
    with open(f"{translations_dir}/en_{lang}.yaml", "r") as f:
        content = yaml.load(f, Loader=yaml.FullLoader).get(level, None)
        assert isinstance(content, dict)
        return content

class Button():
    def __init__(self, image, x, y, text, lang):
        self.font = pygame.font.SysFont("Arial", 36, bold=True)
        self.surface = pygame.image.load(image)
        self.image = pygame.transform.scale(self.surface, (175, 70))
        self.x = x
        self.y = y
        self.text_input = text
        self.text = self.font.render(self.text_input, True, "black")
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))
        self.lang = lang
    
    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    
    def checkForInput(self, pos, function, args):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            function(*args)
    
    def changeColor(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, "green")
        else:
            self.text = self.font.render(self.text_input, True, "black")
