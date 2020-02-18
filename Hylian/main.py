# -*- coding: utf-8 -*-

# Copyright 2019 ICONation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from iconservice import *
from .interfaces import *
from .utils import *
from .checks import *
from .version import *
from .math import *
from .time import *
from .feed.feed_composite import *
from .configuration import *


class WrongTickerName(Exception):
    pass


class NotEnoughFeedsAvailable(Exception):
    pass


class PriceFeedTimeout(Exception):
    pass


class Hylian(IconScoreBase):
    """ Hylian SCORE Base implementation """

    # ================================================
    #  Initialization
    # ================================================
    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)

    def on_install(self,
                   ticker_name: str,
                   minimum_feeds_available: int) -> None:
        super().on_install()

        # Set configuration
        Configuration.minimum_feeds_available(self.db).set(minimum_feeds_available)
        Configuration.ticker_name(self.db).set(ticker_name)
        Configuration.timeout_price_update(self.db).set(DEFAULT_TIMEOUT_PRICE_UPDATE)

        # Set Version
        Version.set(self.db, VERSION)

    def on_update(self) -> None:
        super().on_update()
        Version.set(self.db, VERSION)

    # ================================================
    #  Checks
    # ================================================
    def _check_ticker_name(self, ticker_name: str) -> None:
        if Configuration.ticker_name(self.db).get() != ticker_name:
            raise WrongTickerName(ticker_name)

    def _check_timeout(self, timestamp: int) -> None:
        if Time.is_timeout(self.now(), timestamp, Configuration.timeout_price_update(self.db).get()):
            raise PriceFeedTimeout(timestamp)

    def _check_enough_feeds_available(self, values: list) -> None:
        if len(values) < Configuration.minimum_feeds_available(self.db).get():
            raise NotEnoughFeedsAvailable(len(values))

    # ================================================
    #  External methods
    # ================================================
    @external
    @only_owner
    @catch_error
    def add_feed(self, address: Address, name: str) -> None:
        """ Add a price feed to Hylian """
        FeedComposite.add(self.db, address, name, self.now())

    @external
    @only_owner
    @catch_error
    def remove_feed(self, address: Address) -> None:
        """ Remove a price feed from Hylian """
        FeedComposite.remove(self.db, address)

    @external
    @only_owner
    @catch_error
    def set_timeout_price_update(self, timeout_price_update: int) -> None:
        Configuration.timeout_price_update(self.db).set(timeout_price_update)

    @external
    @only_owner
    @catch_error
    def set_ticker_name(self, ticker_name: str) -> None:
        Configuration.ticker_name(self.db).set(ticker_name)

    @external
    @only_owner
    @catch_error
    def set_minimum_feeds_available(self, minimum_feeds_available: int) -> None:
        Configuration.minimum_feeds_available(self.db).set(minimum_feeds_available)

    # ==== ReadOnly methods =============================================
    @external(readonly=True)
    @catch_error
    def feeds(self) -> list:
        """ Return a list of price feeds registered to Hylian """
        return FeedComposite.serialize(self.db)

    @external(readonly=True)
    @catch_error
    def feed(self, address: Address) -> dict:
        """ Return a single price feed registered to Hylian """
        return FeedComposite.get(self.db, address).serialize()

    @external(readonly=True)
    @catch_error
    def value(self) -> int:
        """ Return the median value of price feeds, computed dynamically """
        values = []

        for address in FeedComposite.feeds(self.db):
            try:
                feed_score = self.create_interface_score(address, PriceFeedInterface)
                # Retrieve the price
                feed = feed_score.peek()
                # Price Feed Checks
                self._check_ticker_name(feed['ticker_name'])
                self._check_timeout(feed['timestamp'])
                # Process
                values.append(feed['value'])
            except Exception as error:
                # A pricefeed SCORE may not work as expected anymore,
                # but we want to keep running Hylian as long as
                # there is a minimum amount of pricefeed available
                Logger.warning(f'{address} didnt work correctly:' +
                               f'{type(error)} : {str(error)}', TAG)
                continue

        self._check_enough_feeds_available(values)
        # Compute the median value
        return Math.median(values)

    @external(readonly=True)
    @catch_error
    def online_feeds(self) -> int:
        """ Return the number of online feeds """
        count = 0

        for address in FeedComposite.feeds(self.db):
            try:
                feed_score = self.create_interface_score(address, PriceFeedInterface)
                # Retrieve the price
                feed = feed_score.peek()
                # Price Feed Checks
                self._check_ticker_name(feed['ticker_name'])
                self._check_timeout(feed['timestamp'])
                # Process
                count += 1
            except Exception as error:
                # A pricefeed SCORE may not work as expected anymore,
                # but we want to keep running Hylian as long as
                # there is a minimum amount of pricefeed available
                Logger.warning(f'{address} didnt work correctly:' +
                               f'{type(error)} : {str(error)}', TAG)
                continue

        # Compute the median value
        return count

    @external(readonly=True)
    @catch_error
    def version(self) -> str:
        """ Return the Hylian version """
        return Version.get(self.db)

    @external(readonly=True)
    @catch_error
    def minimum_feeds_available(self) -> int:
        """ Return the minimum amount of available price feeds required
            for Hylian to work """
        return Configuration.minimum_feeds_available(self.db).get()

    @external(readonly=True)
    @catch_error
    def timeout_price_update(self) -> int:
        """ Return the value of the price feed timeout """
        return Configuration.timeout_price_update(self.db).get()

    @external(readonly=True)
    @catch_error
    def ticker_name(self) -> str:
        """ Return the ticker name of Hylian """
        return Configuration.ticker_name(self.db).get()
