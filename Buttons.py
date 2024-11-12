'''
    Jason Curtis
    CS 5001
    Fall 2022
    Final Project
'''

import turtle as t


class Buttons:
    '''
    A button is an image on the turtle GUI which performs a specific function.
    This class builds the three buttons necessary for a tile game, adding
    the relevant image files, button size, and placing them in the desired
    positions on the screen for use by the game player.
    '''
    def __init__(self):
        '''
        function: object constructor
        parameters: none
        returns: none
        '''
        self.s = t.Screen()
        self.quit_button = t.Turtle()
        self.quit_button.hideturtle()
        self.load_button = t.Turtle()
        self.load_button.hideturtle()
        self.reset_button = t.Turtle()
        self.reset_button.hideturtle()

    def make_buttons(self):
        '''
        function: adds all button skins, runs button creators
        parameters: none
        returns: none
        '''
        self.s.addshape('Resources/quitbutton.gif')
        self.s.addshape('Resources/loadbutton.gif')
        self.s.addshape('Resources/resetbutton.gif')
        self.make_quit()
        self.make_load()
        self.make_reset()

    def make_quit(self):
        '''
        function: builds and places the quit button on the GUI
        parameters: none
        returns: none
        '''
        self.quit_button.shape('Resources/quitbutton.gif')
        self.quit_button.shapesize(80, 53)  # can click anywhere on the image
        self.quit_button.speed(0)
        self.quit_button.pu()
        self.quit_button.goto(280, -270)
        self.quit_button.showturtle()

    def make_load(self):
        '''
        function: builds and places the load button on the GUI
        parameters: none
        returns: none
        '''
        self.load_button.shape('Resources/loadbutton.gif')
        self.load_button.shapesize(80, 76)
        self.load_button.speed(0)
        self.load_button.pu()
        self.load_button.goto(180, -270)
        self.load_button.showturtle()

    def make_reset(self):
        '''
        function: builds and places the reset button on the GUI
        parameters: none
        returns: none
        '''
        self.reset_button.shape('Resources/resetbutton.gif')
        self.reset_button.shapesize(80, 80)
        self.reset_button.speed(0)
        self.reset_button.pu()
        self.reset_button.goto(80, -270)
        self.reset_button.showturtle()
