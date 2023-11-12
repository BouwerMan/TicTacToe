"""
Contains Player class
"""

class Player:
    """
    Class containing all functionality for a human player
    """

    #, computer = False, computerLevel = -1
    def __init__(self, player_char = 'X', player_num = 0):
        self.player_char = player_char
        self.player_num = player_num
    
    def __str__(self, ):
        return f'Player {self.player_num + 1}'
        