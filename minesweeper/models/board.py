from functools import reduce
# Immutable class representing one state of the board.
# minemap, openmap, flagmap are all 0-indexed one dimensional arrays of positions
#  - minemap contains the postitions of each mine on the board
#  - openmap contains all the cells that have been revealed to the player
#  - flagmap contains all the cells the user has listed as a flag
# Each operation on the board returns a new, modified instance that answers questions about the new state.
# Example board positions for a beginner game:
#  0  1  2  3  4  5  6  7
#  8  9  10 11 12 13 14 15
#  16 17 18 19 20 21 22 23
#  24 25 26 27 28 29 30 31
#  32 33 34 35 36 37 38 39
#  40 41 42 43 44 45 46 47
#  48 49 50 51 52 53 54 55
#  56 57 58 59 60 61 62 63


class InvalidPositionException(Exception):
    pass


class AlreadyRevealedException(Exception):
    pass


class Board(object):
    def __init__(self, game_type, minemap, openmap=[], flagmap=[]):
        self.game_type = game_type
        self.minemap = frozenset(minemap)
        self.openmap = frozenset(openmap)
        self.flagmap = frozenset(flagmap)

    # Boolean indicating if the game has been won or lost, or None if the game is still underway
    def won(self):
        # A mine has been revealed, game is lost
        if self.openmap.intersection(self.minemap):
            return False

        # All openable tiles have been opened, game is won
        if (len(self.openmap) + len(self.minemap)) == self.game_type.total_positions():
            return True

        return None

    # Returns a new board with the cell at position (and any side effect cells) revealed
    def open(self, position):
        self._validate_position(position)
        # Add the newly opened position to the list of openend positions
        new_openmap = set(self.openmap)
        new_openmap.add(position)

        # Remove the position from the flag map, since opening means the player thinks there's no mine
        if position in self.flagmap:
            new_flagmap = set(self.flagmap)
            new_flagmap.remove(position)
        else:
            new_flagmap = self.flagmap

        # If this newly openend position is next to 0 mines, then we need to expand the empty zone
        # that might be around this position
        if position not in self.minemap:
            auto_open_queue = set([position])
            while auto_open_queue:
                candidate = auto_open_queue.pop()
                new_openmap.add(candidate)

                if self.adjacent_mine_count(candidate) == 0:
                    # this cell is also open, so look at the adjacent cells we haven 't looked at yet to see if they may be open as well
                    for neighbour in self.game_type.adjacent_positions[candidate]:
                        if neighbour not in new_openmap:
                            auto_open_queue.add(neighbour)

        return Board(self.game_type, self.minemap, new_openmap, new_flagmap)

    # Returns a new board with the cell at the given position's flag toggled
    def toggle_flag(self, position):
        self._validate_position(position)

        if position in self.openmap:
            raise AlreadyRevealedException()

        new_flagmap = set(self.flagmap)
        if position in new_flagmap:
            new_flagmap.remove(position)
        else:
            new_flagmap.add(position)

        return Board(self.game_type, self.minemap, self.openmap, new_flagmap)

    # Returns the number of mines adjacent to position
    def adjacent_mine_count(self, position):
        self._validate_position(position)
        return len(self.game_type.adjacent_positions[position].intersection(self.minemap))

    # Returns a dict of {position: mine_counts} for showing the hint numbers to a player
    def adjacent_mine_counts_for_openmap(self):
        def reducer(counts, position):
            count = self.adjacent_mine_count(position)
            if count > 0:
                counts[position] = count
            return counts

        return reduce(reducer, self.openmap, {})

    def _validate_position(self, position):
        if (position < 0) or (position > self.game_type.total_positions()):
            raise InvalidPositionException()
