import pygame
from pygame import gfxdraw
import time
import sys
import tick
import engine
import constants
import pyautogui

FPS = 120
SCALE = constants.SCALE
scalefactor = 1

currentTime = 0

pygame.init()
screenSize = pyautogui.size()
canvas = pygame.display.set_mode(screenSize)

def drawTrail(objTrail):
    for i in range(len(objTrail.trail)-1):
        pygame.draw.line(canvas, (objTrail.color[0] - (objTrail.color[0]*(1-(i/len(objTrail.trail)))), objTrail.color[1] - (objTrail.color[1]*(1-(i/len(objTrail.trail)))), objTrail.color[2] - (objTrail.color[2]*(1-(i/len(objTrail.trail))))), (int(objTrail.trail[i].x*SCALE + (screenSize[0]/2) + scroll[0]), int(objTrail.trail[i].y*SCALE + (screenSize[1]/2) + scroll[1])), (int(objTrail.trail[i+1].x*SCALE + (screenSize[0]/2) + scroll[0]), int(objTrail.trail[i+1].y*SCALE + (screenSize[1]/2) + scroll[1])), int(objTrail.size*SCALE*scalefactor*(i/len(objTrail.trail))))

scroll = [0, 0]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    tick.tick()
    canvas.fill((0, 0, 0))
    for obj in engine.objects:
        # draw trail
        drawTrail(obj.trail)
        # draw object
        pygame.gfxdraw.filled_circle(canvas, int(obj.position.x*SCALE + (screenSize[0]/2) + scroll[0]), int(obj.position.y*SCALE + (screenSize[1]/2) + scroll[1]), int(obj.size*SCALE*scalefactor), obj.color)
        pygame.gfxdraw.aacircle(canvas, int(obj.position.x*SCALE + (screenSize[0]/2) + scroll[0]), int(obj.position.y*SCALE + (screenSize[1]/2) + scroll[1]), int(obj.size*SCALE*scalefactor), obj.color)
        # label name
        font = pygame.font.SysFont("monospace", 15)
        label = font.render(obj.name, 1, (255, 255, 255))
        canvas.blit(label, (int(obj.position.x*SCALE + (screenSize[0]/2) + scroll[0]), int(obj.position.y*SCALE + (screenSize[1]/2) + scroll[1] - 20)))
    # display time
    currentTime += constants.TIME
    font = pygame.font.SysFont("monospace", 15)
    timeLabel = font.render("Year " + str(round(int(currentTime/31536000))) + ", Day " + str(round(int((currentTime % 31536000)/86400))) + ", Hour " + str(round(int(((currentTime % 31536000)%86400)/3600))), 1, (255, 255, 255))
    canvas.blit(timeLabel, ((screenSize[0]*1/10), (screenSize[1]*6/7)))
    # display scale (1 AU)
    pygame.draw.line(canvas, (255, 255, 255), ((screenSize[0]*1/10), (screenSize[1]*6/7)), ((screenSize[0]*1/10) + 1.496*(10**11)*SCALE, (screenSize[1]*6/7)), 1)
    # display mass density and epsilon
    font = pygame.font.SysFont("monospace", 15)
    massDensityLabel = font.render("Mass Density: " + str(round(engine.massDensity, 2)) + " kg/m^2", 1, (255, 255, 255))
    epsilonLabel = font.render("Epsilon: " + str(round(constants.EPSILON, 2)) + " m", 1, (255, 255, 255))
    canvas.blit(massDensityLabel, ((screenSize[0]*1/10), (screenSize[1]*1/7)))
    canvas.blit(epsilonLabel, ((screenSize[0]*1/10), (screenSize[1]*1.5/7)))
    # display epsilon line
    pygame.draw.line(canvas, (255, 255, 255), ((screenSize[0]*1/10), (screenSize[1]*1.5/7)), ((screenSize[0]*1/10) + constants.EPSILON*SCALE, (screenSize[1]*1.5/7)), 1)
    # move view screen
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        scroll[1] += 10
    if keys[pygame.K_a]:
        scroll[0] += 10
    if keys[pygame.K_s]:
        scroll[1] -= 10
    if keys[pygame.K_d]:
        scroll[0] -= 10
    # rescale screen
    if keys[pygame.K_UP]:
        SCALE *= 1.1
        scroll[0] *= 1.1
        scroll[1] *= 1.1
    if keys[pygame.K_DOWN]:
        SCALE /= 1.1
        scroll[0] /= 1.1
        scroll[1] /= 1.1
    # change time
    if keys[pygame.K_LEFT]:
        constants.setTime(constants.TIME / 1.1)
    if keys[pygame.K_RIGHT]:
        constants.setTime(constants.TIME * 1.1)
    # ESC to quit
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    pygame.display.update()
    time.sleep(1/FPS)

pygame.quit()