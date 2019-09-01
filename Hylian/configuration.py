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
from .constants import *


class Configuration(object):
    # ================================================
    #  DB Variables
    # ================================================
    # The minimum amount of price feeds available required for
    # the oracle to return a valid result
    _MINIMUM_FEEDS_AVAILABLE = 'MINIMUM_FEEDS_AVAILABLE'

    # The amount of time after which the price from the feed
    # is considered if it isn't updated in this time frame
    _TIMEOUT_PRICE_UPDATE = 'TIMEOUT_PRICE_UPDATE'

    # Ticker name, the price feeds need to subscribe to the
    # same ticker name if they want to participate to the
    # price consensus
    _TICKER_NAME = 'TICKER_NAME'

    # ================================================
    #  Public Methods
    # ================================================
    @staticmethod
    def minimum_feeds_available(db: IconScoreDatabase) -> VarDB:
        return VarDB(Configuration._MINIMUM_FEEDS_AVAILABLE, db, value_type=int)

    @staticmethod
    def timeout_price_update(db: IconScoreDatabase) -> VarDB:
        return VarDB(Configuration._TIMEOUT_PRICE_UPDATE, db, value_type=int)

    @staticmethod
    def ticker_name(db: IconScoreDatabase) -> VarDB:
        return VarDB(Configuration._TICKER_NAME, db, value_type=str)

    @staticmethod
    def serialize(db: IconScoreDatabase) -> dict:
        return {
            'minimum_feeds_available': Configuration.minimum_feeds_available(db).get(),
            'timeout_price_update': Configuration.timeout_price_update(db).get(),
            'ticker_name': Configuration.ticker_name(db).get()
        }

    @staticmethod
    def delete(db: IconScoreDatabase) -> None:
        Configuration.minimum_feeds_available(db).remove()
        Configuration.timeout_price_update(db).remove()
        Configuration.ticker_name(db).remove()
