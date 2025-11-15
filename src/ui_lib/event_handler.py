"""Event handler base utilities for UI screens.

This module provides a lightweight `EventHandler` class containing a set of
static methods that represent common user actions (escape, space, enter,
navigation, etc.). UI screens typically assign a handler class (often an
inner `MenuHandler` subclass) to `screen.event_handler`. The UI will call the
matching static method on that handler in response to pygame events.

The default implementations are intentionally no-ops (except `escape` which
posts a quit event) so that screens only need to override the handlers they
require. Methods are static to allow assigning the class itself rather than
an instance.

Pattern (used by all menu screens):
    Screens create a temporary inner class `MenuHandler(EventHandler)` that
    overrides specific static methods. Because the inner class is defined in
    a method scope, those static methods can access the enclosing instance
    (e.g., `self.running`, `self.selected`) via Python's closure mechanism.
    Once the handler is assigned to `self.event_handler`, the UI's
    `event_listener()` method forwards events by calling the appropriate
    static method on the handler class.
"""

import pygame


class EventHandler:
    """Default event handler with no-op methods to be overridden by screens.

    Screens and menus create subclasses (commonly named `MenuHandler`) that
    override the static methods corresponding to the keys they handle. Having
    no-op defaults keeps the event dispatching code simple and tolerant of
    missing handlers.
    """

    @staticmethod
    def escape():
        """Handle the Escape key.

        Default behaviour posts a `pygame.QUIT` event which will be handled by
        the main loop and typically terminate the application. Override this
        method in a screen-specific handler to intercept Escape.
        
        Returns:
            None
        """
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        return

    @staticmethod
    def space():
        """Handle the Space key (default: no-op).

        Commonly used to select or toggle items (e.g., 'take all' in Explore).
        Override in a subclass to implement behaviour.
        
        Returns:
            None
        """
        return

    @staticmethod
    def enter():
        """Handle the Enter/Return key (default: no-op).

        Override to confirm selections.
        
        Returns:
            None
        """
        return

    @staticmethod
    def back():
        """Handle the Back / Backspace key (default: no-op).

        Represents a 'go back' or cancel action; left as a no-op by default so
        screens that do not support back can ignore it harmlessly.
        
        Returns:
            None
        """
        return

    @staticmethod
    def up():
        """Handle an Up navigation action (default: no-op).
        
        Returns:
            None
        """
        return

    @staticmethod
    def down():
        """Handle a Down navigation action (default: no-op).
        
        Returns:
            None
        """
        return

    @staticmethod
    def left():
        """Handle a Left navigation action (default: no-op).
        
        Returns:
            None
        """
        return

    @staticmethod
    def right():
        """Handle a Right navigation action (default: no-op).
        
        Returns:
            None
        """
        return

    @staticmethod
    def explore():
        """Handle the exploration action (bound to the 'i' key by default).

        Override to trigger exploration-specific behaviour when applicable.
        
        Returns:
            None
        """
        return
