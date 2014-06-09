Evaluation
====
\label{sec:eval}

## Experimental Setup

### Features

After initial feature engineering, our current system implements following features: 

1. Unigram and bigram frequency in Google Ngram. (skip “silence”) 
2. All bigrams around “silence”
3. POS tag 2gram and 3gram
4. Candidates that overlap in time cannot be both true (a CRF rule that indicates constraint)
5. Candidates on a same path should be true at same time (a linear-chain CRF rule)

TODO: Next steps: co-reference features and candidate generation

### Datasets

We train and test on broadcast news lattices (LDC2011T06, 150k lattices). We holdout 50% of training set for testing.


## Results

We use SCLITE for scoring. We evaluate a baseline system (Attlia), DeepSpeech and lattice oracle (optimal) error rate.


Performance: DeepSpeech runs 70min for training and testing, while this dataset is ~400 hours of speech (real-time!)

\begin{table}[h]
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


## Feature Engineering

TODO show how good is each feature

