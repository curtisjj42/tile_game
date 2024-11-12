'''
    Jason Curtis
    CS 5001
    Fall 2022
    Final Project
'''

import os
import turtle as t
import time
import math
import random
import Buttons
import GameBoard
import PlayerMoves


def error_log(error, location):
    '''
    function: logs designated errors into target file
    parameters: str, str
        error: error description defined per item
        location: function making the error report
    returns: none
    '''
    cur_time = time.ctime()  # get current date/time
    with open('5001_puzzle.err', mode='a') as error_file:
        error_file.write(cur_time + 'Error: ' + error +
                         'Location: ' + location + '\n')


def victory_checker(game_array, victory, player):
    '''
    function: checks if the current game state matches the winning state.
        Completes victory procedures
    parameters: list, list, list
        game_array: nested list holding current game state
        victory: nested list holding winning game state
        player: list holding player name and number of moves taken
    returns: none
    '''
    if game_array == victory:  # check relative positions of all tile objects
        screen = t.Screen()
        screen.addshape('Resources/winner.gif')
        screen.addshape('Resources/credits.gif')
        # display all associated graphics
        winner = t.Turtle('Resources/winner.gif')
        time.sleep(4)
        winner.shape('Resources/credits.gif')
        time.sleep(5)
        try:  # exception handling for broken leaderboard path
            with open('leaderboard.txt', mode='a') as file:
                file.write('\n' + ' : '.join([str(player[1].get_index()),
                                              player[0].get_player()]))
        except FileNotFoundError:
            error_log('Could not open leaderboard.txt ',
                      'puzzle_game.victory_checker()')
        quit()


def failure():
    '''
    function: displays graphics and quits game when user passes their
        move cap
    parameters: none
    returns: none
    '''
    screen = t.Screen()  # add and display graphics for loss/credits
    screen.addshape('Resources/Lose.gif')
    screen.addshape('Resources/credits.gif')
    loser = t.Turtle('Resources/Lose.gif')
    time.sleep(4)
    loser.shape('Resources/credits.gif')
    time.sleep(5)
    quit()


def move_tiles(obj, blank, obj_coords, blank_coords, moves):
    '''
    function: swaps tile objects on board
    parameters: object, object, tuple, tuple, object
        obj: tile that was clicked
        blank: blank tile object
        obj_coords: x,y coordinates for tile
        blank_coords: x,y coordinates for blank tile
        moves: instance of GameBoard.PlayerMoves(); used to increase the
            move counter and check against move limit
    returns: none
    '''
    obj.pu()
    obj.goto(blank_coords)  # move clicked tile
    blank.pu()
    blank.goto(obj_coords)  # move blank tile
    moves.move_log()  # increase move index by 1
    if moves.get_index() >= moves.get_move_cap():
        failure()  # run loss parameters when user reaches their move limit


def return_index(obj_list, obj):
    '''
    function: locate array indices for target tile object
    parameters: 2d list, object
        obj_list: list of objects in current game state
        obj: tile object
    returns: tuple containing row and column indices for tile swap
    '''
    for i, j in enumerate(obj_list):  # i=row number, j=objects in row
        if obj in j:  # check if target tile is in each row
            return i, j.index(obj)  # return array coordinates for tile


def find_blank(tile_list):
    '''
    function: determine which tile object is the blank tile and call
        return_index() to find its location in the array
    parameters: list
        tile_list: 2d list containing tile objects in current game state
    returns: tuple containing game state array coordinates of blank tile
    '''
    for row in tile_list:  # iterate through each row of the array
        for each in row:  # iterate through each tile object in current row
            shape = each.shape()  # retrieve image associate with object
            shape = shape.split('/')  # split image path info to access file ext
            if shape[2] == 'blank.gif':
                return return_index(tile_list, each)  # call array indexer


def move_maker(obj, game_array, victory, player):
    '''
    function:
    parameters: object, 2d list, 2d list, list
        obj: clicked tile object
        game_array: 2d list with current game state
        victory: 2d list with winning game state
        player: list containing player name and move limit
    returns: none
    '''
    def move_checker():
        '''checks if tile is either one row or column away from blank'''
        if abs(click_i - blank_i) == 1 and abs(click_j - blank_j) == 0:
            return True  # tile is one row above or below blank
        elif abs(click_i - blank_i) == 0 and abs(click_j - blank_j) == 1:
            return True  # tile is one column left or right of blank
        else:
            return False  # tile is not adjacent to the blank tile

    blank_i, blank_j = find_blank(game_array)  # array indices of tiles
    click_i, click_j = return_index(game_array, obj)
    if move_checker() is True:  # function call to determine if the move is valid
        blank = game_array[blank_i][blank_j]  # blank tile object
        blank_coords = blank.xcor(), blank.ycor()  # tile board positions
        obj_coords = obj.xcor(), obj.ycor()
        game_array[blank_i][blank_j] = obj  # game state position swap
        game_array[click_i][click_j] = blank

        # call tile swapping function
        move_tiles(obj, blank, obj_coords, blank_coords, player[1])
        puz_size = len(game_array) - 1  # generate board size de novo
        game_array[:] = game_array  # reference update for swapped objects

        # checks if blank tile is in the bottom right corner
        if game_array[puz_size][puz_size] == blank:
            # determine if the current game state is a win
            victory_checker(game_array, victory, player)


def place_tiles(tile_board):
    '''
    function: place tiles on game board and draw grid borders
    parameters: 2d list
        tile_board: array holding shuffled tile positions
    returns: array holding current game state
    '''
    for row in tile_board:
        for each in row:  # access each tile object
            # each tile draws its own square based on board position
            each.speed(0)
            each.fd(49)
            each.setheading(270)
            each.pd()
            for i in range(4):
                each.fd(49)
                each.rt(90)
                each.fd(49)
            each.pu()
            # adjust to position tile image properly
            each.goto(each.xcor()-49, each.ycor())
            each.showturtle()
    return tile_board


def shuffle_tiles(tile_list, grid, board_size):
    '''
        function: create random puzzle configuration
        parameters: 2d list, list of tuples, int
            tile_list: list with tiles in solved game state
            grid: board coordinates for all tiles
        returns: tile array containing objects with updated x,y positions
    '''
    # create 2d array to track row/column of each tile
    tile_board = [[0 for _ in range(board_size)] for _ in range(board_size)]
    rand_assign = []
    while len(rand_assign) < board_size**2:  # create board from puzzle size
        r = random.randint(0, len(grid) - 1)  # scrambled index list
        if r not in rand_assign:
            rand_assign.append(r)
    for row in tile_list:
        for each in row:
            r = rand_assign.pop()  # stack configuration
            each.goto(grid[r][0], grid[r][1])  # set x,y coordinates for tile
            # migrate tiles from organized array to shuffled array
            # r//2, r%board_size generate row, col based on 1d index
            tile_board[r // board_size][r % board_size] = each
    return place_tiles(tile_board)  # pass shuffled array back up


def make_tiles(metadata, game_array, grid, victory, player):
    '''
    function: generate tile objects for game board
    parameters: list, list, list, list, list
        metadata: list of puzzle information
        game_array: nested list with tile numbers and image file paths
        grid: list of tuples with coordinates for tile placement
        victory: empty list, will hold tile objects in winning game state
        player: player name and move limit
    returns: none
    '''
    screen = t.Screen()  # screen to add tile images
    # determine board size based on puzzle size
    board_size = int(math.sqrt(int(metadata[1][1])))
    tile_board = []
    for each in game_array:  # add each tile image
        screen.addshape(each[1])
    for i in range(board_size):
        holder = []  # empty list to hold row data
        for j in range(board_size):
            number = board_size * i + j  # convert 2d indices to 1d
            # index used to interact between arrays and lists
            tile = t.Turtle(game_array[number][1], visible=False)
            # set clickable region as tile image
            tile.shapesize(int(metadata[2][1]))
            tile.speed(0)
            tile.pu()
            # set tile x,y coordinates for ordered configuration
            tile.goto(grid[number][0], grid[number][1])

            def click_logger(x, y, tile=tile):
                '''add .onclick function for each tile object'''
                return move_maker(tile, game_array, victory, player)

            tile.onclick(click_logger)
            holder.append(tile)  # add each tile to row list
        tile_board.append(holder)  # add each row to the array
    victory[:] = tile_board  # update winning configuration
    # update current configuration based on shuffle
    game_array[:] = shuffle_tiles(tile_board, grid, board_size)


def make_grid(tile_number, tile_size=98):
    '''
    function: generate grid coordinates for tile placement
    parameters: str, int
        tile_number: number of tiles in puzzle
        tile_size: tile size for offset calculations
    returns: list of all grid coordinates for tiles
    '''
    try:  # exception handling for non-square puzzles
        grid_size = int(math.sqrt(int(tile_number)))
    except ValueError:
        error_log('Puzzle size is not a square. ', 'puzzle_game.make_grid()')
        return
    coord_list = []
    j, i = 0, 0  # set up loop conditions
    while i < grid_size:
        while j < grid_size:
            if j == 0 and i == 0:  # no offset for top left tile
                coords = j * tile_size - 263, 220 - i * tile_size
                coord_list.append(coords)
            elif j > 0 and i == 0:  # offset 1st row columns by 4 pixels
                coords = j * (tile_size + 4) - 263, 220 - i * tile_size
                coord_list.append(coords)
            elif j == 0 and i > 0:  # offset 1st column rows by 4 pixels
                coords = j * tile_size - 263, 220 - i * (tile_size + 4)
                coord_list.append(coords)
            else:  # offset all other tiles by 4 pixels in both directions
                coords = j * (tile_size + 4) - 263, 220 - i * (tile_size + 4)
                coord_list.append(coords)
            j += 1
        i += 1
        j = 0  # reset column counter
    return coord_list


def load_puzzle(puz_name, grid, game_array, victory, player):
    '''
    function: puzzle loader
    parameters: str, list, list, list, list
        puz_name: str name of puzzle, default or user input
        grid: empty list to hold tile coordinates
        game_array: empty list to hold current game state
        victory: empty list to hold winning game state
        player: player name and move limit
    returns: none
    '''
    metadata = []
    if len(game_array) != 0:  # check if a puzzle is already loaded
        for row in game_array:
            for each in row:
                each.clear()  # clears drawn grid
                each.hideturtle()  # remove tiles
        game_array[:] = []  # clear stored game state
        player[1].reset_index()  # reset move counter
    with open(puz_name, mode='r') as in_file:
        for each in in_file:
            each = each.strip().split(': ')
            game_array.append(each)  # info for initializing tiles

    for i in range(0, 4):  # queue config to remove puzzle metadata
        metadata.append(game_array.pop(0))

    for i in range(len(game_array)):  # convert all tile numbers to int
        game_array[i][0] = int(game_array[i][0])

    # error handling for .puz file where puzzle size is inaccurate
    if int(metadata[1][1]) != len(game_array):
        error_log(f'File {puz_name} data corrupted. ',
                  'puzzle_game.load_puzzle()')
        screen = t.Screen()
        screen.addshape('Resources/file_error.gif')
        warning = t.Turtle('Resources/file_error.gif')
        time.sleep(4)
        warning.hideturtle()
        return

    # make puzzle grid and update reference
    grid[:] = make_grid(int(metadata[1][1]))
    thumbnail(metadata[3][1])  # place completed puzzle thumbnail
    # create all tile objects with file data
    make_tiles(metadata, game_array, grid, victory, player)


def thumbnail(pic):
    '''
    function: place thumbnail of completed puzzle
    parameters: str
        pic: thumbnail file path
        returns: none
    '''
    screen = t.Screen()
    try:  # exception handling for bad thumbnail path
        screen.addshape(pic)
    except FileNotFoundError:
        error_log('Thumbnail {pic} does not exist. ', 'puzzle_game.thumbnail()')
        return
    t.shape(pic)
    t.speed(7)
    t.pu()
    t.goto(270, 325)


def make_buttons():
    '''
    function: create instance of pressable game buttons
    parameters: none
    returns: buttons class instance
    '''
    buttons = Buttons.Buttons()
    buttons.make_buttons()
    return buttons


def decision_tree(buttons, game_array, victory, grid, player, screen):
    '''
    function: determine function based on clicked button
    parameters: class, list, list, list, list, object
        buttons: initialized instance of game buttons
        game_array: empty list to hold current game state
        victory: empty list to hold winning game state
        grid: empty list to hold tile coordinates
        player: player name and move counter
        screen: instance of active screen
    '''
    screen.addshape('Resources/file_error.gif')  # for exception handling
    screen.addshape('Resources/file_warning.gif')

    def click_l(x, y):  # .onclick function for load button
        # create list with all .puz files in directory
        puzzle_list = [i for i in os.listdir('.') if '.puz' in i]
        if len(puzzle_list) > 10:  # display graphic if list is too long
            warning = t.Turtle('Resources/file_warning.gif')
            time.sleep(3)
            warning.hideturtle()
        puzzles = '\n'.join(i for i in puzzle_list)  # list to str
        puz_name = t.textinput('Puzzles', f'Which puzzle would you '
                                          f'like to play?\n\n{puzzles}')
        if puz_name not in puzzle_list:  # exception handling for bad input
            error_log(f'File {puz_name} does not exist. ',
                      'puzzle_game.click_l()')
            warning = t.Turtle('Resources/file_error.gif')
            time.sleep(3)
            warning.hideturtle()
        else:  # load puzzle based on user input
            load_puzzle(puz_name, grid, game_array, victory, player)

    def click_r(x, y):  # .onclick function for reset button
        for i in range(len(victory)):
            for j in range(len(victory[i])):
                # set all tiles to x,y for their winning configuration
                victory[i][j].goto(grid[i * len(victory) + j])
        game_array[:] = victory  # update current game state to winning state

    def click_q(x, y):  # .onclick function for quit button
        quit_msg = t.Turtle()
        screen.addshape('Resources/quitmsg.gif')
        screen.addshape('Resources/credits.gif')
        quit_msg.shape('Resources/quitmsg.gif')
        time.sleep(3)
        quit_msg.shape('Resources/credits.gif')
        time.sleep(5)
        quit()

    # add .onclick function to game buttons
    buttons.quit_button.onclick(click_q)
    buttons.load_button.onclick(click_l)
    buttons.reset_button.onclick(click_r)


def startup():
    '''
    function: initialize splash art and get user input
    parameters: none
    returns: user input for player name and move limit
    '''
    splash_screen = t.Screen()
    splash_screen.bgpic('Resources/splash_screen.gif')
    splash_screen.setup(449, 373)
    time.sleep(3)  # hang splash for a brief period
    player_name = t.textinput("CS 5001 Puzzle", "Enter your name")
    while True:  # loop to get good data
        try:  # exception handling for move limit values
            move_limit = t.textinput('Moves', 'How many moves '
                                              'would you like? (Enter 5-200)')
            if int(move_limit) > 200 or int(move_limit) < 5:
                raise ValueError
            else:
                break
        except ValueError:  # continue loop
            pass
    splash_screen.bgpic('nopic')  # remove splash
    return player_name, move_limit


def main():
    player_info = startup()  # run startup sequence
    screen = t.Screen()
    # generate instance of gameboard class
    board = GameBoard.GameBoard(screen, player_info[0])
    board.draw_board()
    try:  # bad leaderboard file path
        board.make_leaderboard('leaderboard.txt')
    except FileNotFoundError:
        error_log('Could not open leaderboard.txt. ',
                  'puzzle_game.puzzle_master()')
    buttons = make_buttons()  # create instance of buttons
    # create instance to track player move count
    moves = PlayerMoves.PlayerMoves(player_info[1])
    player = [board, moves]
    grid = []
    game_array = []
    victory = []
    try:  # exception handling for bad default puzzle file path
        load_puzzle('mario.puz', grid, game_array, victory, player)
    except FileNotFoundError:
        error_log('Default puzzle not found. ', 'puzzle_game.puzzle_master()')
        screen.addshape('Resources/file_error.gif')
        badpuz = t.Turtle('Resources/file_error.gif')
        time.sleep(3)
        badpuz.hideturtle()
    # run primary controller function for all in game operations
    decision_tree(buttons, game_array, victory, grid, player, screen)
    t.done()


if __name__ == '__main__':
    main()
