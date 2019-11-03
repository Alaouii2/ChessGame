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

def main():
    b = board.Board()
    run = 1
    player1 = player.Player('Player1', 'w')
    player2 = player.Player('Player2', 'b')
    while run:
        b.initiate()
        turn = 0
        while True:
            turn += 1
            print('turn ', turn)
            if turn % 2 == 1:
                plyer = player1
            else:
                plyer = player2
            while True:
                print(b)
                print('pick a piece: ')
                while True:
                    try:
                        start_x = int(input('pick a row: '))
                        if not 0 <= start_x <= 7:
                            raise ValueError
                    except ValueError:
                        print('Invalid input')
                        continue
                    else:
                        break
                while True:
                    try:
                        start_y = int(input('pick a column: '))
                        if not 0 <= start_y <= 7:
                            raise ValueError
                    except ValueError:
                        print('Invalid input')
                        continue
                    else:
                        break
                sq = b.squares[start_x][start_y]
                print(sq)
                if sq.p.color != plyer.color:
                    print('invalid input')
                    continue
                else:
                    while True:
                        print('pick a destination: ')
                        while True:
                            try:
                                finish_x = int(input('pick a row: '))
                                if not 0 <= finish_x <= 7:
                                    raise ValueError
                            except ValueError:
                                print('Invalid input')
                                continue
                            else:
                                break
                        while True:
                            try:
                                finish_y = int(input('pick a column: '))
                                if not 0 <= finish_y <= 7:
                                    raise ValueError
                            except ValueError:
                                print('Invalid input')
                                continue
                            else:
                                break
                        print(finish_x, finish_y)
                        m = move.Move(b, (start_x, start_y), (finish_x, finish_y))
                        if not m.is_legal():
                            print('invalid input')
                            continue
                        else:
                            b.update(m)
                            break
                break
            if b.stalemate(opposite_color(plyer.color)):
                print('Stalemate! Tie')
                while True:
                    try:
                        inp = input('Replay? [y/n]')
                        if inp not in ['y', 'n']:
                            raise ValueError
                    except ValueError:
                        print('Invalid input')
                        continue
                    else:
                        if inp == 'y':
                            break
                        else:
                            exit()
                break
            if b.checkmate(opposite_color(plyer.color)):
                print('Checkmate! {} wins'.format(plyer.name))
                while True:
                    try:
                        inp = input('Replay? [y/n]')
                        if not inp in ['y', 'n']:
                            raise ValueError
                    except ValueError:
                        print('Invalid input')
                        continue
                    else:
                        if inp == 'y':
                            break
                        else:
                            exit()
                break


if __name__ == '__main__':
    main()
