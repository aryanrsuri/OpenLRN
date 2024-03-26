

import math
import os
from typing import List
import re
import time
import pandas as pd
import matplotlib.pyplot as plt

"""
## OpenLRN

Lexical rigour Numerations

Lexical Bucketing:
    1. The whole text statistics
        a. length
        b. # of words
        c. # of sentences
        d. process of sentence statistics:
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
        a. LEX_TABLE_rigour
        b. NLP_rigour
"""


def _common_en_1000() -> set[str]:
    return {word.strip().lower() for word in open("./util/words.txt")}


COMMEN = _common_en_1000()


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


def tokenise(filepath: str) -> tuple[List[str], int, float]:
    """Take a text file of literature and tokenise it into sentences
    Also return a 'normal' which is the average word length

    @param:
        filepath (str) : path to text
    @returns:
        tuple[List[str],int, float] : tokens , word count, and avg. word length
    """
    tokens: List[str] = []
    count: int = 0
    word_count: int = 0
    with open(filepath, "r") as file:
        text = file.read().lower().replace('\n', ' ')
        sentences = re.split(r"(?<=[.?!])\s+", text)
        sentences = [s for s in sentences if s.strip()]
    for sentence in sentences:
        tokens.extend(sentences)
        for word in sentence:
            count += len(word)
            word_count += 1
    normal: float = count / word_count
    return sentences, word_count, normal


def pipe(filepath: str) -> tuple[pd.DataFrame, float]:
    sentences, word_count, normal = tokenise(filepath)
    LEX_TABLE = pd.DataFrame(sentences, columns=["sentence"])
    LEX_TABLE["count"] = LEX_TABLE["sentence"].apply(
        lambda sentence: len(sentence.split()))
    LEX_TABLE["unique"] = LEX_TABLE["sentence"].apply(
        lambda sentence: len(set(sentence.split())))
    LEX_TABLE["uncommon"] = LEX_TABLE["sentence"].apply(
        lambda sentence: sum(word not in COMMEN for word in sentence.split()))
    LEX_TABLE["weight"] = LEX_TABLE["count"].apply(
        lambda c: (c / LEX_TABLE["count"].mean()))
    LEX_TABLE["uniqueness"] = LEX_TABLE.apply(
        lambda row: row["unique"] / row["count"], axis=1)
    LEX_TABLE["rarity"] = LEX_TABLE.apply(
        lambda row: row["uncommon"] / row["count"], axis=1)
    LEX_TABLE["verbosity"] = LEX_TABLE.apply(
        lambda row:  nverbose(row["sentence"], normal) / row["count"], axis=1)
    LEX_TABLE["complexity"] = LEX_TABLE.apply(
        lambda row: (row["uniqueness"] + row["rarity"] +
                     row["verbosity"] / 3),
        axis=1)
    LEX_TABLE["rigour"] = LEX_TABLE.apply(
        lambda row: ((row["uniqueness"] + row["rarity"] +
                     row["verbosity"] / 3) * row["weight"]) * normal,
        axis=1)

    LEX_TABLE["crigour"] = LEX_TABLE["rigour"].cumsum()
    LEX_TABLE["nlens"] = LEX_TABLE["sentence"].apply(nlen, normal=normal)
    RIGOUR = LEX_TABLE['rigour'].sum() * (word_count)
    # result sent to ./out

    filename = filepath.rsplit('/')[-1]
    LEX_TABLE.to_html(f"./out/{filename}.html")
    plot(filename, LEX_TABLE)

    return LEX_TABLE, RIGOUR


def nlen(sentence: str, normal: float) -> list[float]:
    return [len(word) / normal for word in sentence.split()]


def plot(filename: str, table: pd.DataFrame) -> None:
    fig, axis = plt.subplots(1, 2, figsize=(
        10, 5), gridspec_kw={'width_ratios': [2, 0]})
    axis[0].scatter(table.index, table["crigour"])
    axis[0].grid(True)
    axis[0].set_ylabel('Cumulative rigour')
    # axis[1].scatter(table.index, table["weight"])
    # axis[1].grid(True)
    # axis[1].set_ylabel('Weight')
    plt.suptitle(
        f"rigour analysis of {filename}\nTotal rigour : {round(table['rigour'].sum(), 4)}", ha='center')
    plt.xlabel("Sentence Coordinate")
    plt.tight_layout()
    plt.savefig(f"./out/{filename}.png")


def nverbose(sentence: str, normal: float) -> float:
    count = 0
    for word in sentence.split():
        if len(word) > normal:
            count += 1
        pass
    return count


def process(d: str) -> pd.DataFrame:
    rigours = []
    for filename in os.listdir(d):
        s = time.time()
        print(f"processing {filename}...")
        table, rigour = pipe(os.path.join(d, filename))
        e = time.time()
        rigours.append([filename, rigour, math.log(rigour), len(
            table.index), table["count"].sum(), round(e-s, 3)])
        print(f"[{round(e-s,2)}s] processed  {filename}...")
    processed = pd.DataFrame(rigours, columns=["Text", "Rigour", "Log(Rigour)", "Line Count",
                             "Word Count", "Processing Time"]).sort_values(by=["Rigour"], ignore_index=True)
    processed.to_html("./out/final_processed_data.html")
    return processed


r = {"les_miserables_victor_hugo.txt": 1010, "ulysses_james_joyce.txt": 1050}

print(process("./resources"))
# print(test_pipe("./resources/the_great_gatsby_fitzgerald.txt"))
