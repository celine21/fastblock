DIFFICULTY = 2
import pygame, sys, os, traceback, random
from pygame.locals import *

if sys.platform in ["win32","win64"]: os.environ["images"]="1"
pygame.display.init()
pygame.font.init()
pygame.mixer.init(buffer=125)

font12 = pygame.font.SysFont("Georgia",12)
font18 = pygame.font.SysFont("Georgia",18)
font24 = pygame.font.SysFont("Georgia",24)
screen_size = [50*5+5,350]
lines = [200,50+1+50,50+1+50+2+50]
pygame.display.set_caption("fast block")
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
surface = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
file = open("data/hs.txt","r")
best_score = int(file.read().strip())
file.close()
sounds = { "start" : pygame.mixer.Sound("data/start.ogg"),
           "press" : pygame.mixer.Sound("data/press.ogg"),
           "end"   : pygame.mixer.Sound("data/end.ogg")   }
class Game(object):
    class Block(object):
        def __init__(self,column):
            self.column = column
            self.x = self.column*51
            self.bottom = screen_size[1]
        @staticmethod
        def update(game):
            game.block_counter += 1
            if game.block_counter == game.H/game.rate:
                game.block_counter = 0
                added = []
                for i in range(3):
                    added.append(random.choice([1,2,3]))
                    if random.random() < 0.50:break
                done = []
                for a in added:
                    if a in done:continue
                    game.blocks.append(Game.Block(a))
                    done.append(a)
        def move(self,game):
            self.bottom -= game.rate
        def draw(self,game):
            rect = (self.x,screen_size[1]-self.bottom-game.H,game.W,game.H)
            pygame.draw.rect(surface,(255, 255, 255),rect,0)
            pygame.draw.rect(surface,(0, 0, 155),rect,1)
    def __init__(self):
        self.score = 0
        self.blocks = []
        self.block_counter = 0
        self.W = 50
        if  DIFFICULTY == 1:
            self.H = 100
            self.rate = 1
        elif DIFFICULTY == 2:
            self.H = 100
            self.rate = 2
        elif DIFFICULTY == 3:
            self.H = 100
            self.rate = 3
    def get_input(self):
        global best_score
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT: return False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE: return False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = [mouse_position[0],screen_size[1]-mouse_position[1]]
                for block in self.blocks:
                    if mouse_pos[0] >= block.x and mouse_pos[0]<= block.x+51:
                        if mouse_pos[1] >= block.bottom and mouse_pos[1] <= block.bottom+self.H:
                            sounds["press"].play()
                            self.blocks.remove(block)
                            self.score += 1
                        if self.score > best_score:
                            best_score = self.score
                        break
        return True
    def update(self):
        Game.Block.update(self)
        for block in self.blocks:
            block.move(self)
            if block.bottom <= self.rate:
                return False
        return True
    def draw(self):
        surface.fill((0, 0, 0))
        for block in self.blocks:
            block.draw(self)
        surface.blit(font12.render("Your Score: "+str(self.score),True,(0,50,100)),(10,screen_size[1]-20))
        surface.blit(font12.render("Best Score: "+str(best_score),True,(0,50,100)),(165,screen_size[1]-20))
        pygame.display.flip()
    def run(self):
        while True:
            if not self.get_input(): return -1
            if not self.update(): return self.score
            self.draw()
            clock.tick(60)
def get_input():
    keys_pressed = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()
    mouse_rel = pygame.mouse.get_rel()
    for event in pygame.event.get():
        if event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE: return False
            sounds["start"].play()
            game = Game()
            score = game.run()
            if score == -1:
                return False
            sounds["end"].play()
            file = open("data/hs.txt","w")
            file.write(str(best_score))
            file.close()
    return True
blink = -50
def draw():
    global blink
    surface.fill((255,255,255))
    surface.blit(font12.render("Press ESC to Exit",True,(0,0,0)),(0,0))
    surface.blit(font24.render("Fast Block",True,(100,100,150)),(75,105))
    if blink < 0:
        surface.blit(font18.render("Click Anywhere",True,(0, 0, 255)),(65,150))
    blink += 1
    if blink == 20:
        blink = -20
    surface.blit(font18.render("Best Score: "+str(best_score),True,(0,0,0)),(130,320))
    pygame.display.flip()
def main():
    pygame.event.set_grab(True)
    while True:
        if not get_input():break
        draw()
        clock.tick(80)
    pygame.event.set_grab(False)
    pygame.quit()
if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()