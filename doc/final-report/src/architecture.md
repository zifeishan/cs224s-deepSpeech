Architecture of DeepSpeech
====
\label{sec:archi}

We develop an end-to-end working system, DeepSpeech, which implements our data model. The system takes word lattice as input, performs user-defined feature extraction, factor graph generation, statistical learning and inference, and outputs the best path.

*DeepSpeech* is based on *DeepDive* \cite{deepdive}, a scalable inference engine that facilitates feature extraction and generates factor graphs by a descriptive language. *DeepDive* has a high-throughput Gibbs sampler DimmWitted \cite{dimmwitted}, which learns and samples at a speed of about 10 million variables per second on a laptop for our task.

The system architecture is demonstrated in Figure \ref{fig:archi}. We walk through each step of this data flow in this section.

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

## Data Flow

### Data preprocessing

In this step, DeepSpeech takes input data (lattices in raw format), runs preprocessing scripts on the data and loads them into a database. It also loads other data needed by the system, including transcripts for training, Google Ngram statistics, etc. 

<!-- The end product of this step is a set of database relations including lattices, transcripts, etc. -->

### Feature Extraction

In this step, DeepSpeech extracts linguistic features by running "extractors" written by developers. Extractors are functionalities provided by DeepDive.

<!-- The end product of this step is another set of database relations that contains various features for different word candidates. -->

### Factor Graph Generation

In the next step, DeepDive generates a factor graph. To tell the system how to generate it, developers use a SQL-like declarative language to specify *inference rules*, similar to Markov logic \cite{markovlogic}. In inference rules, one can write first-order logic rules with **weights**, which intuitively model our confidence in a rule.

<!-- The end product is a factor graph. -->

### Statistical Inference and Learning

This step is automatically performed by DeepDive on the generated factor graph. In learning, the values of weights specified in inference rules are calculated. In inference, marginal probabilities of variables are computed.

<!-- The end product is a weight table for all factors, as well as marginal probabilities for all candidate words. -->

### Finding Best Path

After inference, DeepSpeech performs a search for a best path that optimizes the edit distance, with the algorithm discussed in Section \ref{sec:bestpath}. The system then outputs the best path it finds.




## DeepSpeech Features

Our DeepSpeech system provides following benefits, compared to other systems like SCARF \cite{zweig2010scarf}.

### Easy Extraction and Integration of linguistic features

DeepSpeech provides a framework for developers to extract and integrate high-level features by writing MapReduce-like functions in SQL and python. This functionality is provided by DeepDive's feature extraction and factor graph generation frameworks.

<!-- 
For example, if developers want to add a co-reference feature, they can simply write an "extractor" in DeepSpeech, by: (1) write an input SQL query to generate all pairs of candidate words that appear in the same lattice; (2) write a python function that pairs 
.......

For example, if developers want to plug-in a co-reference feature, they can simply write an "extractor" in DeepSpeech, by specifying an input SQL query and a python user-defined-function (UDF). Here are some pseudo code for this example:

**Input SQL:** define a SQL query to generate all pairs of candidate words that appear in the same lattice, and pair it with a python function.

    SELECT t0.CID, t0.TEXT,
           t1.CID, t1.TEXT
    FROM   candidate t0,
           candidate t1
    WHERE  t0.LID = t1.LID
    USEPYTHON pyfunc

**Python UDF:** write a Python function to process all phrase pairs and identify coreferent pairs, in a MapReduce-like manner.

    def pyfunc(c1, t1, c2, t2):
        if edit_dist(t1, t2) < 2:
            emit(“Coref”, c1, c2)

-->


### Simpler Feature Engineering

Powered by DeepDive, DeepSpeech enables developers to conduct
systematic feature engineering iteratively. Same as the "E3-loop"
demonstrated in \cite{brainwash}, developers go through Explore-
Extract-Evaluate loops to continuously improve the system: (1) explore
results and do error analysis, (2) improve extractors to get better
features, and (3) rerun the system to get new results.

### Rigorous Probabilistic Framework

Unlike traditional speech recognition systems that uses ad-hoc methods
to combine the scores given by a language model and an acoustic model,
DeepSpeech provides a rigorous probabilistic framework: every
probability it predicts has the strict probabilistic meaning, which is
"the likelihood of the word candidate to be in the actual word
sequence". The probabilities are well-calibrated, which means that it
is supported by data. With this probabilistic framework, finding the
best-path (or N-best paths) is straightforward.
