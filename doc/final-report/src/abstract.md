We develop a scalable decoding system *DeepSpeech*, which flexibly integrates different levels of knowledge to decode a word lattice in speech recognition within a word-level CRF model.

*DeepSpeech* facilitates feature extraction, factor graph generation, and statistical learning and inference. It takes word lattice as input, perform feature extraction specified by developers, generate factor graphs based on descriptive rules, and perform learning and inference automatically. *DeepSpeech* is based on the scalable statistical inference engine DeepDive (http://deepdive.stanford.edu).

We integrate N-gram based linguistic features as well as some domain specific features. We train and evaluate our system on a dataset of broadcast news lattices, and obtain WER of 10.2%, which beats the baseline (Attila system) by a large margin. We also study a larger set of linguistic features with *DeepSpeech* and report their impact.
