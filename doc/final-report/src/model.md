Model
====
\label{sec:model}

## Problem Definition

Our problem is decoding a word lattice into one-best path, which is
defined as follows: given an word lattice as input, which is a set of
possible word sequences, the system outputs a word sequence with
highest confidence.

## Word-level Factor Graphs

<!-- **TODO Haowen: study decoding approaches. e.g. Viterbi, etc** 
Different with most of previous works, -->

We model the decoding problem as a word-level factor graph (a CRF). 

**Input** to the system is a word lattice, which is a standard output by an acoustic speech recognition system.

**Output** of the system is a sequence of words (one-best path) for each lattice.

**Variables** are candidate words in the lattice. Among all variables, *query variables* are words in the test set, where we are not sure whether a candidate is correct or not; *evidence variables* are words in training set, where we can obtain true / false labels for each candidate word. After learning and inference, the system computes *marginal probabilities* for all query variables, which we will use to find the best path.

**Factors** are features or domain-specific rules that are related to candidate words. For example, the word bigram "of us" might have a feature indicating that it is a frequent bigram, where "of ice" might have a feature saying it is infrequent. Factors with different weights will be connected to the corresponding words. There might be more complex factors like constraints among conflicting candidates, chained candidates, coreferences, etc.

## Distant Supervision to Obtain Training Data

On the factor graph we have factors with different weights to be learned. To train the model we need labeled data for evidence variables. However, although we have the transcript for each lattice in training set, there is no word-level ground truth indicating whether each candidate word is correct or not. To get training labels on a candidate level, we develop a *distant supervision* \cite{mintz2009distant} metric to obtain labeled data in this setting.

Given a lattice and its transcript, we: (1) find all optimal paths in the lattice that matches the transcript with Dynamic Programming (DP), and (2) then label all matched words in all optimal paths as true, others as false.

In the distant supervision metric, we maximize the **number of matched words** on a path inside the lattice with the transcript. An alternative would be minimizing edit distance. The difference between these different objective functions are not studied here.

The distant supervision method is demonstrated in Figure \ref{fig:supervision}. Specifically, in this lattice, both "WAS RETURN TO US ~SIL" and "WAS RETURNED TO ICE ~SIL" is a best path matching the transcript "WAS RETURNED TO US ~SIL", since both of them have 4 matches. 

\begin{figure}[t]
\centering
\includegraphics[width=0.45\textwidth]{img/supervision.pdf}
\caption{Distant Supervision}
\label{fig:supervision}
\end{figure}


As for the DP algorithm, for each candidate in the lattice, we store the maximum numbers of matches with the transcript *up to each position in the transcript*. Denoting the number of candidates in lattice as $N$ and number of words in transcript as $M$, then each candidate $i$ memorizes a vector with length $M$, denoted as $f[i][j]$. The DP function is as below:

<!-- **TODO tianxin**: DP formula -->

<!-- \begin{multline} --> 
\begin{equation*}
\begin{split}
   f[i,j] =   \max\limits_{i' : i' is predecessor of i} &\{f[i', j-1] + 1\{lattice[i] = transcript[j]\} , \\
   & f[i',j] ,\\
   & f[i,j-1] \\
   \}  
\end{split}
\end{equation*}
<!-- \end{multline} -->

<!-- **TODO Cite SCLITE edit distance** -->

## Statistical Learning and Inference

After getting the factor graph with evidence, we perform statistical learning and inference. There are two steps in this procedure:
(1) **learning:** performs *gradient descent* to calculate the values of weights for different factors.
(2) **inference:** performs *gibbs sampling* to calculate the marginal probabilities of query variables. \cite{zhang2013towards}

## Finding Best Path on Factor Graphs
\label{sec:bestpath}

After learning and inference, each candidate word on the lattice gets
a probability of being correct. Therefore the "best path" is well
defined there: we want to find a path that minimizes the edit distance
with the actual word sequence.

Here we formalize this problem:
there exists an actual word sequence $C^*=\{a_1, a_2, ..., a_n\}$. 
Given an arbitrary path in the lattice $C=\{c_1, c_2, ..., c_n\}$, 
we have probabilities for each candidate to appear in the actual word sequence: $p_1, p_2, ..., p_n$.
We want to minimize the edit distance of $C$ and $C^*$, denoted as $Dist(C, C^*)$.

\begin{figure}[t]
\centering
\includegraphics[width=0.3\textwidth]{img/bestpath.eps}
\caption{Finding Best Path with Inference Results}
\label{fig:bestpath}
\end{figure}

<!-- Note that the sum of all probabilities on a path, $E=\sum{p_i}$, is the *expected* number of words in this path that appear in the actual word sequence. A simplest strategy is to find a path with highest $E$. However, this strategy is not minimizing edit distance...
   ...while optimizing $E$ neglects the punishment of wrong insertions.
 -->


We want to minimize *edit distance*, which is the total number of insertions, deletions and substitutions. Consider a case in Figure \ref{fig:bestpath}, where there exists two paths $P1$ (with nodes SABCT) and $P2$ (with nodes SDT) in the lattice. Selecting $P1$ would suffer from an *expected number of insertions or substitutions* of 0.6, where each of A, B and C contributes $1-0.8=0.2$. Similarly, selecting $P2$ only gives 0.1 expectation of insertion or substitution. 

Let's look at *expected deletions*. Selecting $P1$ means not selecting node $D$, which gives expected number of deletions to be 0.9 (since D has the probability 0.9 to appear in actual sequence). Similarly, selecting $P2$ means not selecting A, B or C, which gives $0.8*3=2.4$ expected deletions.

In this way we can develop a dynamic programming metric to optimize edit distance. Equivalent to the above problem, we can add a punishment of -0.5 to each candidate: $p'_i = p_i - 0.5$, and select a path that optimizes $\sum_i{p'_i}$.

<!-- **TODO: cite one-best path algorithms** -->


