from sys import exit
import pygame as pg
from random import randint, choice

def display_score():
    current_time = (pg.time.get_ticks() - start_time)//1000
    score_surface = test_font.render(f'Score:{current_time}', False, (64,64,64))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time




def collision_sprite():
    if pg.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True

class Player(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        player_walk_1 = pg.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pg.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pg.image.load('graphics/player/jump.png').convert_alpha()
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pg.mixer.Sound('audio/audio_jump.mp3')
        self.jump_sound.set_volume(0.01)
    
    def player_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_grav(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
        if self.player_index >= len(self.player_walk):self.player_index = 0
        self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_grav()
        self.animation_state()

class Obstacle(pg.sprite.Sprite):
    def __init__(self, type) -> None:
        super().__init__()
        if type == 'fly':
            fly_1 = pg.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pg.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pg.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pg.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        
        self.animation_index = 0
        
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

pg.init()
screen = pg.display.set_mode((800, 400)) # creates a surface by dimension (width, height)
pg.display.set_caption('Runner') # sets the title
clock = pg.time.Clock() # clock object used to controll frames
test_font = pg.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_Music = pg.mixer.Sound('audio/music.wav')
bg_Music.set_volume(0.01)

# Groups
player = pg.sprite.GroupSingle()
player.add(Player())

obstacle_group = pg.sprite.Group()

sky_surface = pg.image.load('graphics/Sky.png').convert()
ground_surface = pg.image.load('graphics/ground.png').convert()



# Intro screen
player_stand = pg.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pg.transform.rotozoom(player_stand, 0 , 2)
player_stand_rect = player_stand.get_rect(center=(400,200))

title_surface = test_font.render("Run, Pix!p", False, (111,196,169))
title_rect = title_surface.get_rect(center=(400, 80))

instructions_surface = test_font.render("Press Space to start", False, (111,196,169))
instructions_rect = instructions_surface.get_rect(center=(400, 350))

# Timer

obstacle_timer = pg.USEREVENT +1
pg.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pg.USEREVENT + 2
pg.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pg.USEREVENT + 3
pg.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pg.event.get(): # event loop, cycles through all the events
        if event.type == pg.QUIT:
            pg.quit() # quits the game
            exit() # exits the program completely

        if game_active:            
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        
        else:
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                game_active = True
                start_time = int(pg.time.get_ticks())
                bg_Music.play(loops=-1)

    # draw elements and update


    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0, 300))
        
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # collisions
        game_active = collision_sprite()
    # end game
    else:
        screen.fill((94,129, 162))
        screen.blit(player_stand, player_stand_rect)
        bg_Music.stop()
        score_message = test_font.render(f'Score:{score}', False, (64,64,64))
        score_message_rect = score_message.get_rect(center=(400, 350))
        if score == 0:
            screen.blit(instructions_surface, instructions_rect)
        else:
            screen.blit(score_message, score_message_rect)
        screen.blit(title_surface, title_rect)
    pg.display.update() # updates the screen
    clock.tick(60) # max 60 repeats of while in a sec
