Introduction
====

Problem: How to jointly integrate different levels of knowledge in speech recognition?

Solution: Decoding based on Conditional Random Fields that integrates various features.

Results: Got WER 10.2% on 150k broadcast news lattices in near real-time, with a simple feature set. (baseline 22.9%, oracle 2.1%)

Future: Candidate generation with linguistic knowledge might beat oracle error rate; joint inference on acoustic and language models
