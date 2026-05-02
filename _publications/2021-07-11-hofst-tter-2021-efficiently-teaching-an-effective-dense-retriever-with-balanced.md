---
title: "Efficiently Teaching an Effective Dense Retriever with Balanced Topic-Aware Sampling"
collection: "publications"
category: "conferences"
permalink: "/publication/2021-07-11-hofst-tter-2021-efficiently-teaching-an-effective-dense-retriever-with-balanced"
excerpt: "A vital step towards the widespread adoption of neural retrieval models is their resource efficiency throughout the training, indexing and query workflows. The neural IR community made great advancements in training effective dual-encoder dense retrieval (DR) models recently. A dense text retrieval model uses a single vector representation per query and passage to score a match, which enables low-latency first-stage retrieval with a nearest neighbor search. Increasingly common, training approaches require enormous compute power, as they either conduct negative passage sampling out of a continuously updating refreshing index or require very large batch sizes. Instead of relying on more compute capability, we introduce an efficient topic-aware query and balanced margin sampling technique, called TAS-Balanced. We cluster queries once before training and sample queries out of a cluster per batch. We train …"
date: "2021-07-11"
venue: "Proceedings of the 44th international ACM SIGIR conference on research and development in information retrieval"
paperurl: "https://dl.acm.org/doi/abs/10.1145/3404835.3462891"
citation: "Sebastian Hofstätter, Sheng-Chieh Lin, Jheng-Hong Yang, Jimmy Lin, Allan Hanbury (2021). &quot;Efficiently Teaching an Effective Dense Retriever with Balanced Topic-Aware Sampling.&quot; <i>Proceedings of the 44th international ACM SIGIR conference on research and development in information retrieval</i>."
bibtex_key: "hofst-tter-2021-efficiently-teaching-an-effective-dense-retriever-with-balanced"
generated_from_bib: true
---

This publication page is generated from `bibliography/papers.bib`.
Edit the BibTeX entry and run `uv run python scripts/generate_publications.py` to update it.
