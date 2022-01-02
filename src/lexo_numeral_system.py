"""
File:           lexo_numeral_system.py
Author:         Dibyaranjan Sathua
Created on:     08/12/21, 8:22 pm
"""


class LexoNumeralSystem:
    """ Numeral system of 36 characters """
    DIGITS = list("0123456789abcdefghijklmnopqrstuvwxyz")

    def to_char(self, digit: int) -> str:
        """ Convert the digit to character """
        if digit >= len(self.DIGITS):
            raise ValueError(f"digit can not be more than {len(self.DIGITS) - 1}")
        return self.DIGITS[digit]

    @staticmethod
    def to_digit(ch: str) -> int:
        """ Convert characters to digit """
        if "0" <= ch <= "9":
            return ord(ch) - 48
        if "a" <= ch <= "z":
            return ord(ch) - 97 + 10
        raise ValueError(f"Not a valid digit {ch}")

    @property
    def get_base(self) -> int:
        return 36

    @property
    def positive_char(self) -> str:
        return "+"

    @property
    def negative_char(self) -> str:
        return "-"

    @property
    def radix_point_char(self) -> str:
        return ":"
