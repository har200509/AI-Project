class tic_tac_toe:
    def __init__(self):
        self.board = self.make_board()
        self.winner = None

    def make_board(self):
        return [" " for i in range(9)]

    def avail_pos(self):
        return [i for i, x in enumerate(self.board) if x == " "]

    def num_empty_pos(self):
        return self.board.count(" ")

    def display_board(self):
        for i in range(3):
            for j in range(3):
                print('|' + self.board[3 * i + j], end='')
            print('|')
    
    def make_move(self, pos, turn):
        self.board[pos] = turn

        col_num = pos % 3
        row_num = pos // 3

        c = 0
        for i in range(3):
            if self.board[3 * i + col_num] == turn:
                c = c + 1
        if c == 3:
            self.winner = turn
            return True

        c = 0
        for i in range(3):
            if self.board[3 * row_num + i] == turn:
                c = c + 1
        if c == 3:
            self.winner = turn
            return True

        if pos % 2 == 0:
            diag1 = [0, 4, 8]
            c = 0
            for i in diag1:
                if self.board[i] == turn:
                    c = c + 1
            if c == 3:
                self.winner = turn
                return True
            diag2 = [2, 4, 6]
            c = 0
            for i in diag2:
                if self.board[i] == turn:
                    c = c + 1
            if c == 3:
                self.winner = turn
                return True
        return False

    def play(self, x_player, o_player, print_game=True):
        if print_game:
            self.display_board()

        turn = 'X'

        while self.num_empty_pos():
            pos = x_player.get_move(self) if turn == 'X' else o_player.get_move(self)

            if self.board[pos] != " ":
                pos = x_player.get_move(self) if turn == 'X' else o_player.get_move(self)
            b = self.make_move(pos, turn)
            self.display_board()
            if b == True:
                print(self.winner + "won the game")
                break
            else:
                if turn == 'X':
                    turn = 'O'
                else:
                    turn = 'X'

        if self.num_empty_pos() == 0 and self.winner is None:
            print("It was a tie")

import random
import math

class Player():
    def __init__(self, turn):
        self.turn = turn

    def get_move(self, game):
        pass

class Human_player(Player):
    def __init__(self, turn):
        super().__init__(turn)

    def get_move(self, game):
        while True:
            pos = int(input("Enter pos:"))
            if pos in game.avail_pos():
                break
        return pos

class AI_player(Player):
    def __init__(self, turn):
        super().__init__(turn)

    def get_move(self, game):
        return self.minimax(game, self.turn, -math.inf, math.inf)['position']

    def minimax(self, game, curr_player, alpha, beta):
        max_player = self.turn
        prev_player = 'O' if curr_player == 'X' else 'X'

        if game.winner == prev_player:
            return {'position': None, 'score': 1 * (game.num_empty_pos() + 1)} if prev_player == max_player else {'position': None, 'score': -1 * (game.num_empty_pos() + 1)}
        elif game.num_empty_pos() == 0:
            return {'position': None, 'score': 0}

        if curr_player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for a_p in game.avail_pos():
            game.make_move(a_p, curr_player)
            sim_score = self.minimax(game, prev_player, alpha, beta)

            game.board[a_p] = ' '
            game.winner = None
            sim_score['position'] = a_p

            if curr_player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
                alpha = max(alpha, best['score'])
                if beta <= alpha:
                    break
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
                beta = min(beta, best['score'])
                if beta <= alpha:
                    break
        return best

game = tic_tac_toe()
x = Human_player('X')
o = AI_player('O')
game.play(x, o)
