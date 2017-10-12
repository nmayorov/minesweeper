import pygame


LEFT_CLICK = 1


def draw_frame(width, height, frame_color):
    """Draw a rectangular frame on a transparent surface."""
    frame = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.line(frame, frame_color, (0, 0), (width, 0))
    pygame.draw.line(frame, frame_color, (0, 0), (0, height))
    pygame.draw.line(frame, frame_color, (width - 1, 0), (width - 1, height))
    pygame.draw.line(frame, frame_color, (0, height - 1), (width, height - 1))
    return frame


def draw_crossed_square_with_frame(side, color):
    """Draw a square frame with a cross on it."""
    frame = draw_frame(side, side, color)
    shift = 0.3 * side
    pygame.draw.line(frame, color,
                     (shift, shift), (side - shift, side - shift))
    pygame.draw.line(frame, color,
                     (side - shift, shift), (shift, side - shift))
    return frame


class GUIElement:
    """Base class for all GUI elements.

    It assumes that a game element must have a surface to display, and
    `rect` with the size equal to the size of surface.

    You should modify `rect` attribute in order to place the surface.

    Parameters
    ----------
    surface : pygame.Surface
        Element's surface.
    """
    def __init__(self, surface):
        self.surface = surface
        self.rect = self.surface.get_rect()

    def draw(self, other_surface):
        """Draw the element on the other surface.

        ``self.rect`` is used for positioning.
        """
        other_surface.blit(self.surface, self.rect)


class Label(GUIElement):
    """Label GUI element.

    Parameters
    ----------
    font : pygame.Font
        Font to use.
    font_color : compatible with pygame.Color
        Font color.
    text : string
        Label text.
    """
    def __init__(self, font, font_color, text):
        self.font = font
        self.font_color = font_color
        super(Label, self).__init__(font.render(text, True, font_color))

    def set_text(self, text):
        """Set text."""
        old_center = self.rect.center
        self.surface = self.font.render(text, True, self.font_color)
        self.rect = self.surface.get_rect(center=old_center)

    def render(self):
        """Return surface to display."""
        return self.surface


class Button(GUIElement):
    """Button GUI element.

    The visual is a text in a rectangular frame.

    Parameters
    ----------
    font : pygame.Font
        Font to use.
    font_color : compatible with pygame.Color
        Color to use.
    text : string
        Text on button.
    on_click_callback : callable
        Call on click, accepts no arguments. No callback by default.
    frame_color : compatible with pygame.Color
        Color to use for the frame. Use `font_color` by default.
    """
    def __init__(self, font, font_color, text, on_click_callback,
                 frame_color=None):
        self.text = font.render(text, True, font_color)
        margin = 1.5 * font.size("_")[0]
        if frame_color is None:
            frame_color = font_color

        surface = draw_frame(self.text.get_width() + margin,
                             1.2 * self.text.get_height(),
                             frame_color)
        super(Button, self).__init__(surface)
        rect = self.text.get_rect(center=self.rect.center)
        self.surface.blit(self.text, rect.topleft)
        self.on_click_callback = on_click_callback

    def on_mouse_up(self, button):
        """Handle mouse button up."""
        if button != LEFT_CLICK or self.on_click_callback is None:
            return

        if self.rect.collidepoint(*pygame.mouse.get_pos()):
            self.on_click_callback()


class SelectionGroup(GUIElement):
    """Selector from one of many options.

    Parameters
    ----------
    font : pygame.Font
        Font to display text.
    font_color : compatible with pygame.Color
        Font color.
    title : string
        Title for the group.
    options : list of string
        Option names.
    on_change_callback : callable, optional
        Callable with signature ``on_change_callback(option)`` called
        when a new option is selected. No callback by default.
    """
    def __init__(self, font, font_color,
                 title, options,
                 on_change_callback=None,
                 initial_value=None):
        item_size = font.get_height()

        self.unselected_image = draw_frame(item_size, item_size,
                                           font_color)
        self.selected_image = draw_crossed_square_with_frame(item_size,
                                                             font_color)

        self.options = options
        self.n_options = len(options)

        self.title_image = font.render(title, True, font_color)
        option_images = [font.render(option, True, font_color)
                         for option in options]

        item_widths = [1.5 * item_size + option_image.get_width()
                       for option_image in option_images]
        width = max(max(item_widths), self.title_image.get_width())
        height = (self.title_image.get_height()
                  + 0.5 * item_size
                  + 1.5 * item_size * self.n_options)

        super(SelectionGroup, self).__init__(pygame.Surface((width, height),
                                                            pygame.SRCALPHA))
        title_rect = self.title_image.get_rect(centerx=self.rect.centerx)

        self.button_rects = []
        self.item_rects = []
        option_rects = []
        y = title_rect.bottom + 0.5 * item_size
        for option_image, item_width in zip(option_images, item_widths):
            button_rect = self.unselected_image.get_rect(y=y)
            option_rect = option_image.get_rect(
                x=button_rect.right + 0.5 * button_rect.width,
                centery=button_rect.centery)
            item_rect = pygame.Rect(0, y, item_width, item_size)
            self.button_rects.append(button_rect)
            option_rects.append(option_rect)
            self.item_rects.append(item_rect)
            y += 1.5 * item_size

        self._selected = 0
        if initial_value is not None:
            for i, option in enumerate(self.options):
                if option == initial_value:
                    self._selected = i
                    break

        self.callback = on_change_callback

        self.surface_stub = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface_stub.fill((0, 0, 0, 0))
        self.surface_stub.blit(self.title_image, title_rect.topleft)
        for option_rect, option_image in zip(option_rects, option_images):
            self.surface_stub.blit(option_image, option_rect)
        self._render()

    @property
    def selected(self):
        """Currently selected option."""
        return self.options[self._selected]

    def _render(self):
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.surface_stub, (0, 0))
        for i, rect in enumerate(self.button_rects):
            if i == self._selected:
                self.surface.blit(self.selected_image, rect)
            else:
                self.surface.blit(self.unselected_image, rect)

    def on_mouse_up(self, button):
        """Handle mouse button up."""
        if button != LEFT_CLICK:
            return

        mouse_pos = pygame.mouse.get_pos()
        x = mouse_pos[0] - self.rect.left
        y = mouse_pos[1] - self.rect.top
        selected_old = self._selected
        for i, (button_rect, item_rect) in enumerate(
                zip(self.button_rects, self.item_rects)):
            if item_rect.collidepoint(x, y):
                if self.callback is not None and i != self._selected:
                    self.callback(self.options[i])
                self._selected = i
                break

        if self._selected != selected_old:
            self._render()


class Input(GUIElement):
    """Text input.

    It displays a title and a value. Value can be modified by clicking on
    it (if `active_input` is True).

    Parameters
    ----------
    font : pygame.Font
        Font to use.
    font_color : compatible with pygame.Color
        Font color.
    title : string
        Input title.
    value : string
        Input value. Everything will be converted to string.
    delimiter : string
        Delimiter between title and value. Two spaces by default.
    frame_color : pygame.Color compatible, optional
        Color for frame when displaying value being edit. Use `font_color`
        by default.
    active_input : bool, optional
        Whether to allow modifying value by clicking on it. False by default.
    width : int, optional
        Element width. If given the text be centred in a rectangle of the
        given width. If None (default), width be equal to the current text
        to display.
    max_value_length : int, optional
        Maximum length of the value string. Unlimited by default.
    key_filter : callable, optional
        Called like ``key_filter(key_name)`` to determine whether a symbol
        should be accepted. No filter by default.
    on_enter_callback : callable, optional
        Callable to call when the value is entered. The signature is
        ``on_enter_callback(value)``. No callback by default.
    """
    def __init__(self, font, font_color, title, value, delimiter="  ",
                 frame_color=None, active_input=False,
                 width=None, max_value_length=None, key_filter=None,
                 on_enter_callback=None):
        self.font = font
        self.font_color = font_color
        self.width = width
        self._active_input = active_input
        self.in_input = False
        self.title = title
        self.value = str(value)
        self.current_value = self.value
        self.delimiter = delimiter
        if frame_color is None:
            frame_color = font_color
        self.frame_color = frame_color
        self.max_value_length = max_value_length
        self.key_filter = key_filter
        self.on_enter_callback = on_enter_callback

        self.surface = None
        self.text = None
        self.boarder = None
        self.text_rect = None
        self.value_rect = None
        self.rect = None
        self._render()
        super(Input, self).__init__(self.surface)

    def _render(self):
        """Prepare data for render, called as necessary."""
        value = self.current_value
        if self.in_input:
            value += '_'

        text = self.font.render(self.title + self.delimiter + value,
                                True,
                                self.font_color)

        if self.width is None:
            width = text.get_width()
        else:
            width = self.width
        height = text.get_height()
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        text_rect = text.get_rect(center=surface.get_rect().center)

        title_width = self.font.size(self.title + self.delimiter)[0]
        value_width, value_height = self.font.size(value)
        margin = self.font.size('|')[0]
        value_rect = pygame.Rect(text_rect.left + title_width - margin,
                                 text_rect.top,
                                 value_width + 2 * margin,
                                 value_height)

        if self._active_input:
            frame = draw_frame(value_rect.width,
                               value_rect.height,
                               self.frame_color)
            surface.blit(frame, value_rect)
        surface.blit(text, text_rect)
        self.surface = surface
        self.value_rect = value_rect
        if self.rect is not None:
            self.rect.size = surface.get_size()

    @property
    def active_input(self):
        return self._active_input

    @active_input.setter
    def active_input(self, value):
        if value != self._active_input:
            self._active_input = value
            self._render()

    def set_value(self, value):
        """Set value."""
        value = str(value)
        self.current_value = value
        self.value = self.current_value
        self._render()

    def on_mouse_up(self, button):
        """Handle mouse button up."""
        if not self._active_input or button != LEFT_CLICK:
            return

        mouse_pos = pygame.mouse.get_pos()
        x = mouse_pos[0] - self.rect.x
        y = mouse_pos[1] - self.rect.y

        if self.value_rect.collidepoint(x, y):
            self.in_input = True
        else:
            self.in_input = False
            self.current_value = self.value

        self._render()

    def on_key_down(self, event):
        """Handle key down."""
        if not self.in_input:
            return

        key = event.key
        if key == pygame.K_BACKSPACE:
            if self.current_value:
                self.current_value = self.current_value[:-1]
                self._render()
        elif key == pygame.K_RETURN:
            self.in_input = False
            if self.on_enter_callback is not None:
                new_value = str(self.on_enter_callback(self.current_value))
            else:
                new_value = self.current_value
            self.set_value(new_value)
            self._render()
        else:
            if len(self.current_value) == self.max_value_length:
                return

            key_name = event.unicode
            if self.key_filter is None or self.key_filter(key_name):
                self.current_value += key_name
                self._render()


class InputDialogue(GUIElement):
    """Dialogue to input some value.

    Parameters
    ----------
    font : pygame.Font
        Font to use.
    font_color : pygame.Color compatible
        Color for font.
    title : string
        Input title.
    on_enter_callback : callable
        Call on enter like ``on_enter_callback(value)``.
    max_length : int, optional
        Maximum allowed length of the value. Unlimited by default.
    key_filter : callable, optional
        Called like ``key_filter(key_name)`` to determine whether a symbol
        should be accepted. No filter by default.
    """
    def __init__(self, font, font_color, title, on_enter_callback,
                 max_length=None, key_filter=None):
        self.font = font
        self.font_color = font_color
        self.title_image = font.render(title, True, font_color)
        line_height = font.get_height()
        vertical_margin = 0.5 * line_height
        horizontal_margin = font.size("_")[0]

        width = self.title_image.get_width() + 2 * horizontal_margin
        height = 3 * vertical_margin + 2 * line_height

        super(InputDialogue, self).__init__(draw_frame(width, height,
                                                       self.font_color))

        self.title_image_rect = self.title_image.get_rect(x=horizontal_margin,
                                                          y=vertical_margin)

        self.rect = self.surface.get_rect()

        self.value_top = 2 * vertical_margin + line_height

        self.value = ""
        self.on_enter_callback = on_enter_callback
        self.max_length = max_length
        self.key_filter = key_filter

        self._render()

    def _render(self):
        width, height = self.surface.get_size()
        self.surface = draw_frame(width, height, self.font_color)
        self.surface.blit(self.title_image, self.title_image_rect)
        value_image = self.font.render(self.value + "_", True, self.font_color)
        rect = value_image.get_rect(top=self.value_top,
                                    centerx=0.5 * self.surface.get_width())
        self.surface.blit(value_image, rect)

    def set_value(self, value):
        """Set value."""
        self.value = value
        self._render()

    def on_key_down(self, event):
        """Handle key down."""
        key = event.key
        if key == pygame.K_BACKSPACE:
            if self.value:
                self.value = self.value[:-1]
                self._render()
                self._render()
        elif key == pygame.K_RETURN:
            self.on_enter_callback(self.value)
        else:
            if (self.max_length is not None
                    and len(self.value) == self.max_length):
                return

            key_name = event.unicode
            if self.key_filter is None or self.key_filter(key_name):
                self.value += key_name
                self._render()
