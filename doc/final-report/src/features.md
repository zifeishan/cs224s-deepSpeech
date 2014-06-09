<!-- 

Features
====
\label{sec:algo}


After initial feature engineering, our current system implements following features:

1. Unigram and bigram frequency in Google Ngram.
2. All bigrams around "silence"
3. POS tag 2gram and 3gram
4. Candidates that overlap in time cannot be both true
5. Candidates on a same path should be true at same time



    features combination                             accuracy        
    ------------------------------------------      -----------      
    google unigram frequency                             
    google bigram frequency  


    range(1,193) (without delta)                      41.82%       
    MFCC only                              48.48%       
    [7,10,174,183,186,190] (energy and f0 basics)    40.61%       
    max,min,amean,linregc1, stddev only          47.27%
    forward search (with 191 features)           49.10%                       
    forward search (with the top 165 features)       56.97% 

-->