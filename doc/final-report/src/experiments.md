Experiments
====
\label{sec:experiments}

In this section, we report initial experiments we conduct using DeepSpeech. We train and evaluate the system on a large-scale dataset, and compare the results with a baseline system and oracle (lattice optimal) error rate. We further look into the impact of different features.


## System Evaluation


### Datasets

We train and test on broadcast news lattices (LDC2011T06, 152,251 lattices). We holdout 50% of training set for testing.

The oracle error rate (lattice optimal WER) is 2.1% on this dataset. Our baseline is the one-best word detections from the Attila system, provided by LDC2011T06 dataset.

### Features

After initial feature engineering, we use following features: 

1. The "confirmatory" decoding made with an independent speech recognizer

2. Unigram and bigram frequency in Google Ngram: For each candidate word N-gram, we take its frequency (log-scale) in Google Ngram dataset as a feature that indicates whether it is a valid word / phrase. We skip disfluencies such as "um", "uh" and silence in this feature.

3. Bag of word bigrams. Each bag of bigrams itself is a different feature (e.g. "we are", "but uh"). This is a very sparse feature, but with the large dataset and proper regularization, it performs well.

4. All words around silence. We take the bigram of a word and a silence in speech, to capture what words are likely to come before or after a silence.


### Results

We use the standard tool SCLITE for scoring. We evaluate our system, a baseline system (Attila), and lattice oracle (optimal) word error rate. The word error rate includes substitutions, deletions and insertions.

The results are shown in Table \ref{table:results}.

\begin{table}[h]
\label{table:results}
\centering
\begin{tabular}{lllllll}
\hline
System     & Corr & Sub & Del  & Ins & Err  & S.Err \\
\hline
Baseline   & 77.8 & 5.4 & 16.8 & 0.6 & 22.9 & 96.9  \\
DeepSpeech & 92   & 3.6 & 4.3  & 2.2 & 10.2 & 75.7  \\
Oracle     & 99.9 & 0   & 0.1  & 2   & 2.1  & 50.8 \\
\hline
\end{tabular}
\caption{Experiment Results}
\end{table}

About performance: DeepSpeech runs 70 minutes for training and testing, while this dataset is about 400 hours of speech. This indicates that DeepSpeech can potentially make a real-time decoding system that integrates high level knowledge "for free".



## Feature Exploration

In this section, we enumerate a larger set of different features we implement in DeepDive, and test on each feature's impact.

For dataset, we use a subsample of the broadcast lattice dataset. We only takes 1,000 lattices (speeches) and split them half-half for training and testing.

### List of features

Features we implement are listed below. Some are discussed in the above section while some are newly introduced. Some of these features are also shown in Figure \ref{fig:fg}.

1. (*Ngram-freq*) Google Ngram frequency (N=1,2,...)

3. (*confirm*) The "confirmatory" decoding made with an independent speech recognizer, provided by LDC dataset

4. (*start-end*) Start and end marks of sentence (`<s>` and `</s>`): each sentence is starting and ending with a special mark. We add a factor to a candidate word if it is this special mark.

5. (*Ngram-bag*) Bag of word N-grams. Each bag of N-grams itself is a different feature. (N=1,2)

6. (*Ngram-stopword*) Any N-gram containing a stop-word (stopwords include silence). (N=2,3)

7. (*Ngram-silence*) All words around silence, which is the N-gram containing a `~SIL` mark. (we can see that $7 \in 6 \in 5$) (N=2)

8. (*conflict*) Conflict constraint. This is a CRF rule that adds a factor to connect two variables: candidates that overlap in time cannot be both true.

9. (*chain*) Chaining candidates on same paths. This is a linear-chain CRF rule: candidates on a same path should be true at same time.

10. (*pos-Ngram*) POS N-gram and trigram. This rule takes all N-grams and trigrams of candidate as a feature. POS tags are tagged for each word independently with a one-best tagger, without sentence structure. (N=2,3,5)


### Experiments Protocol

We increment features and observe impact for each feature.

We start from unigram frequency;then add bigram frequency and trigram frequency. Then we try using *only* the "confirm" feature, adding start-end feature onto it, adding unigrams and bigrams, then adding bigram-silence, bigram-stopword, and bigram-bag (features get more and more sparse). We further add conflict rule and "chain" rule; at last add larger language models like bags of word 1grams, POS 5grams, and stop word 3grams.

### Experiment results

We report the observed word error rate (WER) and sentence error rate (SER) in Figure \ref{fig:features}.

\begin{figure}[t]
\centering
\includegraphics[width=0.45\textwidth]{img/feature-explore-chart.pdf}
\caption{Feature Exploration Results}
\label{fig:features}
\end{figure}

Specifically, we take the following lessons:

(1) Unigram frequency itself does not work, since most ASR softwares tries to give valid words in dictionary.

(2) 1/2/3gram frequency feature is not as good as the "confirm" feature alone. This indicates that a weak language model is not as competitive as a good second-confirmatory system (ensemble wins).

(3) Sparse bag-of-Ngram feature helps. By adding the features *bigram-silence*, *bigram-stopword* and *bigram-bag* incrementally, we observe continuous decrease in WER (11.3, 10.8, 10.1). It indicates that our system is able to make reasonable regularization and handle sparsity well.

(4) The "conflict" constraint decreases WER, but increases SER; while the "chain" constraint increases WER, but decreases SER.

(5) The larger language model we feed DeepSpeech, the better result it gets. When we feed stopword 3gram and POS 5gram, it gets WER of only 9.1%.


<!-- POS Ngram feature does not help much. However this might be because that we only use single-word one-best tagger. If we find a way to tag in sentences we might observe a better result. -->
