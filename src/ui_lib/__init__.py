"""UI library: pygame-based screens and components for the Blue Prince game.

This package provides the main UI layer for the Blue Prince 2D game. It includes:

- Window and Screen management (`window.py`)
- Event handling and dispatching (`event_handler.py`)
- Image loading and caching helpers (`image.py`)
- Layout and grid systems for inventory and map (`grids.py`)
- Screen implementations:
  - LoadScreen: asynchronous resource loading
  - MainScreen: main gameplay interface
  - MenuScreen subclasses: Shop, Explore, SelectRoom, EndScreen
- Window configuration and display utilities

All screens inherit from the abstract `Screen` base class and implement
`build()` and `blit()` to prepare and render their content.
"""
