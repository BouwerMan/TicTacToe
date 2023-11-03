class Player:
    """
    Class containing all functionality for a human player
    
    ...
    
    Attributes
    ----------
    playerChar: str
        Character used for displaying player moves
    """

    playerChar = ''
    #computer = False
    #computerLevel = -1

    #, computer = False, computerLevel = -1
    def __init__(self, playerChar = 'X'):
        self.playerChar = playerChar
        #self.computer = computer
        #self.computerLevel = computerLevel
        