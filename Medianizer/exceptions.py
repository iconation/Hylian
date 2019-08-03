# ================================================
#  Exceptions
# ================================================


class SenderNotScoreOwner(Exception):
    pass


class FeedAlreadyExists(Exception):
    pass


class FeedNotExists(Exception):
    pass


class FeedNotWhitelisted(Exception):
    pass


class NotEnoughFeedsAvailable(Exception):
    pass


class TimeoutReached(Exception):
    pass
