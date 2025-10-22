#This is a pseudo os-independant shortcut to './src/main.py'

import sys
import os
target_path = os.path.join(os.path.dirname(__file__),'src')
sys.path.append(target_path)    #set python import Path './src/main.py'
os.chdir(target_path)           #set cwd to './src/main.py'

#execute main
import main                     # pyright: ignore[reportMissingImports] 