import random
from player import Player
from board import Board


class Computer(Player):
    def __init__(self, player_char = 'O', player_num = 1, computer_level = 0):
        super().__init__(player_char, player_num)
        self.computer_level = computer_level
        self.board: Board = None
    
    def create_move(self):
        if self.computer_level == 0:
            move = self.__create_random_move()
            if not self.board.is_move_valid(move):
                print('invalid computer move')
                self.create_move()
        return move
    
    def evaluate(self):
        winner = self.board.check_for_win()
        if winner == self:
            return 10
        elif winner == None:
            return 0
        else:
            return -10
    
    def __create_random_move(self):
        return 1 << random.randint(0, 8)

if __name__ == '__main__':
    #! Temporary test code
    player_one_test = Player('X', 0)
    player_two_test = Computer('O', 1, 0)
    board_test = Board(player_one_test, player_two_test)
    player_two_test.board = board_test
    #board_test.board_one = 0b110110001
    board_test.move(player_two_test, board_test.parse_input('a1'))
    board_test.move(player_two_test, board_test.parse_input('b2'))
    board_test.move(player_two_test, board_test.parse_input('c3'))
    board_test.print_board()
    ev = player_two_test.evaluate()
    print(ev)
