import numpy


class Genome:

    def __init__(self, n_rows, n_cols, top_row=None, right_row=None, bot_row=None, left_row=None,
                 top_right_corner=None, bot_right_corner=None, bot_left_corner=None, top_left_corner=None,
                 initialized=bool(False)):
        self.top_row = top_row
        self.right_row = right_row
        self.bot_row = bot_row
        self.left_row = left_row

        self.top_right_corner = top_right_corner
        self.bot_right_corner = bot_right_corner
        self.bot_left_corner = bot_left_corner
        self.top_left_corner = top_left_corner
        self.initialized = initialized

        if not self.initialized:
            DEFAULT = 0.5
            DOMAIN_DIMENSION = 11

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

        return

    def update_genotype(self):


        # TODO: Update genotype on good or bad move

        return

    def get_optimal_move(self, board, n_rows, n_cols):

        fitness_ar = numpy.zeros((n_rows, n_cols), dtype=numpy.float32)
        optimal_fitness = 0
        optimal_row = None
        optimal_column = None

        for iter1 in range(n_rows):
            for iter2 in range(n_cols):
                surrounding_squares = []
                surrounding_squares = self.get_surrounding_squares(board, n_rows, n_cols, iter1, iter2)
                current_top_row = self.top_row[surrounding_squares[0, 0], surrounding_squares[0, 1], surrounding_squares[0, 2]]
                current_right_row = self.right_row[surrounding_squares[0, 2], surrounding_squares[1, 2],
                                                   surrounding_squares[2, 2]]
                current_bot_row = self.bot_row[surrounding_squares[2, 0], surrounding_squares[2, 1], surrounding_squares[2, 2]]
                current_left_row = self.left_row[surrounding_squares[0, 0], surrounding_squares[0, 1],
                                                 surrounding_squares[0, 2]]

                current_top_right_corner = self.top_right_corner[surrounding_squares[0, 0], surrounding_squares[0, 1],
                                                                 surrounding_squares[0, 2]]
                current_bot_right_corner = self.bot_right_corner[surrounding_squares[0, 0], surrounding_squares[0, 1],
                                                                 surrounding_squares[0, 2]]
                current_bot_left_corner = self.bot_left_corner[surrounding_squares[0, 0], surrounding_squares[0, 1],
                                                               surrounding_squares[0, 2]]
                current_top_left_corner = self.top_left_corner[surrounding_squares[0, 0], surrounding_squares[0, 1],
                                                               surrounding_squares[0, 2]]

                chromosomes = []
                mean_fitness = numpy.mean([current_top_row, current_right_row, current_bot_row, current_left_row,
                                           current_top_right_corner, current_bot_right_corner,
                                           current_bot_left_corner, current_top_left_corner])

                fitness_ar[iter1, iter2] = mean_fitness

        for iter1 in range(n_rows):
            for iter2 in range(n_cols):
                if board.tile_status[iter1, iter2] == 0:
                    if fitness_ar[iter1, iter2] > optimal_fitness:
                        optimal_fitness = fitness_ar[iter1, iter2]
                        optimal_row = iter1
                        optimal_column = iter2

        return optimal_row, optimal_column

    def get_surrounding_squares(self, board, n_rows, n_cols, row_pos, col_pos):

        ret = {}

        ret[0, 0] = self.get_square(board, n_rows, n_cols, row_pos - 1, col_pos - 1)
        ret[0, 1] = self.get_square(board, n_rows, n_cols, row_pos - 1, col_pos)
        ret[0, 2] = self.get_square(board, n_rows, n_cols, row_pos - 1, col_pos + 1)
        ret[1, 0] = self.get_square(board, n_rows, n_cols, row_pos, col_pos - 1)
        ret[1, 2] = self.get_square(board, n_rows, n_cols, row_pos, col_pos + 1)
        ret[2, 0] = self.get_square(board, n_rows, n_cols, row_pos + 1, col_pos - 1)
        ret[2, 1] = self.get_square(board, n_rows, n_cols, row_pos + 1, col_pos)
        ret[2, 2] = self.get_square(board, n_rows, n_cols, row_pos + 1, col_pos + 1)

        return ret

    def get_square(self, board, n_rows, n_cols, row_pos, col_pos):

        if row_pos < 0 or col_pos < 0 or row_pos >= n_rows or col_pos >= n_cols:
            ret = 10
        elif board.tile_status[row_pos, col_pos] == 0:
            ret = 9
        else:
            ret = board.mine_count[row_pos, col_pos]

        return ret


def make_move(board, genome, n_rows, n_cols, n_mines):
    mine_count = board.mine_count
    is_mine = board.is_mine
    optimal_move = genome.get_optimal_move(board, n_rows, n_cols)
    if (optimal_move[0] is not None or optimal_move[1] is not None) and board.game_status != 'game_over' and board.game_status != 'victory':
        board.open_tile(optimal_move[0], optimal_move[1])
        board.update_view()
    if board.game_status == 'game_over' or board.game_status == 'victory':
        board.reset(n_rows, n_cols, n_mines)
    return

