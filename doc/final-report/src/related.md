DeepSpeech Features
====

## Extract & Integrate linguistic features

DeepSpeech provides a framework for developers to extract and integrate high-level features

Here is how developers can easily plug-in a corefence feature “extractor” to DeepSpeech:

SQL:

Define a SQL query to generate all pairs of candidate words that appear in the same lattice, and pair it with a python function.

    SELECT t0.CID, t0.TEXT,
           t1.CID, t1.TEXT
    FROM   candidate t0,
           candidate t1
    WHERE  t0.LID = t1.LID
    USEPYTHON pyfunc

PYTHON:

We write a Python function to process all phrase pairs and identify coreferent pairs.


    def pyfunc(c1, t1, c2, t2):
        if edit_dist(t1, t2) < 2:
            emit(“Coref”, c1, c2)


## Simpler Feature Engineering

TODO brainwash paper

## Rigorous Probabilistic Framework

TODO paper

Related Work
====

\cite{bleijml2003}.


