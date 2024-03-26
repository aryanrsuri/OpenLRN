## OpenLRN

Lexical Rigor Notation

Attempts to perform semantic and linguistic analysis on text

This software is pre-pre-alpha

#### Todo

- DONE don't split on new line only on punctuation (poems for example)
- line count is too heavily weighted (double used)
- NLP
- compare other indeces (lexile ...)

#### Triage

```
.
|_utils/ (containing common words.txt)
|_resources/ (containing raw txt represntation of articles/poems/etc)
|_out/ (containing the *.html, *.csv, and *.png)
```

#### Example Output

```
                                  Text        Rigour  Log(Rigour)  Line Count  Word Count  Processing Time
0        emancipation_proclamation.txt  5.576547e+03     8.626325          15         612            0.095
1            ur-facism_umberto_eco.txt  5.165997e+04    10.852439         266        5299            0.113
2                          othello.txt  2.531929e+05    12.441907        2651       27395            0.449
3                           hamlet.txt  2.688555e+05    12.501929        2361       29601            0.416
4      the_great_gatsby_fitzgerald.txt  4.336010e+05    12.979880        2575       48151            0.493
5  price_and_prejudice_jane_austen.txt  1.086440e+06    13.898417        5768      122393            1.024
6        moby_dick_herman_melville.txt  1.903166e+06    14.459029        8670      208455            1.661
7                   finnegans_wake.txt  2.209189e+06    14.608136       13776      219554            3.126
8              ulysses_james_joyce.txt  2.415783e+06    14.697534       23454      264982            7.365
9           les_miserables_victor_hugo  4.994009e+06    15.423750       30678      560682            9.948
```
