DeepSpeech
=======

DeepDive Application for Speech recognition

Dataset
----

/dfs/madmax/0/zifei/LDC2011T06/

Training lattices are derived from the corpora listed below:
LDC Number                 Description   Hours
LDC97S44/LDC97T22          1996 HUB4     104
LDC98S71/LDC98T28          1997 HUB4     97
LDC2005S11/LDC2005T16      TDT4          300

Statistics:
    
    22852182 candidates

    152251 lattices


### Format 

train.db.gz:

The lattices can be related to the original audio files via the file "train.db.gz" which lists for each segment a tag-name, segment number, the original audio file, channel (always 0), start time, and end time (in seconds). A sample line is as follows:

19960510_NPR_ATC#Ailene_Leblanc 0001 19960510_NPR_ATC.sph 0 76.767 89.404 | 


Bbase: baseline full lattice (?)


Bdc: full lattice (152251 lattices)

    19960510_NPR_ATC#Ailene_Leblanc@0001.dc
    1 2 <s> confirm=0
    3 13 THE confirm=1
    3 14 THE confirm=1
    14 37 TWO confirm=1
    15 36 TWO confirm=1
    37 114 HELICOPTERS confirm=1
    38 114 HELICOPTERS confirm=1
    115 131 WERE confirm=1
    132 206 PARTICIPATING confirm=1


Bnc: oracle path (containing the *subset* of paths consistent with the training transcriptions)

    19960510_NPR_ATC#Ailene_Leblanc@0001.nc
    1 2 <s>  0 1 confirm=0
    3 13 THE  1 2 confirm=1
    3 14 THE  1 3 confirm=1
    14 37 TWO  2 5 confirm=1
    15 36 TWO  3 4 confirm=1
    37 114 HELICOPTERS  4 6 confirm=1
    38 114 HELICOPTERS  5 6 confirm=1
    115 131 WERE  6 7 confirm=1
    132 206 PARTICIPATING  7 8 confirm=1


Btr: transcriptions

    19960510_NPR_ATC#Ailene_Leblanc@0001.tr
    <s> THE TWO HELICOPTERS WERE PARTICIPATING IN WAR GAMES WITH BRITISH FORCES OFF THE COAST OF NORTH CAROLINA NEAR JACKSONVILLE ~SIL THE C. H. FORTY SIX ~SIL SEA KNIGHT TRANSPORT AIRCRAFT AND THE A. H. ONE COBRA ATTACK HELICOPTER </s>
    .
    19960510_NPR_ATC#Ailene_Leblanc@0002.tr
    <s> COLLIDED AND CRASHED IN A SWAMPY FIELD SURROUNDED BY WOODS CALLED COURTHOUSE ~SIL BAY </s>
    .
    19960510_NPR_ATC#Ailene_Leblanc@0003.tr
    <s> SECOND LIEUTENANT ~SIL UPTON ~SIL SAYS THE CORPS IS NOW IN THE PROCESS OF LOCATING THE FAMILIES OF THE MARINES INVOLVED </s>
    .
    19960510_NPR_ATC#Ailene_Leblanc@0004.tr


### Example 

    19960510_NPR_ATC#Alan_Liotta@0001.dc
    1 8 <s> confirm=0
    1 9 <s> confirm=0
    9 38 THE confirm=1
    10 38 THE confirm=1
    39 72 REMAINS confirm=1
    39 73 REMAINS confirm=1
    39 79 REMAINDER confirm=-1
    39 80 REMAINDER confirm=-1
    73 85 WHICH confirm=1
    74 79 ARE confirm=-1
    74 79 WERE confirm=-1
    74 80 ARE confirm=-1
    74 81 OF confirm=-1
    80 90 TO confirm=1
    81 90 TO confirm=1
    81 90 TOO confirm=-1
    81 90 TWO confirm=-1
    82 90 TWO confirm=-1
    86 96 WERE confirm=-1
    91 141 RETURN confirm=-1
    91 142 RETURNED confirm=-1
    97 142 RETURNED confirm=-1
    142 153 TO confirm=1
    142 153 TWO confirm=-1
    142 155 TO confirm=1
    142 156 TO confirm=1
    143 153 TO confirm=1
    143 154 TO confirm=1
    143 155 TO confirm=1
    143 156 TO confirm=1
    154 187 S. confirm=-1
    155 187 US confirm=1
    156 187 US confirm=1
    157 187 ICE confirm=-1
    188 205 ~SIL confirm=0
    188 207 ~SIL confirm=0
    206 234 ~SIL confirm=0
    206 235 ~SIL confirm=0

    19960510_NPR_ATC#Alan_Liotta@0001.nc
    1 8 <s>  0 1 confirm=0
    1 9 <s>  0 2 confirm=0
    9 38 THE  1 3 confirm=1
    10 38 THE  2 3 confirm=1
    39 72 REMAINS  3 4 confirm=1
    73 85 WHICH  4 6 confirm=1
    86 96 WERE  6 7 confirm=-1
    97 142 RETURNED  7 8 confirm=-1
    143 154 TO  8 10 confirm=1
    143 155 TO  8 11 confirm=1
    155 187 US  10 87 confirm=1
    156 187 US  11 86 confirm=1
    188 207 ~SIL  87 15 confirm=0
    188 207 ~SIL  86 15 confirm=0

    19960510_NPR_ATC#Alan_Liotta@0001.tr
    <s> THE REMAINS WHICH WERE RETURNED TO US ~SIL AH THE CENTRAL IDENTIFICATION LABORATORY HAS REVIEWED THOSE REMAINS AND ~SIL AND UM ~SIL WE'VE NOT BEEN AB- WE'VE ONLY POSITIVELY IDENTIFIED FIVE SETS OF REMAINS ~SIL THEIR RECOVERY TECHNIQUES ~SIL WERE NOT ALLOWING US TO MAKE ~SIL POSITIVE IDENTIFICATIONS ~SIL </s>

Knowledge Taxonomy
----

- ASR-software specific knowledge: 
    - What errors that ASR systems tend to make?
    - Can we learn rules to fix software errors and generate 
      correct candidates?

- Corpus statistics: 
    - word-level: frequency of word N-grams in corpus
    - sentence level: frequency of sentences 
    - conversation level: frequency of conversations

- Deep linguistic features:
    - POS, NER and parsing

- High-level knowledge:
    - Topic-specific: weight words by topic
    - Speaker-specific: weight words by personal habit
    - Context-specific: condition on social relationships, emotion, time, etc.

Experiments
----

There is no systematic experiments about how these different kinds of
knowledge can fix errors in speech recognition systems.  We propose to
conduct an error analysis about how different knowledge can improve
error rates in our system, and implement a most useful subset of
knowledge listed above.

We propose to experiment on several existing word lattices with
different lattice error rate ("oracle" error rate). We aim to generate
output sequences that can approach the oracle error rate, or even go
beyond it on bad-quality lattices (if time permits).


Preliminary Results
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
DD 12.9%

 # Snt # Wrd | Corr    Sub    Del    Ins    Err  S.Err |
  500  20165 | 94.9    4.8    0.3    7.5   12.6   90.0 |

