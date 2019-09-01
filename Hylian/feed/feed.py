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
from ..constants import *


class FeedFactory(object):
    @staticmethod
    def create(db: IconScoreDatabase,
               address: Address,
               name: str,
               now: int) -> Address:

        feed = Feed(db, address)

        feed._registration.set(now)
        feed._name.set(name)

        return address


class Feed(object):
    # ================================================
    #  DB Variables
    # ================================================
    _REGISTRATION = 'FEED_REGISTRATION'
    _NAME = 'FEED_NAME'

    # ================================================
    #  Initialization
    # ================================================
    def __init__(self, db: IconScoreDatabase, address: Address) -> None:
        self._registration = VarDB(f'{Feed._REGISTRATION}_{address}', db, value_type=int)
        self._name = VarDB(f'{Feed._NAME}_{address}', db, value_type=str)

    # ================================================
    #  Public Methods
    # ================================================
    def serialize(self) -> dict:
        return {
            'registration': self._registration.get(),
            'name': self._name.get()
        }

    def delete(self) -> None:
        self._registration.remove()
        self._name.remove()
