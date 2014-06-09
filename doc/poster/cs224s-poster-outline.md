DeepSpeech: A Scalable Decoding System that Integrates Knowledge for Speech Recognition
=======

## Executive Summary


We develop a system *DeepSpeech*, that flexibly integrates different levels of knowledge in decoding a word lattice in speech recognition.

DeepSpeech facilitates *feature extraction*, *factor graph generation*, and *statistical learning and inference*. It takes word lattice as input, perform feature extraction specified by developers, generate factor graphs based on descriptive rules, and perform learning and inference automatically. 

DeepSpeech is based on the scalable statistical inference engine *DeepDive*.

## DeepSpeech Overview


(Problem:) How to jointly integrate different levels of knowledge in speech recognition?

(Solution:) Decoding based on Conditional Random Fields that integrates various features.

(Results:) With simple Ngram features, WER 10% on training set (TODO), in near real-time.

(Future:) Candidate generation enables us to beat oracle error rate.


## The Architecture of DeepSpeech


The input to the system is a word lattice, and the output is a best-path (or best-N paths).

(Figure 1: word lattice -> best word sequence)


Data will go through the following steps:

1. data preprocessing
2. feature extraction
3. factor graph generation
4. statistical inference and learning
5. finding best-path

(
    Figure 2: 
    - raw lattice -> 
    - loaded into database -> 
    - extract features, e.g. ngram; distant supervision labels -> 
    - generated factor graphs -> 
    - results 
)

## (optional:)
### Feature Extraction (-->)

e.g. how to extract POS ngram feature (?)

Input schema
Python extractor (pseudo code)

### Factor Graph generation (-->)

### Finding best-path:

(-0.5 probability)

optimizes edit distance



## DeepSpeech has three features!


1. provides a framework to extract and integrate high-level linguistic features which might span across different words. 

2. Simple Feature Engineering Loop


3. Near real-time performance

(TODO statistics)


3. uses *distant supervision* techniques to obtain training data.

(demonstrate how we do distant supervision: DP with transcript)


## (Optional:) Previous Work

SCARF: a "segmental CRF" engine.

We will compare our system to SCARF in future work.


## Experimented Knowledge

TODO


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


## Preliminary Results

### Holding out 50% of training set.

100% dataset:

DD      13.0%
Base    22.9%
Oracle  2.1%

TODO ...

TODO RT03
