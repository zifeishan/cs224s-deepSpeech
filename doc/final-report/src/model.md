The Architecture of DeepSpeech
====
\label{sec:model}

Architecture: See Figure \ref{fig:archi}.

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

## Distant supervision to obtain training data

We use distant supervision techniques to get training labels on candidate level: given a lattice and its transcript, we:

1. Find optimal paths in the lattice that matches the transcript with Dynamic Programming
2. Label all matched words in all optimal paths as true, others as false

See Figure \ref{fig:supervision}

\begin{figure}[t]
\centering
\includegraphics[width=0.45\textwidth]{img/supervision.pdf}
\caption{Distant Supervision}
\label{fig:supervision}
\end{figure}