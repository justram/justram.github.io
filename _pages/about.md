---
layout: home-compact
permalink: /
title: "About Me"
excerpt: "Hello!"
author_profile: false
redirect_from: 
  - /about/
  - /about.html
---

I'm Jheng-Hong (Matt) Yang. I built <a href="https://github.com/justram/pi-serini"><span class="small-caps">Pi-Serini</span></a> around a choice: show a search agent five excerpts, but keep the whole ranking within reach. The agent can go back to that list without searching again and decide which document is worth opening. I wanted to see what it would find if I left that decision to the agent.

<details markdown="1">
<summary>What can we learn from those choices?</summary>

When an agent misses a useful document, I want to know where it lost the trail. Was the document missing from the ranking, or did the agent never look far enough down the list? I can tell those cases apart by comparing the ranking with the excerpts the agent saw and the documents it opened. As agents grow more capable, I'd rather keep that interface simple than write more rules about where to look.

Those choices also give me a way to think about training. If an agent keeps searching from scratch when a promising result is already on its list, that's a behavior we could teach it to change. At Mixedbread, I worked on agent training as a Member of Technical Staff. I designed and built the reinforcement learning environment our team used to train [Toast 1](https://www.mixedbread.com/blog/toast-1). I handled evaluation and improved the agent's harness, the software that runs it. I left at the end of October.

I keep coming back to that search record. It's useful to me when I look back over a run. What's the simplest piece of that experience the agent itself could return to and use?

I came to agents through information retrieval. During my doctoral research in computer science at the University of Waterloo in Canada, I studied neural ranking, conversational search, and multimodal retrieval. Before Waterloo, I researched recommender systems and data-driven modeling at Academia Sinica. I started out in physics and electronics engineering: after my B.S. in Electrophysics and M.Sc. in Electronics Engineering at National Chiao Tung University, I modeled semiconductor devices in TSMC R&D.

</details>

If you're building a search agent or deciding how to evaluate one, I'd be glad to compare notes. For consulting or collaboration, email me at [jhyang@stencilzeit.com](mailto:jhyang@stencilzeit.com).
