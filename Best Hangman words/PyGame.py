import pygame
import sys
from difficulty import WordScore

class HangmanGame:
    def __init__(self):
        pygame.init()

        self.WIDTH = 800
        self.HEIGHT = 600
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hangman")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (200, 200, 200)

        # Fonts
        self.TITLE_FONT = pygame.font.SysFont('comicsans', 60)
        self.MEDIUM_FONT = pygame.font.SysFont('comicsans', 40)
        self.SMALL_FONT = pygame.font.SysFont('comicsans', 30)

        # Game state
        self.state = "word_length"  # or "difficulty", "play", "result"
        self.word_length = 5
        self.difficulty = 2
        self.word = ""
        self.guessed = []
        self.incorrect = []
        self.lives = 6
        self.result_message = ""

    def draw_text_button(self, text, font, color, x, y):
        render = font.render(text, True, color)
        rect = render.get_rect(center=(x, y))
        self.window.blit(render, rect)
        return rect

    def draw_word_length_screen(self):
        self.window.fill(self.WHITE)
        title = self.TITLE_FONT.render("Select Word Length", True, self.BLACK)
        self.window.blit(title, (self.WIDTH // 2 - title.get_width() // 2, 50))

        buttons = []
        for i in range(4, 9):
            btn = self.draw_text_button(f"{i} Letters", self.MEDIUM_FONT, self.BLUE, self.WIDTH//2, 150 + (i - 4) * 70)
            buttons.append((btn, i))
        return buttons

    def draw_difficulty_screen(self):
        self.window.fill(self.WHITE)
        title = self.TITLE_FONT.render("Select Difficulty", True, self.BLACK)
        self.window.blit(title, (self.WIDTH // 2 - title.get_width() // 2, 50))

        easy_btn = self.draw_text_button("Easy", self.MEDIUM_FONT, self.BLUE, self.WIDTH//2, 200)
        med_btn = self.draw_text_button("Medium", self.MEDIUM_FONT, self.BLUE, self.WIDTH//2, 270)
        hard_btn = self.draw_text_button("Hard", self.MEDIUM_FONT, self.BLUE, self.WIDTH//2, 340)
        return [("easy", easy_btn), ("medium", med_btn), ("hard", hard_btn)]

    def draw_game_screen(self):
        self.window.fill(self.WHITE)

        # Title
        title_text = self.TITLE_FONT.render("Hangman", True, self.BLACK)
        self.window.blit(title_text, (self.WIDTH // 2 - title_text.get_width() // 2, 20))

        # Word display
        display_word = " ".join([letter if letter in self.guessed else "_" for letter in self.word])
        word_text = self.MEDIUM_FONT.render(display_word, True, self.BLACK)
        self.window.blit(word_text, (self.WIDTH // 2 - word_text.get_width() // 2, 150))

        # Incorrect letters
        incorrect_text = self.SMALL_FONT.render(f"Incorrect: {' '.join(self.incorrect)}", True, self.RED)
        self.window.blit(incorrect_text, (50, 250))

        # Lives
        lives_text = self.SMALL_FONT.render(f"Lives left: {self.lives}", True, self.BLACK)
        self.window.blit(lives_text, (50, 290))

    def draw_result_screen(self):
        self.window.fill(self.WHITE)
        result = self.TITLE_FONT.render(self.result_message, True, self.RED if self.lives == 0 else self.BLUE)
        word_text = self.MEDIUM_FONT.render(f"The word was: {self.word}", True, self.BLACK)
        self.window.blit(result, (self.WIDTH // 2 - result.get_width() // 2, 200))
        self.window.blit(word_text, (self.WIDTH // 2 - word_text.get_width() // 2, 300))

    def generate_word(self):
        word_scorer = WordScore()
        word_scorer.score_word(self.word_length)
        self.word = word_scorer.wordpicker(self.difficulty)[0]
        self.guessed = []
        self.incorrect = []
        self.lives = 13

    def game_loop(self):
        clock = pygame.time.Clock()
        run = True

        while run:
            clock.tick(60)

            if self.state == "word_length":
                buttons = self.draw_word_length_screen()
            elif self.state == "difficulty":
                buttons = self.draw_difficulty_screen()
            elif self.state == "play":
                self.draw_game_screen()
            elif self.state == "result":
                self.draw_result_screen()

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.state == "word_length":
                        for btn, length in buttons:
                            if btn.collidepoint(x, y):
                                self.word_length = length
                                self.state = "difficulty"
                    elif self.state == "difficulty":
                        for name, btn in buttons:
                            if btn.collidepoint(x, y):
                                self.difficulty = {"easy": 1, "medium": 2, "hard": 3}[name]
                                self.generate_word()
                                self.state = "play"

                if event.type == pygame.KEYDOWN and self.state == "play":
                    if event.unicode.isalpha():
                        letter = event.unicode.lower()
                        if letter not in self.guessed and letter not in self.incorrect:
                            if letter in self.word:
                                self.guessed.append(letter)
                            else:
                                self.incorrect.append(letter)
                                self.lives -= 1

                    if all(l in self.guessed for l in self.word):
                        self.result_message = "You won!"
                        self.state = "result"

                    if self.lives == 0:
                        self.result_message = "You lost!"
                        self.state = "result"

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = HangmanGame()
    game.game_loop()
