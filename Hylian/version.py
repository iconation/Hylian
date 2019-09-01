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


class Version(object):

    # ================================================
    #  DB Variables
    # ================================================
    _VERSION = 'VERSION'

    # ================================================
    #  Private Methods
    # ================================================
    @staticmethod
    def _version(db: IconScoreDatabase) -> VarDB:
        return VarDB(Version._VERSION, db, value_type=str)

    @staticmethod
    def _as_tuple(version: str):
        parts = []
        for part in version.split('.'):
            parts.append(int(part))
        return tuple(parts)

    # ================================================
    #  Public Methods
    # ================================================
    @staticmethod
    def set(db: IconScoreDatabase, version: str) -> None:
        Version._version(db).set(version)

    @staticmethod
    def get(db: IconScoreDatabase) -> str:
        return Version._version(db).get()

    @staticmethod
    def is_less_than_target_version(last: str, target: str) -> bool:
        return Version._as_tuple(last) < Version._as_tuple(target)
