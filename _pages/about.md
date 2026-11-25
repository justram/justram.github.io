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

I'm Jheng-Hong (Matt) Yang. I work on search agents: how they find evidence, and how we tell whether they found what matters. At Mixedbread I built the reinforcement learning environment our team used to train [Toast 1](https://www.mixedbread.com/blog/toast-1). Now I'm exploring what agents need to remember when they return to a task. We built pi-link around one example: a rule an agent should still follow the next time it touches someone else's work.

<details markdown="1">
<summary>Read more about the agents I build and test</summary>

One decision worth remembering is a working rule. Take an agent sharing a repository with someone else: it should stage the files it changed, not everything in the directory. When we built pi-link, we made that rule something we could check against the agent's actual tool call. A written instruction tells us what the agent should do; the call tells us what it did.

Search raises a similar question. A plausible answer doesn't tell you whether the agent found useful evidence along the way. My work on how language models search, inspect evidence, and reason led to <a href="https://github.com/justram/pi-serini"><span class="small-caps">Pi-Serini</span></a>, a minimal search agent for building reliable deep-research workflows without letting costs run away.

At Mixedbread, I worked on both sides of that distinction as a Member of Technical Staff. I designed and built the environment we trained Toast 1 in. I also handled evaluation and improved the harness, the software that runs the agent. I left Mixedbread at the end of October.

I came to agents through information retrieval. During my doctoral research in computer science at the University of Waterloo in Canada, I studied neural ranking, conversational search, and multimodal retrieval. Before Waterloo, I researched recommender systems and data-driven modeling at Academia Sinica. I started out in physics and electronics engineering: after my B.S. in Electrophysics and M.Sc. in Electronics Engineering at National Chiao Tung University, I modeled semiconductor devices in TSMC R&D.

</details>

If you're building a search agent or deciding how to evaluate one, I'd be glad to compare notes. For consulting or collaboration, email me at [jhyang@stencilzeit.com](mailto:jhyang@stencilzeit.com).
