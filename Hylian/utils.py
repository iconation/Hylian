class Utils():
    @staticmethod
    def array_db_remove(array: list, element) -> None:
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

    @staticmethod
    def compute_median(values: list) -> int:
        sorted_values = sorted(values)
        length = len(sorted_values)
        if length % 2 == 0:
            return (sorted_values[length // 2] +
                    sorted_values[length // 2 - 1]) // 2
        else:
            return sorted_values[length // 2]
