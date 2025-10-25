# Blue_prince_2D

A 2D rendition of the the Blue Prince game, just for fun !

## Requirements
- Python 3
- pip

## Install
1. Clone the deposit
    ```sh
    git clone url_de_mon_projet.git
    ```
2. Create a virtual environnement

3. Install the dependencies
    ```sh
    pip install -r requirements.txt
    ```


## Launch
Set cwd to ```src/``` then run:
```sh
python main.py
```
Or from any cwd :
- you may create a shortcut to src/main.py
- you can run file  : ```blueprince.py``` (with python)\
It is a pseudo os-independant shortcut to ./src/main.py (automatically sets the cwd)\
Note : the blueprince.py file must stay at Project root.

## Developpement
The UserInterface and the game controller (Navigation) have been separated and can be tested independently.\
Run ```test_ui.py``` for UI testing, and ```test_nav.py``` fo Navigation.

You can do so either from ```./src``` ro from ```./test``` :

Set cwd to ```src/``` then run:
```sh
python ../test/test_ui.py
```
Or from cwd at ```test/```, run:
```sh
python test_ui.py
```

## Authors

## Credentials
Image ressources:
- items icon : https://blueprince.wiki.gg/wiki/Allowance_Token
- permanant objects icon : https://blue-prince.fandom.com/wiki/Power_Hammer
- Menu background image : https://www.blueprincegame.com/
- Logo : https://fr.wikipedia.org/wiki/Blue_Prince
