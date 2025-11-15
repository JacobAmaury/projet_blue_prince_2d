"""Window and Screen helpers for the UI subsystem.

This module exposes two primary classes used by the UI layer:

- `Window`: Responsible for creating and managing the pygame display surface
  (window size, icon, buffer) and providing utilities for sizing the window
  to fit the user's desktop while preserving a target aspect ratio.
  The point being that you can't maximize the window with pygame, so this
  class does the best it can to pick a large size that fits the screen.
- `Screen`: Abstract base class for all drawable UI screens. Screens access
  the global `Screen.window` set by `Window` to obtain the current buffer
  surface, and more directly the default font sizing and the default `event_handler`.

The design uses small, focused helpers so screen implementations can focus
on layout and drawing logic.
"""

import pygame
from .event_handler import EventHandler
from abc import ABC, abstractmethod


class Window:
    """Manage the application window and its size/scale configuration.
    
    Handles creation of the pygame display surface, desktop sizing,
    window resizing, and aspect ratio management. The Window is created
    hidden initially (to allow image conversion), then made visible when
    the UI is ready to display.
    
    Class Attributes:
        WINDOW_RATIO (tuple): Target aspect ratio (16, 9) used for resizing.
        default_window_size (tuple): Preferred initial window size (1920, 1080).
    
    Attributes:
        ui: Reference to the top-level UI controller.
        size (tuple): Current window size (width, height) in pixels.
        buffer (pygame.Surface): Display surface for rendering.
        desk_W, desk_H (int): Desktop dimensions in pixels.
    """

    WINDOW_RATIO = (16, 9)
    default_window_size = (1920, 1080)

    def __init__(self, UI):
        """Create the window object and prepare the hidden display buffer.

        This will query the desktop size, choose a fitting window size using
        `window_try_size`, set the window caption and icon, and create an
        initially-hidden display buffer. The global `Screen.window` is set
        to this instance so screens can access the buffer and size.

        Args:
            UI: The top-level UI controller class (used by screens to access
                shared objects such as the current player).
        """
        self.ui = UI
        # window size
        self.desk_W, self.desk_H = pygame.display.get_desktop_sizes()[0]
        W, H = self.window_try_size(self.default_window_size)
        self.size = W, H
        # window creation
        pygame.display.set_caption("Blue prince 2D")
        blueprince_icon = pygame.image.load("../images/blueprince_icon.jpeg")
        pygame.display.set_icon(blueprince_icon)
        # create a hidden buffer first (allows image conversion later)
        self.buffer = pygame.display.set_mode(self.size, pygame.HIDDEN)
        Screen.window = self

    def show_window(self):
        """Show the previously created buffer as a resizable window.

        Call this when the UI is ready to be displayed to the user.
        
        Returns:
            None
        """
        self.buffer = pygame.display.set_mode(self.size, pygame.RESIZABLE)

    def set_window_size(self, W, H):
        """Update the stored window size.

        This does not re-create the display mode; use `show_window` to apply
        resizable behavior when needed.
        
        Returns:
            None
        """
        self.size = W, H

    def window_try_size(self, window_size):
        """Return a window size that fits inside the desktop while preserving
        the configured aspect ratio.

        If the requested `window_size` is larger than the desktop, this will
        reduce it down using `maximize_window_with_ratio`.

        Args:
            window_size (tuple): Desired (width, height) in pixels.

        Returns:
            tuple[int, int]: Adjusted (width, height) suitable for the current desktop.
        """
        W, H = window_size
        # if default_window_size > display_size
        if W > self.desk_W or H > self.desk_H:
            (W, H) = self.maximize_window_with_ratio(self.desk_W, self.desk_H, W, H)
        return (W, H)

    def maximize_window_with_ratio(self, desk_w, desk_h, W, H):
        """Reduce (W,H) in steps (respecting the target ratio) until it fits
        within (desk_w, desk_h).

        This helper subtracts the ratio width/height in a loop until the size
        fits the desktop, preserving the aspect ratio defined by
        `WINDOW_RATIO`.
        
        Args:
            desk_w (int): Desktop width in pixels.
            desk_h (int): Desktop height in pixels.
            W (int): Candidate window width.
            H (int): Candidate window height.
        
        Returns:
            tuple[int, int]: Adjusted (width, height) fitting within desktop bounds.
        """
        ratio_W, ratio_H = self.WINDOW_RATIO
        while W > desk_w or H > desk_h:
            W -= ratio_W
            H -= ratio_H
        return (W, H)


class Screen(ABC):
    """Abstract base for drawable screens in the UI.

    Screens access the global `Screen.window` to obtain the current buffer
    surface and sizing information. Subclasses must implement `build` and
    `blit` to prepare and draw the screen contents. A default `event_handler`
    class is provided which screens can override by assigning `self.event_handler`.
    
    All screens share class attributes that store loaded images (populated
    by LoadScreen): `consumable_imgs`, `permanant_imgs`, `room_imgs`, 
    `bg_color_images`, `other_imgs`. These are set once and reused by all
    screen instances.
    
    Class Attributes:
        window (Window): Global reference to the active Window object.
        FONT_SIZE (float): Base font size relative to screen height.
        TXT_POSITION (tuple): Default center position for text overlay (0-1 relative).
        FONT (str): Font name used for all text rendering.
        consumable_imgs (dict): Cached consumable item images.
        permanant_imgs (dict): Cached permanent item images.
        room_imgs (dict): Cached room images.
        bg_color_images (dict): Cached background images by color.
        other_imgs (dict): Cached misc item images.
    """

    window = None  # set by Window
    FONT_SIZE = 0.035
    TXT_POSITION = (0.5, 0.875)  # center_position
    FONT = 'Arial'

    def __init__(self):
        """Initialise common screen properties (font, buffer, event handler).
        
        Returns:
            None
        """
        self.size = Screen.window.size
        self.buffer = Screen.window.buffer
        self.event_handler = EventHandler
        _, h = self.size
        self.font = pygame.font.SysFont(self.FONT, int(h * self.FONT_SIZE))

    def print(self, msg):
        """Utility: render a centered text message and flip the display.
        
        Renders a message at the screen's default TXT_POSITION and updates
        the display immediately. The message will be displayed until the
        next screen update (or blit). Useful for debug messages or temporary
        notifications.

        Args:
            msg (str): Message text to render.
        
        Returns:
            None
        """
        txt = self.font.render(msg, True, (255, 255, 255))
        X, Y = self.TXT_POSITION
        w, h = self.size
        txt_w, txt_h = txt.get_size()
        position = (X * w - txt_w / 2, Y * h + txt_h / 2)
        self.buffer.blit(txt, position)
        pygame.display.flip()   #needed to show immediately (for debug messages)

    def update(self):
        """Rebuild and blit the screen content.

        Calls the abstract `build` followed by `blit`. Subclasses should use
        `build` to prepare surfaces and `blit` to draw them to `self.buffer`.
        This is typically called during initialization and after significant
        state changes (e.g., inventory update, player movement).
        
        Returns:
            None
        """
        self.build()
        self.blit()

    @abstractmethod
    def build(self):
        """Prepare any scaled surfaces or layout for the screen (abstract).
        
        Subclasses implement this to compute positions, scale images, and
        render text surfaces based on the current `self.size` and other
        mutable state. Called by `update()` before `blit()`.
        
        Returns:
            None
        """
        pass

    @abstractmethod
    def blit(self):
        """Blit prepared surfaces onto `self.buffer` (abstract).
        
        Subclasses implement this to compose and draw their UI elements to
        `self.buffer`. Called by `update()` after `build()`.
        
        Returns:
            None
        """
        pass

    # loaded images (populated by the load screen)
    consumable_imgs = {}
    permanant_imgs = {}  # Note: spelled "permanant" (not "permanent") throughout codebase (¬_¬")
    room_imgs = {}
    bg_color_images = {}
    other_imgs = {}
