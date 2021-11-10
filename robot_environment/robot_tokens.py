"""
Bool

Trans
Move down
Move right
Move left
Move up
Drop
Grab

-	Grab (robots) - grabs a ball into hand 
						  -	if the ball is not at the current position, don't take anything
		  -	Drop (robots)  - drop a ball at the current position
						  -	if no ball in hand, nothing happens
		  -	MoveRight (robots/strings/pixels) - move the position of the robot to the right
						  -	if it crosses the boundary, return exception
						  -	if it holds the ball, also change the position of the ball 
		  -	MoveLeft (robots/strings/pixels)
		  -	MoveUp (robots/pixels)
		  -	MoveDown (robots/pixels)
		  -	MakeUppercase (strings) - make the character at the current position uppercase 
								  -	if it is already uppercase, no changes
		  -	MakeLowercase (string) - opposite of MakeUppercase
		  -	Drop (strings) - drop the current character
					  -	if the last char, then delete and move one position to the left 
		  -	DrawPixel (pixels)- set the pixel at the current position to 1
"""

from common_environment.abstract_tokens import *
from common_environment.environment import *

class AtTop(BoolToken):
    pass 

class AtBottom(BoolToken):
    pass

class AtLeft(BoolToken):
    pass

class AtRight(BoolToken):
    pass




