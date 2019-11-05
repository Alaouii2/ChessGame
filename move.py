import piece
import square
import copy

placeholder = piece.Piece('0')


def opposite_color(color):
    if color == 'b':
        opp = 'w'
    elif color == 'w':
        opp = 'b'
    else:
        opp = '0'
    return opp


class Move:
    def __init__(self, board, start, finish):
        self.board = board
        self.start = self.board.squares[start[0]][start[1]]
        self.finish = self.board.squares[finish[0]][finish[1]]
        self.en_passant = None
        self.taking = None

    def is_possible(self):
        # same color check
        if self.start.p.color == self.finish.p.color:
            return False

        # white pawn
        if self.start.p.name == 'p' and self.start.p.color == 'w':
            if self.start.x == self.finish.x + 1 and self.start.y == self.finish.y:
                if self.finish.p.color == '0':
                    self.taking = False
                    return True
            if self.start.x == 6:
                if self.start.x == self.finish.x + 2 and self.start.y == self.finish.y:
                    if self.finish.p.color == '0' and self.board.squares[self.start.x - 1][self.start.y].p.color == '0':
                        self.taking = False
                        return True
            if self.start.y == self.finish.y - 1 and self.start.x == self.finish.x + 1:
                self.taking = True
                if self.finish.p.color == 'b':
                    return True
                elif self.start.x == 3:
                    if self.board.moves[-1][1] == square.Square((3, self.start.y - 1), self.start.p):
                        self.taking = True
                        self.en_passant = True
                        return True
            if self.start.y == self.finish.y + 1 and self.start.x == self.finish.x + 1:
                self.taking = True
                if self.finish.p.color == 'b':
                    return True
                elif self.start.x == 3:
                    s = square.Square((3, self.start.y + 1), piece.Pawn('b'))
                    if self.board.moves[-1][0].p.name == s.p.name and self.board.moves[-1][1].coord == s.coord:
                        self.en_passant = True
                        return True
        # black pawn
        if self.start.p.name == 'p' and self.start.p.color == 'b':
            if self.start.x == self.finish.x - 1 and self.start.y == self.finish.y:
                if self.finish.p.color == '0':
                    self.taking = False
                    return True
            if self.start.x == 1:
                if self.start.x == self.finish.x - 2 and self.start.y == self.finish.y:
                    if self.finish.p.color == '0' and self.board.squares[self.start.x + 1][self.start.y].p.color == '0':
                        self.taking = False
                        return True
            if self.start.y == self.finish.y + 1 and self.start.x == self.finish.x - 1:
                self.taking = True
                if self.finish.p.color == 'w':
                    return True
                elif self.start.x == 4:
                    s = square.Square((3, self.start.y - 1), piece.Pawn('b'))
                    if self.board.moves[-1][0].p.name == s.p.name and self.board.moves[-1][1].coord == s.coord:
                        self.taking = True
                        self.en_passant = True
                        return True
            if self.start.y == self.finish.y - 1 and self.start.x == self.finish.x - 1:
                self.taking = True
                if self.finish.p.color == 'w':
                    return True
                elif self.start.x == 6:
                    s = square.Square((3, self.start.y + 1), piece.Pawn('b'))
                    if self.board.moves[-1][0].p.name == s.p.name and self.board.moves[-1][1].coord == s.coord:
                        self.taking = True
                        self.en_passant = True
                        return True

        # cavalier
        if self.start.p.name == 'c':
            l_moves_coord = [(self.start.x + 1, self.start.y + 2), (self.start.x + 2, self.start.y + 1),
                             (self.start.x - 1, self.start.y - 2), (self.start.x - 2, self.start.y - 1),
                             (self.start.x + 1, self.start.y - 2), (self.start.x - 1, self.start.y + 2),
                             (self.start.x + 2, self.start.y - 1), (self.start.x - 2, self.start.y + 1)]
            if self.finish.coord in l_moves_coord:
                self.taking = True
                return True

        # bishop
        if self.start.p.name == 'b':
            return bishop_checker(self)

        # rook
        if self.start.p.name == 'r':
            return rook_checker(self)

        # queen
        if self.start.p.name == 'q':
            if self.start.x + self.start.y == self.finish.x + self.finish.y or self.start.x - self.start.y == self.finish.x - self.finish.y:
                return bishop_checker(self)
            else:
                return rook_checker(self)

        # king
        if self.start.p.name == 'k':
            k_moves_coord = [(self.start.x + 1, self.start.y), (self.start.x - 1, self.start.y),
                             (self.start.x, self.start.y + 1),
                             (self.start.x, self.start.y - 1), (self.start.x + 1, self.start.y + 1),
                             (self.start.x + 1, self.start.y - 1),
                             (self.start.x - 1, self.start.y + 1), (self.start.x - 1, self.start.y - 1), ]
            if self.finish.coord in k_moves_coord:
                self.taking = True
                return True
        return False

    def puts_in_check(self):
        color = self.start.p.color
        board = copy.deepcopy(self.board)
        board.execute(self)
        if board.check(color):
            return True
        return False

    def is_legal(self):
        return ((self.is_possible() or self.king_side_castling()
                or self.queen_side_castling()) and not self.puts_in_check())

    def king_side_castling(self):
        start = self.start
        finish = self.finish
        color = self.start.p.color
        if self.start.p.name == 'k':
            if not self.board.did_king_move[color] and finish.coord ==(start.x, start.y + 2):
                if not self.board.did_rook_move[color][1]:
                    x, y = self.start.coord
                    s1 = self.board.squares[x][y + 1]
                    s2 = self.board.squares[x][y + 2]
                    if all(x.p.color == '0' for x in [s1, s2]) and \
                        all(x not in self.board.range(opposite_color(color)) for x in [start, s1, s2]):
                        return True
        return False

    def queen_side_castling(self):
        start = self.start
        finish = self.finish
        color = self.start.p.color
        if self.start.p.name == 'k':
                if not self.board.did_king_move[color] and finish.coord ==(start.x, start.y - 2):
                    if not self.board.did_rook_move[color][0]:
                        x, y = self.start.coord
                        s1 = self.board.squares[x][y - 1]
                        s2 = self.board.squares[x][y - 2]
                        s3 = self.board.squares[x][y - 3]
                        if all(x.p.color == '0' for x in [s1, s2, s3]) and \
                                all(x not in self.board.range(opposite_color(color)) for x in [start, s1, s2]):
                            return True
        return False

    def __repr__(self):
        return 'move:{},{}'.format(self.start, self.finish)


def bishop_checker(move):
    if move.start.x - move.start.y == move.finish.x - move.finish.y:
        if move.start.x > move.finish.x:
            for i in range(move.start.x - 1, move.finish.x - 1, -1):
                if move.board.squares[i][move.start.y - move.start.x + i].p.color != '0':
                    if move.board.squares[i][move.start.y - move.start.x + i].p.color != move.start.p.color \
                            and move.finish.coord == (i, move.start.y - move.start.x + i):
                        move.taking = True
                        return True
                    else:
                        return False
                move.taking = True
                return True
        elif move.start.x < move.finish.x:
            for i in range(move.start.x + 1, move.finish.x + 1):
                if move.board.squares[i][move.start.y - move.start.x + i].p.color != '0':
                    if move.board.squares[i][move.start.y - move.start.x + i].p.color != move.start.p.color \
                            and move.finish.coord == (i, move.start.y - move.start.x + i):
                        move.taking = True
                        return True
                    else:
                        return False
                move.taking = True
                return True
    if move.start.x + move.start.y == move.finish.x + move.finish.y:
        if move.start.x > move.finish.x:
            for i in range(move.start.x - 1, move.finish.x - 1, -1):
                if move.board.squares[i][move.start.x + move.start.y - i].p.color != '0':
                    if move.board.squares[i][move.start.x + move.start.y - i].p.color != move.start.p.color \
                            and move.finish.coord == (i, move.start.x + move.start.y - i):
                        move.taking = True
                        return True
                    else:
                        return False
                move.taking = True
                return True
        elif move.start.x < move.finish.x:
            for i in range(move.start.x + 1, move.finish.x + 1):
                if move.board.squares[i][move.start.x + move.start.y - i].p.color != '0':
                    if move.board.squares[i][
                        move.start.x + move.start.y - i].p.color != move.start.p.color \
                            and move.finish.coord == (i, move.start.x + move.start.y - i):
                        move.taking = True
                        return True
                    else:
                        return False
                move.taking = True
                return True
    return False


def rook_checker(move):
    if move.start.x == move.finish.x:
        if move.start.y > move.finish.y:
            for i in range(move.start.y - 1, move.finish.y - 1, -1):
                if move.board.squares[move.start.x][i].p.color != '0':
                    if move.board.squares[move.start.x][i].p.color != move.start.p.color \
                            and move.finish.coord == (move.start.x, i):
                        move.taking = True
                        return True
                    else:
                        return False
                move.taking = True
                return True
        elif move.start.y < move.finish.y:
            for i in range(move.start.y + 1, move.finish.y + 1):
                if move.board.squares[move.start.x][i].p.color != '0':
                    if move.board.squares[move.start.x][i].p.color != move.start.p.color \
                            and move.finish.coord == (move.start.x, i):
                        move.taking = True
                        return True
                    else:
                        return False
                move.taking = True
                return True
    elif move.start.y == move.finish.y:
        if move.start.x > move.finish.x:
            for i in range(move.start.x - 1, move.finish.x - 1, -1):
                if move.board.squares[i][move.start.y].p.color != '0':
                    if move.board.squares[i][move.start.y].p.color != move.start.p.color \
                            and move.finish.coord == (i, move.start.y):
                        move.taking = True
                        return True
                    else:
                        return False
                move.taking = True
                return True
        if move.start.x < move.finish.x:
            for i in range(move.start.x + 1, move.finish.x + 1):
                if move.board.squares[i][move.start.y].p.color != '0':
                    if move.board.squares[i][move.start.y].p.color != move.start.p.color \
                            and move.finish.coord == (i, move.start.y):
                        move.taking = True
                        return True
                    else:
                        return False
                move.taking = True
                return True
    return False

