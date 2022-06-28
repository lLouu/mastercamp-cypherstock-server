class ThisGuyTriedSomethingFishy(Exception):
    pass

class ThisIsNotAValidTokenBoy(Exception):
    pass

class ExpiredToken(Exception):
    pass

class NoAuthTokenGiven(Exception):
    pass

class NothingAsked(Warning):
    pass

class FANeeded(Exception):
    pass

class FANotPassed(Exception):
    pass

class NotEnoughtDataForRequest(Exception):
    pass

class TokenNeedToExpireSooner(Exception):
    pass

class AccessRefused(Exception):
    pass