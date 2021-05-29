#Создай собственный Шутер!
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

class Enemy(GameSprite):
    def __init__(self, fileName, x, y, size_x, size_y, speed):
        super().__init__(fileName, x, y, size_x, size_y, speed)
        
    def update(self):
        if self.rect.y > 500:
            self.rect.y = -50
            self.rect.x = randint(0, 350)

            global lost
            lost += 1
        else:
            self.rect.y += self.speed

class Bullet(GameSprite):
    def __init__(self, fileName, x, y, size_x, size_y, speed):
        super().__init__(fileName, x, y, size_x, size_y, speed)
        
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -50:
            self.kill()
    
#музыка
# mixer.init()
# mixer.music.load('space.ogg')
# mixer.music.play()

#создай окно игры
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')

#задай фон сцены
background = transform.scale(image.load('backgraund.png'), (win_width, win_height))

player1 = Player("racket.png", 0, 150, 50, 200, 5, 1)
player2 = Player("racket.png", 650, 150, 50, 200, 5, 2)

bullets = sprite.Group()

score = 0
lost = 0

font.init()

font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 80)

you_win = font2.render("Ты победил!", 1, (255, 255, 0))
you_lose = font2.render("Ты проиграл(", 1, (255, 0, 0))

#игровой цикл
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
        player1.update()
        player1.reset()

        text_score = font1.render("Счёт: " + str(score), 1, (255, 255, 255))
        window.blit(text_score, (0, 0))

        bullets.update()
        bullets.draw(window)

        # colides = sprite.groupcollide(enemys, bullets, True, True)
        # for e in colides:
        #     score += 1
        #     enemy = Enemy("ufo.png", randint(0, 350), -50, 150, 50, randint(2, 3))
        #     enemys.add(enemy)
        
        # if lost >= 3:
        #     window.blit(you_lose, (200, 200))
        #     finish = True

        # if score >= 10:
        #     window.blit(you_win, (200, 200))
        #     finish = True
    
    display.update()
    clock.tick(FPS)