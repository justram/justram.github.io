---
layout: home-compact
permalink: /zh-tw/
lang: zh-TW
locale: zh_TW
title: 關於我
excerpt: 你好，我是 Matt。
author_profile: false
footnotes:
  - "我在 2026 年 10 月底離職。"
  - "我原本學的是物理與電子工程。在國立交通大學取得電子物理學士及電子工程碩士學位後，我到台積電做半導體元件建模的研發工作。後來我在中央研究院研究推薦系統與資料驅動建模，再到加拿大滑鐵盧大學做電腦科學博士研究，探討怎麼用神經網路排序檢索結果，也研究多模態檢索與對話式搜尋。"
---

我是楊政紘（Jheng-Hong "Matt" Yang）。做 <a href="https://github.com/justram/pi-serini"><span class="small-caps">Pi-Serini</span></a> 時，我想試試看：先讓搜尋代理讀五段摘錄，但把整份排序結果留著。這樣一來，代理不用重新搜尋，就能回到同一份清單往下看。哪篇值得打開來讀？我想把這個決定留給代理，而不是事先替它訂好規則。

<details markdown="1">
<summary>從代理怎麼找資料，可以看出什麼？</summary>

代理漏掉一篇有用的文件，不一定是搜尋沒找到。文件也許就在清單裡，只是代理沒往下看到那一筆。把查詢、排序結果、代理看過的摘錄和打開過的文件對照起來，就能分清楚它在哪一步錯過了線索。代理越有能力，我越希望這層介面保持簡單，讓它自己決定下一步怎麼找。

這也讓我想到訓練。如果清單裡已經有值得追的線索，代理卻一再從頭搜尋，那麼該學著改變的，就是這個選擇。我在 Mixedbread 擔任 <span lang="en">Member of Technical Staff</span><sup><a id="ref-1" href="#note-1" role="doc-noteref" aria-label="註 1">1</a></sup> 時，設計並建置了一套強化學習環境，我們用它訓練了 [Toast 1](https://www.mixedbread.com/blog/toast-1)。我也負責評測，並改進了執行代理的程式（<span lang="en">harness</span>）。

現在想起那份搜尋紀錄，我關心的是記憶。我可以回頭讀紀錄，弄清楚上次怎麼走到那一步。那麼對代理自己來說，一次搜尋的經驗可以用多簡單的形式留下來，讓它下次回頭找得到，也用得上？

想到這裡，我就想起在中央研究院時<sup><a id="ref-2" href="#note-2" role="doc-noteref" aria-label="註 2">2</a></sup>，我們在 [2019 年一篇談對話式搜尋的論文](https://cs.uwaterloo.ca/~jimmylin/publications/YangJH_etal_TREC2019.pdf)裡試過的做法。遇到新問題，不必每次都從頭找；先前的問答也能幫我們決定下一次要怎麼查。Pi-Serini 留下的是另一種線索：上次搜尋的排序清單。代理可以回去接著往下讀，不必再查一次。

</details>

如果你正在做搜尋代理，或在想該怎麼評測它，歡迎找我交換想法。想談顧問服務或合作，可以來信：[jhyang@stencilzeit.com](mailto:jhyang@stencilzeit.com)。
