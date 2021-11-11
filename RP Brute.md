
# Evironments

RobotEnv:
     - position of the robot
	 - position of the ball
	 - has the ball
	 - size of the environment
	 
Strings:
     - string 
	 - position in the list of characters
	 
PixelImages:
     - size of the image
	 - pixel values (matrix)
	 - position of the pointer


# Language tokens


Class Token:

  - BoolToken:    ()
		  -	AtTop
		  -	AtBottom
		  -	AtLeft
		  -	AtRight
		  -	AtStart
		  -	AtEnd
		  -	isLetter
		  -	notLetter
		  -	isUpperCase
		  -	NotUpperCase
		  -	IsLowerCase
		  -	NotLowercase
		  -	IsNumber
		  -	NotNumber
		  -	isSpace
		  -	NotSpace
  -	TransToken:    (return the env)
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
  -	controlToken:
		  -	If (cond,b1,b2)
		  -	Recurse(cond, [base_case], [transform]+Recurse)
  -	InventedToken:  these come from the invent stage


Exception: throw the actual Python exception


Class AtTop:

  def apply(env):
       return True/False
	   
	   
Class MoveLeft:
   
       def apply(env):
	            do what you need
				return NewEnv/Exception


		  

					 