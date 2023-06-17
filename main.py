import pygame
from pygame.locals import *
import time
import random
SIZE = 40


class Delay:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.Delay = 0.3


class Level:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.level = 1


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def move(self):
        self.x = random.randint(0, 24)*SIZE
        self.y = random.randint(0, 19)*SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()


class Limit:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.a = 0
        self.b = SIZE*25
        self.c = SIZE*20


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'
        self.change = self.direction

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):

        for i in range(self.length):
             self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.direction == 'left':
            self.x[0] -= SIZE

        if self.direction == 'right':
            self.x[0] += SIZE

        if self.direction == 'up':
            self.y[0] -= SIZE

        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill((120, 120, 120))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.Level = Level(self.surface)
        self.Delay = Delay(self.surface)
        self.limit = Limit(self.surface)

        with open("highscore.txt", "r") as f:
            self.highscore = f.read()

    def display_score(self):
        font = pygame.font.SysFont('arial', 25)
        score = font.render(f"score: {self.snake.length-1}", True, (200, 200, 200))
        self.surface.blit(score, (800, 10))
        pygame.display.flip()

    def display_level(self):
        font = pygame.font.SysFont('arial', 23)
        score = font.render(f"Level: {self.Level.level}", True, (200, 200, 200))
        self.surface.blit(score, (800, 40))
        pygame.display.flip()

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def collision(self, x1, y1, x2, y2):
        if y1 == y2:
            if x1 == x2:
                return True
        return False

    def contact(self, x1, y1, x2, y2):
        if y1>= y2 and x1== x2:
            return True
        return False

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        self.display_level()
        pygame.display.flip()

        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()
            if self.snake.length-1 > int(self.highscore):
                self.highscore = self.snake.length-1

        for i in range(2, self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game over"

        if self.contact(self.snake.x[0], self.snake.y[0], self.limit.a, self.limit.a):
            raise "Game over"
        if self.contact(self.snake.y[0], self.snake.x[0], self.limit.a, self.limit.a):
            raise "Game over"
        if self.contact(self.snake.x[0], self.snake.y[0], self.limit.b, self.limit.a):
            raise "Game over"
        if self.contact(self.snake.y[0], self.snake.x[0], self.limit.c, self.limit.a):
            raise "Game over"

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game over! your score is {self.snake.length-1}", True, (200, 200, 200))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press quit!", True, (200, 200, 200))
        self.surface.blit(line2, (200, 400))
        line3 = font.render(f"High score :{self.highscore} ", True, (200, 200, 200))
        self.surface.blit(line3, (200, 350))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            if self.Level.level == 1 and self.snake.length == 101:
                self.Level.level += 1
                self.Delay.Delay *= 0.8
            if self.Level.level == 2 and self.snake.length == 201:
                self.Level.level += 1
                self.Delay.Delay *= 0.7
            if self.Level.level == 3 and self.snake.length == 301:
                self.Level.level += 1
                self.Delay.Delay *= 0.5
            if self.Level.level == 4 and self.snake.length == 401:
                self.Level.level += 1
                self.Delay.Delay *= 0.7

            with open("highscore.txt", "w") as f:
                f.write(str(self.highscore))
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.change = "left"

                        if event.key == K_RIGHT:
                            self.snake.change = "right"

                        if event.key == K_UP:
                            self.snake.change = "up"

                        if event.key == K_DOWN:
                            self.snake.change = "down"

                if event.type == QUIT:
                    running = False

            if self.snake.change == "left" and self.snake.direction != 'right':
                self.snake.direction = "left"

            if self.snake.change == "right" and self.snake.direction != 'left':
                self.snake.direction = "right"

            if self.snake.change == "up" and self.snake.direction != 'down':
                self.snake.direction = "up"

            if self.snake.change == "down" and self.snake.direction != 'up':
                self.snake.direction = "down"

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(self.Delay.Delay)


if __name__ == "__main__":
    game = Game()
    game.run()








