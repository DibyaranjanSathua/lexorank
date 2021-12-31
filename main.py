"""
File:           main.py
Author:         Dibyaranjan Sathua
Created on:     31/12/21, 8:38 pm
"""
from src.lexo_rank import LexoRank


def main():
    min_lexo_rank = LexoRank.min()
    print(min_lexo_rank)
    max_lexo_rank = LexoRank.max()
    print(max_lexo_rank)
    mid_lexo_rank = LexoRank.middle()
    print(mid_lexo_rank)


if __name__ == "__main__":
    main()
