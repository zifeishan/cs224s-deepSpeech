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
sophisticated knowledge because of scalability reasons. However, with the
cutting-edge researches on graph learning and sampling, we are now able
to perform massive learning with a speed of millions of variables per
second \cite{dimmwitted}. 
Weaponed with this, we use general factor graphs to
do learning and inference on word lattices, which is able to integrate different kinds
of knowledge including syntactic, semantic, context and higher-level
knowledge.

Specifically, this paper tries to answer following questions:

1. How to jointly integrate different levels of knowledge in speech recognition?
2. Is it possible to have a real-time decoding system that approach oracle error rate of word lattices?
3. How to engineer the high-level features for language models 
   in real-time ASR applications within current technology?


Previous Works
----

Previous works on integrating knowledge into speech recognition include different models: HMMs \cite{bahl1983maximum}, Segmental CRFs \cite{zweig2010scarf}, and Deep Neural Networks \cite{dahl2012context, hinton2012deep}. Most works separate acoustic and language models, and it is hard for those works that focus on acoustic models to integrate higher-level language than lexicons. Most previous works on advanced decoding try to combine acoustic and language models by rescoring, without a rigorous probabilistic framework. 

SCARF \cite{zweig2010scarf} is a platform that utilizes segmental conditional random fields. It provides a framework for developers to add their own linguistic features. However, the scalability of SCARF is questionable while it does not claim to be able to do real-time speech recognition. 


<!-- **TODO Haowen:** advanced search (decoding): lecture 4 slides, related papers? (optional) -->

<!-- We want to conduct joint inference on acoustic and language models in decoding, taking acoustic model as a feature on lattices and integrate it into a rigorous probabilistic framework. -->



Our approach
----

We propose a decoding system based on word-level Conditional Random Fields (CRFs) that is able to integrate various linguistic and domain-specific features. 

CRFs are a type of general factor graphs. In our factor graph model, each **variable** is a word candidate in the lattice, and each **factor** is a feature or a domain-specific rule.

\begin{figure}[t]
\centering
\includegraphics[width=0.45\textwidth]{img/factor-graph.eps}
\caption{A Sample Factor Graph in DeepSpeech CRF Model}
\label{fig:fg}
\end{figure}

An example factor graph is shown in Figure \ref{fig:fg}. In this example, "was returned to us" and "was return to ice" are two different paths in the lattice. Each word in the lattice corresponds to a variable (shown as circles), and different factors might connect to them (shown as rectangles).

We obtain labels for variable-level training data by *distant supervision*: we match each lattice with its corresponding transcript, find all best paths in the lattice, and label all words on the best paths that matches a word in the transcript as *true*, other words as *false*.

As shown in Figure \ref{fig:fg}, the features we present in our system are such as:
(1) word N-gram frequency;
(2) bag of word N-grams (each N-gram itself is a feature);
(3) a second "confirmatory" decoding made with an independent speech recognizer (which comes with the lattice data);
(4) words around silence, etc.

DeepSpeech also enables developers to plug in more complicated features such as dependency paths, co-references, speaker-specific and contextual features.

Results
----
We got WER 10.2% on 152,251 broadcast news lattices with a simple feature set. (baseline 22.9%, oracle 2.1%) We finished training and testing in 70 minutes while the whole corpus is 400 hours, which indicates that our approach can be developed into a system that performs real-time decoding.

System
----

We propose to release *DeepSpeech* system \footnote{Currently available at: \url{https://github.com/zifeishan/cs224s-deepSpeech/}} as an open-source platform for advanced decoding with flexible knowledge integration. Developers will be able to plug in their own extractors and apply the system to their own datasets. The system is built on a scalable inference engine *DeepDive* \cite{deepdive}. 

Using DeepSpeech provides following benefits: (1) easy extraction and integration of linguistic features; (2) simpler feature engineering loops; (3) a rigorous probabilistic framework.

