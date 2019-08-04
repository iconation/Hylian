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
    _VALUE = 'VALUE'
    # The timestamp of the latest computed median value
    _TIMESTAMP = 'TIMESTAMP'
    # Whitelist SCORE addresses of the price feed contracts
    _FEEDS = 'FEEDS'
    # The minimum amount of price feeds available required for
    # the oracle to return a valid result
    _MINIMUM_FEEDS_AVAILABLE = 'MINIMUM_FEEDS_AVAILABLE'
    # The amount of time after which the price from the feed
    # is considered if it isn't updated in this time frame
    _TIMEOUT_PRICE_UPDATE = 'TIMEOUT_PRICE_UPDATE'
    # Ticker name (for display purpose)
    _TICKER_NAME = 'TICKER_NAME'

    # ================================================
    #  Constants
    # ================================================
    # After 6 hours, the price from the feed is considered
    # as invalid if it isn't updated
    _DEFAULT_TIMEOUT_PRICE_UPDATE = 6 * 60 * 60 * 1000 * 1000
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
        self._timeout = VarDB(self._TIMEOUT_PRICE_UPDATE, db, value_type=int)
        self._ticker_name = VarDB(self._TICKER_NAME, db, value_type=str)

    def on_install(self,
                   minimum_feeds_available: int,
                   ticker_name: str) -> None:
        super().on_install()
        self._minimum_feeds_available.set(minimum_feeds_available)
        self._ticker_name = ticker_name
        self._timeout = self._DEFAULT_TIMEOUT_PRICE_UPDATE

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

    @external
    def set_timeout(self, timeout: int) -> None:
        # ==========================
        # Input Checks
        try:
            self._check_is_score_operator(self.msg.sender)
        except SenderNotScoreOwner:
            revert(self._SENDER_NOT_SCORE_OWNER)

        # ==========================
        # Process
        self._timeout.set(timeout)

    @external
    def set_ticker_name(self, ticker_name: str) -> None:
        # ==========================
        # Input Checks
        try:
            self._check_is_score_operator(self.msg.sender)
        except SenderNotScoreOwner:
            revert(self._SENDER_NOT_SCORE_OWNER)

        # ==========================
        # Process
        self._ticker_name.set(ticker_name)

    # ==== ReadOnly methods =============================================

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
            # Get all the feed values
            values = self._get_feeds_values()
            self._check_enough_feeds_available(values)
            # Compute the median value
            median = Utils.compute_median(values)
        except NotEnoughFeedsAvailable:
            revert(self._NOT_ENOUGH_FEEDS_AVAILABLE)

        return median

    @external(readonly=True)
    def timeout(self) -> int:
        """ Return the value of the price feed timeout """
        return self._timeout.get()

    @external(readonly=True)
    def ticker_name(self) -> str:
        """ Return the ticker name of the medianizer """
        return self._ticker_name.get()

    # ================================================
    #  Private methods
    # ================================================
    def _is_timeout(self, timestamp: int) -> bool:
        return (self.now() - timestamp) > self._timeout.get()

    def _get_feeds_values(self) -> list:
        """ Calls the "peek" method for each price feed and
            return the results as a list """
        values = []

        for feed_address in self._feeds:
            try:
                feed_score = self.create_interface_score(
                    feed_address, PriceFeedInterface)

                # Retrieve the price here
                feed = json_loads(feed_score.peek())

                # Make sure the feed is updated
                if not self._is_timeout(feed['timestamp']):
                    values.append(feed['value'])

            except Exception as err:
                # A pricefeed SCORE may not work as expected anymore,
                # but we want to keep running the medianizer as long as
                # there is a minimum amount of pricefeed available
                Logger.warning(f'{feed_address} didnt work correctly:' +
                               f'{str(err)}', TAG)
                continue

        return values
