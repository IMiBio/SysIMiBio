def create_subplot_name_choices(ncols, nrows):
    """Create list consisting on a sequence of letters for the ncols amount
    and numbers for the nrows amount concatenated is a tuple list.
    eg.:
    crete_subplot_name(1,2)
    will return [('A1', 'A1'),('A2', 'A2')]"""
    from string import ascii_uppercase

    letters = [letter for letter in ascii_uppercase[0:ncols]]
    numbers = [number for number in range(1, nrows + 1)]
    return [
        (f"{letter}{number}", f"{letter}{number}")
        for letter in letters
        for number in numbers
    ]
