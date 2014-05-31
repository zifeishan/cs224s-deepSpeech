Error analysis & feature engineering Round 1
----

### Holding out 50% of training set.

100% dataset:

DD      13.0%
Base    22.9%
Oracle  2.1%

1k dataset:

## before improving
DD 13.4% 

## add skip2gram

DD 12.6%

     # Snt # Wrd | Corr    Sub    Del    Ins    Err  S.Err |
      500  20165 | 94.9    4.8    0.3    7.5   12.6   90.0 |

## Add bag of words (2gram) around skipwords

DD 11.7%

    # Snt # Wrd | Corr    Sub    Del    Ins    Err  S.Err |
     500  20165 | 95.1    4.6    0.3    6.8   11.7   87.6 |

(11.6% on 10k)

    # Snt # Wrd | Corr    Sub    Del    Ins    Err  S.Err |
     500  20165 | 95.1    4.6    0.2    6.7   11.6   87.6 |


11.0% : Added 0.5 punishment to findbestpath (1k)

    # Snt # Wrd | Corr    Sub    Del    Ins    Err  S.Err |
     500  20165 | 90.9    4.0    5.1    1.8   11.0   78.0 |
