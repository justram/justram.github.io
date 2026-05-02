---
title: "In-Batch Negatives for Knowledge Distillation with Tightly-Coupled Teachers for Dense Retrieval"
collection: "publications"
category: "conferences"
permalink: "/publication/2021-08-01-lin-2021-in-batch-negatives-for-knowledge-distillation-with-tightly-coupled-teac"
excerpt: "We present an efficient training approach to text retrieval with dense representations that applies knowledge distillation using the ColBERT late-interaction ranking model. Specifically, we propose to transfer the knowledge from a bi-encoder teacher to a student by distilling knowledge from ColBERT’s expressive MaxSim operator into a simple dot product. The advantage of the bi-encoder teacher–student setup is that we can efficiently add in-batch negatives during knowledge distillation, enabling richer interactions between teacher and student models. In addition, using ColBERT as the teacher reduces training cost compared to a full cross-encoder. Experiments on the MS MARCO passage and document ranking tasks and data from the TREC 2019 Deep Learning Track demonstrate that our approach helps models learn robust representations for dense retrieval effectively and efficiently."
date: "2021-08-01"
venue: "Proceedings of the 6th Workshop on Representation Learning for NLP (RepL4NLP-2021)"
authors: "Sheng-Chieh Lin, Jheng-Hong Yang, Jimmy Lin"
authors_html: "Sheng-Chieh Lin, <strong>Jheng-Hong Yang</strong>, Jimmy Lin"
paperurl: "https://aclanthology.org/2021.repl4nlp-1.17/"
citation: "Sheng-Chieh Lin, Jheng-Hong Yang, Jimmy Lin (2021). &quot;In-Batch Negatives for Knowledge Distillation with Tightly-Coupled Teachers for Dense Retrieval.&quot; <i>Proceedings of the 6th Workshop on Representation Learning for NLP (RepL4NLP-2021)</i>."
bibtex_key: "lin-2021-in-batch-negatives-for-knowledge-distillation-with-tightly-coupled-teac"
generated_from_bib: true
---

This publication page is generated from `bibliography/papers.bib`.
Edit the BibTeX entry and run `uv run python scripts/generate_publications.py` to update it.
