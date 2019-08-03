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