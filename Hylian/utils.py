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


class Utils():

    @staticmethod
    def array_db_clear(array: ArrayDB) -> None:
        while array:
            array.pop()

    @staticmethod
    def array_db_exists(array: ArrayDB, element) -> bool:
        for cur in array:
            if cur == element:
                return True
        return False

    @staticmethod
    def array_db_remove(array: ArrayDB, element, keep_order=True) -> None:
        if keep_order:
            tmp = []
            while array:
                cur = array.pop()
                # Keep all the elements
                if cur != element:
                    tmp.append(cur)
                # except for the one we're looking for
                else:
                    break
            # Add the next elements
            while tmp:
                cur = tmp.pop()
                array.put(cur)
        else:
            length = len(array)
            for idx, cur in enumerate(array):
                if cur == element:
                    if idx == length - 1:
                        # Nothing left in the array
                        array.pop()
                    else:
                        # Replace the old value with the tail of the array
                        array[idx] = array.pop()
                    break
