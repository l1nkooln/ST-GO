#---------------------------------------------------------------------------------------
# Program by l1nkooln
#
#
# Version	Date                  Info
# 1.0		2022	          Initial Version
#---------------------------------------------------------------------------------------


from pygame import*
import math
import random

init()
mixer.init()

# mixer.music.load("theme.ogg")
# mixer.music.play()

FPS = 60
clock = time.Clock()

x_sp2 = 200
y_sp2 = 100
win_width = 700

#Вікно
win = display.set_mode((700, 500))
display.set_caption('CS:GO')
display.set_icon(image.load("ICO.bmp"))
font = font.Font(None, 40)

#Спрайти
point_text = font.render('Killed: ', True, (255, 200, 0))
cash_text = font.render('Cash: ', True, (33, 254, 45))
background = transform.scale(image.load('background.png'), (700, 500))

bullets = sprite.Group()

class Player(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y):
        super().__init__()
        self.width = 100
        self.height = 100
        self.image_orig = transform.scale(image.load(player_image), (self.width, self.height))
        self.image = self.image_orig
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
      
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
    def update(self):
        if keys_pressed[K_a] and self.rect.x > -1000:
            self.rect.x -= self.speed
            self.image = transform.rotate(self.image_orig, 180)
        if keys_pressed[K_d] and self.rect.x > -1000:
            self.rect.x += self.speed
            self.image = self.image_orig 
        if keys_pressed[K_w] and self.rect.y > -1000:
            self.rect.y -= self.speed
            self.image = transform.rotate(self.image_orig, 90)
        if keys_pressed[K_s] and self.rect.y > -1000:
            self.rect.y += self.speed
            self.image = transform.rotate(self.image_orig, -90)
        
    def fire(self):
            print(self.rect.right)
            bullets.add(Bullet(self.rect.x + self.width - 10, self.rect.y + self.height * 0.75))

class Enemy(sprite.Sprite):
    def __init__(self, enem_image, enem_speed, enem_x, enem_y):
        super().__init__()
        self.width = 100
        self.height = 100
        self.image = transform.scale(image.load(enem_image), (self.width, self.height))
        self.speed = enem_speed
        self.rect = self.image.get_rect()
        self.rect.x = enem_x
        self.rect.y = enem_y
    def update(self):
        # if self.rect.x > 0:
        #     self.rect.x -= self.speed  

        if self.rect.x > player.rect.x:
            self.rect.x -= self.speed
        elif self.rect.x < player.rect.x:
            self.rect.x += self.speed
        # Movement along y direction
        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player.rect.y:
            self.rect.y -= self.speed
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = (x, y)
        mx, my = mouse.get_pos()
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.image = Surface((9, 4)).convert_alpha()
        self.image.fill((156, 91, 0))
        self.image = transform.rotate(self.image, angle)
        self.speed = 13
        self.rect = Rect(x, y, 9, 4)
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):  
        self.rect.x += self.dir[0]*self.speed
        self.rect.y += self.dir[1]*self.speed
        if not win.get_rect().collidepoint(self.pos):
            self.kill()
    
    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center = self.pos)
        surf.blit(self.bullet, bullet_rect) 

class Menu:
    def __init__(self):
        self._options = []
        self._callbacks = []
        self._current_option_index = 0

    def append_option(self, option, callback):
        self._options.append(font.render(option, True, (255, 255, 255)))
        self._callbacks.append(callback)

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._options) - 1))

    def select(self):
        self._callbacks[self._current_option_index]()

    def draw(self, surf, x, y, option_y_padding):
        for i, option in enumerate(self._options):
            option_rect: Rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if i == self._current_option_index:
                draw.rect(surf, (0, 100, 0), option_rect)
            surf.blit(option, option_rect)

player = Player('AK47.png', 5, 100, 200)
enem = Enemy('M4.png', 1, 600, 50)
enem1 = Enemy('M4.png', 1, 600, 300)

enems = sprite.Group()
enems.add(enem)
enems.add(enem1)

playr = sprite.Group()
playr.add(player)

win_txt = font.render('', True, (255, 0, 0))

pos = (185, 276)

game = False
run = True
menu_on = True
finish = False
gameover = False

points = 0
cash = 0


def quit_game():
    global run
    run = False
def game_on():
    global game, menu_on
    game = True
    menu_on = False
def game_over():
    gm = font.render('Ти програв, натисни - R, щоб відродитися', True, (255, 0, 0))
    win.blit(gm, 50, 200)
    gameover = True

menu = Menu()
menu.append_option('Play', game_on)
menu.append_option('Quit', quit_game)
def start():
    global game, points, enems, playr, cash
    game=True
    points = 0
    cash = 0
    # e = random.randint('M4.png', 'gl.png')
    player = Player('AK47.png', 5, 100, 200)
    enem = Enemy('M4.png', 1, 600, 50)
    enem1 = Enemy('M4.png' , 1, 600, 300)

    enems =  sprite.Group()
    enems.add(enem)
    enems.add(enem1)
    playr = sprite.Group()
    playr.add(player)
    

while run:
    for e in event.get():
        if e.type == MOUSEBUTTONDOWN:
            player.fire()
       
        if e.type == QUIT:
            run = False

        if e.type == KEYDOWN and menu:
            if e.key == K_w:
                menu.switch(-1)
            elif e.key == K_s:
                menu.switch(1)
            elif e.key == K_SPACE:
                menu.select()
            if e.key == K_ESCAPE:
                game = False
                menu_on = True
        if e.type == KEYDOWN:
            if e.key == K_r:
                start()


    if menu_on == True:
        win.fill((0, 0, 0))
        menu.draw(win, 100, 100, 75)
 
    if game == True:
        win.blit(background,(0, 0))
        player.reset()
        enems.update()
        keys_pressed = key.get_pressed()
        player.update()
        enem_list =  sprite.groupcollide(bullets, enems, True, True)
        for enemmy in enem_list:
            points += 1
            cash += 10
            point_text = font.render('Killed: '+str(points), True, (255, 0, 0))
            cash_text = font.render('Cash: '+str(cash), True, (33, 254, 45))
            x = random.randint(700, 900)
            y = random.randint(500, 900)
            enem = Enemy('M4.png', 2, x, y)
            enems.add(enem)
        r = random.randint(0, 100)

        if r == 50:
            x = random.randint(200, 600)
            y = random.randint(100, 400)
            enem = Enemy('M4.png', 2, x, y)
            enems.add(enem)
        if points == 50:
            win_txt = font.render('YOU WIN', True, (255, 0, 0))
            win.blit(win_txt, (300, 220))
            game = False

        kill_list =  sprite.spritecollide(player, enems, False)
        if len(kill_list) > 0:
            game = False
            restart = font.render('Ти програв, натисни - R, щоб відродитися', True, (255, 0, 0))
            win.blit(restart, (50, 200))

            
            
        
        win.blit(point_text, (30, 30))
        win.blit(cash_text, (550, 30))
               
        bullets.update()
        enems.draw(win)
        bullets.draw(win)
    clock.tick(FPS)
    display.update()