---
title: "Contextualized Query Embeddings for Conversational Search"
collection: "publications"
category: "conferences"
permalink: "/publication/2021-11-01-lin-2021-contextualized-query-embeddings-for-conversational-search"
excerpt: "This paper describes a compact and effective model for low-latency passage retrieval in conversational search based on learned dense representations. Prior to our work, the state-of-the-art approach uses a multi-stage pipeline comprising conversational query reformulation and information retrieval modules. Despite its effectiveness, such a pipeline often includes multiple neural models that require long inference times. In addition, independently optimizing each module ignores dependencies among them. To address these shortcomings, we propose to integrate conversational query reformulation directly into a dense retrieval model. To aid in this goal, we create a dataset with pseudo-relevance labels for conversational search to overcome the lack of training data and to explore different training strategies. We demonstrate that our model effectively rewrites conversational queries as dense representations in conversational search and open-domain question answering datasets. Finally, after observing that our model learns to adjust the L2 norm of query token embeddings, we leverage this property for hybrid retrieval and to support error analysis."
date: "2021-11-01"
venue: "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing"
paperurl: "https://aclanthology.org/2021.emnlp-main.77/"
citation: "Sheng-Chieh Lin, Jheng-Hong Yang, Jimmy Lin (2021). &quot;Contextualized Query Embeddings for Conversational Search.&quot; <i>Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing</i>."
bibtex_key: "lin-2021-contextualized-query-embeddings-for-conversational-search"
generated_from_bib: true
---

This publication page is generated from `bibliography/papers.bib`.
Edit the BibTeX entry and run `uv run python scripts/generate_publications.py` to update it.
