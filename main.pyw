import time
import random
import pygame
import pyttsx3
import threading

engine = pyttsx3.init()

pygame.init()

WHITE = (255,255,255)
WHITE_RED = (255,200,200)
GREEN = (0,255,0)
RED = (255,0, 0)
ORANGE = (255,128, 64)
YELLOW = (255,255,0)
BLUE_DARK = (0, 0, 255)
BLUE_LIGHT = (100,100,255)
GREY = (200,200,200)
BLACK = (0,0,0)

colors = [WHITE, WHITE_RED,GREEN, RED, ORANGE, BLUE_DARK, BLUE_LIGHT]

width = 1920
height = 1080

screen = pygame.display.set_mode((width, height))

cars = []
trucks = []
pause = False

class Player:
    def __init__(self):
        self.x = width / 2
        self.y = height / 2
        self.speed = 0
        self.maxSpeed = 50
        self.color = colors[random.randint(0, len(colors)-1)]
    def acelarate(self):
        if self.speed < self.maxSpeed:
            self.speed += 5
        else:
            self.speed = self.maxSpeed
    def brake(self):
        if self.speed > 0:
            self.speed -= 5
        else:
            self.speed = 0
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 50, 50))
        pygame.draw.rect(screen, YELLOW, (self.x+5, self.y-5, 5, 5))
        pygame.draw.rect(screen, YELLOW, (self.x+40, self.y-5, 5, 5))
        pygame.draw.rect(screen, RED, (self.x+5, self.y+50, 40, 5))
        pygame.draw.rect(screen, GREY, (self.x+20, self.y+55.5, 10, 5))

class Car:
    def __init__(self):
        self.x = random.randint(0, width-50)
        self.y = random.randint(-1000, 0)
        self.speed = random.randint(15 ,20)
        self.color = colors[random.randint(0, len(colors)-1)]
    def draw(self):
        self.y+=self.speed
        pygame.draw.rect(screen, self.color, (self.x, self.y, 50, 50))
        pygame.draw.rect(screen, YELLOW, (self.x+5, self.y+50, 5, 5))
        pygame.draw.rect(screen, YELLOW, (self.x+40, self.y+50, 5, 5))
        pygame.draw.rect(screen, RED, (self.x+5, self.y-5, 40, 5))
        pygame.draw.rect(screen, GREY, (self.x+20, self.y-7.5, 10, 5))

class Truck:
    def __init__(self):
        self.x = random.randint(0, width-50)
        self.y = random.randint(-1000, 0)
        self.speed = random.randint(10 ,15)
        self.color = colors[random.randint(0, len(colors)-1)]
    def draw(self):
        self.y+=self.speed
        pygame.draw.rect(screen, self.color, (self.x, self.y, 50, 50))
        if self.color == BLUE_LIGHT:
            pygame.draw.rect(screen, BLUE_DARK, (self.x+10, self.y+15, 30, 20))
        elif self.color == BLUE_DARK:
            pygame.draw.rect(screen, BLUE_LIGHT, (self.x+10, self.y+15, 30, 20))
        else:
            pygame.draw.rect(screen, WHITE, (self.x+10, self.y+15, 30, 20))
        pygame.draw.rect(screen, YELLOW, (self.x+5, self.y+50, 5, 5))
        pygame.draw.rect(screen, YELLOW, (self.x+40, self.y+50, 5, 5))
        pygame.draw.rect(screen, BLUE_DARK, (self.x+10, self.y-15, 30, 15))
        pygame.draw.rect(screen, BLUE_LIGHT, (self.x, self.y-105, 50, 100))
        pygame.draw.rect(screen, BLUE_DARK, (self.x+5, self.y-100, 40, 80))
        pygame.draw.rect(screen, BLACK, (self.x+20, self.y-25, 10, 5))
        pygame.draw.rect(screen, RED, (self.x+5, self.y-110, 40, 5))
        
def Pause():
    global pause
    if pause:
        pause = False
    else:
        pause = True
p = Player()
init = time.time()
def speak():
    global init
    current = int(time.time()-init)
    if current % 2 == 0:
        engine.say(f"speed is: {p.speed}")
        print("speaked")
        try:
            engine.runAndWait()
        except:
            pass


running = True

game_font = pygame.font.SysFont("Ubuntu", 50)
big_font = pygame.font.SysFont("Ubuntu", 255)
target = 50000
engine.say("Ready")
engine.runAndWait()

while True:
    pos = 0
    while running:
        speaker = threading.Thread(target=speak)
        speaker.daemon = True
        speaker.start()
        screen.fill(BLACK)
        if not pause:
            speed = game_font.render(F"speed: {p.speed}", False, WHITE_RED)
            screen.blit(speed, (10, 10))
            distance = game_font.render(F"distance: {target - pos}", False, WHITE_RED)
            screen.blit(distance, (10, 50))
            if len(cars) < 4:
                cars.append(Car())
            for car in cars:
                if car.x+50 >= p.x and car.x <= p.x+50:
                    #pygame.draw.rect(screen, WHITE_RED, (car.x, 0, 50, p.y))
                    #pygame.draw.rect(screen, WHITE_RED, (p.x, 0, 50, p.y))
                    if car.y <= p.y and car.y+50>=p.y:
                        running = False
                car.y += p.speed
                if car.y > height:
                    cars.remove(car)
                car.draw()
            if len(trucks) == 0:
                trucks.append(Truck())
            for truck in trucks:
                if truck.x+50 >= p.x and truck.x <= p.x+50:
                    #pygame.draw.rect(screen, WHITE_RED, (car.x, 0, 50, p.y))
                    #pygame.draw.rect(screen, WHITE_RED, (p.x, 0, 50, p.y))
                    if truck.y <= p.y and truck.y+50>=p.y:
                        running = False
                truck.y += p.speed
                if truck.y > height:
                    trucks.remove(truck)
                truck.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        p.acelarate()
                    if event.key == pygame.K_s:
                        p.brake()
                    if event.key == pygame.K_d:
                        p.x += 50
                    if event.key == pygame.K_a:
                        p.x -= 50
                    if event.key == pygame.K_ESCAPE:
                        Pause()
            p.draw()
            
            pos += p.speed
            time.sleep(0.05)
        if pause:
            pause_message = big_font.render("Pause",False, RED)
            screen.blit(pause_message, (width/2-255, height/2-255/2))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Pause()
        pygame.display.update()
    screen.fill(BLACK)
    game_over = game_font.render("GAME OVER", False, RED)
    screen.blit(game_over, (10,10))
    restart = game_font.render("1 for restart", False, RED)
    screen.blit(restart, (10,50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 or event.key == pygame.K_KP_1:
                for car in cars:
                    cars.remove(car)
                for truck in trucks:
                    trucks.remove(truck)
                del p
                p = Player()
                running = True
    pygame.display.update()