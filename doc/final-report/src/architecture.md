Architecture of DeepSpeech
====
\label{sec:archi}

We develop a end-to-end working system DeepSpeech which implements our data model. The system takes word lattice as input, performs user-defined feature extraction, factor graph generation, statistical learning and inference, and outputs the best path.

*DeepSpeech* is based on *DeepDive*, a scalable inference engine that facilitates feature extraction and generates factor graphs by a descriptive language. *DeepDive* has a high-throughput Gibbs sampler DimmWitted \cite{dimmwitted}, which learns and samples at a speed of about 10 million variables per second on a laptop for our task.

**TODO cite** DeepDive and *DimmWhitted* 

The system architecture is demonstrated in Figure \ref{fig:archi}. We walk through each step in this section.

<!-- 
\begin{figure*}[t]
\centering
\subfigure[]{
    \includegraphics[width=0.45\textwidth]{img/system-action.png}
}
\subfigure[]{
    \includegraphics[width=0.45\textwidth]{img/system-action2.png}
}
\caption{Frontend Interface of Kaleidoscope System}
\label{fig:vis}
\end{figure*}
 -->

\begin{figure}[t]
\centering
\includegraphics[width=0.45\textwidth]{img/deepspeech-archi.pdf}
\caption{Architecture of DeepSpeech}
\label{fig:archi}
\end{figure}

## Data preprocessing

In this step, DeepSpeech takes input data (lattices in raw format), runs preprocessing scripts on the data and loads them into a database. It also loads other data needed by the system, including transcripts for training, Google Ngram statistics, etc. 

The end product of this step is a set of database relations including lattices, transcripts, etc.

## Feature Extraction

In this step, DeepSpeech extracts linguistic features by running "extractors" written by developers. Extractors are functionalities provided by DeepDive.

The end product of this step is another set of database relations that contains various features for different word candidates.

## Factor Graph Generation

In the next step, DeepDive generates a factor graph. To tell the system how to generate it, developers use a SQL-like declarative language to specify *inference rules*, similar to Markov logic \cite{markovlogic}. In inference rules, one can write first-order logic rules with **weights**, which intuitively model our confidence in a rule.

The end product is a factor graph.

## Statistical Inference and Learning

This step is automatically performed by DeepDive on the generated factor graph. In learning, the values of weights specified in inference rules are calculated. In inference, marginal probabilities of variables are computed.

The end product is a weight table for all factors, as well as marginal probabilities for all candidate words.

## Finding Best Path

After inference, DeepSpeech performs a search for a best path that optimizes edit distance, with the algorithm discussed in Section \ref{sec:bestpath}. The system then outputs the best path it finds.


