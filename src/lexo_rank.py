"""
File:           lexo_rank.py
Author:         Dibyaranjan Sathua
Created on:     27/12/21, 9:39 pm

Code transpiled from: https://github.com/kvandake/lexorank-ts
"""
from typing import Optional

from src.lexo_numeral_system import LexoNumeralSystem
from src.lexo_decimal import LexoDecimal
from src.lexo_rank_bucket import LexoRankBucket


class LexoRank:
    """ Lexo rank main class """
    NUMERAL_SYSTEM: LexoNumeralSystem = LexoNumeralSystem()
    _ZERO_DECIMAL: Optional[LexoDecimal] = None
    _ONE_DECIMAL: Optional[LexoDecimal] = None
    _EIGHT_DECIMAL: Optional[LexoDecimal] = None
    _MIN_DECIMAL: Optional[LexoDecimal] = None
    _MAX_DECIMAL: Optional[LexoDecimal] = None
    _MID_DECIMAL: Optional[LexoDecimal] = None
    _INITIAL_MIN_DECIMAL: Optional[LexoDecimal] = None
    _INITIAL_MAX_DECIMAL: Optional[LexoDecimal] = None

    def __init__(self, bucket: LexoRankBucket, decimal: LexoDecimal):
        self.value = str(bucket) + "|" + LexoRank._format_decimal(decimal)
        self.bucket = bucket
        self.decimal = decimal

    def __eq__(self, other: "LexoRank"):
        if id(self) == id(other):
            return True
        if not other:
            return False
        return self.value == other.value

    def __str__(self):
        return self.value

    def between(self, other: "LexoRank") -> "LexoRank":
        if not self.bucket == other.bucket:
            raise ValueError("between works on same bucket")
        cmp = self.decimal.compare_to(other.decimal)
        if cmp == 0:
            raise ValueError("Try to rank between different ranks")
        if cmp > 0:
            return LexoRank(self.bucket, LexoRank.between_decimal(other.decimal, self.decimal))
        return LexoRank(self.bucket, LexoRank.between_decimal(self.decimal, other.decimal))

    def gen_prev(self) -> "LexoRank":
        if self.is_max():
            return LexoRank(self.bucket, LexoRank.get_initial_max_decimal())
        floor_integer = self.decimal.floor()
        floor_decimal = LexoDecimal.make_from(floor_integer)
        next_decimal = floor_decimal - LexoRank.get_eight_decimal()
        if next_decimal.compare_to(LexoRank.get_min_decimal()) <= 0:
            next_decimal = LexoRank.between_decimal(LexoRank.get_min_decimal(), self.decimal)
        return LexoRank(self.bucket, next_decimal)

    def gen_next(self) -> "LexoRank":
        if self.is_min():
            return LexoRank(self.bucket, LexoRank.get_initial_min_decimal())
        ceil_integer = self.decimal.ceil()
        ceil_decimal = LexoDecimal.make_from(ceil_integer)
        next_decimal = ceil_decimal + LexoRank.get_eight_decimal()
        if next_decimal.compare_to(LexoRank.get_max_decimal()) >= 0:
            next_decimal = LexoRank.between_decimal(self.decimal, LexoRank.get_max_decimal())
        return LexoRank(self.bucket, next_decimal)

    def get_bucket(self) -> LexoRankBucket:
        return self.bucket

    def get_decimal(self) -> LexoDecimal:
        return self.decimal

    def in_next_bucket(self) -> "LexoRank":
        return LexoRank.make_from(self.bucket.next(), self.decimal)

    def in_prev_bucket(self) -> "LexoRank":
        return LexoRank.make_from(self.bucket.prev(), self.decimal)

    def is_min(self) -> bool:
        return self.decimal == self.get_min_decimal()

    def is_max(self) -> bool:
        return self.decimal == self.get_max_decimal()

    def compare_to(self, other: "LexoRank") -> int:
        if id(self) == id(other):
            return 0
        if not other:
            return 1
        return -1 if self.value < other.value else 1 if self.value > other.value else 0

    @staticmethod
    def get_zero_decimal() -> LexoDecimal:
        if LexoRank._ZERO_DECIMAL is None:
            LexoRank._ZERO_DECIMAL = LexoDecimal.parse("0", LexoRank.NUMERAL_SYSTEM)
        return LexoRank._ZERO_DECIMAL

    @staticmethod
    def get_one_decimal() -> LexoDecimal:
        if LexoRank._ONE_DECIMAL is None:
            LexoRank._ONE_DECIMAL = LexoDecimal.parse("1", LexoRank.NUMERAL_SYSTEM)
        return LexoRank._ONE_DECIMAL

    @staticmethod
    def get_eight_decimal() -> LexoDecimal:
        if LexoRank._EIGHT_DECIMAL is None:
            LexoRank._EIGHT_DECIMAL = LexoDecimal.parse("8", LexoRank.NUMERAL_SYSTEM)
        return LexoRank._EIGHT_DECIMAL

    @staticmethod
    def get_min_decimal() -> LexoDecimal:
        if LexoRank._MIN_DECIMAL is None:
            LexoRank._MIN_DECIMAL = LexoRank.get_zero_decimal()
        return LexoRank._MIN_DECIMAL

    @staticmethod
    def get_max_decimal() -> LexoDecimal:
        if LexoRank._MAX_DECIMAL is None:
            LexoRank._MAX_DECIMAL = LexoDecimal.parse("1000000", LexoRank.NUMERAL_SYSTEM) - \
                                    LexoRank.get_one_decimal()
        return LexoRank._MAX_DECIMAL

    @staticmethod
    def get_mid_decimal() -> LexoDecimal:
        if LexoRank._MID_DECIMAL is None:
            LexoRank._MID_DECIMAL = LexoRank.between_decimal(
                LexoRank.get_min_decimal(), LexoRank.get_max_decimal()
            )
        return LexoRank._MID_DECIMAL

    @staticmethod
    def get_initial_min_decimal() -> LexoDecimal:
        if LexoRank._INITIAL_MIN_DECIMAL is None:
            LexoRank._INITIAL_MIN_DECIMAL = LexoDecimal.parse("100000", LexoRank.NUMERAL_SYSTEM)
        return LexoRank._INITIAL_MIN_DECIMAL

    @staticmethod
    def get_initial_max_decimal() -> LexoDecimal:
        if LexoRank._INITIAL_MAX_DECIMAL is None:
            LexoRank._INITIAL_MAX_DECIMAL = LexoDecimal.parse(
                LexoRank.NUMERAL_SYSTEM.to_char(LexoRank.NUMERAL_SYSTEM.get_base - 2) + "00000",
                LexoRank.NUMERAL_SYSTEM
            )
        return LexoRank._INITIAL_MAX_DECIMAL

    @staticmethod
    def min() -> "LexoRank":
        return LexoRank.make_from(LexoRankBucket.get_bucket_0(), LexoRank.get_min_decimal())

    @staticmethod
    def max(bucket: Optional[LexoRankBucket] = None) -> "LexoRank":
        if bucket is None:
            bucket = LexoRankBucket.get_bucket_0()
        return LexoRank.make_from(bucket, LexoRank.get_max_decimal())

    @staticmethod
    def middle() -> "LexoRank":
        min_lexo_rank = LexoRank.min()
        return min_lexo_rank.between(LexoRank.max(min_lexo_rank.bucket))

    @staticmethod
    def initial(bucket: LexoRankBucket) -> "LexoRank":
        return LexoRank.make_from(bucket, LexoRank.get_initial_min_decimal()) \
            if bucket == LexoRankBucket.get_bucket_0() \
            else LexoRank.make_from(bucket, LexoRank.get_initial_max_decimal())

    @staticmethod
    def between_decimal(old_left: LexoDecimal, old_right: LexoDecimal) -> LexoDecimal:
        left = old_left
        right = old_right
        if old_left.get_scale() < old_right.get_scale():
            new_left = old_right.set_scale(old_left.get_scale(), ceiling=False)
            if old_left.compare_to(new_left) >= 0:
                return LexoRank._mid(old_left, old_right)
            right = new_left

        if old_left.get_scale() > right.get_scale():
            new_left = old_left.set_scale(right.get_scale(), ceiling=True)
            if new_left.compare_to(right) >= 0:
                return LexoRank._mid(old_left, old_right)
            left = new_left
        scale = left.get_scale()
        while scale > 0:
            new_scale1 = scale - 1
            new_left1 = left.set_scale(new_scale1, ceiling=True)
            new_right = right.set_scale(new_scale1, ceiling=False)
            cmp = new_left1.compare_to(new_right)
            if cmp == 0:
                return LexoRank._check_mid(old_left, old_right, new_left1)
            if cmp > 0:
                break
            scale = new_scale1
            left = new_left1
            right = new_right

        mid = LexoRank._middle_internal(old_left, old_right, left, right)
        mid_scale = mid.get_scale()
        while mid_scale > 0:
            new_scale = mid_scale - 1
            new_mid = mid.set_scale(new_scale, ceiling=False)
            if old_left.compare_to(new_mid) >= 0  or new_mid.compare_to(old_right) >= 0:
                break
            mid = new_mid
            mid_scale = new_scale
        return mid

    @staticmethod
    def parse(string: str) -> "LexoRank":
        parts = string.split("|")
        bucket = LexoRankBucket.make_from(parts[0])
        decimal = LexoDecimal.parse(parts[1], LexoRank.NUMERAL_SYSTEM)
        return LexoRank(bucket, decimal)

    @staticmethod
    def make_from(bucket: LexoRankBucket, decimal: LexoDecimal) -> "LexoRank":
        return LexoRank(bucket, decimal)

    @staticmethod
    def _mid(left: LexoDecimal, right: LexoDecimal) -> LexoDecimal:
        sum_value = left + right
        mid = sum_value * LexoDecimal.half(left.get_system())
        scale = max(left.get_scale(), right.get_scale())
        if mid.get_scale() > scale:
            round_down = mid.set_scale(scale, ceiling=False)
            if round_down.compare_to(left) > 0:
                return round_down
            round_up = mid.set_scale(scale, ceiling=True)
            if round_up.compare_to(right) < 0:
                return round_up
        return mid

    @staticmethod
    def _check_mid(
            left_bound: LexoDecimal, right_bound: LexoDecimal, mid: LexoDecimal
    ) -> LexoDecimal:
        if left_bound.compare_to(mid) >= 0 or mid.compare_to(right_bound) >= 0:
            return LexoRank._mid(left_bound, right_bound)
        return mid

    @staticmethod
    def _middle_internal(
            left_bound: LexoDecimal,
            right_bound: LexoDecimal,
            left: LexoDecimal,
            right: LexoDecimal
    ) -> LexoDecimal:
        mid = LexoRank._mid(left, right)
        return LexoRank._check_mid(left_bound, right_bound, mid)

    @staticmethod
    def _format_decimal(decimal: LexoDecimal) -> str:
        format_value = str(decimal)
        new_value = format_value
        partial_index = format_value.find(LexoRank.NUMERAL_SYSTEM.radix_point_char)
        zero = LexoRank.NUMERAL_SYSTEM.to_char(0)
        if partial_index < 0:
            partial_index = len(format_value)
            new_value += LexoRank.NUMERAL_SYSTEM.radix_point_char
        while partial_index < 6:
            new_value = zero + new_value
            partial_index += 1
        new_value = new_value.rstrip(zero)
        return new_value
