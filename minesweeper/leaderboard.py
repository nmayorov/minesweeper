import pygame


class Leaderboard:
    """Store, update and display leaderboard.

    Parameters
    ----------
    font : pygame.Font
        Font to use.
    font_color : pygame.Color compatible
        Font color.
    max_items : int
        Maximum number of items to store for each difficulty.
    width : int
        Total width of the leaderboard.
    data : dict
        Dictionary with keys 'EASY', 'NORMAL', 'HARD', for each key there is
        a list of (name, time) tuples describing player results.
        If None (default), create empty dictionary.
    """
    def __init__(self, font, font_color, max_items, width,
                 data=None):
        self.font = font
        self.font_color = font_color
        self.max_items = max_items

        self.section_width = width // 3
        self.text_height = font.get_height()
        self.horizontal_margin = 2 * font.size("|")[0]
        self.vertical_margin = 0.5 * self.text_height

        self.width = 3 * self.section_width
        self.height = ((4 + max_items) * self.vertical_margin
                       + (2 + max_items) * self.text_height)

        self.surface = pygame.Surface((self.width, self.height),
                                      pygame.SRCALPHA)
        self.rect = self.surface.get_rect()

        self.title = font.render("LEADER BOARD", True, font_color)
        self.easy_title = font.render("EASY", True, font_color)
        self.normal_title = font.render("NORMAL", True, font_color)
        self.hard_title = font.render("HARD", True, font_color)
        self.list_start_y = (self.vertical_margin + 2 * self.text_height
                             + self.text_height + self.vertical_margin)

        if data is None:
            self.data = {'EASY': [], 'NORMAL': [], 'HARD': []}
        else:
            self.data = data

        self._prepare_render()

    def _prepare_surface(self):
        """Prepare surface with all titles."""
        self.surface.fill((0, 0, 0, 0))

        title_top = self.vertical_margin
        section_titles_top = title_top + 2 * self.text_height
        line_top = section_titles_top + self.text_height

        frame_x = 0
        frame_y = title_top + self.text_height + self.vertical_margin
        pygame.draw.line(self.surface, self.font_color,
                         (frame_x, frame_y),
                         (self.width, frame_y))
        pygame.draw.line(self.surface, self.font_color,
                         (frame_x, frame_y),
                         (frame_x, self.height))
        pygame.draw.line(self.surface, self.font_color,
                         (self.width - 1, frame_y),
                         (self.width - 1, self.height))
        pygame.draw.line(self.surface, self.font_color,
                         (frame_x, self.height - 1),
                         (self.width, self.height - 1))
        pygame.draw.line(self.surface, self.font_color,
                         (self.section_width, line_top),
                         (self.section_width,
                          self.height - self.vertical_margin))
        pygame.draw.line(self.surface, self.font_color,
                         (2 * self.section_width, line_top),
                         (2 * self.section_width,
                          self.height - self.vertical_margin))

        title_rect = self.title.get_rect(
            top=self.vertical_margin, centerx=0.5 * self.width)
        easy_title_rect = self.easy_title.get_rect(
            top=section_titles_top, centerx=0.5 * self.section_width)
        normal_title_rect = self.normal_title.get_rect(
            top=section_titles_top, centerx=1.5 * self.section_width)
        hard_title_rect = self.hard_title.get_rect(
            top=section_titles_top, centerx=2.5 * self.section_width)

        self.surface.blit(self.title, title_rect)
        self.surface.blit(self.easy_title, easy_title_rect)
        self.surface.blit(self.normal_title, normal_title_rect)
        self.surface.blit(self.hard_title, hard_title_rect)

    def _prepare_render(self):
        """Prepare surface to render."""
        self._prepare_surface()
        x_name = self.horizontal_margin
        x_time = self.section_width - self.horizontal_margin
        for difficulty in ["EASY", "NORMAL", "HARD"]:
            y = self.list_start_y
            for name, time in self.data[difficulty]:
                name_image = self.font.render(name, True, self.font_color)
                score_image = self.font.render(str(time), True, self.font_color)
                time_width = self.font.size(str(time))[0]
                self.surface.blit(name_image, (x_name, y))
                self.surface.blit(score_image,
                                  (x_time - time_width, y))
                y += self.text_height + self.vertical_margin

            x_name += self.section_width
            x_time += self.section_width

    def needs_update(self, difficulty, time):
        """Check whether the leaderboard needs to be updated."""
        if difficulty not in self.data:
            return False

        data = self.data[difficulty]
        if len(data) < self.max_items:
            return True

        return data[-1][1] > time

    def update(self, difficulty, name, time):
        """Update the leaderboard."""
        if difficulty not in self.data:
            return

        data = self.data[difficulty]
        i = 0
        while i < len(data) and time >= data[i][1]:
            i += 1
        data.insert(i, (name, time))

        if len(data) > self.max_items:
            data.pop()

        self._prepare_render()

    def draw(self, surface):
        """Draw on the surface."""
        surface.blit(self.surface, self.rect)