"""
Contains Player class
"""

class Player:
    """Class containing all functionality for a human player"""

    def __init__(self, player_char = 'X', player_num = 1):
        """Initializes a player

        Args:
            player_char (str, optional): Character to use when printing. Defaults to 'X'.
            player_num (int, optional): Player ID number. Defaults to 1.
        """
        self.player_char = player_char
        self.player_num = player_num
    
    def __str__(self, ):
        """Formats self for standard printing and string manipulation"""
        return f'Player {self.player_num}'
        