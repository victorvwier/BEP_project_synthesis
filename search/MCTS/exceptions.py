
class IllegalActionException(Exception):
    """Raised when an illegal Action is applied to a Completable Token or a Program"""
    pass


class ApplyingIncompleteTokenException(Exception):
    """"Raised when you try to apply a CompletableToken on an environment while this token has not been completed yet"""
    pass


class TokenAlreadyCompletedException(Exception):
    """Raised when a Token is already complete,
    but you try to do an action/method call that is only possible for incomplete tokens"""
    pass


class ProgramAlreadyCompletedException(Exception):
    """Is raised when a method/action is called that should only be called on an incomplete program"""
    pass


class MaxNumberOfIterationsExceededException(Exception):
    """Raised when the maximum number of iterations is exceeded"""
    pass


class CannotInterpIncompleteProgram(Exception):
    """Raised when a program is interpret while not yet completed"""
    pass


class InvalidRewardValue(Exception):
    """Raised when the value of reward is greater than 1.001 or a lot smaller than zero"""
    pass


class InvalidProgramException(Exception):
    """Raised when the program threw an exception upon interpreting an Environment"""
    pass


class SimilarProgramAlreadyFoundException(Exception):
    """Raised when a similar program was found already."""
    pass


class SelectedTokenHasIntiniteTokenScoreException(Exception):
    """Raised when a token has a token_score of -inf."""
    pass


class RootHasNoOptionsException(Exception):
    pass
