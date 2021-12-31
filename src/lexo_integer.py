"""
File:           lexo_integer.py
Author:         Dibyaranjan Sathua
Created on:     09/12/21, 8:32 pm
"""
from typing import List
from src.lexo_numeral_system import LexoNumeralSystem


class LexoInteger:
    """ Integer system """
    ZERO_MAG = [0]
    ONE_MAG = [1]
    NEGATIVE_SIGN = -1
    ZERO_SIGN = 0
    POSITIVE_SIGN = 1

    def __init__(self, system: LexoNumeralSystem, sign: int, mag: List[int]):
        self.system = system
        self.sign = sign
        self.mag = mag

    def __add__(self, other: "LexoInteger") -> "LexoInteger":
        """ Addition of two LexoInteger """
        if self.is_zero():
            return other
        if other.is_zero():
            return self
        if self.sign == other.sign:
            result = LexoInteger.add(self.system, self.mag, other.mag)
            return LexoInteger.make(self.system, self.sign, result)
        # If signs are different
        if self.sign == -1:
            negate = self.negate()
            value = negate - other
            return value.negate()
        negate = other.negate()
        return self - negate

    def __iadd__(self, other: "LexoInteger") -> "LexoInteger":
        return self.__add__(other)

    def __sub__(self, other: "LexoInteger") -> "LexoInteger":
        """ Subtraction of two LexoInteger """
        if self.is_zero():
            return other.negate()
        if other.is_zero():
            return self
        if self.sign == other.sign:
            cmp = LexoInteger.compare(self.mag, other.mag)
            if cmp == 0:
                return LexoInteger.zero(self.system)
            elif cmp < 0:
                return LexoInteger.make(
                    self.system,
                    1 if self.sign == -1 else -1,
                    LexoInteger.subtract(self.system, other.mag, self.mag)
                )
            else:
                return LexoInteger.make(
                    self.system,
                    -1 if self.sign == -1 else 1,
                    LexoInteger.subtract(self.system, self.mag, other.mag)
                )
        # If signs are different
        if self.sign == -1:
            negate = self.negate()
            value = negate + other
            return value.negate()
        negate = other.negate()
        return self + negate

    def __isub__(self, other: "LexoInteger") -> "LexoInteger":
        return self.__isub__(other)

    def __mul__(self, other: "LexoInteger") -> "LexoInteger":
        if self.is_zero():
            return self
        if other.is_zero():
            return other
        if self.is_oneish():
            return LexoInteger.make(self.system, 1, other.mag) \
                if self.sign == other.sign \
                else LexoInteger.make(self.system, -1, other.mag)
        if other.is_oneish():
            return LexoInteger.make(self.system, 1, self.mag) \
                if self.sign == other.sign \
                else LexoInteger.make(self.system, -1, self.mag)
        new_mag = LexoInteger.multiply(self.system, self.mag, other.mag)
        return LexoInteger.make(self.system, 1, new_mag) \
            if self.sign == other.sign \
            else LexoInteger.make(self.system, -1, new_mag)

    def __imul__(self, other):
        return self.__mul__(other)

    def __lshift__(self, other: int = 1) -> "LexoInteger":
        """ Left shift by other times """
        if not other:
            return self
        if other < 0:
            return self >> abs(other)
        new_mag = [0] * other + self.mag    # Shift the mah list to left by other
        return LexoInteger.make(self.system, self.sign, new_mag)

    def __rshift__(self, other: int = 1) -> "LexoInteger":
        """ Right shift by other times """
        if len(self.mag) - other <= 0:
            return LexoInteger.zero(self.system)
        new_mag = self.mag[other:-1]        # Shift the mag list to right by other
        return LexoInteger.make(self.system, self.sign, new_mag)

    def __eq__(self, other: "LexoInteger") -> bool:
        """ Compare two lexo integer objects """
        if id(self) == id(other):
            return True
        if not other:
            return False
        return self.system.get_base == other.system.get_base and self.compare_to(other)

    def __str__(self) -> str:
        if self.is_zero():
            return self.system.to_char(0)
        string = ""
        for x in self.mag:
            string += self.system.to_char(x)
        if self.sign == -1:
            string = self.system.negative_char + string
        return string

    def complement_digits(self, digits: int) -> "LexoInteger":
        return LexoInteger.make(
            self.system,
            self.sign,
            LexoInteger.complement(self.system, self.mag, digits)
        )

    def compliment(self) -> "LexoInteger":
        return self.complement_digits(len(self.mag))

    def negate(self) -> "LexoInteger":
        """ Negate the sign of a LexoInteger """
        if self.is_zero():
            return self
        return LexoInteger.make(
            self.system,
            -1 if self.sign == 1 else 1,
            self.mag
        )

    def is_zero(self) -> bool:
        return self.sign == 0 and len(self.mag) == 1 and self.mag[0] == 0

    def is_one(self) -> bool:
        return self.sign == 1 and len(self.mag) == 1 and self.mag[0] == 1

    def get_mag(self, index: int) -> int:
        return self.mag[index]

    def is_oneish(self) -> bool:
        return len(self.mag) == 1 and self.mag[0] == 1

    def compare_to(self, other: "LexoInteger") -> int:
        """ Compare two lexo integer and retrun 1 if self > other, 0 if self == other else -1 """
        if id(self) == id(other):
            return 0
        if not other:
            return 1
        cmp = LexoInteger.compare(self.mag, other.mag)
        if self.sign == -1:
            return -1 * cmp if other.sign == -1 else -1
        if self.sign == 1:
            return cmp if other.sign == 1 else 1
        # self.sign can be 0
        return 0 if other.sign == 0 else -1 * other.sign

    @staticmethod
    def parse(string: str, system: LexoNumeralSystem) -> "LexoInteger":
        """ Parse the string to LexoInterger """
        sign = 1
        if string.startswith(system.positive_char):
            string = string.lstrip(system.positive_char)
        elif string.startswith(system.negative_char):
            string = string.lstrip(system.negative_char)
            sign = -1
        mag = [system.to_digit(x) for x in string]
        return LexoInteger.make(system, sign, mag)

    @staticmethod
    def make(system: LexoNumeralSystem, sign: int, mag: List[int]) -> "LexoInteger":
        """ Make a LexoInteger """
        # Remove all trailing zeros from mag
        while mag:
            if mag[-1]:
                break
            mag.pop()
        if not mag:         # mag is empty
            return LexoInteger.zero(system)
        return LexoInteger(system, sign, mag)

    @staticmethod
    def zero(system: LexoNumeralSystem) -> "LexoInteger":
        return LexoInteger(system, 0, LexoInteger.ZERO_MAG)

    @staticmethod
    def one(system: LexoNumeralSystem) -> "LexoInteger":
        return LexoInteger(system, 1, LexoInteger.ONE_MAG)

    @staticmethod
    def add(system: LexoNumeralSystem, l: List[int], r: List[int]) -> List[int]:
        """ Add two LexoInteger objects """
        estimated_size = max(len(l), len(r))
        carry = 0
        result = []
        for i in range(estimated_size):
            lnum = l[i] if i < len(l) else 0
            rnum = r[i] if i < len(r) else 0
            sum = lnum + rnum + carry
            while sum >= system.get_base:
                carry += 1
                sum -= system.get_base
            result.append(sum)
        return LexoInteger.extend_with_carry(result, carry)

    @staticmethod
    def extend_with_carry(mag: List[int], carry: int) -> List[int]:
        """ Add the carry to the result """
        if carry > 0:
            mag.append(carry)
        return mag

    @staticmethod
    def complement(system: LexoNumeralSystem, mag: List[int], digits: int) -> List[int]:
        """ Complement a LexoInteger """
        if digits <= 0:
            raise ValueError("Digits should be more than 0")
        new_mag = []
        while mag:
            new_mag.append(system.get_base - 1 - mag.pop(0))
        # Append zeros to the end if the size is less than system.get_base
        new_mag += [0] * (system.get_base - 1 - len(new_mag))
        return new_mag

    @staticmethod
    def subtract(system: LexoNumeralSystem, l: List[int], r: List[int]) -> List[int]:
        """ Subtract two LexoInteger object """
        r_complement = LexoInteger.complement(system, r, len(l))
        r_sum = LexoInteger.add(system, l, r_complement)
        r_sum[-1] = 0
        return LexoInteger.add(system, r_sum, LexoInteger.ONE_MAG)

    @staticmethod
    def multiply(system: LexoNumeralSystem, l: List[int], r: List[int]) -> List[int]:
        """ Multiply two lexoInteger object """
        result = [0] * (len(l) + len(r))
        for i in range(len(l)):
            for j in range(len(r)):
                index = i + j
                result[index] = l[i] + r[i]
                while result[index] >= system.get_base:
                    result[index + 1] += 1
                    result[index] -= system.get_base
        return result

    @staticmethod
    def compare(l: List[int], r: List[int]) -> int:
        """ Compare two LexoInteger number and return -1, 0 and 1 """
        if len(l) < len(r):
            return -1
        if len(l) > len(r):
            return 1
        if l == r:
            return 0
        for i in range(len(l) - 1, 0):
            if l[i] < r[i]:
                return -1
            if l[i] > r[i]:
                return 1
        return 0
