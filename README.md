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
    git clone https://github.com/JacobAmaury/projet_blue_prince_2d.git
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

## Items description

| Item                    | Image                                                                             | Description                                                                                                                                 |
| ----------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Shovel**              | <img src="images/items/permanents/Shovel_White_Icon.png" width="64"/>             | Allows digging in **green rooms**, giving random loot (coins, gems, fruits…).                                                               |
| **Lockpick Kit**        | <img src="images/items/permanents/Lockpick_Kit_White_Icon.png" width="64"/>       | Automatically opens **level-1 locked doors** without spending a key.                                                                        |
| **Lucky Rabbit’s Foot** | <img src="images/items/permanents/Lucky_Rabbits_Foot_White_Icon.png" width="64"/> | Greatly improves item luck in rooms (better loot chances).                                                                                  |
| **Metal Detector**      | <img src="images/items/permanents/Metal_Detector_White_Icon.png" width="64"/>     | Increases the chance to find **keys / coins** and other valuables in rooms.                                                                 |
| **Power Hammer**        | <img src="images/items/permanents/Power_Hammer_White_Icon.png" width="64"/>       | Allows opening **coffers and lockers** *without consuming a key*.                                                                           |
| **Fall it a day**       | <img src="images/items/permanents/fall_it_a_day_White_Icon.png" width="64"/>      | Resets the entire map and sends the player back to the **EntranceHall**, while keeping the full inventory and all triggered global effects. |
| **Coupon_Book**       | <img src="images/items/permanents/Coupon_Book_White_Icon.png" width="64"/>      | The Coupon Book saves one Gold on any purchase made from any Shop




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



