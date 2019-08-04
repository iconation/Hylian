
class SenderNotScoreOwner(Exception):
    message = 'SENDER_NOT_SCORE_OWNER'


class FeedAlreadyExists(Exception):
    message = 'FEED_ALREADY_EXISTS'


class FeedNotExists(Exception):
    message = 'FEED_NOT_EXISTS'


class NotEnoughFeedsAvailable(Exception):
    message = 'NOT_ENOUGH_FEEDS_AVAILABLE'


class PriceFeedTimeout(Exception):
    message = 'PRICE_FEED_TIMEOUT'


class WrongTickerName(Exception):
    message = 'WRONG_TICKER_NAME'


class MaximumAmountOfFeedsReached(Exception):
    message = 'MAXIMUM_AMOUNT_OF_FEEDS_REACHED'
