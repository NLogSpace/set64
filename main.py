import pygame
import sys
import random
import time

pygame.init()

pygame.font.init()
font = pygame.font.Font(None, 72)

screen = pygame.display.set_mode((1050, 1000))

colors = [(255, 0, 0), (0, 255, 0), (0, 255, 255), (255, 255, 0)]
white = (255, 255, 255)
card_background = (50, 50, 50)

class Card:
    def __init__(self, shape, color, filling):
        self.shape = shape
        self.color = color
        self.filling = filling
        self.image = draw_card(shape, color, filling)

def check_attribute(extensions):
    counter = dict()
    for x in extensions:
        if x in counter:
            counter[x] += 1
        else:
            counter[x] = 1
    if sorted(list(counter.values())) not in [[1, 1, 1, 1], [2, 2], [4]]:
        return False
    return True
        
def check_set(cards):
    if len(cards) != 4:
        raise ValueError("Set candidates must consist of exactly four cards.")
    shapes = [card.shape for card in cards]
    colors = [card.color for card in cards]
    fillings = [card.filling for card in cards]
    return check_attribute(shapes) and check_attribute(colors) and check_attribute(fillings)

def draw_card(shape, color, filling):
    card = pygame.Surface((200, 200), pygame.SRCALPHA)
    card.fill(card_background)

    # draw shape
    shape_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
    if shape == 0:
        pygame.draw.rect(shape_surface, white, (50, 50, 100, 100))
    elif shape == 1:
        pygame.draw.polygon(shape_surface, white, [(100, 50), (150, 100), (100, 150), (50, 100)])
    elif shape == 2:
        pygame.draw.polygon(shape_surface, white, [(80, 50), (120, 50), (120, 80), (150, 80), (150, 120), (120, 120), (120, 150), (80, 150), (80, 120), (50, 120), (50, 80), (80, 80)])
    elif shape == 3:
        pygame.draw.circle(shape_surface, white, (100, 100), 50)

    # draw filling
    fill_surface = pygame.Surface((200, 200))
    fill_surface.fill(card_background)
    if filling == 0:
        fill_surface.fill(colors[color])
    elif filling == 1:
        for i in range(20):
            pygame.draw.line(fill_surface, colors[color], (i*10, 0), (i*10, 200))
    elif filling == 2:
        for i in range(20):
            for j in range(20):
                pygame.draw.circle(fill_surface, colors[color], (i*10, j*10), 2)
    elif filling == 3:
        pass
    
    shape_surface.blit(fill_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    card.blit(shape_surface, (0, 0))

    # draw outline
    if shape == 0:
        pygame.draw.rect(card, colors[color], (50, 50, 100, 100), 5)
    elif shape == 1:
        pygame.draw.polygon(card, colors[color], [(100, 50), (150, 100), (100, 150), (50, 100)], 5)
    elif shape == 2:
        pygame.draw.polygon(card, colors[color], [(80, 50), (120, 50), (120, 80), (150, 80), (150, 120), (120, 120), (120, 150), (80, 150), (80, 120), (50, 120), (50, 80), (80, 80)], 5)
    elif shape == 3:
        pygame.draw.circle(card, colors[color], (100, 100), 50, 5)

    return card

cards = None
table = None
selection = None
game_over = False
start_time = None

def reset_game():
    global cards
    global table
    global selection
    global game_over
    global start_time

    cards = []
    for i in range(4):
        for j in range(4):
            for k in range(4):
                cards.append(Card(i, j, k))

    random.shuffle(cards)

    table = []                
    selection = []
    for i in range(12):
        table.append(cards.pop())

    game_over = False
    start_time = time.time()

reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                x = (event.pos[0]-25) // 250
                y = (event.pos[1]-25) // 250
                index = x+4*y
                if index >= 0 and index < 12:
                    if index in selection:
                        selection.remove(index)
                    else:
                        selection.append(index)
                    if len(selection) == 4:
                        candidate = [table[i] for i in selection]
                        if check_set(candidate):
                            if len(cards) >= 4:
                                for i in selection:
                                    table[i] = cards.pop()
                                selection = []
                            else:
                                game_over = True
                                end_time = time.time()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    screen.fill((0, 0, 0))
    for y in range(3):
        for x in range(4):
            screen.blit(table[4*y+x].image, (250*x+50, 250*y+50))

    for i in selection:
        x = i % 4
        y = i // 4
        pygame.draw.rect(screen, white, (250*x+40, 250*y+40, 220, 220), 10)

    if game_over:
        time_to_display = end_time - start_time
    else:
        time_to_display = time.time() - start_time
    time_to_display = int(time_to_display)

    timer_surface = font.render(str(time_to_display), True, white)
    screen.blit(timer_surface, (200, 900))
            
    pygame.display.flip()
