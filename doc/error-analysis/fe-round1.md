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

12.2 Only stopword around: (bad)

    # Snt # Wrd | Corr    Sub    Del    Ins    Err  S.Err |
     500  20165 | 89.7    3.9    6.4    1.9   12.2   77.2 |


## Adding conflict constraint

BEFORE:
  nvar               : 157613
  nfac               : 3128783
  nweight            : 16247
  nedge              : 3128783
AFTER:
  nvar               : 157613
  nfac               : 8420170
  nweight            : 16248
  nedge              : 13711557

    # Snt # Wrd | Corr    Sub    Del    Ins    Err  S.Err |
     500  20165 | 92.7    4.1    3.2    2.8   10.2   81.4 |

## Add chaining: Interestingly, increase Err but decrese S.Err?!

    # Snt # Wrd | Corr    Sub    Del    Ins    Err  S.Err |
     500  20165 | 89.9    5.1    5.0    2.3   12.4   78.2 |

## Add POS 2/3gram: increase Err... 
experiments/2014-05-31T162303-/

    # Snt # Wrd | Corr    Sub    Del    Ins    Err  S.Err |
     500  20165 | 91.6    5.9    2.5    3.4   11.8   84.2 |

Change -a from 0.01 to 0.1: 14.1
| SPKR                             | # Snt # Wrd | Corr    Sub    Del    Ins    Err  S.Err |
| Sum/Avg                          |  500  20165 | 89.4    8.0    2.6    3.5   14.1   88.0 |

Change -a 0.001:

| SPKR                             | # Snt # Wrd | Corr    Sub    Del    Ins    Err  S.Err |
| Sum/Avg                          |  500  20165 | 92.2    4.7    3.1    3.3   11.1   82.2 |

Only with POS 2gram (-a 0.001):

     # Snt # Wrd | Corr    Sub    Del    Ins    Err  S.Err |
      500  20165 | 92.6    4.3    3.1    3.0   10.4   81.4 |

Without POS -a 0.001:

    # Snt # Wrd | Corr    Sub    Del    Ins    Err  S.Err |
    500  20165 | 92.5    4.3    3.2    2.9   10.4   82.8 |

Changed back to -a 0.01.

With POS window:

    # Snt # Wrd | Corr    Sub    Del    Ins    Err  S.Err |
     500  20165 | 91.8    5.0    3.1    3.4   11.6   83.2 |
Experiment result saved to: experiments/2014-05-31T165652-/


## With cand 3gram:

    # Snt # Wrd | Corr    Sub    Del    Ins    Err  S.Err |
     500  20165 | 92.8    4.1    3.1    2.9   10.1   82.0 |

## With cand 3gram + 4gram:

    | SPKR    | # Snt   # Wrd  | Corr     Sub     Del     Ins    Err   S.Err  |
    | Sum/Avg |  500    20165  | 92.7     4.2     3.1     2.8   10.1    81.8  |

Running on full table:

12:26:19 [sampler] INFO  # nvar               : 22852182
12:26:19 [sampler] INFO  # nfac               : 1314953737
12:26:19 [sampler] INFO  # nweight            : 6079863
12:26:19 [sampler] INFO  # nedge              : 2173745783

