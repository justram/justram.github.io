---
title: "Distilling Dense Representations for Ranking Using Tightly-Coupled Teachers"
collection: "publications"
category: "manuscripts"
permalink: "/publication/2020-10-22-lin-2020-distilling-dense-representations-for-ranking-using-tightly-coupled-teac"
excerpt: "We present an approach to ranking with dense representations that applies knowledge distillation to improve the recently proposed late-interaction ColBERT model. Specifically, we distill the knowledge from ColBERT's expressive MaxSim operator for computing relevance scores into a simple dot product, thus enabling single-step ANN search. Our key insight is that during distillation, tight coupling between the teacher model and the student model enables more flexible distillation strategies and yields better learned representations. We empirically show that our approach improves query latency and greatly reduces the onerous storage requirements of ColBERT, while only making modest sacrifices in terms of effectiveness. By combining our dense representations with sparse representations derived from document expansion, we are able to approach the effectiveness of a standard cross-encoder reranker using BERT that is orders of magnitude slower."
date: "2020-10-22"
venue: "arXiv preprint arXiv:2010.11386"
paperurl: "https://arxiv.org/abs/2010.11386"
citation: "Sheng-Chieh Lin, Jheng-Hong Yang, Jimmy Lin (2020). &quot;Distilling Dense Representations for Ranking Using Tightly-Coupled Teachers.&quot; <i>arXiv preprint arXiv:2010.11386</i>."
bibtex_key: "lin-2020-distilling-dense-representations-for-ranking-using-tightly-coupled-teac"
generated_from_bib: true
---

This publication page is generated from `bibliography/papers.bib`.
Edit the BibTeX entry and run `uv run python scripts/generate_publications.py` to update it.
