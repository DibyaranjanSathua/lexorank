"""
File:           lexo_decimal.py
Author:         Dibyaranjan Sathua
Created on:     26/12/21, 5:00 pm
"""
from src.lexo_numeral_system import LexoNumeralSystem
from src.lexo_integer import LexoInteger


class LexoDecimal:
    """ Decimal class for lexo ranking """

    def __init__(self, mag: LexoInteger, sig: int):
        self.mag = mag
        self.sig = sig

    def __add__(self, other: "LexoDecimal") -> "LexoDecimal":
        self_mag = self.mag
        self_sig = self.sig
        other_mag = other.mag
        other_sig = other.sig
        while self_sig < other_sig:
            self_mag = self_mag << 1
            self_sig += 1
        while other_sig < self_sig:
            other_mag = other_mag << 1
            other_sig += 1
        return LexoDecimal.make(self_mag + other_mag, self_sig)

    def __sub__(self, other: "LexoDecimal") -> "LexoDecimal":
        self_mag = self.mag
        self_sig = self.sig
        other_mag = other.mag
        other_sig = other.sig
        while self_sig < other_sig:
            self_mag = self_mag << 1
            self_sig += 1
        while other_sig < self_sig:
            other_mag = other_mag << 1
            other_sig += 1
        return LexoDecimal.make(self_mag - other_mag, self_sig)

    def __mul__(self, other: "LexoDecimal") -> "LexoDecimal":
        return LexoDecimal.make(self.mag * other.mag, self.sig + other.sig)

    def __eq__(self, other: "LexoDecimal") -> bool:
        if id(self) == id(other):
            return True
        if not other:
            return False
        return self.mag == other.mag and self.sig == other.sig

    def __str__(self) -> str:
        int_str = str(self.mag)
        if self.sig == 0:
            return int_str
        head = ""
        if int_str.startswith(self.mag.system.positive_char) or \
                int_str.startswith(self.mag.system.negative_char):
            head = int_str[0]
            int_str = int_str[1:]
        while len(int_str) < self.sig + 1:
            int_str = self.mag.system.to_char(0) + int_str
        pos = len(int_str) - self.sig
        int_str = int_str[:pos] + self.mag.system.radix_point_char + int_str[pos:]
        if len(int_str) - self.sig == 0:
            int_str = self.mag.system.to_char(0) + int_str
        if head:
            int_str = head + int_str
        return int_str

    def __repr__(self):
        return str(self)

    def floor(self) -> "LexoInteger":
        return self.mag >> self.sig

    def ceil(self) -> "LexoInteger":
        if self.is_exact():
            return self.mag
        integer = self.floor()
        return integer + LexoInteger.one(integer.system)

    def is_exact(self) -> bool:
        if self.sig == 0:
            return True
        for i in range(0, self.sig):
            if self.mag.get_mag(i) != 0:
                return False
        return True

    def get_system(self) -> LexoNumeralSystem:
        return self.mag.system

    def get_scale(self) -> int:
        return self.sig

    def set_scale(self, nsig: int, ceiling: bool = False) -> "LexoDecimal":
        if nsig >= self.sig:
            return self
        nsig = max(nsig, 0)
        diff = self.sig - nsig
        new_mag = self.mag >> diff
        if ceiling:
            new_mag += LexoInteger.one(new_mag.system)
        return LexoDecimal.make(new_mag, nsig)

    def compare_to(self, other: "LexoDecimal") -> int:
        if id(self) == id(other):
            return 0
        if not other:
            return 1
        self_mag = self.mag
        other_mag = other.mag
        if self.sig > other.sig:
            other_mag = other_mag << (self.sig - other.sig)
        elif self.sig < other.sig:
            self_mag = self_mag << (other.sig - self.sig)
        return self_mag.compare_to(other_mag)

    @staticmethod
    def make(integer: LexoInteger, sig: int) -> "LexoDecimal":
        if integer.is_zero():
            return LexoDecimal(integer, 0)
        # Count zeros at the beginning of integer.mag
        zero_count = 0
        while zero_count < sig and integer.get_mag(zero_count) == 0:
            zero_count += 1
        new_integer = integer >> zero_count
        new_sig = sig - zero_count
        return LexoDecimal(new_integer, new_sig)

    @staticmethod
    def make_from(integer: LexoInteger) -> "LexoDecimal":
        return LexoDecimal.make(integer, 0)

    @staticmethod
    def half(system: LexoNumeralSystem) -> "LexoDecimal":
        mid = system.get_base // 2 | 0
        return LexoDecimal.make(LexoInteger.make(system, 1, [mid]), 1)

    @staticmethod
    def parse(string: str, system: LexoNumeralSystem) -> "LexoDecimal":
        partial_index = string.find(system.radix_point_char)
        if string.count(system.radix_point_char) > 1:
            raise ValueError(f"More than one {system.radix_point_char}")
        if partial_index < 0:
            return LexoDecimal.make(LexoInteger.parse(string, system), 0)
        int_str = string[0:partial_index] + string[partial_index+1:]
        return LexoDecimal.make(LexoInteger.parse(int_str, system), len(string) - 1 - partial_index)


if __name__ == "__main__":
    d1 = LexoDecimal.parse("1", LexoNumeralSystem())
    print(d1)
    d2 = LexoDecimal.parse("1000000", LexoNumeralSystem())
    print(d2)
