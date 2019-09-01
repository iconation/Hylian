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
from .feed import *
from ..utils import *
from ..configuration import *


class TooMuchFeedsError(Exception):
    pass


class FeedAlreadyExistsError(Exception):
    pass


class FeedNotExistsError(Exception):
    pass


class FeedComposite(object):
    # ================================================
    #  Constants
    # ================================================
    # Maximum amount of feeds subscribed
    _MAXIMUM_FEEDS = 1000

    # ================================================
    #  DB Variables
    # ================================================
    # Feeds are indexed by their SCORE address
    _INDEX = 'FEED_COMPOSITE_INDEX'

    # ================================================
    #  Private Methods
    # ================================================
    @staticmethod
    def feeds(db: IconScoreDatabase) -> ArrayDB:
        return ArrayDB(FeedComposite._INDEX, db, value_type=Address)

    # ================================================
    #  Checks
    # ================================================
    @staticmethod
    def _check_maximum_amount_feeds(db: IconScoreDatabase) -> None:
        feeds_count = len(FeedComposite.feeds(db))
        if feeds_count > FeedComposite._MAXIMUM_FEEDS:
            raise TooMuchFeedsError(feeds_count)

    @staticmethod
    def _check_feed_not_already_exists(db: IconScoreDatabase, address: Address) -> None:
        if address in FeedComposite.feeds(db):
            raise FeedAlreadyExistsError(str(address))

    @staticmethod
    def _check_feed_already_exists(db: IconScoreDatabase, address: Address) -> None:
        if address not in FeedComposite.feeds(db):
            raise FeedNotExistsError(str(address))

    # ================================================
    #  Public Methods
    # ================================================
    @staticmethod
    def add(db: IconScoreDatabase,
            address: Address,
            name: str,
            now: int) -> Address:
        FeedComposite._check_maximum_amount_feeds(db)
        FeedComposite._check_feed_not_already_exists(db, address)

        # Add new feed object
        feed = FeedFactory.create(db, address, name, now)
        FeedComposite.feeds(db).put(feed)

        return feed

    @staticmethod
    def remove(db: IconScoreDatabase, address: Address) -> None:
        FeedComposite._check_feed_already_exists(db, address)
        Utils.array_db_remove(FeedComposite.feeds(db), address, False)

    @staticmethod
    def get(db: IconScoreDatabase, address: Address) -> Feed:
        FeedComposite._check_feed_already_exists(db, address)
        return Feed(db, address)

    @staticmethod
    def serialize(db: IconScoreDatabase) -> list:
        return list(map(lambda address: {
            'address': address,
            'feed': Feed(db, address).serialize()
        }, FeedComposite.feeds(db)))

    @staticmethod
    def delete(db: IconScoreDatabase) -> None:
        feeds = FeedComposite.feeds(db)
        while feeds:
            address = feeds.pop()
            Feed(db, address).delete()
