# import sys
import os

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ___________________________________________________________________________ #
def F_initialPosition(pathXY):

        if not os.path.exists(pathXY):
            with open(pathXY, 'w') as file:
                file.write('')

        with open(pathXY, 'r') as file:
            contents = file.read()

        if contents:
            parts  = [part.strip() for part in contents.split(',')]
            x      = int(parts[0]) if int(parts[0]) > 0 else 50  
            y      = int(parts[1]) if int(parts[1]) > 0 else 50 
            width  = int(parts[2]) if int(parts[2]) > 0 else 840
            height = int(parts[3]) if int(parts[3]) > 0 else 480 
        
        else:
            x      = 50
            y      = 50
            width  = 840
            height = 480

        return x, y, width, height

# ___________________________________________________________________________ #
def F_savePosition(currentScreen, pathXY):

    # Save the current window position
    x      = currentScreen.x()
    y      = currentScreen.y()
    width  = currentScreen.width()
    height = currentScreen.height()

    with open(pathXY, "w") as arquivo:
        arquivo.write(f"{x},{y},{width},{height}")

# ___________________________________________________________________________ #
