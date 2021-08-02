"""
https://rosettacode.org/wiki/Burrows%E2%80%93Wheeler_transform
"""


def bwt(s: str) -> str:
    """Apply Burrows-Wheeler transform to input string."""
    assert not {"\002", "\003"}.intersection(s), "Input string cannot contain STX and ETX characters"
    s = "\002" + s + "\003"  # Add start and end of text marker
    table = sorted(s[i:] + s[:i] for i in range(len(s)))  # Table of rotations of string
    last_column = [row[-1:] for row in table]  # Last characters of each row
    return "".join(last_column)  # Convert list of characters into string


def ibwt(r: str) -> str:
    """Apply inverse Burrows-Wheeler transform."""
    table = [""] * len(r)  # Make empty table
    for i in range(len(r)):
        table = sorted(r[i] + table[i] for i in range(len(r)))  # Add a column of r
    s = [row for row in table if row.endswith("\003")][0]  # Find the correct row (ending in ETX)
    return s[1:-1]  # Get rid of start and end markers


if __name__ == "__main__":
    import argparse

    P = argparse.ArgumentParser(description="Burrows-Wheeler transform")
    P.add_argument("string", help="string to transform")
    p = P.parse_args()

    T = bwt(p.string)
    print(T)
    orig = ibwt(T)
    print(orig)
