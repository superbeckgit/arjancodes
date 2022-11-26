"""
Given an NxM input array A, generate the elements of A starting at A[0][0], and then spiralling in in a clockwise manner. The array need not be square.

There at least three possible constraints on the solution you might try to satisfy, but none of them are mandatory. From first to last, each makes the problem slightly harder.

You may modify the contents of A
You may not modify the contents of A, but your code may allocate an auxilliary array of the same size
You may not modify the contents of A, and you must only use a fixed amount of extra storage.

The last constraint, in particular, means that your code to walk the spiral can't an auxilliary array of the same size as A, or any other dynamically sized structure.

Here are a handful of tests. No particular test harness, just a test function you can write to invoke your code and compare the result to the expected value.

test([[1]], [1])
test([[1, 2]], [1, 2])
test([[1], [2]], [1, 2])
test(
    [
        [1, 2],
        [3, 4]
    ],
    [1, 2, 4, 3]
)
test(
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ],
    [1, 2, 3, 6, 9, 8, 7, 4, 5]
)
test(
    [
        [ 1,  2,  3,  4],
        [ 5,  6,  7,  8],
        [ 9, 10, 11, 12],
        [13, 14, 15, 16]
    ],
    [1, 2, 3, 4, 8, 12, 16, 15, 14, 13, 9, 5, 6, 7, 11, 10]
)
test(
    [
        [1, 2, 3, 4],
        [5, 6, 7, 8]
    ],
    [1, 2, 3, 4, 8, 7, 6, 5]
)
test(
    [
        [1, 2],
        [3, 4],
        [5, 6],
        [7, 8]
    ],
    [1, 2, 4, 6, 8, 7, 5, 3]
)
"""

from typing import Any, Optional

import pytest


class Matrix:
    def __init__(self, values: list[list[Any]]):
        self.length = len(values[0])
        self.height: int = len(values)
        self.values = values

    @classmethod
    def from_length_and_height(cls, length: int, height: int):
        """Create matrix with increasing values based on size"""
        values = []
        count = 0
        for _ in range(height):
            this_row = []
            for _ in range(length):
                this_row.append(count)
                count += 1
            values.append(this_row)
        return Matrix(values=values)

    def get_horizontal(
        self, row: int, h_min: Optional[int] = None, h_max: Optional[int] = None
    ) -> list[Any]:
        """Return a horizontal slice of the matrix given a row and min/max index (inclusive)"""
        if h_min is None:
            h_min = 0
        if h_max is None:
            h_max = self.length
        return self.values[row][h_min : h_max + 1]

    def get_vertical(
        self, col: int, v_min: Optional[int] = None, v_max: Optional[int] = None
    ) -> list[Any]:
        """Return a vertical slice of the matrix given a column and min/max index (inclusive)"""
        if v_min is None:
            v_min = 0
        if v_max is None:
            v_max = self.height
        return [row[col] for ix, row in enumerate(self.values) if v_min <= ix <= v_max]

    def spiral_walk(self):
        """Return a flat list of values from walking the matrix right, down, left, and up."""
        h_min = 0
        h_max = self.length - 1
        v_min = 0
        v_max = self.height - 1

        spiral = []
        dircount = 0
        loopcount = 0
        directions = ['right', 'down', 'left', 'up']
        while h_max >= h_min and v_max >= v_min:
            # even access is horizontal, odd is vertical
            match directions[dircount%4]:
                case 'right':
                    # row down from the top
                    rownum = loopcount
                    spiral.extend(self.get_horizontal(row=rownum, h_min=h_min, h_max=h_max))
                    v_min += 1
                case 'down':
                    # column in from right
                    colnum = self.length - loopcount - 1
                    spiral.extend(self.get_vertical(col=colnum, v_min=v_min, v_max=v_max))
                    h_max -= 1
                case 'left':
                    # row up from the bottom, reversed
                    rownum = self.height - loopcount - 1
                    spiral.extend(
                        reversed(self.get_horizontal(row=rownum, h_min=h_min, h_max=h_max))
                    )
                    v_max -= 1
                case 'up':
                    # colunm in from left, reversed
                    colnum = loopcount
                    spiral.extend(
                        reversed(self.get_vertical(col=colnum, v_min=v_min, v_max=v_max))
                    )
                    h_min += 1
                    loopcount += 1

            dircount += 1
        return spiral


## Test Code
def test_matrix_init():
    mat = Matrix([[0]])
    assert mat.length == 1
    assert mat.height == 1
    assert mat.values == [[0]]

    mat = Matrix([["a", "b"], [0, 1]])
    assert mat.length == 2
    assert mat.height == 2
    assert mat.values[0] == ["a", "b"]


def test_matrix_from_length_and_width():
    mat = Matrix.from_length_and_height(length=3, height=4)
    assert mat.length == 3
    assert mat.height == 4
    assert mat.values[0][0] == 0
    assert mat.values[0] == [0, 1, 2]
    assert mat.values[-1] == [9, 10, 11]


def test_get_horizontal():
    mat = Matrix.from_length_and_height(length=3, height=4)
    assert mat.get_horizontal(row=0) == [0, 1, 2]
    assert mat.get_horizontal(row=0, h_min=1) == [1, 2]
    assert mat.get_horizontal(row=3, h_min=1, h_max=1) == [10]


def test_get_vertical() -> None:
    mat = Matrix.from_length_and_height(length=3, height=4)
    assert mat.get_vertical(0) == [0, 3, 6, 9]
    assert mat.get_vertical(col=0, v_min=1, v_max=2) == [3, 6]


test_data: list[tuple[list[list[Any]], list[Any]]] = [
    ([[1]], [1]),
    ([[1, 2]], [1, 2]),
    ([[1], [2]], [1, 2]),
    ([[1, 2], [3, 4]], [1, 2, 4, 3]),
    ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1, 2, 3, 6, 9, 8, 7, 4, 5]),
    (
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]],
        [1, 2, 3, 4, 8, 12, 16, 15, 14, 13, 9, 5, 6, 7, 11, 10],
    ),
    ([[1, 2, 3, 4], [5, 6, 7, 8]], [1, 2, 3, 4, 8, 7, 6, 5]),
    ([[1, 2], [3, 4], [5, 6], [7, 8]], [1, 2, 4, 6, 8, 7, 5, 3]),
]


@pytest.mark.parametrize("values, expected", test_data)
def test_spiral_walk(values, expected) -> None:
    assert Matrix(values=values).spiral_walk() == expected
