from iconservice import *
from .exceptions import *
from .interfaces import *
from .utils import *

TAG = 'Medianizer'


class Medianizer(IconScoreBase):
    """ Medianizer SCORE Base implementation """

    # ================================================
    #  DB Variables
    # ================================================
    # The median price value
    _VALUE = "VALUE"
    # The timestamp of the latest computed median value
    _TIMESTAMP = "TIMESTAMP"
    # Whitelist SCORE addresses of the price feed contracts
    _FEEDS = "FEEDS"
    # The minimum amount of price feeds available required for
    # the oracle to return a valid result
    _MINIMUM_FEEDS_AVAILABLE = "MINIMUM_FEEDS_AVAILABLE"

    # ================================================
    #  Constants
    # ================================================
    # After 6 hours, the price from the feed is considered
    # as invalid if it isn't updated
    _TIMEOUT_PRICE_UPDATE = 6 * 60 * 60 * 1000 * 1000
    # Do not exceed 100 price feeds subscribed
    _MAXIMUM_FEEDS = 100

    # ================================================
    #  Error codes
    # ================================================
    _SENDER_NOT_SCORE_OWNER = 'SENDER_NOT_SCORE_OWNER'
    _NOT_ENOUGH_FEEDS_AVAILABLE = 'NOT_ENOUGH_FEEDS_AVAILABLE'
    _FEED_ALREADY_EXISTS = 'FEED_ALREADY_EXISTS'
    _FEED_NOT_EXISTS = 'FEED_NOT_EXISTS'
    _FEED_NOT_WHITELISTED = 'FEED_NOT_WHITELISTED'
    _MAXIMUM_AMOUNT_OF_FEEDS_REACHED = 'MAXIMUM_AMOUNT_OF_FEEDS_REACHED'

    # ================================================
    #  Initialization
    # ================================================
    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._feeds = ArrayDB(self._FEEDS, db, value_type=Address)
        self._minimum_feeds_available = VarDB(self._MINIMUM_FEEDS_AVAILABLE,
                                              db, value_type=int)

    def on_install(self, minimum_feeds_available: int) -> None:
        super().on_install()
        self._minimum_feeds_available.set(minimum_feeds_available)

    def on_update(self) -> None:
        super().on_update()

    # ================================================
    #  Checks
    # ================================================
    def _check_is_score_operator(self, address: Address) -> None:
        if self.owner != address:
            raise SenderNotScoreOwner

    def _check_feed_is_whitelisted(self, address: Address) -> None:
        if address not in self._feeds:
            raise FeedNotWhitelisted

    def _check_feed_not_already_exists(self, address: Address) -> None:
        if address in self._feeds:
            raise FeedAlreadyExists

    def _check_feed_already_exists(self, address: Address) -> None:
        if address not in self._feeds:
            raise FeedNotExists

    def _check_enough_feeds_available(self, values: list) -> None:
        if len(values) < self._minimum_feeds_available.get():
            raise NotEnoughFeedsAvailable

    def _check_maximum_amount_feeds(self) -> None:
        if len(self._feeds) > self._MAXIMUM_FEEDS:
            raise MaximumAmountOfFeedsReached

    # ================================================
    #  External methods
    # ================================================
    @external
    def add_feed(self, address: Address) -> None:
        """ Add a price feed to the whitelist """
        # ==========================
        # Input Checks
        try:
            self._check_is_score_operator(self.msg.sender)
            self._check_feed_not_already_exists(address)
            self._check_maximum_amount_feeds()
        except SenderNotScoreOwner:
            revert(self._SENDER_NOT_SCORE_OWNER)
        except FeedAlreadyExists:
            revert(self._FEED_ALREADY_EXISTS)
        except MaximumAmountOfFeedsReached:
            revert(self._MAXIMUM_AMOUNT_OF_FEEDS_REACHED)

        # ==========================
        # Process
        self._feeds.put(address)

    @external
    def remove_feed(self, address: Address) -> None:
        """ Remove a price feed from the whitelist """
        # ==========================
        # Input Checks
        try:
            self._check_is_score_operator(self.msg.sender)
            self._check_feed_already_exists(address)
        except SenderNotScoreOwner:
            revert(self._SENDER_NOT_SCORE_OWNER)
        except FeedNotExists:
            revert(self._FEED_NOT_EXISTS)

        # ==========================
        # Process
        Utils.array_db_remove(self._feeds, address)

    @external(readonly=True)
    def feeds(self) -> str:
        """ Return a list of whitelisted price feeds SCORE addresses """
        feeds = list(map(lambda feed: str(feed), self._feeds))
        return json_dumps(feeds)

    @external(readonly=True)
    def minimum_feeds_available(self) -> int:
        """ Return the minimum amount of available price feeds required
            for the Medianizer to work """
        return self._minimum_feeds_available.get()

    @external(readonly=True)
    def value(self) -> int:
        """ Return the median value of price feeds, computed dynamically """
        # ==========================
        # Process
        try:
            values = self._get_feeds_values()
            self._check_enough_feeds_available(values)
            median = self._compute_median(values)
        except NotEnoughFeedsAvailable:
            revert(self._NOT_ENOUGH_FEEDS_AVAILABLE)

        return median

    # ================================================
    #  Private methods
    # ================================================
    def _timeout(self, timestamp):
        return (self.now() - timestamp) > self._TIMEOUT_PRICE_UPDATE

    def _get_feeds_values(self) -> list:
        values = []

        for feed_address in self._feeds:
            feed_score = self.create_interface_score(
                feed_address, PriceFeedInterface)
            try:
                feed = json_loads(feed_score.peek())
            except:
                # A pricefeed SCORE may not work anymore, but we
                # want to keep running the medianizer as long as
                # there is a minimum amount of pricefeed available
                Logger.warning(f'{feed_address} didnt work correctly', TAG)
                continue

            # Make sure the feed is updated
            if not self._timeout(feed['timestamp']):
                values.append(feed['value'])

        return values

    def _compute_median(self, values: list) -> int:
        sorted_values = sorted(values)
        length = len(sorted_values)
        if length % 2 == 0:
            return (sorted_values[length // 2] +
                    sorted_values[length // 2 - 1]) // 2
        else:
            return sorted_values[length // 2]
