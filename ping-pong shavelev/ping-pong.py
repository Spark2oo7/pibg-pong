#dy spark2oo7
from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, fileName, x, y, size_x, size_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(fileName), (size_x, size_y))
        self.size_x = size_x
        self.size_y = size_y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, fileName, x, y, size_x, size_y, speed, namber):
        super().__init__(fileName, x, y, size_x, size_y, speed)
        self.recharge = 0
        self.namber = namber
    
    def update(self):
        if self.recharge != 0:
            self.recharge -= 1

        keys_pressed = key.get_pressed()
        if self.namber == 1:
            if keys_pressed[K_s] and self.rect.y < win_height-self.speed-self.size_y:
                self.rect.y += self.speed
            if keys_pressed[K_w] and self.rect.y > self.speed:
                self.rect.y -= self.speed
        else:
            if keys_pressed[K_DOWN] and self.rect.y < win_height-self.speed-self.size_y:
                self.rect.y += self.speed
            if keys_pressed[K_UP] and self.rect.y > self.speed:
                self.rect.y -= self.speed


class Ball(GameSprite):
    def __init__(self, fileName, x, y, size_x, size_y, speed, dir_x, dir_y):
        super().__init__(fileName, x, y, size_x, size_y, speed)
        self.dir_x = dir_x
        self.dir_y = dir_y

    def update(self):
        self.rect.x += self.dir_x * self.speed
        self.rect.y += self.dir_y * self.speed

        if self.rect.y < 0:
            self.dir_y = randint(8, 12) / 10
        if self.rect.y > win_height - self.size_y:
            self.dir_y = randint(8, 12) / -10
        
        if sprite.collide_rect(self, player1):
            self.dir_x = randint(8, 12) / 10
            if randint(0, 5) == 5:
                self.speed += 1
        if sprite.collide_rect(self, player2):
            self.dir_x = randint(8, 12) / -10
            if randint(0, 5) == 5:
                self.speed += 1
        
        global win
        if self.rect.x < -50:
            win = 2

        if self.rect.x > 650:
            win = 1
    

#создай окно игры
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')

#задай фон сцены
background = transform.scale(image.load('backgraund.png'), (win_width, win_height))

player1 = Player("racket.png", 0, 150, 50, 200, 5, 1)
player2 = Player("racket.png", 650, 150, 50, 200, 5, 2)

ball = Ball("ball.png", 300, 150, 50, 50, 5, 1, 1)


font.init()

font = font.SysFont("Arial", 80)

win1 = font.render("Игрок 1 победил!", 1, (255, 255, 0))
win2 = font.render("Игрок 2 победил!", 1, (255, 255, 0))

#игровой цикл
win = 0
clock = time.Clock()
FPS = 60
game = True
finish = False
while game:
    #обработай событие «клик по кнопке "Закрыть окно"»
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0, 0))

        ball.update()
        ball.reset()

        player1.update()
        player1.reset()
        
        player2.update()
        player2.reset()

        if win == 1:
            window.blit(win1, (100, 200))
            finish = True
        if win == 2:
            window.blit(win2, (100, 200))
            finish = True
    
    display.update()
    clock.tick(FPS)
