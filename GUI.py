import pygame
import board
import move
import player
import piece

placeholder = piece.Piece('0')


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
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(CAPTION)
pygame.display.set_icon(pygame.image.load(ICON))
clc = pygame.time.Clock()

# Board
b = board.Board()

all_rects = [[pygame.Rect(j * SQUAREW, i * SQUAREH, SQUAREW, SQUAREH) for j in range(8)] for i in range(8)]
hitboxes = [[pygame.Rect(j * SQUAREW + 4, i * SQUAREH + 4, SQUAREW - 8, SQUAREH - 8) for j in range(8)] for i in
            range(8)]


def drawboard(bd):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, (240, 240, 240), all_rects[i][j])
            else:
                pygame.draw.rect(screen, (100, 100, 100), all_rects[i][j])


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
empty = pygame.image.load('assets/empty.png')


def draw_piece(p, rec):
    if p.name == 'k' and p.color == 'w':
        screen.blit(white_king, rec)
    elif p.name == 'q' and p.color == 'w':
        screen.blit(white_queen, rec)
    elif p.name == 'b' and p.color == 'w':
        screen.blit(white_bishop, rec)
    elif p.name == 'c' and p.color == 'w':
        screen.blit(white_knight, rec)
    elif p.name == 'r' and p.color == 'w':
        screen.blit(white_rook, rec)
    elif p.name == 'p' and p.color == 'w':
        screen.blit(white_pawn, rec)
    elif p.name == 'k' and p.color == 'b':
        screen.blit(black_king, rec)
    elif p.name == 'q' and p.color == 'b':
        screen.blit(black_queen, rec)
    elif p.name == 'b' and p.color == 'b':
        screen.blit(black_bishop, rec)
    elif p.name == 'c' and p.color == 'b':
        screen.blit(black_knight, rec)
    elif p.name == 'r' and p.color == 'b':
        screen.blit(black_rook, rec)
    elif p.name == 'p' and p.color == 'b':
        screen.blit(black_pawn, rec)
    else:
        screen.blit(empty, rec)


def draw_pieces(bd):
    for i in range(8):
        for j in range(8):
            p = b.squares[i][j].p
            draw_piece(p, all_rects[i][j])


# cursor
class Cursor:
    def __init__(self):
        self.p = placeholder
        self.rect = pygame.Rect(0, 0, SQUAREW, SQUAREH)


# Moves
moves = []


def repetition():
    if len(moves) >= 6:
        if moves[-5:-7] == moves[-3:-5] == moves[-1:-3]:
            return True


# Takeback
def takeback():
    if b.last_move != None:
        if len(b.last_move) == 2:
            laststart, lastfinish = b.last_move[0], b.last_move[1]
            backmove = move.Move(b, lastfinish.coord, laststart.coord)
            b.update(backmove)
            b.append_piece(lastfinish.p, *lastfinish.coord)
        if len(b.last_move) == 4:
            laststart1, lastfinish1 = b.last_move[0], b.last_move[1]
            laststart2, lastfinish2 = b.last_move[2], b.last_move[3]
            backmove2 = move.Move(b, lastfinish2.coord, laststart2.coord)
            backmove1 = move.Move(b, lastfinish1.coord, laststart1.coord)
            b.update(backmove2)
            b.update(backmove1)
        if len(b.last_move) == 3:
            laststart, lastfinish = b.last_move[0], b.last_move[1]
            b.append_piece(piece.Pawn(b.last_move[2]), *lastfinish.coord)
            backmove = move.Move(b, lastfinish.coord, laststart.coord)
            b.update(backmove)
            b.append_piece(lastfinish.p, *lastfinish.coord)


# initiation
b.initiate()
player1 = player.Player('Player1', 'w')
player2 = player.Player('Player2', 'b')
cursor = Cursor()
drag, dragging = False, False
selected, select_x, select_y = False, None, None
offset_x, offset_y, start_x, start_y, finish_x, finish_y, rect = 0, 0, None, None, None, None, None
allowed = []
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if moves != [None]:
                    takeback()
                    moves = moves[:-len(b.last_move)//2]
                    b.last_move = moves[-1]
                    allowed = []
                    turn -= 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('Click')
            if event.button == 1:
                mouse_pos = mouse_x, mouse_y = pygame.mouse.get_pos()
                for i in range(8):
                    for j in range(8):
                        rect = hitboxes[i][j]
                        if rect.collidepoint(mouse_x, mouse_y):
                            cursor.rect.center = mouse_pos
                            start_x, start_y = i, j
                            if b.squares[i][j].p.color == plyer.color:
                                drag = True
                                p = b.squares[i][j].p
                                for m in b.allmoves(plyer.color, pos=(i, j)):
                                    allowed.append(m)

        elif event.type == pygame.MOUSEMOTION:
            if drag:
                drag = False
                dragging = True
            if dragging:
                mouse_pos = mouse_x, mouse_y = pygame.mouse.get_pos()
                cursor.rect.center = mouse_pos
                cursor.p = p

        elif event.type == pygame.MOUSEBUTTONUP:
            drag = False
            cursor.p = placeholder
            for i in range(8):
                for j in range(8):
                    sq = all_rects[i][j]
                    if cursor.rect.collidepoint(sq.centerx, sq.centery):
                        finish_x, finish_y = i, j
                        if dragging:
                            dragging = False
                            allowed = []
                            m = move.Move(b, (start_x, start_y), (finish_x, finish_y))
                            print(m, m.finish.p.color)
                            if m.is_legal():
                                print('legal')
                                b.update(m)
                                if b.stalemate(opposite_color(plyer.color)) and repetition():
                                    print('Stalemate! Tie')
                                    run = 0
                                if b.checkmate(opposite_color(plyer.color)):
                                    print('Checkmate! {} wins'.format(plyer.name))
                                    run = 0
                                turn += 1
                        print(start_x, start_y, finish_x, finish_y)
                        if start_x == finish_x and start_y == finish_y and not selected and b.squares[i][
                            j].p.color == plyer.color:
                            print('yes')
                            selected = True
                            select_x, select_y = start_x, start_y
                            for m in b.allmoves(plyer.color, pos=(select_x, select_y)):
                                allowed.append(m)
                        elif start_x == finish_x and start_y == finish_y and selected:
                            print('no')
                            allowed = []
                            selected = False
                            m = move.Move(b, (select_x, select_y), (finish_x, finish_y))
                            if m.is_legal():
                                print('legal')
                                b.update(m)
                                if b.stalemate(opposite_color(plyer.color)) and repetition():
                                    print('Stalemate! Tie')
                                    run = 0
                                if b.checkmate(opposite_color(plyer.color)):
                                    print('Checkmate! {} wins'.format(plyer.name))
                                    run = 0
                                turn += 1
    if moves != []:
        if b.last_move != moves[-1]:
            moves.append(b.last_move)
    else:
        moves.append(b.last_move)
    print(moves)
    # drawing
    drawboard(b)
    for m in allowed:
        pygame.draw.circle(screen, (0, 200, 10), all_rects[m.finish.x][m.finish.y].center, 5)
    draw_pieces(b)
    if dragging:
        color = (240, 240, 240) if (start_x + start_y) % 2 == 0 else (100, 100, 100)
        pygame.draw.rect(screen, color, all_rects[start_x][start_y])
    try:
        draw_piece(cursor.p, cursor.rect)
    except AttributeError:
        pass

    pygame.display.flip()
    clc.tick(FPS)

pygame.quit()
exit()
