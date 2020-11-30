import random
import copy


def choose_the_game():
    options = True
    while options != 'exit':
        options = input('Input command: ').split(' ')
        while not analyze_options(options):
            options = input('Input command: ').split(' ')
        if options[0] == 'exit':
            exit()

        play_the_game(options)


def analyze_options(options):
    players = ['user', 'easy', 'medium', 'hard']
    if len(options) == 1 and options[0] == 'exit':
        return True
    elif len(options) == 3 and options[0] == 'start':
        if options[1] in players and options[2] in players:
            return True
    print('Bad parameters!')
    return False


def play_the_game(options):
    player_X = options[1]
    player_O = options[2]
    cells = [' ', ' ', ' ',
             ' ', ' ', ' ',
             ' ', ' ', ' ']
    show_the_field(cells)

    game_state = {'free': [0, 1, 2,
                           3, 4, 5,
                           6, 7, 8],
                  'occupied': []}

    sign = 'O'
    end_of_the_game = False
    while not end_of_the_game:
        if sign == 'O':
            sign = 'X'
            if player_X == 'user':
                the_turn = user_play(cells)
            elif player_X == 'easy':
                the_turn = ai_make_turn(game_state)
            elif player_X == 'medium':
                the_turn = ai_medium_make_turn(game_state, cells, sign)
            elif player_X == 'hard':
                if cells.count(' ') == 9:
                    the_turn = ai_make_turn(game_state)
                else:
                    the_turn = minimax(cells, game_state, sign)[1]
        else:
            sign = 'O'
            if player_O == 'user':
                the_turn = user_play(cells)
            elif player_O == 'easy':
                the_turn = ai_make_turn(game_state)
            elif player_O == 'medium':
                the_turn = ai_medium_make_turn(game_state, cells, sign)
            elif player_O == 'hard':
                the_turn = minimax(cells, game_state, sign)[1]

        cells[the_turn] = sign
        game_state['free'].remove(the_turn)
        game_state['occupied'].append(the_turn)
        show_the_field(cells)
        end_of_the_game = check_the_winner(cells, game_state)
    print(end_of_the_game)


def minimax(board, game_state, player):
    avail_spots = copy.deepcopy(game_state['free'])
    new_game_state = copy.deepcopy(game_state)

    if player == 'O':
        if check_the_winner(board, game_state) == "O wins":
            return [10, ' ']
        elif check_the_winner(board, game_state) == "X wins":
            return [-10, ' ']
        elif len(avail_spots) == 0:
            return [0, ' ']
    else:
        if check_the_winner(board, game_state) == "X wins":
            return [10, ' ']
        elif check_the_winner(board, game_state) == "O wins":
            return [-10, ' ']
        elif len(avail_spots) == 0:
            return [0, ' ']

    # game continues
    result = []
    for turn in avail_spots:
        cells = board.copy()
        cells[turn] = player
        new_game_state['free'].remove(turn)
        new_game_state['occupied'].append(turn)
        if player == 'X':
            result.append((turn, minimax(cells, new_game_state, 'O')[0]))
        else:
            result.append((turn, minimax(cells, new_game_state, 'X')[0]))
        new_game_state = copy.deepcopy(game_state)

    if player == 'X':
        best_score = -1000
        for choice in result:
            if choice[1] > best_score:
                best_score = choice[1]
                best_move = choice[0]
            else:
                pass
    elif player == 'O':
        best_score = 1000
        for choice in result:
            if choice[1] < best_score:
                best_score = choice[1]
                best_move = choice[0]
    return [best_score, best_move]


def show_the_field(cells):
    first_line = ' '.join(cells[0:3])
    second_line = ' '.join(cells[3:6])
    third_line = ' '.join(cells[6:9])
    the_field = f"""---------
| {first_line} |
| {second_line} |
| {third_line} |
---------
    """
    print(the_field)


def ai_make_turn(game_state):
    print('Making move level "easy"')
    return random.choice(game_state['free'])


def ai_medium_make_turn(game_state, cells, sign):
    diagonal_1 = [cells[0], cells[4], cells[8]]
    diagonal_2 = [cells[6], cells[4], cells[2]]
    column_1 = [cells[0], cells[3], cells[6]]
    column_2 = [cells[1], cells[4], cells[7]]
    column_3 = [cells[2], cells[5], cells[8]]

    cells_lines = [cells[0:3],
                   cells[3:6],
                   cells[6:9],
                   diagonal_1,
                   diagonal_2,
                   column_1,
                   column_2,
                   column_3]

    antisign = ('O' if sign == 'X' else 'X')

    for i, line in enumerate(cells_lines):
        if (line.count(sign) == 2) and (line.count(" ") == 1):
            return medium_intelligent_play(i, cells_lines)
        elif (line.count(antisign) == 2) and (line.count(" ") == 1):
            return medium_intelligent_play(i, cells_lines)
    return random.choice(game_state['free'])


def medium_intelligent_play(i, cells_lines):
    if i in range(0, 3):
        return i * 3 + cells_lines[i].index(' ')
    if i == 3:
        return cells_lines[i].index(' ') * 4
    if i == 4:
        return 6 - cells_lines[i].index(' ') * 2

    if i in range(5, 8):
        return (i - 5) + cells_lines[i].index(' ') * 3


        # dict_turn_to_cell = {'1 3': 0, '2 3': 1, '3 3': 2,
        #                      '1 2': 3, '2 2': 4, '3 2': 5,
        #                      '1 1': 6, '2 1': 7, '3 1': 8}
        # if i in range(0, 3):
        #     number = i * 3 + cells_lines[i].index(' ')
        #     for key, value in dict_turn_to_cell.values():
        #         if value == number:
        #             return key
        # if i == 3:
        #     number = cells_lines[i].index(' ') * 4
        #     for key, value in dict_turn_to_cell.values():
        #         if value == number:
        #             return key
        # if i == 4:
        #     number = 6 - cells_lines[i].index(' ') * 2
        #     for key, value in dict_turn_to_cell.values():
        #         if value == number:
        #             return key
        #
        # if i in range(5, 8):
        #     number = (i - 5) + cells_lines[i].index(' ') * 3
        #     for key, value in dict_turn_to_cell.values():
        #         if value == number:
        #             return key



def analyze_input(input_for_test, cells, input_to_cells):
    # if user enters other symbols
    input_list = input_for_test.split(' ')
    try:
        int(input_list[0])
    except ValueError:
        print("You should enter numbers!")
        return False
    else:
        pass

    # if the user goes beyond the field

    if int(input_list[0]) not in [1, 2, 3] or int(input_list[1]) not in [1, 2, 3]:
        print("Coordinates should be from 1 to 3!")
        return False

    # if the cell is not empty

    if cells[input_to_cells[input_for_test]] != ' ':
        print("This cell is occupied! Choose another one!")
        return False

    return True


def user_play(cells):
    dict_turn_to_cell = {'1 3': 0, '2 3': 1, '3 3': 2,
                         '1 2': 3, '2 2': 4, '3 2': 5,
                         '1 1': 6, '2 1': 7, '3 1': 8}
    user_input = input('Enter the coordinates: ')
    while not analyze_input(user_input, cells, dict_turn_to_cell):
        user_input = input('Enter the coordinates: ')
    return dict_turn_to_cell[user_input]


def check_the_winner(cells, game_state):
    diagonal_1 = [cells[0], cells[4], cells[8]]
    diagonal_2 = [cells[2], cells[4], cells[6]]
    column_1 = [cells[0], cells[3], cells[6]]
    column_2 = [cells[1], cells[4], cells[7]]
    column_3 = [cells[2], cells[5], cells[8]]

    cells_lines = [cells[0:3],
                   cells[3:6],
                   cells[6:9],
                   diagonal_1,
                   diagonal_2,
                   column_1,
                   column_2,
                   column_3]

    for line in cells_lines:
        if line.count("O") == 3:
            return 'O wins'
        elif line.count("X") == 3:
            return 'X wins'
    if len(game_state['free']) == 0:
        return "Draw"
    return False


choose_the_game()

# First Stage

# def play_the_game():
#     # start_the_game
#     game_init_cells = [(x if x != '_' else ' ') for x in list(input('Enter cells: '))]
#     first = game_init_cells[:3]
#     second = game_init_cells[3:6]
#     third = game_init_cells[6:9]
#     cells = [third, second, first]
#     show_the_field(cells)
#
#
#     user_input = get_coordinates()
#     while not analyze_input(user_input, cells):
#         user_input = get_coordinates()
#
#     col, row = user_input
#     the_move = choose_move(game_init_cells)
#     cells[row - 1][col - 1] = the_move
#
#     show_the_field(cells)
#     print(show_the_game_state(cells))
#
#
# def get_coordinates():
#     return input('Enter the coordinates: ').split(' ')
#
#
# def analyze_input(input_for_test, cells):
#     # if user enters other symbols
#     try:
#         int(input_for_test[0])
#     except ValueError:
#         print("You should enter numbers!")
#         return False
#     else:
#         input_for_test[0], input_for_test[1] = int(input_for_test[0]), int(input_for_test[1])
#
#     # if the user goes beyond the field
#
#     if int(input_for_test[0]) not in [1, 2, 3] or int(input_for_test[1]) not in [1, 2, 3]:
#         print("Coordinates should be from 1 to 3!")
#         return False
#
#     # if the cell is not empty
#
#     if cells[input_for_test[1] - 1][input_for_test[0] - 1] != ' ':
#         print("This cell is occupied! Choose another one!")
#         return False
#
#     return input_for_test
#
#
# def choose_move(start_cells):
#     Os = start_cells.count("O")
#     Xs = start_cells.count("X")
#     if Os == Xs:
#         return "X"
#     return "O"
#
#
# def show_the_field(cells):
#
#     first_line = ' '.join(cells[2])
#     second_line = ' '.join(cells[1])
#     third_line = ' '.join(cells[0])
#     the_field = f"""---------
#     | {first_line} |
#     | {second_line} |
#     | {third_line} |
#     ---------
#     """
#     print(the_field)
#
#
# def show_the_game_state(cells):
#     empty_cells = []
#     for line in cells:
#         if line.count("O") == 3:
#             return 'O wins'
#         if line.count("X") == 3:
#             return 'X wins'
#         if " " in line:
#             empty_cells.append(True)
#
#     # diagonal
#     diagonal_1 = [cells[0][0], cells[1][1], cells[2][2]]
#     diagonal_2 = [cells[2][0], cells[1][1], cells[0][2]]
#     if (diagonal_1.count("O") == 3) or (diagonal_2.count("O") == 3):
#         return 'O wins'
#     elif (diagonal_1.count("X") == 3) or (diagonal_2.count("X") == 3):
#         return 'X wins'
#
#     if True not in empty_cells:
#         return 'Draw'
#     else:
#         return 'Game not finished'
#
#
# play_the_game()
#
#
