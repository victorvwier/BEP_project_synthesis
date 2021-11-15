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
    def apply(self, env: RobotEnvironment) -> bool:
        return env.ry == 0


class AtBottom(BoolToken):
    def apply(self, env: RobotEnvironment) -> bool:
        return env.ry == env.size - 1


class AtLeft(BoolToken):
    def apply(self, env: RobotEnvironment) -> bool:
        return env.rx == 0


class AtRight(BoolToken):
    def apply(self, env: RobotEnvironment) -> bool:
        return env.rx == env.size - 1


class NotAtTop(BoolToken):
    def apply(self, env: RobotEnvironment) -> bool:
        return env.ry != 0


class NotAtBottom(BoolToken):
    def apply(self, env: RobotEnvironment) -> bool:
        return env.ry != env.size - 1


class NotAtLeft(BoolToken):
    def apply(self, env: RobotEnvironment) -> bool:
        return env.rx != 0


class NotAtRight(BoolToken):
    def apply(self, env: RobotEnvironment) -> bool:
        return env.rx != env.size - 1


class MoveRight(TransToken):
    def apply(self, env: RobotEnvironment) -> RobotEnvironment:
        if env.rx == env.size - 1:
            raise InvalidTransition()
        env.rx += 1
        if env.holding:
            env.bx += 1
        return env


class MoveLeft(TransToken):
    def apply(self, env: RobotEnvironment) -> RobotEnvironment:
        if env.rx == 0:
            raise InvalidTransition()
        env.rx -= 1
        if env.holding:
            env.bx -= 1
        return env


class MoveUp(TransToken):
    def apply(self, env: RobotEnvironment) -> RobotEnvironment:
        if env.ry == 0:
            raise InvalidTransition()
        env.ry -= 1
        if env.holding:
            env.by -= 1
        return env


class MoveDown(TransToken):
    def apply(self, env: RobotEnvironment) -> RobotEnvironment:
        if env.ry == env.size - 1:
            raise InvalidTransition()
        env.ry += 1
        if env.holding:
            env.by += 1
        return env


class Drop(TransToken):
    def apply(self, env: RobotEnvironment) -> RobotEnvironment:
        if not env.holding:
            raise InvalidTransition()
        env.holding = False
        env.bx = env.rx
        env.by = env.ry
        return env


class Grab(TransToken):
    def apply(self, env: RobotEnvironment) -> RobotEnvironment:
        if env.holding or env.rx != env.bx or env.ry != env.by:
            raise InvalidTransition()
        env.holding = True
        return env


BoolTokens = {AtTop, AtBottom, AtLeft, AtRight, NotAtTop, NotAtBottom, NotAtLeft, NotAtRight}
TransTokens = {MoveRight, MoveDown, MoveLeft, MoveUp, Drop, Grab}
