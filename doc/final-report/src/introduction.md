Introduction
====

Motivation
----

Speech recognition has been suffering from bad independence assumptions
across different phases. Acoustic models are trained without syntactic
and semantic knowledge beyond words, thus underestimated probabilities
of correct words are hard to be captured by subsequent naive language
models. We believe that eventually, joint inference on acoustic and
language models is an especially promising future. As a first step
towards this goal, we concentrate on advanced decoding in the language
model phase. We propose to integrate more knowledge in decoding the word
lattice, with the help of joint inference.

For state-of-the-art decoding approaches, it is hard to integrate
sophisticated knowledge because of scalability reasons. With the
cutting-edge researches on graph learning and sampling, we are now able
to perform massive learning with a speed of millions of variables per
second. Weaponed with this, we propose to use general factor graphs to
do learning and inference on word lattices, integrating different kinds
of knowledge including syntactic, semantic, context and higher-level
knowledge. If time permits, we will try generating new candidates
outside the lattice, with the help of knowledge.

Specifically, this paper tries to answer following questions:

1. How to jointly integrate different levels of knowledge in speech recognition?
2. Is it possible to have a real-time decoding system that approach (or even beat) oracle error rate of word lattices?
3. How to make the trade-off of knowledge-featured language models 
   in real-time ASR applications within current technology?

Previous Works
----

Previous works on integrating knowledge into speech recognition include ...

TODO SCARF is a platform that utilizes segmental conditional random fields... (cons) Its performance... (pros) Flexibility..

TODO DNN

TODO cite CRF, 
factor graph,



Our approach
----

We propose a decoding system based on word-level Conditional Random Fields (CRFs) that is able to integrate various linguistic and domain-specific features. 

CRFs are a type of general factor graphs. In our factor graph model, each **variable** is a word candidate in the lattice, and each **factor** is a feature or a domain-specific rule. 

**TODO plot**

For example, "eat the apple" in the lattice corresponds to three variables, and different factors might apply to them.

We obtain labels for variable-level training data by *distant supervision*: we match each lattice with its corresponding transcript, find all best paths in the lattice, and label all words on the best paths that matches a word in the transcript as *true*, other words as *false*.

The features we present in our system include following: 

- word N-gram based statistics (check N-gram frequency in Google Ngram)
- bag of word N-grams (each N-gram itself is a feature) 
- a second "confirmatory" decoding made with an independent speech recognizer (which comes with the lattice data)
- words around silence

These are simple features we can add, however DeepSpeech enables developers to plug in more complicated features such as dependency paths, co-references, speaker-specific and contextual features.

Results
----
We got WER 10.2% on 152,251 broadcast news lattices with a simple feature set. (baseline 22.9%, oracle 2.1%) We finished training and testing in 70 minutes while the whole corpus is 400 hours, which indicates that our approach can be developed into a system that performs real-time decoding.

System
----

We will release *DeepSpeech* system as an open-source platform for advanced decoding with flexible knowledge integration. Developers will be able to plug in their own extractors and apply the system to their own datasets.

Using DeepSpeech provides following benefits: (1) easy extraction and integration of linguistic features; (2) simpler feature engineering loops; (3) a rigorous probabilistic framework.

