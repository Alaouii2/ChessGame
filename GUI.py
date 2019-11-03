import pygame
import board
import move
import player


def opposite_color(color):
    if color == 'b':
        opp = 'w'
    elif color == 'w':
        opp = 'b'
    else:
        opp = '0'
    return opp


SIZE = W, H = 512, 512
CAPTION = 'ChessGame with Python3'
ICON = 'assets/2000px-Chess_Pieces_Sprite_07.png'
SQUARESIZE = SQUAREW, SQUAREH = W // 8, H // 8
FPS = 30

pygame.init()

# Screen
screen = pygame.display.set_mode(SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption(CAPTION)
pygame.display.set_icon(pygame.image.load(ICON))
clc = pygame.time.Clock()

# Board
b = board.Board()

all_rects = [[pygame.Rect(j * SQUAREW, i * SQUAREH, SQUAREW, SQUAREH) for j in range(8)] for i in range(8)]
hitboxes = {}
for i in [0, 1, 6, 7]:
    for j in range(8):
        if i in [0, 1]:
            hitboxes[(i, j, 'b')] = pygame.Rect(j * SQUAREW, i * SQUAREH, SQUAREW, SQUAREH)
        else:
            hitboxes[(i, j,  'w')] = pygame.Rect(j * SQUAREW, i * SQUAREH, SQUAREW, SQUAREH)

def drawboard(bd):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, (240, 240, 240), all_rects[i][j])
            else:
                pygame.draw.rect(screen, (100, 100, 100), all_rects[i][j])


# pieces
white_king = pygame.transform.scale(pygame.image.load('assets/2000px-Chess_Pieces_Sprite_01.png'),  (SQUAREW, SQUAREH))
white_queen = pygame.transform.scale(pygame.image.load('assets/2000px-Chess_Pieces_Sprite_02.png'), (SQUAREW, SQUAREH))
white_bishop = pygame.transform.scale(pygame.image.load('assets/2000px-Chess_Pieces_Sprite_03.png'), (SQUAREW, SQUAREH))
white_knight = pygame.transform.scale(pygame.image.load('assets/2000px-Chess_Pieces_Sprite_04.png'), (SQUAREW, SQUAREH))
white_rook = pygame.transform.scale(pygame.image.load('assets/2000px-Chess_Pieces_Sprite_05.png'), (SQUAREW, SQUAREH))
white_pawn = pygame.transform.scale(pygame.image.load('assets/2000px-Chess_Pieces_Sprite_06.png'), (SQUAREW, SQUAREH))
black_king = pygame.transform.scale(pygame.image.load('assets/2000px-Chess_Pieces_Sprite_07.png'), (SQUAREW, SQUAREH))
black_queen = pygame.transform.scale(pygame.image.load('assets/2000px-Chess_Pieces_Sprite_08.png'), (SQUAREW, SQUAREH))
black_bishop = pygame.transform.scale(pygame.image.load('assets/2000px-Chess_Pieces_Sprite_09.png'), (SQUAREW, SQUAREH))
black_knight = pygame.transform.scale(pygame.image.load('assets/2000px-Chess_Pieces_Sprite_10.png'), (SQUAREW, SQUAREH))
black_rook = pygame.transform.scale(pygame.image.load('assets/2000px-Chess_Pieces_Sprite_11.png'), (SQUAREW, SQUAREH))
black_pawn = pygame.transform.scale(pygame.image.load('assets/2000px-Chess_Pieces_Sprite_12.png'), (SQUAREW, SQUAREH))


def draw_pieces(bd):
    for i in [0, 1, 6, 7]:
        for j in range(8):
            sq = b.squares[i][j]
            if sq.p.name == 'k' and sq.p.color == 'w':
                screen.blit(white_king, hitboxes[(i, j, sq.p.color)])
            if sq.p.name == 'q' and sq.p.color == 'w':
                screen.blit(white_queen, hitboxes[(i, j, sq.p.color)])
            if sq.p.name == 'b' and sq.p.color == 'w':
                screen.blit(white_bishop, hitboxes[(i, j, sq.p.color)])
            if sq.p.name == 'c' and sq.p.color == 'w':
                screen.blit(white_knight, hitboxes[(i, j, sq.p.color)])
            if sq.p.name == 'r' and sq.p.color == 'w':
                screen.blit(white_rook, hitboxes[(i, j, sq.p.color)])
            if sq.p.name == 'p' and sq.p.color == 'w':
                screen.blit(white_pawn, hitboxes[(i, j, sq.p.color)])
            if sq.p.name == 'k' and sq.p.color == 'b':
                screen.blit(black_king, hitboxes[(i, j, sq.p.color)])
            if sq.p.name == 'q' and sq.p.color == 'b':
                screen.blit(black_queen, hitboxes[(i, j, sq.p.color)])
            if sq.p.name == 'b' and sq.p.color == 'b':
                screen.blit(black_bishop, hitboxes[(i, j, sq.p.color)])
            if sq.p.name == 'c' and sq.p.color == 'b':
                screen.blit(black_knight, hitboxes[(i, j, sq.p.color)])
            if sq.p.name == 'r' and sq.p.color == 'b':
                screen.blit(black_rook, hitboxes[(i, j, sq.p.color)])
            if sq.p.name == 'p' and sq.p.color == 'b':
                screen.blit(black_pawn, hitboxes[(i, j, sq.p.color)])


b.initiate()
player1 = player.Player('Player1', 'w')
player2 = player.Player('Player2', 'b')

dragging = False
offset_x, offset_y, start_x, start_y, finish_x, finish_y, rect, init_rect = 0, 0, None, None, None, None, None, None
run = 1
turn = 1

while run:
    if turn % 2 == 1:
        plyer = player1
    else:
        plyer = player2
    color = plyer.color
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('Click')
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i in [0, 1, 6, 7]:
                    for j in range(8):
                        try:
                            rect = hitboxes[(i, j, color)]
                            if rect.collidepoint(mouse_x, mouse_y):
                                print(rect)
                                dragging = True
                                init = start_x, start_y = i, j
                                offset_x = rect.x - mouse_x
                                offset_y = rect.y - mouse_y
                                break
                        except KeyError:
                            continue

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                rect.x = mouse_x + offset_x
                rect.y = mouse_y + offset_y
        elif event.type == pygame.MOUSEBUTTONUP:
            print('Drop')
            if dragging:
                dragging = False
                for i in range(8):
                    for j in range(8):
                        sq = all_rects[i][j]
                        if rect.collidepoint(sq.centerx, sq.centery):
                            print('yes')
                            finish_x, finish_y = i, j
                            m = move.Move(b, (start_x, start_y), (finish_x, finish_y))
                            if m.is_legal():
                                print('legal')
                                rect.center = sq.center
                                b.update(m)
                                if b.stalemate(opposite_color(plyer.color)):
                                    print('Stalemate! Tie')
                                    run = 0
                                if b.checkmate(opposite_color(plyer.color)):
                                    print('Checkmate! {} wins'.format(plyer.name))
                                    run = 0
                                turn += 1
                            else:
                                print(init, rect.x, rect.y)
                                rect.center = all_rects[start_x][start_y].center
    # print(rect)
    drawboard(b)
    draw_pieces(b)
    # for i in range(8):
    #     for j in range(8):
    #         pygame.draw.rect(screen,(200, 0, 0), hitboxes[(i, j]))

    pygame.display.flip()
    clc.tick(FPS)

pygame.quit()
exit()
