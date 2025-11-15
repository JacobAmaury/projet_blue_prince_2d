"""Image helpers for the UI layer.

This module provides lightweight wrapper classes around pygame surfaces to
simplify scaling, positioning and blitting of images used across UI screens.

Classes:
    Image: Abstract base class for image wrappers.
    ImageSimple: Wrapper for single images with a position and scaled cache.
    ImageReapeated: Wrapper for images that are repeated/ tiled at multiple positions.
    ImageRoom: Specialized wrapper for room images with precomputed rotations.

Utility functions are provided as static methods on `Image` to load images
with or without alpha transparency.
"""

import pygame
from abc import ABC, abstractmethod


class Image(ABC):
    """Abstract base for image wrapper objects.

    Subclasses wrap a loaded pygame Surface and provide a `scale` method that
    caches scaled or transformed surfaces for blitting. The concrete API used
    by screens is intentionally small: `scale(...)` followed by a blit method
    on the specific subclass.
    """

    def __init__(self, loaded_image):
        """Store the raw loaded pygame Surface.

        Args:
            loaded_image (pygame.Surface): The surface returned by pygame.image.load.
        """
        self.loaded = loaded_image

    @abstractmethod
    def scale(self, size):
        """Scale or transform the wrapped image for later blitting.

        This abstract method must be implemented by subclasses to generate and
        cache one or more transformed surfaces in a subclass-specific attribute
        (for example `scaled` or `scaled[i]`). The `size` parameter semantics
        depend on the subclass.

        Args:
            size (tuple): Width/height or other size descriptor (subclass-specific).
        """
        pass

    # Static convenience loaders -------------------------------------------------
    @staticmethod
    def loadFull(path):
        """Load an image and convert it to the display format (no alpha).

        Args:
            path (str): File path to the image.

        Returns:
            pygame.Surface: Converted surface without per-pixel alpha.
        """
        return pygame.image.load(path).convert()

    @staticmethod
    def loadTransparent(path):
        """Load an image keeping per-pixel alpha (transparent backgrounds).

        Args:
            path (str): File path to the image.

        Returns:
            pygame.Surface: Converted surface with per-pixel alpha.
        """
        return pygame.image.load(path).convert_alpha()


class ImageSimple(Image):
    """Simple single-image wrapper.

    Use this class for images that have a single position on screen. After
    initialisation call `scale(size)` or `smoothscale(size)` to prepare the
    scaled surface and then `blit(buffer)` to draw it at `self.position`.
    """

    def __init__(self, loaded_image):
        Image.__init__(self, loaded_image)
        self.scaled = None
        self.position = None

    def smoothscale(self, size):
        """Smoothly scale the image and cache the result.

        Args:
            size (tuple): (width, height) in pixels.
        
        Returns:
            None
        """
        self.scaled = pygame.transform.smoothscale(self.loaded, size)

    def scale(self, size):
        """Scale the image (fast) and cache the result.

        Args:
            size (tuple): (width, height) in pixels.
        
        Returns:
            None
        """
        self.scaled = pygame.transform.scale(self.loaded, size)

    def blit(self, buffer):
        """Blit the cached scaled image onto the given buffer at `self.position`.

        Args:
            buffer (pygame.Surface): Destination surface.
        
        Returns:
            None
        """
        buffer.blit(self.scaled, self.position)


class ImageReapeated(Image):
    """Wrapper for images that are drawn multiple times at different positions.

    The class stores a `positions` list and a single `scaled` surface which is
    blitted repeatedly by index using `blit_single`.
    
    Note:
        The class name has a (mis)spelling variant: `ImageReapeated` instead of
        `ImageRepeated`. This is the current name used throughout the codebase. (¬_¬")
    """

    def __init__(self, loaded_image):
        Image.__init__(self, loaded_image)
        self.positions = []
        self.scaled = None

    def scale(self, size):
        """Scale the underlying image once for all repeated draws.

        Args:
            size (tuple): (width, height) in pixels to scale to.
        
        Returns:
            None
        """
        self.scaled = pygame.transform.scale(self.loaded, size)

    def blit_single(self, buffer, id):
        """Blit the scaled image at the position indexed by `id`.

        Args:
            buffer (pygame.Surface): Destination surface.
            id (int): Index in the `positions` list.
        
        Returns:
            None
        """
        buffer.blit(self.scaled, self.positions[id])


class ImageRoom(Image):
    """Room image wrapper that precomputes rotated variants.

    Stores four rotated versions of a room image to avoid recomputing rotations
    on each frame. `scale(room_size)` expects a `(w_size, h_size)` tuple and
    populates `self.scaled` with four variants corresponding to 0, 90, 180 and
    270 degree orientations.
    """

    def __init__(self, loaded_image):
        Image.__init__(self, loaded_image)
        self.positions = []
        self.scaled = [None] * 4  # [0:0°,1:90°,2:180°,3:270°]

    def scale(self, room_size):
        """Scale and precompute rotated images for the room.

        Args:
            room_size (tuple): (width, height) in pixels used for the base orientation.
        
        Returns:
            None
        """
        (w_size, h_size) = room_size
        # base orientation (0°)
        self.scaled[0] = pygame.transform.scale(self.loaded, (w_size, h_size))
        # 180° rotation from base
        self.scaled[2] = pygame.transform.rotate(self.scaled[0], 180)
        # due to some background/screen ratio differences, create a temporary
        # scaled image with swapped dimensions then rotate for 90°/270° variants
        im_temp = pygame.transform.scale(self.loaded, (h_size, w_size))
        self.scaled[1] = pygame.transform.rotate(im_temp, 90)
        self.scaled[3] = pygame.transform.rotate(im_temp, 270)