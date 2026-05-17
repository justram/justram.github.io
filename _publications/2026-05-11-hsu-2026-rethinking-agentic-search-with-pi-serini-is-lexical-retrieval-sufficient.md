---
title: "Rethinking Agentic Search with Pi-Serini: Is Lexical Retrieval Sufficient?"
collection: "publications"
category: "manuscripts"
permalink: "/publication/2026-05-11-hsu-2026-rethinking-agentic-search-with-pi-serini-is-lexical-retrieval-sufficient"
excerpt: "Does a lexical retriever suffice as large language models (LLMs) become more capable in an agentic loop? This question naturally arises when building deep research systems. We revisit it by pairing BM25 with frontier LLMs that have better reasoning and tool-use abilities. To support researchers asking the same question, we introduce Pi-Serini, a search agent equipped with three tools for retrieving, browsing, and reading documents. Our results show that, on BrowseComp-Plus, a well-configured lexical retriever with sufficient retrieval depth can support effective deep research when paired with more capable LLMs. Specifically, Pi-Serini with gpt-5.5 achieves 83.1% answer accuracy and 94.7% surfaced evidence recall, outperforming released search agents that use dense retrievers. Controlled ablations further show that BM25 tuning improves answer accuracy by 18.0% and surfaced evidence recall by 11.1% over the default BM25 setting, while increasing retrieval depth further improves surfaced evidence recall by 25.3% over the shallow-retrieval setting."
date: "2026-05-11"
venue: "arXiv preprint arXiv:2605.10848"
authors: "Tz-Huan Hsu, Jheng-Hong Yang, Jimmy Lin"
authors_html: "Tz-Huan Hsu, <strong>Jheng-Hong Yang</strong>, Jimmy Lin"
paperurl: "https://arxiv.org/abs/2605.10848"
citation: "Tz-Huan Hsu, Jheng-Hong Yang, Jimmy Lin (2026). &quot;Rethinking Agentic Search with Pi-Serini: Is Lexical Retrieval Sufficient?.&quot; <i>arXiv preprint arXiv:2605.10848</i>."
bibtex_key: "hsu-2026-rethinking-agentic-search-with-pi-serini-is-lexical-retrieval-sufficient"
generated_from_bib: true
---

This publication page is generated from `bibliography/papers.bib`.
Edit the BibTeX entry and run `uv run python scripts/generate_publications.py` to update it.
