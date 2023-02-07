import pygame as pg
import random
from pygame.math import Vector2
from sys import exit

class SNAKE:
    def __init__(self):
        self.body = [Vector2(7,10),Vector2(6,10),Vector2(5,10)]
        self.direction = Vector2(1,0)
        self.new_block = False
        
    def draw_snake(self):
        for block in self.body:
            block_rect = pg.Rect((block.x * cell_size) - 1,(block.y * cell_size) - 1 , cell_size, cell_size)
            pg.draw.rect(window,(183,133,122),block_rect)
    
    def move_snake(self):
        if self.new_block:
            body_copy = self.body
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy
    
    def grow_snake(self):
        self.new_block = True
        
class FRUIT:
    def __init__(self):
        self.randomize()
    
    def draw_fruit(self):
        fruit_rect = pg.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size - 5, cell_size - 5)
        window.blit(apple, fruit_rect)
        
    def randomize(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1) 
        self.pos = Vector2(self.x,self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        
    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.grow_snake()
            
    def check_fail(self):
        if not(0 <= self.snake.body[0].x < cell_number) or not(0 <= self.snake.body[0].y < cell_number):
            self.game_over()        
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
  
    def game_over(self):
        pg.quit()
        exit()
    
    def draw_score(self):
        score_txt = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_txt, True, (56,74,12))
        scx = int(cell_size * cell_number - 60)
        scy = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (scx,scy))
        window.blit(score_surface, score_rect)

pg.init()
cell_size = 35
cell_number = 20
window = pg.display.set_mode((cell_number*cell_size, cell_number*cell_size))
pg.display.set_caption("Snake")
clock = pg.time.Clock()
apple = pg.image.load('apple.png').convert_alpha()
game_font = pg.font.Font(None,35)

SCREEN_UPDATE = pg.USEREVENT
pg.time.set_timer(SCREEN_UPDATE,100)

main_game = MAIN()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            main_game.game_over()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pg.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pg.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
            if event.key == pg.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
        

    window.fill((175,215,70))
    main_game.draw_elements()
    pg.display.update()
    clock.tick(80)