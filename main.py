import pygame
from manager import *
pygame.init()
TILESIZE = 64
WIDTH = TILESIZE * 8
HEIGHT = TILESIZE * 8
clock = pygame.time.Clock()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hyper's Chess Game: White Turn")
background = pygame.transform.scale(pygame.image.load("rect-8x8.png"), (WIDTH, HEIGHT))

manager = Manager() 
tileSelect = None
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if manager.selected == None:
                tileSelect = ((pos[0] // TILESIZE) * TILESIZE, (pos[1] // TILESIZE) * TILESIZE, 64, 64)
                manager.selected = (tileSelect[1] // TILESIZE, tileSelect[0] // TILESIZE)
            else:
                tile = [pos[1] // TILESIZE, pos[0] // TILESIZE]
                manager.confirmMove(tile[0], tile[1])
                manager.selected = None
                tileSelect = None
            
            if manager.whiteTurn == True:
                pygame.display.set_caption("Hyper's Chess Game: White Turn")
            else:
                pygame.display.set_caption("Hyper's Chess Game: Black Turn")
            

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    if tileSelect:
        manager.returnSelected(screen, tileSelect[1] // TILESIZE, tileSelect[0] // TILESIZE)

    manager.draw(screen)
    
    pygame.display.flip()
    clock.tick()

