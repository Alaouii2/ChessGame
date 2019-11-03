import pygame
import board

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


def rect(s):
    top, left = s.x * SQUAREH, s.y * SQUAREW
    return pygame.Rect(left, top, SQUAREW, SQUAREH)


def drawboard(bd):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, (240, 240, 240), rect(bd.squares[i][j]))
            else:
                pygame.draw.rect(screen, (100, 100, 100), rect(bd.squares[i][j]))


# pieces
white_king = pygame.transform.scale(pygame.image.load('assets/2000px-Chess_Pieces_Sprite_01.png'), (SQUAREW, SQUAREH))
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
    for i in range(8):
        for j in range(8):
            sq = bd.squares[i][j]
            if sq.p.name == 'k' and sq.p.color == 'w':
                screen.blit(white_king, rect(sq))
            if sq.p.name == 'q' and sq.p.color == 'w':
                screen.blit(white_queen, rect(sq))
            if sq.p.name == 'b' and sq.p.color == 'w':
                screen.blit(white_bishop, rect(sq))
            if sq.p.name == 'c' and sq.p.color == 'w':
                screen.blit(white_knight, rect(sq))
            if sq.p.name == 'r' and sq.p.color == 'w':
                screen.blit(white_rook, rect(sq))
            if sq.p.name == 'p' and sq.p.color == 'w':
                screen.blit(white_pawn, rect(sq))
            if sq.p.name == 'k' and sq.p.color == 'b':
                screen.blit(black_king, rect(sq))
            if sq.p.name == 'q' and sq.p.color == 'b':
                screen.blit(black_queen, rect(sq))
            if sq.p.name == 'b' and sq.p.color == 'b':
                screen.blit(black_rook, rect(sq))
            if sq.p.name == 'c' and sq.p.color == 'b':
                screen.blit(black_knight, rect(sq))
            if sq.p.name == 'r' and sq.p.color == 'b':
                screen.blit(black_rook, rect(sq))
            if sq.p.name == 'p' and sq.p.color == 'b':
                screen.blit(black_pawn, rect(sq))


b.initiate()

run = 1

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0

    drawboard(b)
    draw_pieces(b)
    pygame.display.flip()
    clc.tick(FPS)

pygame.quit()
exit()
