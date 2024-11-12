'''
    Jason Curtis
    CS 5001
    Fall 2022
    Final Project
'''

import turtle as t


class PlayerMoves:
    '''
    PlayerMoves is a class built to index the number of moves a player
    has taken as well as track their move limit for later comparison.
    '''
    def __init__(self, move_cap):
        '''
        function: constructor
        parameters: str
            move_cap: user input of their move limit, as a string
        returns: none
        '''
        self.index = 0
        self.move_cap = move_cap
        self.s = t.Screen()
        self.t = t.Turtle(visible=False)
        self.t.speed(0)
        self.t.pensize(5)
        self.startup()

    def startup(self):
        '''
        function: initializes player move counter graphic
        parameters: none
        returns: none
        '''
        self.t.pu()
        self.t.goto(-310, -280)
        self.t.pd()
        self.t.color('#b7410e')
        self.t.write(f'Player moves: {self.index} / {self.move_cap}', font=('Arial', 18, 'normal'))

    def move_log(self):
        '''
        function: update player move counter in memory and on GUI
        parameters: none
        returns: none
        '''
        self.t.clear()
        self.index += 1
        self.t.color('#b7410e')
        self.t.write(f'Player moves: {self.index} / {self.move_cap}', align='left', font=('Arial', 18, 'normal'))

    def get_move_cap(self):
        '''
        function: returns current move limit
        parameters: none
        returns: player move limit
        '''
        return int(self.move_cap)

    def get_index(self):
        '''
        function: returns current move counter
        parameters: none
        returns: current number of moves taken
        '''
        return int(self.index)

    def reset_index(self):
        '''
        function: resets the move index for use when a player loads new puzzle
        parameters: none
        returns: none
        '''
        self.index = 0
        self.t.clear()
        self.startup()
