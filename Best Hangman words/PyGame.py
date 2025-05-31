import pygame
import sys
from difficulty import WordScore

class HangmanGame:

    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.FONT = pygame.font.SysFont("Times New Roman")
        self.word_list = self.load_words()
        
    



    def load_words(self):
        word_scorer = WordScore

    def game(self):

        pygame.init()
        window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hangman")



