import pygame
from pygame.locals import *
import random 


pygame.init()

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
fps = 60 #frame per second e.g. in flip book one page is one frame

ground_scroll = 0 
scroll_speed = 4 
flying = False
game_over = False
pipe_gap = 200
pipe_frequeny = 1500 #time in miiliesecondes
last_pipe = pygame.time.get_ticks() - pipe_frequeny
score = 0 
pass_pipe = False
FONT = pygame.font.SysFont("Times new roman", 50)


#how to get path of any image
bg = pygame.image.load("images/bg.png")
ground_img = pygame.image.load("images/ground.png")
button_img = pygame.image.load("images/restart.png")

class Bird(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [] # variables with self are global within the class variables without self can only be used in designated fonction
        self.index = 0 
        self.counter = 0 
        for i in range(1,4):
            img = pygame.image.load(f"images/bird{i}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.val = 0 
        self.clicked = False 

    def update(self):
        self.counter += 1 
        flap_cool_down = 5 #in millieseocndes, images chnages after this amount of time 
        if flying: # flying is when the bird goes or down
            #adding gravity to ball when the bird is flying (gravity is for briging the bird down)
            self.val += 0.5
            if self.val > 6:
                self.val = 6
            if self.rect.bottom < 768: # based on the total screen size
                self.rect.y += int(self.val)
        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.val = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            self.counter += 1
            flap_cool_down = 5
            
            if self.counter > flap_cool_down: 
                self.counter = 0 
                self.index += 1 
                if self.index >= len(self.images):
                    self.index = 0 
            self.image = self.images[self.index]

            # rotate the bird:
            self.image = pygame.transform.rotate(self.images[self.index], self.val * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x,y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/pipe.png")
        self.rect = self.image.get_rect()
        
        #position 1 if for the top, position -1 is for the bottom

        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            #first False is for the x axsis and second True is for the y axsis and it is True as it has to be flipped
            self.rect.bottomleft = [x, y - int(pipe_gap/2)]

        if position == -1: 
            self.rect.topleft = [x, y + int(pipe_gap/2)]


    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

bird_group = pygame.sprite.Group()
flappy = Bird(100,int(screen_height/2))
bird_group.add(flappy)

pipe_group = pygame.sprite.Group()

is_running = True 

while is_running:
    clock.tick(fps)
    screen.blit(bg, (0,0))
    bird_group.draw(screen)
    bird_group.update()

    pipe_group.draw(screen)

    screen.blit(ground_img, (ground_scroll, 768))

    score_text = FONT.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (30, 30))

    #look for collision 
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0: 
        game_over = True
    
    if flying == True and game_over == False:
        # generaiting new pipes 
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequeny:
            pipe_height = random.randint(-100,100)
            bottom_pipe = Pipe(screen_width, int(screen_height/2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height/2) + pipe_height, 1)
            pipe_group.add(top_pipe)
            pipe_group.add(bottom_pipe)
            last_pipe = time_now 
        
        score += 1 

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

    if flappy.rect.bottom > 768:
        game_over = True     
        flying = False

    pipe_group.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True 
    

    
    pygame.display.update()

pygame.quit()

