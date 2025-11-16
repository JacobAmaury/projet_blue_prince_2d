# Blue_prince_2D

A 2D non-official fan-made rendition of the **Blue Prince** game, written in Python with Pygame.  
The goal was to recreate a basic version of the game. We managed to implement a really good UI and a lot of game mechanics.


---

## Features

- Grid-based room navigation  
- Procedural room selection with rarity & effects
- coffers with random loot
- dig holes to find items
- Inventory system (consumables, permanents, others)  
- Explore menu for looting items  
- Shop system  
- Door mechanics (open, locked, gem cost…)  
- Multiple UI screens:
  - Load screen  
  - Main screen  
  - Explore screen  
  - Shop  
  - Select Room  
  - End Screens  

---

## Requirements
- Python 3
- pip

## Install
1. Clone the repository
    ```sh
    git clone url_de_mon_projet.git
    ```
2. Create a virtual environment
    ```sh
    python -m venv venv
    source venv/bin/activate   # Linux / macOS
    venv\Scripts\activate      # Windows
    ```
3. Install the dependencies
    ```sh
    pip install -r requirements.txt
    ```

4. Launch the game
    ```sh
    python blueprince.py
    ```


## Controls

| Input             | Action                  |
| ----------------- | ----------------------- |
| **↑**             | Move up / navigate menu |
| **↓**             | Move down               |
| **←**             | Move left               |
| **→**             | Move right              |
| **SPACE**         | Select / take all       |
| **ENTER**         | Validate / take one     |
| **ESC**           | Cancel / Quit           |
| **I**             | Explore current room    |


## Authors

THOLIN Florian
JACOB Amaury
MALARVIJY Sharaine

## Credentials
Image resources:
- items icon : https://blueprince.wiki.gg/wiki/Allowance_Token
- permanent objects icon : https://blue-prince.fandom.com/wiki/Power_Hammer
- Menu background image : https://www.blueprincegame.com/
- Logo : https://fr.wikipedia.org/wiki/Blue_Prince
- other : https://www.vecteezy.com under Creative Commons Attribution License (CC BY)


For educational and non-commercial use only.
