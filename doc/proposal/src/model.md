# Proposed Model

## Feature Engineering

The first step is extracting useful features from datasets.
We will propose a taxonomy of knowledge that might help attributing authorship, which might include:

<!-- % TODO anything missed here? -->

1. **Corpus statistics:** frequent and surprising words, K-grams, and sentences.
2. **Shallow NLP features:** distribution of POS tags, NER tags, etc.
3. **Deep NLP features:** parse tree structure, frequent dependency paths, etc
4. **Knowledge base:** entities and relations in the article; what kinds of relations are the author supporting or attacking.
5. **Domain-specific features:** 
	- article structure and flow organization, citation patterns, tables and figures, order of authors, author affiliations, etc.
	- *Non-double-blind features:* features that are not applicable in double-blind review process, e.g. explicit self-citations (``our work'', etc).


With a knowledge taxonomy, we will extract features from our datasets. Extracting features will blow up the size of data.

We propose to conduct experiments to engineer useful features. This study might cast insight to authorship attribution as well as general knowledge-driven applications.

## Supervised Classification

With extracted features, we propose to train several kinds of state-of-the-art supervised classifiers, e.g. Logistic Regression and SVM.

However, traditional supervised classification is not expressive enough to capture some of the available knowledge. For example, 

TODO: Examples that joint inference help; motivation for next subsection

## Probabilistic Joint Inference

<!-- % Extract NLP features. This will blow up the data. Next, we'll do feature Engineering and train a supervised classifier, Logistic Regression or SVM. We then want to compare the performance of the model to a probabilistic joint inference model. 
% Why do we expect joint inference to help here?
 -->