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
            DOMAIN_DIMENSION = 10

            self.top_row = numpy.full((DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION),
                                      DEFAULT, dtype=numpy.int32)

            self.right_row = numpy.full((DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION),
                                        DEFAULT, dtype=numpy.int32)
            self.bot_row = numpy.full((DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION),
                                      DEFAULT, dtype=numpy.int32)
            self.left_row = numpy.full((DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION),
                                       DEFAULT, dtype=numpy.int32)

            self.top_right_corner = numpy.full((DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION),
                                               DEFAULT, dtype=numpy.int32)
            self.bot_right_corner = numpy.full((DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION),
                                               DEFAULT, dtype=numpy.int32)
            self.bot_left_corner = numpy.full((DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION),
                                              DEFAULT, dtype=numpy.int32)
            self.top_left_corner = numpy.full((DOMAIN_DIMENSION, DOMAIN_DIMENSION, DOMAIN_DIMENSION),
                                              DEFAULT, dtype=numpy.int32)

        return

    def update_genotype(self):

        return

    def get_optimal_move(self, board):

        return


def make_move(board, genome, n_rows, n_cols):
    mine_count = board.mine_count
    is_mine = board.is_mine
    optimal_move = []
    for iter1 in range(n_rows):
        for iter2 in range(n_cols):
            optimal_move = genome.get_optimal_move(board)
    board.open_tile(0, 1)
    board.update_view()
    return

