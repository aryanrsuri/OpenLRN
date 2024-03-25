

from typing import List
import re
import numpy as np
import pandas as pd

"""
## OpenLRN

Lexical Rigor Numerations

Lexical Bucketing:
    1. The whole text statistics
        a. length
        b. # of words
        c. # of sentences
        d. aggregate of sentence statistics:
            i. average difficulty
            ii. average uncommeness (is it in 1000 most common words?)
            iii. average disparetness (# of different words)

    2. Syntax (Sentence)
        a. length
        b. simple v complex
        c. # of uncommen terms
        d. Morphemes (Words):
            i. uncommon or not
            ii. unit length (n / 5.05 [wolframalpha])
Tasks:
    1. serialise text into sentences
    2. perform simple (no processing) analysis
    3. nlp analysis
    4. attempt to reduce this analysis to 2 distinct numbers
        a. LEX_TABLE_RIGOR
        b. NLP_RIGOR
"""


def _common_en_1000() -> set[str]:
    return {word.strip().lower() for word in open("./util/words.txt")}


def serialise_common_words(filepath: str) -> pd.DataFrame:
    """
    DEPRECATED: use _common_en_1000() instead
    ---
    Serialises 1000 words into a more readable data frame
    For now only adds the nlen , normalised word length
    to average length of 5.05 characters

    args:
        filepath (str) : path to words.txt

    returns:
        pd.DataFrame : processed df

    Examples
        serialise_common_words("./words.txt")
        ->   words    nlen
        -> 0   the   0.549
    """

    LEX_TABLE = pd.read_csv(filepath, names=["words"])
    LEX_TABLE["nlen"] = LEX_TABLE["words"].apply(lambda word: len(word) / 5.05)
    return LEX_TABLE


def pipe(filepath: str) -> pd.DataFrame:
    sentences: List[str] = []
    count: int = 0
    word_count: int = 0
    with open(filepath, "r") as file:

        trim = [line.strip().lower()
                for line in file.readlines() if line.strip()]
        for line in trim:
            sentence = re.split(r'(?<=[.!?])\s+', line)
            sentences.extend(sentence)

            # Must be more effecient or pythonic way to do this... or both
            for word in sentence[0].split():
                count += len(word)
                word_count += 1

    normal: float = count / word_count
    common = _common_en_1000()

    LEX_TABLE = pd.DataFrame(sentences, columns=["sentence"])
    LEX_TABLE["count"] = LEX_TABLE["sentence"].apply(
        lambda sentence: len(sentence.split()))
    LEX_TABLE["unique"] = LEX_TABLE["sentence"].apply(
        lambda sentence: len(set(sentence.split())))
    LEX_TABLE["uncommon"] = LEX_TABLE["sentence"].apply(
        lambda sentence: sum(word not in common for word in sentence.split()))
    LEX_TABLE["distribution"] = LEX_TABLE["count"].apply(
        lambda c: (c / LEX_TABLE["count"].sum()))
    LEX_TABLE["rarity"] = LEX_TABLE.apply(
        lambda row: row["uncommon"] / row["count"], axis=1)
    LEX_TABLE["verbosity"] = LEX_TABLE.apply(
        lambda row:  nverbose(row["sentence"], normal) / row["count"], axis=1)
    LEX_TABLE["nlens"] = LEX_TABLE["sentence"].apply(nlen, normal=normal)

    print(LEX_TABLE.head(n=20))
    print(LEX_TABLE.describe())
    return LEX_TABLE


def nlen(sentence: str, normal: float) -> list[float]:
    return [len(word) / normal for word in sentence.split()]


def nverbose(sentence: str, normal: float) -> float:
    count = 0
    for word in sentence.split():
        if len(word) > normal:
            count += 1
        pass
    return count


(pipe("./resources/ur-facism.txt"))
