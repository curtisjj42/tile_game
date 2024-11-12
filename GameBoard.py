'''
    Jason Curtis
    CS 5001
    Fall 2022
    Final Project
'''

import turtle as t


class GameBoard:
    '''
    GameBoard is the primary design element for the visual effects of the tile
    game turtle GUI. This class functions as the scaffold for the full user
    interface. All methods are designed for in-class use, except get_player()
    which returns the name of the player for each instance of the game.
    '''
    def __init__(self, screen, player):
        '''
        function: constructor function
        parameters: object, str
            screen: current instance of turtle.Screen() being used
            player: current player name
        returns: none
        '''
        self.board = screen
        self.t = t.Turtle()
        self.player = player
        self.t.hideturtle()
        self.t.speed(0)
        self.t.pensize(5)

    def move_turtle(self, xcoord, ycoord):
        '''
        function: moves board's turtle to a specific x,y
        parameters: int, int
            xcoord: target x-coordinate
            ycoord: target y-coordinate
        returns: none
        '''
        self.t.penup()
        self.t.goto(xcoord, ycoord)
        self.t.pendown()

    def set_x(self, xcoord):
        '''
        function: sets x-coordinate of board's turtle
        parameters: int
            xcoord: target x-coordinate
        returns: none
        '''
        self.t.penup()
        self.t.setx(xcoord)
        self.t.pendown()

    def set_y(self, ycoord):
        '''
        function: sets y-coordinate of board's turtle
        parameters: int
            ycoord: target y-coordinate
        returns: none
        '''
        self.t.penup()
        self.t.sety(ycoord)
        self.t.pendown()

    def draw_square(self, width, height):
        '''
        function: draws a box using the provided dimensions
        parameters: str, str
            width: desired horizontal dimension of the box
            height: desired vertical dimension of the box
        returns:
        '''
        for i in range(0, 2):
            self.t.fd(width)
            self.t.right(90)
            self.t.fd(height)
            self.t.right(90)

    def draw_board(self):
        '''
        function: builds boxes for tile grid and leaderboard
        parameters: none
        returns: none
        '''
        self.board.setup(800, 800)
        self.move_turtle(-340, 320)
        self.draw_square(460, 520)
        self.move_turtle(130, 320)
        self.t.pencolor('teal')
        self.t.setheading(0)
        self.draw_square(200, 520)
        self.move_turtle(-340, -220)
        self.t.color('#b7410e')
        self.draw_square(670, 100)

    def make_leaderboard(self, leaderboard):
        '''
        function: reads the leaderboard information from file and illustrates
        parameters: str
            leaderboard: leaderboard.txt file name and path
        returns: none
        '''
        self.move_turtle(145, 275)
        self.t.color('teal')
        self.t.write('Leaders', False, align='left', font=('Arial', 18, 'normal'))
        self.set_y(225)
        with open(leaderboard, mode='r') as in_file:
            for each in in_file:
                self.t.write(each, False, align='left', font=('Arial', 16, 'normal'))
                self.set_y(self.t.ycor() - 30)

    def get_player(self):
        '''
        function: returns player name
        parameters: none
        returns: current player name
        '''
        return self.player
