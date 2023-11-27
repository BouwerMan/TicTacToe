import random
from timeit import default_timer as timer

from player import Player
from game import Game


class Computer(Player):
    
    DEBUG = True
    
    def __init__(self, player_char = 'O', player_num = 2, computer_level = 0):
        super().__init__(player_char, player_num)
        self.game: Game = None
        
        # Can be 0-8 (0 being easiest, 8 being impossible)
        # 7 and 8 seem to be very similar, maybe if computer went first?
        self.depth_limit = computer_level
        
        #! Debugging
        self.hit_max_depth = False
        self.max_depth = 0
        self.eval_time = 0
        self.total_searches = 0
        self.max_eval_time = 0
    
    def create_move(self, current_game: Game) -> bytes:
        self.game = current_game
        if self.DEBUG:
            start = timer()
        # A max depth of 0 causes some exceptionally poor moves
        # Making the computer pick at random in that case just to
        if self.depth_limit == 0:
            move = self.__create_random_move()
            if not self.game.is_move_valid(move):
                print('invalid computer move')
                self.create_move(self.game)
        else:
            move = self.find_best_move()
        if self.DEBUG:
            end = timer()
            #! Debugging to find what is slow
            print('\nCOMPUTER DEBUGGING!')
            print(f'Time to find best move: {(end-start) * 1000:.4f}ms')
            print(f'Time spent evaluating: {self.eval_time * 1000:.4f}ms')
            print(f'Percent of time taken by evaluating: {(self.eval_time/(end-start))*100:.2f}%')
            print(f'Reached a depth of: {self.max_depth}')
            print(f'Hit max depth? {self.hit_max_depth}')
            print(f'Total searches: {self.total_searches}')
            print(f'Max eval time: {self.max_eval_time * 1000:.4f}ms')
            print()
            self.eval_time = 0
            self.total_searches = 0
        
        return move
    
    def evaluate(self, board):
        if self.DEBUG:
            start = timer()
        winner = self.game.check_for_win(board)
        if self.DEBUG:
            end = timer()
            self.max_eval_time = max(end-start, self.max_eval_time)
        # Check if we won
        if winner == self.player_num:
            return 10
        # Check if tie or no win
        elif (winner == 0b11) or (winner == 0b00):
            return 0
        # Only other option is we lost
        else:
            return -10
    
    def find_best_move(self) -> bytes:
        # TODO: Should probably clean this substantially
        best_move = 0
        best_score = -1000
        board = self.game._board_state
        moves = self.__get_available_moves(board)
        shift = self.game.board_shift * (self.player_num - 1)
        
        # Iterates through the possible moves and calls
        # __minimax() to find the score of said move
        for i in range(9):
            # If move is available on both boards
            if (moves >> i) & 1:
                guess_move = (1 << i) << shift
                
                # Checks if move blocked other player win
                # deals with depth limits by incentivising
                # moves that prevent other player from winning
                score_blocked = self.__did_move_block(board, guess_move)
                
                # Makes the move on a copied board
                board += guess_move
                
                score_minimax = self.__minimax(board, 0, False)
                
                # Undoes the move
                board -= guess_move
                
                score = max(score_blocked, score_minimax)
                if score > best_score:
                    best_score = score
                    best_move = guess_move
        
        return best_move
        
    def __minimax(self, board, depth: int, is_max: bool):
        if self.DEBUG:
            self.total_searches += 1
            self.max_depth = max(depth, self.max_depth)
        moves = self.__get_available_moves(board)
        
        # Limits depth to simulate computer levels
        if depth > self.depth_limit:
            self.hit_max_depth = True
            # Returning -10 to not incentivise games that
            # the computer doesn't know the outcome of
            return -10

        start = timer()
        result = self.evaluate(board)
        end = timer()
        self.eval_time += end-start
        
        # Returns score if either the player or computer wins
        if (result == 10) or (result == -10):
            return result
        
        # Checks if no moves are left, indicating a tie
        if moves == 0:
            return 0

        # If maximizer(computer)'s move
        if is_max:
            best_score = -1000
            
            # Iterates through the possible moves and calls
            # __minimax() to find the score of said move
            for i in range(9):
                # If move is available
                if (moves >> i) & 1:
                    guess_move = (1 << i) << self.game.board_shift
                    # Makes the move
                    board += guess_move
                    score = self.__minimax(board, depth + 1, False)
                    # Undoes the move
                    board -= guess_move
                    best_score = max(score, best_score)
                    
            return best_score
        else:
            best_score = 1000
            
            # Iterates through the possible moves and calls
            # __minimax() to find the score of said move
            for i in range(9):
                # If move is available
                if (moves >> i) & 1:
                    guess_move = (1 << i)
                    # Makes the move
                    board += guess_move
                    score = self.__minimax(board, depth + 1, True)
                    # Undoes the move
                    board -= guess_move
                    best_score = min(score, best_score)
            return best_score
            
                
    def __get_available_moves(self, board: bytes) -> bytes:
        # Using old method of getting boards to allow for custom boards
        combined_boards = self.game.get_boards(board)
        moves = (~(combined_boards)) & self.game.board_one_mask
        
        return moves
    
    def __create_random_move(self):
        shift = self.game.board_shift * (self.player_num - 1)
        move_rand = 1 << random.randint(0, 8)
        return move_rand << shift
    
    def __did_move_block(self, board, move):
        # Checks if move blocked other player win
        # Does so by simulating if other player played said move
        alt_board = board + (move >> self.game.board_shift)
        
        # Checks if other player won
        if self.evaluate(alt_board) == -10:
            return 5
        
        # Chose -20 to hopefully prevent interference with other evals
        #? Could remove?
        return -20

if __name__ == '__main__':
    #! Temporary test code
    player_one_test = Player('X', 0)
    player_two_test = Computer('O', 1, 7)
    board_test = Game(player_one_test, player_two_test)
    #player_two_test.game = board_test
    board_test.board_one = 0b111010001
    board_test.board_two = 0b000100010
    board_test.board_state += (0x0 << 16) | (0x1)
    #board_test.move(player_two_test, board_test.parse_input('a2'))
    #board_test.move(player_two_test, board_test.parse_input('b2'))
    #board_test.move(player_two_test, board_test.parse_input('c3'))
    board_test.print_board()
    ev = player_two_test.evaluate(board_test.board_state)
    print(ev)
    test = player_two_test.create_move(board_test)
    print(bin(test >> 16))