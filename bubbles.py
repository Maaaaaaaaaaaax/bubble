import pygame
import os
from random import randrange
from time import sleep
from math import sqrt

class Settings(object):
    width = 960
    height = 540
    fps = 60
    title = "Bubbles"
    file_path = os.path.dirname(os.path.abspath(__file__))
    images_path = os.path.join(file_path, "images")
    border = 10
    gameover = False
    click = False
    hold = False
    bubbles = 0
    timeunit = 1
    hover = False
    score = 0
    pause = False

    # Highscore
    try:
        f = open("highscore.json", "r")
        data = f.readlines()
        f.close()
        highscore = data[0][13:].rstrip("\n")
        if len(data) == 2:
            highscorename = data[1][8:]
            #print(highscorename)

    except:
        f = open("highscore.json", "w")
        f.write("\"highscore\": 0\n")
        f.write("\"name\": ")
        f.close()
        highscore = 0

    # Sounds
    pygame.mixer.init()
    popsound = pygame.mixer.Sound('sounds/pop.mp3')
    popsound.set_volume(0.3)

    spawnsound = pygame.mixer.Sound('sounds/drop.mp3')
    spawnsound.set_volume(0.3)

    gameoversound = pygame.mixer.Sound('sounds/gameover.mp3')
    gameoversound.set_volume(0.1)
    

    @staticmethod
    def get_dim():
        return (Settings.width, Settings.height)


class Bubble(pygame.sprite.Sprite):
    def __init__(self, pygame, pos):
        super().__init__()
        self.radius = 5
        self.image = pygame.image.load(os.path.join(Settings.images_path, "bubble1.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
        self.rect = self.image.get_rect()
        self.rect.left = pos[0] + 10
        self.rect.top = pos[1] + 10
        self.t = 0
        self.growth = randrange(1, 5)
        pygame.mixer.Sound.play(Settings.spawnsound)

    def update(self, bubbles):
        self.t += 1
        #print(float(Settings.timeunit) * 60.0)
        if float(self.t) >= float(Settings.timeunit) * 60.0:
            self.t = 0
            self.radius += self.growth
            self.image = pygame.image.load(os.path.join(Settings.images_path, "bubble1.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
            self.rect.left -= self.growth
            self.rect.top -= self.growth 
            self.rect.width += self.growth * 2  # Das Benötige ich, damit die Hitbox stimmt
            self.rect.height += self.growth * 2 # Das auch

        if self.rect.left <= 0:
            self.pop(False)
        if self.rect.right >= Settings.width:
            self.pop(False)
        if self.rect.top <= 0:
            self.pop(False)
        if self.rect.bottom >= Settings.height:
            self.pop(False)
            
        if Settings.click == True and pygame.mouse.get_pos()[0] >= self.rect.left and pygame.mouse.get_pos()[0] <= self.rect.right and pygame.mouse.get_pos()[1] >= self.rect.top and pygame.mouse.get_pos()[1] <= self.rect.bottom:
            self.pop(True)

    def pop(self, score):
        self.kill()
        Settings.bubbles -= 1
        pygame.mixer.Sound.play(Settings.popsound)
        if score == True:
            Settings.score += self.radius
            
            

# Zur Kollisionsüberprüfung (10 Pixel Abstand)
class Spawnbubble(pygame.sprite.Sprite):
    def __init__(self, pygame):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.images_path, "bubble1.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.left = randrange(0 + Settings.border, Settings.width - Settings.border - 30)
        self.rect.top = randrange(0 + Settings.border, Settings.height - Settings.border - 30)

    def update(self):
        self.rect.left = randrange(0 + Settings.border, Settings.width - Settings.border - 30)
        self.rect.top = randrange(0 + Settings.border, Settings.height - Settings.border - 30)

    def get_pos(self):
        return [self.rect.left, self.rect.top]
        


class Mouse(pygame.sprite.Sprite):
    def __init__(self, pygame):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.images_path, "mouse.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, 40))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.left = pygame.mouse.get_pos()[0]
        self.rect.top = pygame.mouse.get_pos()[1]
        #print(pygame.mouse.get_pos())

        if Settings.hover == True:
            self.image = pygame.image.load(os.path.join(Settings.images_path, "mouse_top.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.rect.centerx = pygame.mouse.get_pos()[0]
            self.rect.centery = pygame.mouse.get_pos()[1]

        else:
            self.image = pygame.image.load(os.path.join(Settings.images_path, "mouse.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (35, 40))
            self.rect.left = pygame.mouse.get_pos()[0]
            self.rect.top = pygame.mouse.get_pos()[1]


class Pixel(pygame.sprite.Sprite):
    def __init__(self, pygame):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.images_path, "mouse.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (1, 1))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.left = pygame.mouse.get_pos()[0]
        self.rect.top = pygame.mouse.get_pos()[1]


class Game(object):
    def __init__(self):
        self.screen = pygame.display.set_mode(Settings.get_dim())
        pygame.display.set_caption(Settings.title)
        self.background = pygame.image.load(os.path.join(Settings.images_path, "background.jpg")).convert()
        self.background = pygame.transform.scale(self.background, (Settings.width, Settings.height))
        self.background_rect = self.background.get_rect()

        self.grey = pygame.image.load(os.path.join(Settings.images_path, "black.png")).convert()
        self.grey = pygame.transform.scale(self.grey, (Settings.width, Settings.height))
        self.grey_rect = self.grey.get_rect()
        self.grey.set_alpha(120)
        

        self.all_bubbles = pygame.sprite.Group()
        self.spawnbubble = Spawnbubble(pygame)
        self.bubble = Bubble(pygame, self.spawnbubble.get_pos())
        Settings.bubbles += 1
        self.all_bubbles.add(self.bubble)

        self.all_mouse = pygame.sprite.Group()
        self.mouse1 = Mouse(pygame)
        self.all_mouse.add(self.mouse1)
        self.pixel = Pixel(pygame)

        self.clock = pygame.time.Clock()
        self.done = False
        pygame.mouse.set_visible(False)
        self.t = 0
        self.spawn = True
        self.input = False
        self.name = ""
        self.newhighscore = False

        pygame.mixer.music.load('sounds/background.mp3')
        pygame.mixer.music.play(-1,0.0)
        pygame.mixer.music.set_volume(.03)

        pygame.font.init()
        self.font = pygame.font.SysFont("", 30)
        self.font2 = pygame.font.SysFont("", 75)
        self.gameovertext = self.font2.render("GAMEOVER", False , (0,0,0))
        self.pausetext = self.font2.render("PAUSED", False , (0,0,0))
        self.againtext = self.font.render("Press \"R\" to play again", False , (0,0,0))
        self.scoretext = self.font.render("Score: " + str(Settings.score), False , (0,0,0))

    def run(self):
        while not self.done:
            self.clock.tick(Settings.fps)  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.done = True
                    if event.key == pygame.K_p:
                        if Settings.gameover == False:
                            if Settings.pause == False:
                                Settings.pause = True
                            else:
                                Settings.pause = False

                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] != True:
                    if Settings.gameover == False:
                        if Settings.pause == False:
                            Settings.pause = True
                        else:
                            Settings.pause = False

                if event.type == pygame.KEYDOWN and self.input == True:
                    if event.key == pygame.K_RETURN:
                        self.input = False
                        self.newhighscore = False
                        f = open("highscore.json").read().splitlines()
                        f[1] = "\"name\": " + str(self.name)
                        open("highscore.json", "w").write("\n".join(f))
                        Settings.highscorename = self.name
                        self.name = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.name =  self.name[:-1]
                    else:
                        self.name += event.unicode
						
            if Settings.pause == False and Settings.gameover == False:

                pygame.mixer.music.unpause()

                # Kollision
                if pygame.mouse.get_pressed()[0] == True and Settings.click == False and Settings.hold == False:
                    Settings.click = True
                    Settings.hold = True
                elif pygame.mouse.get_pressed()[0] == True and Settings.click == True:
                    Settings.click = False
                    Settings.hold = True
                elif pygame.mouse.get_pressed()[0] == False and Settings.hold == True:
                    Settings.hold = False
                    Settings.click = False

                if pygame.sprite.spritecollide(self.pixel, self.all_bubbles, False):
                    Settings.hover = True
                else:
                    Settings.hover = False

                for bubble in self.all_bubbles:
                    for bubble2 in self.all_bubbles:
                        if bubble != bubble2:
                            collision = pygame.sprite.collide_circle(bubble, bubble2)
                            if collision == True:
                                Settings.gameover = True
                                print("Gameover")
                                pygame.mixer.Sound.play(Settings.gameoversound)
                                self.all_bubbles.draw(self.screen)

                # Zeiteinheit wird kleiner
                if Settings.timeunit > 0.1:
                    Settings.timeunit -= 0.0001


                # Blasen spawnen
                self.t += 1
                if float(self.t) >= float(Settings.timeunit) * 60.0 and Settings.bubbles < sqrt(Settings.width**2 + Settings.height**2) // 100 - 1:
                    self.t = 0
                    self.spawnbubble.update()
                    while self.spawn == True:
                        for self.bubble in self.all_bubbles:
                            if pygame.sprite.collide_circle(self.spawnbubble, self.bubble):
                        #if pygame.sprite.spritecollide(self.spawnbubble, self.all_bubbles, False):
                                self.spawnbubble.update()
                            else:
                                self.spawn = False
                    self.bubble = Bubble(pygame, self.spawnbubble.get_pos())
                    self.all_bubbles.add(self.bubble)
                    Settings.bubbles += 1
                    self.spawn = True
                    #print(Settings.bubbles, "Blase erschaffen")

                self.all_bubbles.update(self.all_bubbles)
                self.all_mouse.update()
                self.pixel.update()
                
            # Zeichnung
            self.screen.blit(self.background, self.background_rect)
            self.all_bubbles.draw(self.screen)
            self.all_mouse.draw(self.screen)

            self.scoretext = self.font.render("Score: " + str(Settings.score) , False , (0,0,0))
            self.screen.blit(self.scoretext, (5, 5))

            if Settings.pause == True and Settings.gameover == False:
                # Graues Bild
                self.screen.blit(self.grey, self.grey_rect)
                self.screen.blit(self.pausetext, (Settings.width // 2 - 110, Settings.height //2 - 100))
                self.screen.blit(self.scoretext, (5, 5))

                # Soundstop
                pygame.mixer.music.pause()

            if Settings.gameover == True:
                #print("a")

                if Settings.score > int(Settings.highscore):
                    Settings.highscore = Settings.score
                    self.input = True
                    self.newhighscore = True
                    f = open("highscore.json").read().splitlines()
                    f[0] = "\"highscore\": " + str(Settings.highscore)
                    open("highscore.json", "w").write("\n".join(f))

                self.screen.blit(self.gameovertext, (Settings.width // 2 - 150, Settings.height //2 - 100))

                if self.newhighscore == False and int(Settings.highscore) > 0:
                    self.highscoretext = self.font.render("Highscore from " + Settings.highscorename + ": " + str(Settings.highscore), False , (0,0,0))
                    self.screen.blit(self.againtext, (Settings.width // 2 - 115, Settings.height //2 - 50))
                    self.screen.blit(self.scoretext, (Settings.width // 2 - 60, Settings.height //2 - 20))
                    self.screen.blit(self.highscoretext, (Settings.width // 2 - 100, Settings.height //2 + 10))

                if int(Settings.highscore) == 0:
                    self.screen.blit(self.againtext, (Settings.width // 2 - 115, Settings.height //2 - 50))
                    self.screen.blit(self.scoretext, (Settings.width // 2 - 60, Settings.height //2 - 20))

                if self.newhighscore == True:
                    self.newhighscoretext = self.font.render("NEW HIGHSCORE: " + str(Settings.highscore), False , (0,0,0))
                    self.screen.blit(self.newhighscoretext, (Settings.width // 2 - 100, Settings.height //2 + 10))
                    self.nametext = self.font.render("Enter Name Here: " + self.name, False , (0,0,0))
                    self.screen.blit(self.nametext, (Settings.width // 2 - 100, Settings.height //2 + 40))
                
                if pygame.key.get_pressed()[pygame.K_r] == True and self.input == False:
                    self.all_bubbles.empty()
                    Settings.score = 0
                    Settings.gameover = False
                    Settings.timeunit = 1
                    self.spawnbubble.update()
                    self.bubble = Bubble(pygame, self.spawnbubble.get_pos())
                    Settings.bubbles = 1
                    self.all_bubbles.add(self.bubble)
                    self.newhighscore = False

            self.all_mouse.update()
            self.all_mouse.draw(self.screen)
            pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()
