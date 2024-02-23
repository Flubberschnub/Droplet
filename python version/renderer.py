import pygame
from pygame import gfxdraw
import time
import sys
import tick
import engine
import constants
import pyautogui
import barneshut
import preferences

FPS = 120
SCALE = constants.SCALE
scalefactor = 1

currentTime = 0
system_last_time = time.time()

pygame.init()
screenSize = pyautogui.size()
canvas = pygame.display.set_mode(screenSize)

def drawTrail(objTrail):
    """
    Draw the trail of an object on the canvas.

    Args:
        objTrail: The object trail to be drawn.

    Returns:
        None
    """

    for i in range(len(objTrail.trail)-1):
        pygame.draw.line(canvas, (objTrail.color[0] - (objTrail.color[0]*(1-(i/len(objTrail.trail)))), objTrail.color[1] - (objTrail.color[1]*(1-(i/len(objTrail.trail)))), objTrail.color[2] - (objTrail.color[2]*(1-(i/len(objTrail.trail))))), (int(objTrail.trail[i].x*SCALE + (screenSize[0]/2) + scroll[0]), int(objTrail.trail[i].y*SCALE + (screenSize[1]/2) + scroll[1])), (int(objTrail.trail[i+1].x*SCALE + (screenSize[0]/2) + scroll[0]), int(objTrail.trail[i+1].y*SCALE + (screenSize[1]/2) + scroll[1])), int(objTrail.size*SCALE*scalefactor*(i/len(objTrail.trail))))


def clampInt(num, low, high):
    return max(low, min(num, high))

def drawQuad(quad):
    if quad.children[0] != None:
        drawQuad(quad.children[0])
    if quad.children[1] != None:
        drawQuad(quad.children[1])
    if quad.children[2] != None:
        drawQuad(quad.children[2])
    if quad.children[3] != None:
        drawQuad(quad.children[3])
    # Only draw if on screen and not too small
    if -32767 <= int(quad.x*SCALE + (screenSize[0]/2) + scroll[0]) <= 32767 and -32767 <= int(quad.y*SCALE + (screenSize[1]/2) + scroll[1]) <= 32767 and quad.width*SCALE > 1:
        pygame.draw.rect(canvas, (0, 255, 0), (int((quad.x - quad.width/2)*SCALE + (screenSize[0]/2) + scroll[0]), int((quad.y - quad.height/2)*SCALE + (screenSize[1]/2) + scroll[1]), int(quad.width*SCALE), int(quad.height*SCALE)), 1)
        # draw center of mass if cursor is inside quad
        if ((quad.x*SCALE + (screenSize[0]/2) + scroll[0] - pygame.mouse.get_pos()[0])**2 + (quad.y*SCALE + (screenSize[1]/2) + scroll[1] - pygame.mouse.get_pos()[1])**2 <= 100):
            pygame.gfxdraw.filled_circle(canvas, int(quad.center_of_mass_x*SCALE + (screenSize[0]/2) + scroll[0]), int(quad.center_of_mass_y*SCALE + (screenSize[1]/2) + scroll[1]), int(quad.mass**0.03)*2, (255, 0, 0))

scroll = [0, 0]
lockedObject = None
while True:
    clickPos = None
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONUP:
            clickPos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    tick.tick()
    if lockedObject != None:
        scroll[0] = -(lockedObject.position.x*SCALE)
        scroll[1] = -(lockedObject.position.y*SCALE)
    canvas.fill((0, 0, 0))

    #Visualize Partitioning
    if preferences.visualizePartitioning:
        drawQuad(engine.quadtree)

    for obj in engine.objects:
        # draw object if on screen
        if -32767 <= int(obj.position.x*SCALE + (screenSize[0]/2) + scroll[0]) <= 32767 and -32767 <= int(obj.position.y*SCALE + (screenSize[1]/2) + scroll[1]) <= 32767:
            # draw trail
            if preferences.displayTrails:
                drawTrail(obj.trail)
            if preferences.displayObjects:
                pygame.gfxdraw.filled_circle(canvas, clampInt(int(obj.position.x*SCALE + (screenSize[0]/2) + scroll[0]), -32767, 32767), clampInt(int(obj.position.y*SCALE + (screenSize[1]/2) + scroll[1]), -32767, 32767), clampInt(int(obj.size*SCALE*scalefactor), -32767, 32767), obj.color)
                pygame.gfxdraw.aacircle(canvas, clampInt(int(obj.position.x*SCALE + (screenSize[0]/2) + scroll[0]), -32767, 32767), clampInt(int(obj.position.y*SCALE + (screenSize[1]/2) + scroll[1]), -32767, 32767), clampInt(int(obj.size*SCALE*scalefactor), -32767, 32767), obj.color)
            # label name
            if preferences.displayNames:
                font = pygame.font.SysFont("monospace", 15)
                label = font.render(obj.name, 1, (255, 255, 255))
                canvas.blit(label, (int(obj.position.x*SCALE + (screenSize[0]/2) + scroll[0]), int(obj.position.y*SCALE + (screenSize[1]/2) + scroll[1] - 20)))
        # if clicked, lock object
        if clickPos != None:
            if (obj.position.x*SCALE + (screenSize[0]/2) + scroll[0] - clickPos[0])**2 + (obj.position.y*SCALE + (screenSize[1]/2) + scroll[1] - clickPos[1])**2 <= (obj.size*SCALE*scalefactor)**2 + 20:
                lockedObject = obj
        if obj is lockedObject:
            pygame.gfxdraw.aacircle(canvas, int(obj.position.x*SCALE + (screenSize[0]/2) + scroll[0]), int(obj.position.y*SCALE + (screenSize[1]/2) + scroll[1]), 20, (255, 255, 255))
            # display information about locked object on the right side of screen
            font = pygame.font.SysFont("monospace", 15)
            mainLabel = font.render(obj.name + ":", 1, (0, 255, 0))
            massLabel = font.render("Mass: " + str(round(obj.mass, 2)) + " kg", 1, (0, 150, 0))
            velocityLabel = font.render("Velocity: " + str(round(obj.velocity.getMagnitude(), 2)) + " m/s", 1, (0, 150, 0))
            diameterLabel = font.render("Diameter: " + str(round(obj.size*2, 2)) + " m", 1, (0, 150, 0))
            canvas.blit(mainLabel, ((screenSize[0]*8/10), (screenSize[1]*1/7 - 20)))
            canvas.blit(massLabel, ((screenSize[0]*8/10), (screenSize[1]*1/7)))
            canvas.blit(velocityLabel, ((screenSize[0]*8/10), (screenSize[1]*1/7 + 20)))
            canvas.blit(diameterLabel, ((screenSize[0]*8/10), (screenSize[1]*1/7 + 40)))
    # display time
    currentTime += constants.TIME
    font = pygame.font.SysFont("monospace", 15)
    timeLabel = font.render("Year " + str(round(int(currentTime/31536000))) + ", Day " + str(round(int((currentTime % 31536000)/86400))) + ", Hour " + str(round(int(((currentTime % 31536000)%86400)/3600))), 1, (255, 255, 255))
    canvas.blit(timeLabel, ((screenSize[0]*1/10), (screenSize[1]*6/7)))
    # display scale (1 Gigameter) with label
    font = pygame.font.SysFont("monospace", 15)
    scaleLabel = font.render("1 Gigameter", 1, (255, 255, 255))
    canvas.blit(scaleLabel, ((screenSize[0]*1/10), (screenSize[1]*6/7 - 40)))
    pygame.draw.line(canvas, (255, 255, 255), ((screenSize[0]*1/10), (screenSize[1]*6/7) - 20), ((screenSize[0]*1/10) + 1*(10**9)*SCALE, (screenSize[1]*6/7) - 20), 1)
    # display scale (1 AU) with label
    font = pygame.font.SysFont("monospace", 15)
    scaleLabel = font.render("1 AU", 1, (255, 255, 255))
    canvas.blit(scaleLabel, ((screenSize[0]*1/10), (screenSize[1]*6/7 - 20)))
    pygame.draw.line(canvas, (255, 255, 255), ((screenSize[0]*1/10), (screenSize[1]*6/7)), ((screenSize[0]*1/10) + 1.496*(10**11)*SCALE, (screenSize[1]*6/7)), 1)
    # display mass density and epsilon
    font = pygame.font.SysFont("monospace", 15)
    massDensityLabel = font.render("Mass Density: " + str(round(engine.massDensity, 2)) + " kg/m^2", 1, (255, 255, 255))
    epsilonLabel = font.render("Epsilon: " + str(round(constants.EPSILON, 2)) + " m", 1, (255, 255, 255))
    canvas.blit(massDensityLabel, ((screenSize[0]*1/10), (screenSize[1]*1/7)))
    canvas.blit(epsilonLabel, ((screenSize[0]*1/10), (screenSize[1]*1.5/7)))
    # display epsilon line
    pygame.draw.line(canvas, (255, 255, 255), ((screenSize[0]*1/10), (screenSize[1]*1.5/7)), ((screenSize[0]*1/10) + constants.EPSILON*SCALE, (screenSize[1]*1.5/7)), 1)
    # display frames per second
    font = pygame.font.SysFont("monospace", 15)
    rightAdjustment = len(str(int(1/(time.time() - system_last_time))) + " FPS")
    fpsLabel = font.render( str(int(1/(time.time() - system_last_time))) + " FPS", 1, (255, 255, 255))
    canvas.blit(fpsLabel, ((screenSize[0]*9/10)-10*rightAdjustment, (screenSize[1]*6/7)))
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
    # CTRL to unlock
    if keys[pygame.K_LCTRL]:
        lockedObject = None
    # ESC to quit
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    pygame.display.update()
    time.sleep(1/FPS)
    # debug print actual frames per second
    print(1/(time.time() - system_last_time))
    # display frames per second
    system_last_time = time.time()


pygame.quit()
