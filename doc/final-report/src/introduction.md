Introduction
====

- Problem: How to jointly integrate different levels of knowledge in speech recognition?

- Solution: Decoding based on Conditional Random Fields that integrates various features.

- Results: Got WER 10.2% on 150k broadcast news lattices in near real-time, with a simple feature set. (baseline 22.9%, oracle 2.1%)

- Future: Candidate generation with linguistic knowledge might beat oracle error rate; joint inference on acoustic and language models

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

Specifically, we aim to answer following questions:

1. How can different levels of knowledge help in speech recognition?
2. Can we approach or even beat the oracle error rate of word lattices?
3. How to make the trade-off of knowledge-featured language models 
   in real-time ASR applications within current technology?
