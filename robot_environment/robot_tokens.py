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
"""

from common_environment.abstract_tokens import *
from common_environment.environment import *


class AtTop(BoolToken):
    def apply(self, env: Environment) -> bool:
        return env.ry == 0


class AtBottom(BoolToken):
    def apply(self, env: Environment) -> bool:
        return env.ry == env.size - 1


class AtLeft(BoolToken):
    def apply(self, env: Environment) -> bool:
        return env.rx == 0


class AtRight(BoolToken):
    def apply(self, env: Environment) -> bool:
        return env.rx == env.size - 1


class MoveRight(TransToken):
    def apply(self, env: Environment) -> RobotEnvironment:
        if(env.rx == env.size - 1):
            raise InvalidTransition()
        env.rx += 1
        if(env.holding):
            env.bx += 1
        return env


class MoveLeft(TransToken):
    def apply(self, env: Environment) -> RobotEnvironment:
        if(env.rx == 0):
            raise InvalidTransition()
        env.rx -= 1
        if(env.holding):
            env.bx -= 1
        return env


class MoveUp(TransToken):
    def apply(self, env: Environment) -> RobotEnvironment:
        if(env.ry == 0):
            raise InvalidTransition()
        env.ry -= 1
        if(env.holding):
            env.by -= 1
        return env


class MoveDown(TransToken):
    def apply(self, env: Environment) -> RobotEnvironment:
        if(env.ry == env.size - 1):
            raise InvalidTransition()
        env.ry += 1
        if(env.holding):
            env.by += 1
        return env


class Drop(TransToken):
    def apply(self, env: Environment) -> RobotEnvironment:
        if(not env.holding):
            raise InvalidTransition()
        env.holding = False
        env.bx = env.rx
        env.by = env.ry


class Grab(TransToken):
    def apply(self, env: Environment) -> RobotEnvironment:
        if(env.holding):
            raise InvalidTransition()
        env.holding = True


BoolTokens = {AtTop, AtBottom, AtLeft, AtRight}
TransTokens = {MoveRight, MoveDown, MoveLeft, MoveUp, Drop, Grab}
