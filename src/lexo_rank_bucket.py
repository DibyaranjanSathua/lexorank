"""
File:           lexo_rank_bucket.py
Author:         Dibyaranjan Sathua
Created on:     27/12/21, 8:31 pm
"""
from typing import Optional, List
from src.lexo_integer import LexoInteger
from src.lexo_numeral_system import LexoNumeralSystem


class LexoRankBucket:
    """ Lexo rank bucket class """
    _BUCKET_0: Optional["LexoRankBucket"] = None
    _BUCKET_1: Optional["LexoRankBucket"] = None
    _BUCKET_2: Optional["LexoRankBucket"] = None
    _VALUES: List["LexoRankBucket"] = []

    def __init__(self, value: str):
        self.value = LexoInteger.parse(value, LexoNumeralSystem())

    def __eq__(self, other: "LexoRankBucket") -> bool:
        if id(self) == id(other):
            return True
        if not other:
            return False
        return self.value == other.value

    def __str__(self):
        return str(self.value)

    def next(self) -> "LexoRankBucket":
        if self == LexoRankBucket.get_bucket_0():
            bucket = LexoRankBucket.get_bucket_1()
        elif self == LexoRankBucket.get_bucket_2():
            bucket = LexoRankBucket.get_bucket_0()
        else:
            bucket = LexoRankBucket.get_bucket_2()
        return bucket

    def prev(self) -> "LexoRankBucket":
        if self == LexoRankBucket.get_bucket_0():
            bucket = LexoRankBucket.get_bucket_2()
        elif self == LexoRankBucket.get_bucket_2():
            bucket = LexoRankBucket.get_bucket_1()
        else:
            bucket = LexoRankBucket.get_bucket_0()
        return bucket

    @classmethod
    def get_bucket_0(cls) -> "LexoRankBucket":
        if cls._BUCKET_0 is None:
            cls._BUCKET_0 = cls("0")
        return cls._BUCKET_0

    @classmethod
    def get_bucket_1(cls) -> "LexoRankBucket":
        if cls._BUCKET_1 is None:
            cls._BUCKET_1 = cls("1")
        return cls._BUCKET_1

    @classmethod
    def get_bucket_2(cls) -> "LexoRankBucket":
        if cls._BUCKET_2 is None:
            cls._BUCKET_2 = cls("2")
        return cls._BUCKET_2

    @staticmethod
    def get_values() -> List["LexoRankBucket"]:
        if not LexoRankBucket._VALUES:
            LexoRankBucket._VALUES = [
                LexoRankBucket.get_bucket_0(),
                LexoRankBucket.get_bucket_1(),
                LexoRankBucket.get_bucket_2()
            ]
        return LexoRankBucket._VALUES

    @staticmethod
    def get_max() -> "LexoRankBucket":
        return LexoRankBucket._VALUES[-1]

    @staticmethod
    def make_from(string: str) -> "LexoRankBucket":
        value = LexoInteger.parse(string, LexoNumeralSystem())
        for bucket in LexoRankBucket.get_values():
            if bucket.value == value:
                return bucket
        raise ValueError(f"Unknown bucket: {string}")

    @staticmethod
    def resolve(bucket_id: int) -> "LexoRankBucket":
        for bucket in LexoRankBucket.get_values():
            if bucket == LexoRankBucket.make_from(str(bucket_id)):
                return bucket
        raise ValueError(f"No bucket found with id: {bucket_id}")
