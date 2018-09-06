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
    def __init__(self, gametype, minemap, openmap=[], flagmap=[]):
        self.gametype = gametype
        self.minemap = frozenset(minemap)
        self.openmap = frozenset(openmap)
        self.flagmap = frozenset(flagmap)

    # Boolean indicating if the game has been won or lost, or None if the game is still underway
    def won(self):
        # A mine has been revealed, game is lost
        if self.openmap.intersection(self.minemap):
            return False

        # All openable tiles have been opened, game is won
        if (len(self.openmap) + len(self.minemap)) == self.gametype.total_positions():
            return True

        return None

    def open(self, position):
        self._validate_position(position)
        # Add the newly opened position to the list of openend positions
        new_openmap = set(self.openmap)
        new_openmap.add(position)

        # If this newly openend position is next to 0 mines, then we need to expand the empty zone
        # that might be around this position
        auto_open_queue = set([position])
        processed_positions = set()
        while auto_open_queue:
            candidate = auto_open_queue.pop()
            processed_positions.add(candidate)
            if self.adjacent_mine_count(candidate) == 0:
                new_openmap.add(candidate)
                for neighbour in self.gametype.adjacent_positions[candidate]:  # look at the adjacent cells to see if they may be open as well
                    if neighbour not in processed_positions:
                        auto_open_queue.add(neighbour)

        return Board(self.gametype, self.minemap, new_openmap, self.flagmap)

    def toggle_flag(self, position):
        self._validate_position(position)

        if position in self.openmap:
            raise AlreadyRevealedException()

        new_flagmap = set(self.flagmap)
        if position in new_flagmap:
            new_flagmap.remove(position)
        else:
            new_flagmap.add(position)

        return Board(self.gametype, self.minemap, self.openmap, new_flagmap)

    def adjacent_mine_count(self, position):
        self._validate_position(position)
        return len(self.gametype.adjacent_positions[position].intersection(self.minemap))

    def _validate_position(self, position):
        if (position < 0) or (position > self.gametype.total_positions()):
            raise InvalidPositionException()
