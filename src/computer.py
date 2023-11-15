import random
import copy
from timeit import default_timer as timer

from player import Player
from game import Game


class Computer(Player):
    # TODO: Fix immediate win blindspot
    #? Can't replicate now?
    def __init__(self, player_char = 'O', player_num = 1, computer_level = 0):
        super().__init__(player_char, player_num)
        self.game: Game = None
        
        # Can be 0-7 (0 being easiest, 7 being impossible)
        self.depth_limit = computer_level
        
        #! Debugging
        self.hit_max_depth = False
        self.max_depth = 0
        self.eval_time = 0
        self.total_searches = 0
        self.max_eval_time = 0
    
    def create_move(self):
        start = timer()
        # A max depth of 0 causes some exceptionally poor moves
        # Making the computer pick at random in that case just to
        if self.depth_limit == 0:
            move = self.__create_random_move()
            if not self.game.is_move_valid(move):
                print('invalid computer move')
                self.create_move()
        else:
            move = self.find_best_move()
        end = timer()
        #! Debugging to find what is slow
        print('\nCOMPUTER DEBUGGING!')
        print(f'Time to find best move: {(end-start) * 1000:.4f}ms')
        print(f'Time spent evaluating: {self.eval_time * 1000:.4f}ms')
        print(f'Percent of time taken by evaluating: {(self.eval_time/(end-start))*100:.2f}%')
        print(f'Reached a depth of: {self.max_depth}')
        print(f'Hit max depth? {self.hit_max_depth}')
        print(f'Total searches: {self.total_searches}')
        print(f'Max eval time: {self.max_eval_time * 1000:.4f}ms\n')
        self.eval_time = 0
        self.total_searches = 0
        return move
    
    def evaluate(self, board):
        start = timer()
        winner = self.game.check_for_win(board)
        end = timer()
        self.max_eval_time = max(end-start, self.max_eval_time)
        if winner == 1:
            return 10
        elif winner == 0:
            return -10
        else:
            return 0
    
    def find_best_move(self) -> bytes:
        # TODO: Should probably clean this substantially
        best_move = 0
        best_score = -1000
        board = copy.deepcopy(self.game.board)
        
        # Iterates through the possible moves and calls
        # __minimax() to find the score of said move
        for i in range(9):
            # If move is available on both boards
            if (~(board[0] | board[1]) >> i) & 1:
                guess_move = 1 << i

                # Makes the move on a copied board
                board[1] += guess_move
                score = self.__minimax(board, 0, False)
                
                # Undoes the move
                board[1] -= guess_move
                if score > best_score:
                    best_score = score
                    best_move = guess_move
                    
        return best_move
        
    def __minimax(self, board, depth: int, is_max: bool):
        self.total_searches += 1
        self.max_depth = max(depth, self.max_depth)
        
        # Limits depth for computer levels
        #! Had this return 10 for a bit, idk if that changes much
        if depth > self.depth_limit:
            self.hit_max_depth = True
            # Returning 5 to slightly incentivize a longer game
            #? Good idea?
            return 5

        start = timer()
        result = self.evaluate(board)
        end = timer()
        self.eval_time += end-start
        
        # Returns score if either the player or computer wins
        if (result == 10) or (result == -10):
            return result
        
        # Checks if no moves are left, indicating a tie
        if (board[0] | board[1]) == 0x1FF:
            return 0

        # If maximizer(computer)'s move
        if is_max:
            best_score = -1000
            
            # Iterates through the possible moves and calls
            # __minimax() to find the score of said move
            for i in range(9):
                # If move is available
                if (~(board[0] | board[1]) >> i) & 1:
                    guess_move = 1 << i
                    # Makes the move
                    board[1] += guess_move
                    score = self.__minimax(board, depth + 1, False)
                    # Undoes the move
                    board[1] -= guess_move
                    best_score = max(score, best_score)
                    
            return best_score
        else:
            best_score = 1000
            
            # Iterates through the possible moves and calls
            # __minimax() to find the score of said move
            for i in range(9):
                # If move is available
                if (~(board[0] | board[1]) >> i) & 1:
                    guess_move = 1 << i
                    # Makes the move
                    board[0] += guess_move
                    score = self.__minimax(board, depth + 1, True)
                    # Undoes the move
                    board[0] -= guess_move
                    best_score = min(score, best_score)
            return best_score
            
                
            
    
    def __create_random_move(self):
        return 1 << random.randint(0, 8)

if __name__ == '__main__':
    #! Temporary test code
    player_one_test = Player('X', 0)
    player_two_test = Computer('O', 1, 0)
    board_test = Game(player_one_test, player_two_test)
    player_two_test.game = board_test
    board_test.board_one = 0b111010001
    board_test.board_two = 0b000100010
    #board_test.move(player_two_test, board_test.parse_input('a2'))
    #board_test.move(player_two_test, board_test.parse_input('b2'))
    #board_test.move(player_two_test, board_test.parse_input('c3'))
    board_test.print_board()
    #ev = player_two_test.evaluate(board_test.board_one, board_test.board_two)
    #print(ev)
    player_two_test.find_best_move()