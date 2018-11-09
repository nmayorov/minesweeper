import numpy
import random

class Genome:

    def __init__(self, n_rows, n_cols, top_row=None, right_row=None, bot_row=None, left_row=None,
                 top_right_corner=None, bot_right_corner=None, bot_left_corner=None, top_left_corner=None):

        self.n_rows = n_rows
        self.n_cols = n_cols

        self.top_row = top_row
        self.right_row = right_row
        self.bot_row = bot_row
        self.left_row = left_row

        self.top_right_corner = top_right_corner
        self.bot_right_corner = bot_right_corner
        self.bot_left_corner = bot_left_corner
        self.top_left_corner = top_left_corner

        DOMAIN_DIMENSION = 11

        self.top_row_history = numpy.full(
            (DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION), 1, dtype=numpy.float32)
        self.right_row_history = numpy.full(
            (DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION), 1, dtype=numpy.float32)
        self.bot_row_history = numpy.full(
            (DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION), 1, dtype=numpy.float32)
        self.left_row_history = numpy.full(
            (DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION), 1, dtype=numpy.float32)

        self.top_right_corner_history = numpy.full(
            (DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION), 1, dtype=numpy.float32)
        self.bot_right_corner_history = numpy.full(
            (DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION), 1, dtype=numpy.float32)
        self.bot_left_corner_history = numpy.full(
            (DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION), 1, dtype=numpy.float32)
        self.top_left_corner_history = numpy.full(
            (DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION), 1, dtype=numpy.float32)

        self.genome = []
        self.update_genome()

        if top_row is None:
            DEFAULT = 0.5

            self.top_row = numpy.full((DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION),
                                      DEFAULT, dtype=numpy.float32)
            self.right_row = numpy.full((DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION),
                                        DEFAULT, dtype=numpy.float32)
            self.bot_row = numpy.full((DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION),
                                      DEFAULT, dtype=numpy.float32)
            self.left_row = numpy.full((DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION),
                                       DEFAULT, dtype=numpy.float32)

            self.top_right_corner = numpy.full((DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION),
                                               DEFAULT, dtype=numpy.float32)
            self.bot_right_corner = numpy.full((DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION),
                                               DEFAULT, dtype=numpy.float32)
            self.bot_left_corner = numpy.full((DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION),
                                              DEFAULT, dtype=numpy.float32)
            self.top_left_corner = numpy.full((DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION),
                                              DEFAULT, dtype=numpy.float32)

            VARIANCE = 0.5
            for iter1 in range(DOMAIN_DIMENSION):
                for iter2 in range(DOMAIN_DIMENSION):
                    for iter3 in range(DOMAIN_DIMENSION):
                        self.top_row[iter1, iter2, iter3] = DEFAULT + (random.random() * VARIANCE) - (0.5 * VARIANCE)
                        self.right_row[iter1, iter2, iter3] = DEFAULT + (random.random() * VARIANCE) - (0.5 * VARIANCE)
                        self.bot_row[iter1, iter2, iter3] = DEFAULT + (random.random() * VARIANCE) - (0.5 * VARIANCE)
                        self.left_row[iter1, iter2, iter3] = DEFAULT + (random.random() * VARIANCE) - (0.5 * VARIANCE)

                        self.top_right_corner[iter1, iter2, iter3] = DEFAULT + (random.random() * VARIANCE) - (0.5 *
                                                                                                               VARIANCE)
                        self.bot_right_corner[iter1, iter2, iter3] = DEFAULT + (random.random() * VARIANCE) - (0.5 *
                                                                                                               VARIANCE)
                        self.bot_left_corner[iter1, iter2, iter3] = DEFAULT + (random.random() * VARIANCE) - (0.5 *
                                                                                                              VARIANCE)
                        self.top_left_corner[iter1, iter2, iter3] = DEFAULT + (random.random() * VARIANCE) - (0.5 *
                                                                                                              VARIANCE)


        self.update_genome()
        return

    def update_genome(self):
        self.genome = [self.top_row, self.right_row, self.bot_row, self.left_row, self.top_right_corner,
                       self.bot_right_corner, self.bot_left_corner, self.top_left_corner]

    def update_genotype(self, board, row_pos, col_pos, game_status):

        LEARNING_RATE = 5

        if game_status == 'victory' or game_status == 'running':
            response = 1 * LEARNING_RATE
        else:
            response = 0 * LEARNING_RATE

        chromosomes = self.get_chromosomes(board, row_pos, col_pos)
        history = self.get_history(board, row_pos, col_pos)

        surrounding_squares = self.get_surrounding_squares(board, row_pos, col_pos)

        self.top_row_history[surrounding_squares[0, 0], surrounding_squares[0, 1], surrounding_squares[0, 2]] = \
            self.top_row_history[surrounding_squares[0, 0], surrounding_squares[0, 1], surrounding_squares[0, 2]] + \
            (1 * LEARNING_RATE)

        self.right_row_history[surrounding_squares[0, 2], surrounding_squares[1, 2], surrounding_squares[2, 2]] = \
            self.right_row_history[surrounding_squares[0, 2], surrounding_squares[1, 2], surrounding_squares[2, 2]] + \
            (1 * LEARNING_RATE)

        self.bot_row_history[surrounding_squares[2, 0], surrounding_squares[2, 1], surrounding_squares[2, 2]] = \
            self.bot_row_history[surrounding_squares[2, 0], surrounding_squares[2, 1], surrounding_squares[2, 2]] + \
            (1 * LEARNING_RATE)

        self.left_row_history[surrounding_squares[0, 0], surrounding_squares[0, 1], surrounding_squares[0, 2]] = \
            self.left_row_history[surrounding_squares[0, 0], surrounding_squares[0, 1], surrounding_squares[0, 2]] + \
            (1 * LEARNING_RATE)

        #
        self.top_right_corner_history[surrounding_squares[0, 1], surrounding_squares[0, 2], surrounding_squares[1, 2]] \
            = self.top_right_corner_history[surrounding_squares[0, 1], surrounding_squares[0, 2],
                                            surrounding_squares[1, 2]] + (1 * LEARNING_RATE)

        self.bot_right_corner_history[surrounding_squares[1, 2], surrounding_squares[2, 2], surrounding_squares[2, 1]] \
            = self.bot_right_corner_history[surrounding_squares[1, 2], surrounding_squares[2, 2],
                                            surrounding_squares[2, 1]] + (1 * LEARNING_RATE)

        self.bot_left_corner_history[surrounding_squares[2, 1], surrounding_squares[2, 0], surrounding_squares[1, 0]] \
            = self.bot_left_corner_history[surrounding_squares[2, 1], surrounding_squares[2, 0],
                                           surrounding_squares[1, 0]] + (1 * LEARNING_RATE)

        self.top_left_corner_history[surrounding_squares[1, 0], surrounding_squares[0, 0], surrounding_squares[0, 1]] \
            = self.top_left_corner_history[surrounding_squares[1, 0], surrounding_squares[0, 0],
                                           surrounding_squares[0, 1]] + (1 * LEARNING_RATE)

        #
        top_row = self.top_row[surrounding_squares[0, 0], surrounding_squares[0, 1], surrounding_squares[0, 2]]
        top_row_history = self.top_row_history[surrounding_squares[0, 0], surrounding_squares[0, 1],
                                               surrounding_squares[0, 2]]
        self.top_row[surrounding_squares[0, 0], surrounding_squares[0, 1], surrounding_squares[0, 2]] = \
            ((top_row * (top_row_history - 1)) + response) / top_row_history

        right_row = self.right_row[surrounding_squares[0, 2], surrounding_squares[1, 2], surrounding_squares[2, 2]]
        right_row_history = self.right_row_history[surrounding_squares[0, 2], surrounding_squares[1, 2],
                                                   surrounding_squares[2, 2]]
        self.right_row[surrounding_squares[0, 2], surrounding_squares[1, 2], surrounding_squares[2, 2]] = \
            ((right_row * (right_row_history - 1)) + response) / right_row_history

        bot_row = self.bot_row[surrounding_squares[2, 0], surrounding_squares[2, 1], surrounding_squares[2, 2]]
        bot_row_history = self.bot_row_history[surrounding_squares[2, 0], surrounding_squares[2, 1], surrounding_squares[2, 2]]
        self.bot_row[surrounding_squares[2, 0], surrounding_squares[2, 1], surrounding_squares[2, 2]] = \
            ((bot_row * (bot_row_history - 1)) + response) / bot_row_history

        left_row = self.left_row[surrounding_squares[0, 0], surrounding_squares[0, 1], surrounding_squares[0, 2]]
        left_row_history = self.left_row_history[surrounding_squares[0, 0], surrounding_squares[0, 1],
                                                 surrounding_squares[0, 2]]
        self.left_row[surrounding_squares[0, 0], surrounding_squares[0, 1], surrounding_squares[0, 2]] = \
            ((left_row * (left_row_history - 1)) + response) / left_row_history

        top_right_corner = self.top_right_corner[surrounding_squares[0, 1], surrounding_squares[0, 2],
                                                 surrounding_squares[1, 2]]
        top_right_corner_history = self.top_right_corner_history[surrounding_squares[0, 1], surrounding_squares[0, 2],
                                                                 surrounding_squares[1, 2]]
        self.top_right_corner[surrounding_squares[0, 1], surrounding_squares[0, 2], surrounding_squares[1, 2]] = \
            ((top_right_corner * (top_right_corner_history - 1)) + response) / top_right_corner_history

        bot_right_corner = self.bot_right_corner[surrounding_squares[1, 2], surrounding_squares[2, 2],
                                                 surrounding_squares[2, 1]]
        bot_right_corner_history = self.bot_right_corner_history[surrounding_squares[1, 2], surrounding_squares[2, 2],
                                                                 surrounding_squares[2, 1]]
        self.bot_right_corner[surrounding_squares[1, 2], surrounding_squares[2, 2], surrounding_squares[2, 1]] = \
            ((bot_right_corner * (bot_right_corner_history - 1)) + response) / bot_right_corner_history

        bot_left_corner = self.bot_left_corner[surrounding_squares[2, 1], surrounding_squares[2, 0],
                                               surrounding_squares[1, 0]]
        bot_left_corner_history = self.bot_left_corner_history[surrounding_squares[2, 1], surrounding_squares[2, 0],
                                                               surrounding_squares[1, 0]]
        self.bot_left_corner[surrounding_squares[2, 1], surrounding_squares[2, 0], surrounding_squares[1, 0]] = \
            ((bot_left_corner * (bot_left_corner_history - 1)) + response) / bot_left_corner_history

        top_left_corner = self.top_left_corner[surrounding_squares[1, 0], surrounding_squares[0, 0],
                                               surrounding_squares[0, 1]]
        top_left_corner_history = self.top_left_corner_history[surrounding_squares[1, 0], surrounding_squares[0, 0],
                                                               surrounding_squares[0, 1]]
        self.top_left_corner[surrounding_squares[1, 0], surrounding_squares[0, 0], surrounding_squares[0, 1]] = \
            ((top_left_corner * (top_left_corner_history - 1)) + response) / top_left_corner_history

        self.update_genome()
        return

    def get_optimal_move(self, board):

        fitness_ar = numpy.zeros((self.n_rows, self.n_cols), dtype=numpy.float32)
        optimal_fitness = -1
        optimal_row = -1
        optimal_column = -1

        for iter1 in range(self.n_rows):
            for iter2 in range(self.n_cols):
                chromosomes = self.get_chromosomes(board, iter1, iter2)
                current_top_row = chromosomes[0]
                current_right_row = chromosomes[1]
                current_bot_row = chromosomes[2]
                current_left_row = chromosomes[3]

                current_top_right_corner = chromosomes[4]
                current_bot_right_corner = chromosomes[5]
                current_bot_left_corner = chromosomes[6]
                current_top_left_corner = chromosomes[7]

                mean_fitness = numpy.mean([current_top_row, current_right_row, current_bot_row, current_left_row,
                                           current_top_right_corner, current_bot_right_corner,
                                           current_bot_left_corner, current_top_left_corner])

                fitness_ar[iter1, iter2] = mean_fitness

        for iter1 in range(self.n_rows):
            for iter2 in range(self.n_cols):
                if board.tile_status[iter1, iter2] == 0:
                    if fitness_ar[iter1, iter2] > optimal_fitness:
                        optimal_fitness = fitness_ar[iter1, iter2]
                        optimal_row = iter1
                        optimal_column = iter2

        return optimal_row, optimal_column

    def get_chromosomes(self, board, row_pos, col_pos):

        surrounding_squares = self.get_surrounding_squares(board, row_pos, col_pos)

        return \
            self.top_row[surrounding_squares[0, 0], surrounding_squares[0, 1], surrounding_squares[0, 2]], \
            self.right_row[surrounding_squares[0, 2], surrounding_squares[1, 2], surrounding_squares[2, 2]], \
            self.bot_row[surrounding_squares[2, 0], surrounding_squares[2, 1], surrounding_squares[2, 2]], \
            self.left_row[surrounding_squares[0, 0], surrounding_squares[0, 1], surrounding_squares[0, 2]], \
            self.top_right_corner[surrounding_squares[0, 1], surrounding_squares[0, 2], surrounding_squares[1, 2]], \
            self.bot_right_corner[surrounding_squares[1, 2], surrounding_squares[2, 2], surrounding_squares[2, 1]], \
            self.bot_left_corner[surrounding_squares[2, 1], surrounding_squares[2, 0], surrounding_squares[1, 0]], \
            self.top_left_corner[surrounding_squares[1, 0], surrounding_squares[0, 0], surrounding_squares[0, 1]]

    def get_history(self, board, row_pos, col_pos):

        surrounding_squares = []
        surrounding_squares = self.get_surrounding_squares(board, row_pos, col_pos)

        return \
            self.top_row_history[surrounding_squares[0, 0], surrounding_squares[0, 1], surrounding_squares[0, 2]], \
            self.right_row_history[surrounding_squares[0, 2], surrounding_squares[1, 2], surrounding_squares[2, 2]], \
            self.bot_row_history[surrounding_squares[2, 0], surrounding_squares[2, 1], surrounding_squares[2, 2]], \
            self.left_row_history[surrounding_squares[0, 0], surrounding_squares[0, 1], surrounding_squares[0, 2]], \
            self.top_right_corner_history[surrounding_squares[0, 1], surrounding_squares[0, 2],
                                          surrounding_squares[1, 2]], \
            self.bot_right_corner_history[surrounding_squares[1, 2], surrounding_squares[2, 2],
                                          surrounding_squares[2, 1]], \
            self.bot_left_corner_history[surrounding_squares[2, 1], surrounding_squares[2, 0],
                                         surrounding_squares[1, 0]], \
            self.top_left_corner_history[surrounding_squares[1, 0], surrounding_squares[0, 0],
                                         surrounding_squares[0, 1]]

    def get_surrounding_squares(self, board, row_pos, col_pos):

        ret = {}

        ret[0, 0] = self.get_square(board, row_pos - 1, col_pos - 1)
        ret[0, 1] = self.get_square(board, row_pos - 1, col_pos)
        ret[0, 2] = self.get_square(board, row_pos - 1, col_pos + 1)
        ret[1, 0] = self.get_square(board, row_pos, col_pos - 1)
        ret[1, 2] = self.get_square(board, row_pos, col_pos + 1)
        ret[2, 0] = self.get_square(board, row_pos + 1, col_pos - 1)
        ret[2, 1] = self.get_square(board, row_pos + 1, col_pos)
        ret[2, 2] = self.get_square(board, row_pos + 1, col_pos + 1)

        return ret

    def get_square(self, board, row_pos, col_pos):

        if row_pos < 0 or col_pos < 0 or row_pos >= self.n_rows or col_pos >= self.n_cols:
            ret = 10
        elif board.tile_status[row_pos, col_pos] == 0:
            ret = 9
        else:
            ret = board.mine_count[row_pos, col_pos]

        return ret


def make_move(board, genome, n_mines):
    mine_count = board.mine_count
    is_mine = board.is_mine
    optimal_move = genome.get_optimal_move(board)
    if (optimal_move[0] is not -1 and optimal_move[1] is not -1) and board.game_status != 'game_over' and board.game_status != 'victory':
        board.open_tile(optimal_move[0], optimal_move[1])
        board.update_view()
        genome.update_genotype(board, optimal_move[0], optimal_move[1], board.game_status)

    if board.game_status == 'game_over' or board.game_status == 'victory':
        board.reset(genome.n_rows, genome.n_cols, n_mines)
        genome.update_genotype(board, optimal_move[0], optimal_move[1], board.game_status)

    return

