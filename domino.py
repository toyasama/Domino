import itertools
import random


def highest_double(liste):
    double = "none"
    for value in liste:
        if value[0] == value[1]:
            chiffre = value[0]
            if double == 'none':
                double = chiffre
            else:
                if double < chiffre:
                    double = chiffre
    return double


def starting_player(player1, player2):
    double_player1 = highest_double(player1)
    double_player2 = highest_double(player2)
    if double_player1 == 'none' and double_player2 == 'none':
        return 'shuffle', []
    elif double_player1 != 'none' and double_player2 == 'none':
        player1.remove([double_player1, double_player1])
        return 'computer', [double_player1, double_player1]
    elif double_player1 == 'none' and double_player2 != 'none':
        player2.remove([double_player2, double_player2])
        return 'player', [double_player2, double_player2]
    else:
        if double_player1 > double_player2:
            player1.remove([double_player1, double_player1])
            return 'computer', [double_player1, double_player1]
        else:
            player2.remove([double_player2, double_player2])
            return 'player', [double_player2, double_player2]


def shuffle_pieces(pieces):
    computer_pieces = []
    player_pieces = []
    stock_pieces = []
    while len(pieces) >= 22:
        number = random.randrange(0, len(pieces))
        if len(pieces) > 35:
            if random.random() <= 0.5 and len(computer_pieces) < 7:
                computer_pieces.append(pieces[number])
                del pieces[number]
            elif len(player_pieces) < 7:
                player_pieces.append(pieces[number])
                del pieces[number]
        elif len(pieces) > 21:
            stock_pieces.append(pieces[number])
            del pieces[number]
    return computer_pieces, player_pieces, stock_pieces


def init_pieces():
    status = 'shuffle'
    while status == 'shuffle':
        domino_snake = []
        pieces = [[x, y] for x in range(7) for y in range(7)]
        computer_pieces, player_pieces, stock_pieces = shuffle_pieces(pieces)
        status, starting_pieces = starting_player(player_pieces, computer_pieces)
        domino_snake.append(starting_pieces)
    # print(computer_pieces)
    # print(player_pieces)
    # print(stock_pieces)
    # print(domino_snake)
    return computer_pieces, player_pieces, stock_pieces, domino_snake, status


def val_input(piece):
    while 1:
        x = input()
        try:
            x = int(x)
            if abs(x) <= len(piece):
                break
            else:
                print("Invalid input. Please try again.")
        except:
            print("Invalid input. Please try again.")
    return x


def extra_piece(piece, stock):
    if len(stock) != 0:
        number = random.randrange(0, len(stock))
        piece.append(stock[number])
        del stock[number]
    return piece, stock


def turn_domino(liste):
    save = liste[0]
    liste = [liste[1], save]
    return liste


def legal_move(pieces, snake, pos,player):
    left_number = snake[0][0]
    right_number = snake[-1][-1]
    valid_move = True

    if pos < 0 and left_number in pieces[abs(pos) - 1]:
        if pieces[abs(pos) - 1][1] == left_number:
            snake.insert(0, pieces[abs(pos) - 1])
            del pieces[abs(pos) - 1]
        elif pieces[abs(pos) - 1][0] == left_number:
            domino = turn_domino(pieces[abs(pos) - 1])
            snake.insert(0, domino)
            del pieces[abs(pos) - 1]
        valid_move = False

    elif pos > 0 and right_number in pieces[abs(pos) - 1]:
        if pieces[abs(pos) - 1][0] == right_number:
            snake.append(pieces[abs(pos) - 1])
            del pieces[abs(pos) - 1]
        elif pieces[abs(pos) - 1][1] == right_number:
            domino = turn_domino(pieces[abs(pos) - 1])
            snake.append(domino)
            del pieces[abs(pos) - 1]
        valid_move = False

    else:
        if player == "player":
            print("Illegal move. Please try again.")

    return pieces, snake, valid_move


def player_turn(player_pieces, domino_snake, stock):
    end = True
    while end:
        value = val_input(player_pieces)
        if value == 0:
            player_pieces, stock = extra_piece(player_pieces, stock)
            end = False
        else:
            player_pieces, domino_snake, end = legal_move(player_pieces, domino_snake, value, 'player')

    return player_pieces, domino_snake, stock


def new_status(computer_pieces, player_pieces, stock_pieces, domino_snake, status):
    if status == "computer":
        print("\nStatus: Computer is about to make a move. Press Enter to continue...")
        computer_pieces, domino_snake, stock_pieces = computer_turn(computer_pieces, domino_snake, stock_pieces)
        status = "player"
    elif status == 'player':
        print("\nStatus: It's your turn to make a move. Enter your command.")
        player_pieces, domino_snake, stock_pieces = player_turn(player_pieces, domino_snake, stock_pieces)
        status = 'computer'
    return status


def field(computer_pieces, player_pieces, stock_pieces, domino_snake):
    header = ''
    for i in range(70):  header = header + '='
    print(header)
    print('Stock size:', len(stock_pieces))
    print('Computer pieces:', len(computer_pieces))
    print()
    if len(domino_snake) < 7:
        for i in range(len(domino_snake)):
            if i == len(domino_snake) - 1:
                print(domino_snake[i])
            else:
                print(domino_snake[i], end='')

    else:
        for i in range(len(domino_snake)):
            if i < 3:
                print(domino_snake[i], end='')
            elif i == len(domino_snake) - 5:
                print('...', end='')
            elif i > len(domino_snake) - 4:
                print(domino_snake[i], end='')
            elif i == len(domino_snake) - 1:
                print(domino_snake[i])

    print()
    print('Your pieces:')
    for i in range(len(player_pieces)):
        show = str(i + 1) + ':'
        print(show, player_pieces[i])


def end_game(p_pieces, c_pieces, snake):
    win = ''
    if snake[0][0] == snake[-1][-1]:
        count = 0
        for domino in snake:
            for chiffre in domino:
                if chiffre == snake[0][0]:
                    count += 1
        if count == 8:
            win = 'draw'
    if len(p_pieces) == 0:
        win = 'player'
    elif len(c_pieces) == 0:
        win = 'computer'
    return win




# ---------------------------------------AI------------------------------------------------

def count_numbers(piece,snake):
    count_dict = {}
    for i in range(7):
        count = 0
        for domino1,domino2 in itertools.zip_longest(piece,snake,fillvalue=[]) :
            count += domino1.count(i) + domino2.count(i)
        count_dict[i] = count
    
    return count_dict

def domino_score(piece,snake):
    number_dict = count_numbers(piece,snake)
    score_list = []

    for domino in piece :
        score = 0
        for i in domino :
            score += number_dict[i]
        score_list.append((score,domino))
    score_list.sort(reverse=True)
    return score_list

def ai_legal_move(domino,snake,piece):
    left_number = snake[0][0]
    right_number = snake[-1][-1]
    valid_move = False

    if left_number in domino:
        if domino[-1] == left_number:
            snake.insert(0, domino)
            piece.remove(domino)
        elif domino[0] == left_number:
            piece.remove(domino)
            domino = turn_domino(domino)
            snake.insert(0, domino)
        valid_move = True

    elif right_number in domino:
        if domino[0] == right_number:
            snake.append(domino)
            piece.remove(domino)    
        elif domino[-1] == right_number:
            piece.remove(domino)
            domino = turn_domino(domino)
            snake.append(domino)
        valid_move = True


    return piece, snake, valid_move

def computer_turn(computer_piece, domino_snake, stock):
    input()

    skip = False
    sorted_piece = domino_score(computer_piece,domino_snake)
    print('c',computer_piece)
    print('s',sorted_piece)
    for tuple in sorted_piece :
        print(tuple[1])
        computer_piece, domino_snake,skip = ai_legal_move(tuple[1], domino_snake,computer_piece)
        if skip :
            break
    
    if skip == False :
        computer_piece, stock = extra_piece(computer_piece,stock)



    # if len(stock) != 0:
    #     while end:
    #         number = random.randrange(-len(computer_piece) + 1, len(computer_piece))
    #         if number == 0:
    #             computer_piece, stock = extra_piece(computer_piece,stock)
    #             end = False
    #         else:
    #             computer_piece, domino_snake, end = legal_move(computer_piece, domino_snake, number,'c')
    # else:
    #     number = -len(computer_piece)
    #     while end and number <= len(computer_piece):
    #         #print(number)
    #         computer_piece, domino_snake, end = legal_move(computer_piece, domino_snake, number,'c')
    #         number += 1
    return computer_piece, domino_snake, stock


if __name__ == "__main__":
    computer_pieces, player_pieces, stock_pieces, domino_snake, status = init_pieces()
    end = False
    while not end:
        field(computer_pieces, player_pieces, stock_pieces, domino_snake)
        win = end_game(player_pieces, computer_pieces, domino_snake)
        if win == 'draw':
            print("Status: The game is over. It's a draw!")
            end = True
            break
        elif win == 'player':
            print("Status: The game is over. You won!")
            end = True
            break
        elif win == 'computer':
            print("Status: The game is over. The computer won!")
            end = True
            break
        status = new_status(computer_pieces, player_pieces, stock_pieces, domino_snake, status)


