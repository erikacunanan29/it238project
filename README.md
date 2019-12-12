Battle City

A game developed using Python and PyGame.

To Install PyGame:
        - pip install pygame
        
Available Classes:
        - Tank Class: Used to create objects for the instances of the Tank Players
        - Map Class: Used to render the map elements that will be the obstacles of the player
        - Bullet Class: Used to create bullets for an instance of a Tank Player
        
Collision Detection Available: 
        - Bullets and Tanks will stop when it reaches the min and max height of the window.
        - Bullets will hit enemy players. If an enemy is hit, the player who hit him/her will get 100 points. 

Other Functionalities Available:
        - Renders the scores of each of the available players.
        - Tanks will respawn after 5 seconds of being hit. 
	- Random map generator, get random map from the Maps directory	
	- Game will end when all players are in state = False, if only one tank is active game ends
	- Game over screen will show the winner
        
OTHER COLLISION DETECTION:
        - Tanks collide with each other.(missing)
        - Tanks collide with map elements.
	- Bullets collide with map elements(brick/steel).

How To Run
	- python3 main.py

