"""
File:           main.py
Author:         Dibyaranjan Sathua
Created on:     31/12/21, 8:38 pm

Reference: https://github.com/kvandake/lexorank-ts
"""
from src.lexo_rank import LexoRank


def main():
    # min_lexo_rank = LexoRank.min()
    # print(min_lexo_rank)
    # max_lexo_rank = LexoRank.max()
    # print(max_lexo_rank)
    # mid_lexo_rank = LexoRank.middle()
    # print(mid_lexo_rank)
    # next_lexo_rank = mid_lexo_rank.gen_next()
    # print(next_lexo_rank)
    # next_lexo_rank = next_lexo_rank.gen_next()
    # print(next_lexo_rank)
    # prev_lexo_rank = next_lexo_rank.gen_prev()
    # print(prev_lexo_rank)
    # prev_lexo_rank1 = mid_lexo_rank.gen_prev()
    # print(prev_lexo_rank1)
    # prev_lexo_rank2 = prev_lexo_rank.gen_prev()
    # print(prev_lexo_rank2)

    # ranks = []
    # lexo_rank1 = LexoRank.parse('0|0i0000:')
    # print(f"1. {lexo_rank1}")
    # ranks.append(str(lexo_rank1))
    # lexo_rank2 = lexo_rank1.gen_next()
    # print(f"2. {lexo_rank2}")
    # ranks.append(str(lexo_rank2))
    # lexo_rank3 = lexo_rank2.gen_next()
    # print(f"3. {lexo_rank3}")
    # ranks.append(str(lexo_rank3))
    # lexo_rank31 = lexo_rank3.gen_next()
    # print(f"4. {lexo_rank31}")
    # ranks.append(str(lexo_rank31))
    # lexo_rank4 = lexo_rank3.gen_prev()
    # print(f"<-3. {lexo_rank4}")
    # ranks.append(str(lexo_rank4))
    # lexo_rank5 = lexo_rank4.gen_prev()
    # print(f"<-<-3. {lexo_rank5}")
    # ranks.append(str(lexo_rank5))
    # lexo_rank6 = lexo_rank5.gen_prev()
    # print(f"<-<-<-3. {lexo_rank6}")
    # ranks.append(str(lexo_rank6))
    #
    # # Sort all the ranks
    # ranks.sort()
    # print(ranks)
    #
    # lexo_rank1 = LexoRank.parse('0|0i0008:')
    # print(f"1. {lexo_rank1}")
    # lexo_rank2 = lexo_rank1.gen_next()
    # print(f"1->. {lexo_rank2}")
    # lexo_rank3 = lexo_rank1.gen_prev()
    # print(f"1<-. {lexo_rank3}")

    ranks = []
    lexo_rank1 = LexoRank.parse('0|0i0000:')
    print(lexo_rank1)
    ranks.append(lexo_rank1)
    lexo_rank2 = lexo_rank1.gen_next()
    print(lexo_rank2)
    ranks.append(lexo_rank2)
    lexo_rank1p5 = lexo_rank1.between(lexo_rank2)
    print(lexo_rank1p5)
    ranks.append(lexo_rank1p5)
    lexo_rank1p25 = lexo_rank1.between(lexo_rank1p5)
    print(lexo_rank1p25)
    ranks.append(lexo_rank1p25)
    lexo_rank1p75 = lexo_rank1p5.between(lexo_rank2)
    print(lexo_rank1p75)
    ranks.append(lexo_rank1p75)

    ranks.sort()
    print(ranks)


if __name__ == "__main__":
    main()
