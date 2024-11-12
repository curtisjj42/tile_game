## Python Version
This project was created with Python 3.11.  
Other versions of python may not work as intended.

## Project Overview
This project was developed as part of a Master's program course designed to facilitate holistic comprehensive learning of software development skills and best practices. All resources are provided by Northeastern University as part of relevant course materials. Operation of this game is not limited to the provided puzzle files and can be completed with any appropriately formatted .puz file.
The goal of this project is to create a digitally playable "tile mover game", a classic puzzle in which the player attempts to create a picture out of tiles by moving them into the appropriate positions. There is one empty tile square which allows neighbor tiles to shift into different positions for solving. 

## Winning the Game
The game is considered "won" when all tiles are in the appropriate position to create the unbroken picture. Each .puz file is equipped with a thumbnail image which represents the target puzzle state.

## Adding Puzzle Files
Any picture can be added to this game using an image splitter such as https://pinetools.com/split-image as follows:
1. The selected number of blocks must be a square (2x2 = 4, 3x3 = 9, etc.). Higher numbers equate to more difficult puzzles
2. All files should be stored as .png or .gif files
3. A blank tile is provided in the Images folder under each provided puzzle. Copy this and remove either the 1st or last block of your split image
4. Make a new folder titled as the name of your puzzle and save each block as 1.gif, 2.gif, etc. ordinally from top left to bottom right of the image
5. Format a .txt file with the puzzle name, number of tiles, block size (in pixels), thumbnail image (original picture file), and the path for each .gif/.png file ("Images/{puzzle_name}/{1.gif}")
6. Save this .txt file with the suffix .puz
7. Save the puzzle directory under the "Images" directory and the .puz file in the primary project directory
  
## Playing the Game  
1. Download all project files
2. Add any puzzles besides those provided
3. Ensure python is appropraitely updated and you have a valid interpreter configured
4. Run puzzle_game.py and select your puzzle from the intro screen\
5. Play your puzzle!
