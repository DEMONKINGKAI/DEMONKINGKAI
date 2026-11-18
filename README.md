<div align="center">

<picture>
  <source media="(prefers-color-scheme: light)" srcset="https://www.gitskins.com/api/section/hero?username=demonkingkai&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F63913065%3Fu%3D1497b9cc0589a542f218f63c488d6220f474bfa0%26v%3D4&variant=living-identity&label=Kai&v=wow-living-identity-1&mode=light" />
  <img src="https://www.gitskins.com/api/section/hero?username=demonkingkai&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F63913065%3Fu%3D1497b9cc0589a542f218f63c488d6220f474bfa0%26v%3D4&variant=living-identity&label=Kai&v=wow-living-identity-1&mode=dark" width="100%" alt="Kai animated portrait and ASCII name" />
</picture>

<h3>I build AI that shows its work.</h3>
<p>MSc AI &amp; ML @ TU Darmstadt · causal inference · probabilistic models · grounded generative AI</p>

<a href="https://github.com/DEMONKINGKAI"><img src="https://img.shields.io/badge/GitHub-DEMONKINGKAI-181717?style=flat-square&logo=github" /></a>
<!-- TODO: replace with your real LinkedIn URL -->
<a href="https://www.linkedin.com/in/YOUR-HANDLE"><img src="https://img.shields.io/badge/LinkedIn-Archit%20Sharma-0A66C2?style=flat-square&logo=linkedin" /></a>
<img src="https://img.shields.io/badge/Based%20in-Darmstadt%2C%20DE-555?style=flat-square" />
<img src="https://img.shields.io/badge/Open%20to-Werkstudent%20%C2%B7%20ML%20roles-2ea44f?style=flat-square" />

</div>

<p align="center"><sub>✦ ───────────────────────────── ✦</sub></p>

Most models will confidently tell you something they can't back up. My work is about the opposite:
systems where **every claim, edge, or probability can be traced back to the evidence that produced it**,
and where I measure how often that actually holds.

Before my master's I was a Product Engineer at **EffiGO**, shipping generative-AI applications and MLOps
pipelines across GCP, AWS and Azure. Right now I'm working on **visual hallucinations in multimodal reasoning traces**
in the Multimodal AI Project Lab at TU Darmstadt.

<p align="center"><sub>✦ ───────────────────────────── ✦</sub></p>

<h2>What moves the work</h2>

<picture>
  <source media="(prefers-color-scheme: light)" srcset="https://www.gitskins.com/api/section/highlights?username=demonkingkai&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F63913065%3Fu%3D1497b9cc0589a542f218f63c488d6220f474bfa0%26v%3D4&items=Causal%20discovery%3A%3Apharmacausal%20%C2%B7%20422k%20FDA%20reports%7CGrounded%20RAG%3A%3Aad-fontes%20%C2%B7%20fons-iuris%7CExplainable%20PGMs%3A%3Aevidentia%20%C2%B7%20895-node%20BN&variant=wow&v=wow-highlights-2&mode=light" />
  <img src="https://www.gitskins.com/api/section/highlights?username=demonkingkai&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F63913065%3Fu%3D1497b9cc0589a542f218f63c488d6220f474bfa0%26v%3D4&items=Causal%20discovery%3A%3Apharmacausal%20%C2%B7%20422k%20FDA%20reports%7CGrounded%20RAG%3A%3Aad-fontes%20%C2%B7%20fons-iuris%7CExplainable%20PGMs%3A%3Aevidentia%20%C2%B7%20895-node%20BN&variant=wow&v=wow-highlights-2&mode=dark" width="100%" alt="Focus areas: causal discovery, grounded RAG, explainable PGMs" />
</picture>

<p align="center"><sub>✦ ───────────────────────────── ✦</sub></p>

<h2>Built, shipped, shared</h2>

<picture>
  <source media="(prefers-color-scheme: light)" srcset="https://www.gitskins.com/api/section/projects?username=demonkingkai&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F63913065%3Fu%3D1497b9cc0589a542f218f63c488d6220f474bfa0%26v%3D4&repos=demonkingkai%2Fad-fontes%2Cdemonkingkai%2Fpharmacausal%2Cdemonkingkai%2Fevidentia%2Cdemonkingkai%2Ffons-iuris&variant=wow&v=wow-projects-2&mode=light" />
  <img src="https://www.gitskins.com/api/section/projects?username=demonkingkai&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F63913065%3Fu%3D1497b9cc0589a542f218f63c488d6220f474bfa0%26v%3D4&repos=demonkingkai%2Fad-fontes%2Cdemonkingkai%2Fpharmacausal%2Cdemonkingkai%2Fevidentia%2Cdemonkingkai%2Ffons-iuris&variant=wow&v=wow-projects-2&mode=dark" width="100%" alt="Project constellation" />
</picture>

### 🔎 [ad-fontes](https://github.com/DEMONKINGKAI/ad-fontes): a RAG assistant that isn't allowed to exaggerate
A recruiter-facing assistant about my own portfolio, built so it can't inflate claims about my work.
Each generated claim must cite a retrieved chunk, then passes three checks: **structural** (was the chunk retrieved?),
**NLI entailment** (does it support the claim?), and a **numeric guard** (do the numbers appear in the source?).
A small generator is then tuned with **DPO** to prefer faithful answers over fluent ones.

- Retrieval: **93.9% chunk-level hit@6** (MRR 0.74) on a 76-question eval set
- Base-model baseline: 44.7 unsupported claims per 100 answers, the number DPO is meant to bring down *(tuning in progress)*
- `Qwen2.5-1.5B` · `QLoRA` · `TRL` · `ChromaDB` · `FastAPI` · `Docker`

### 💊 [pharmacausal](https://github.com/DEMONKINGKAI/pharmacausal): causal discovery on 422k FDA adverse-event reports
Co-prescription correlations are confounded by comorbidities and prescribing patterns. This runs **PC** and **FCI**
causal discovery on FAERS, using tiered background knowledge so edges respect time order
(demographics → indication → drug → event), and validates drug → event edges against **SIDER**.

- Recovers known signals such as *rosuvastatin → myalgia* and *medroxyprogesterone → meningioma*
- FCI: 67% precision on SIDER-covered edges; assumption violations are documented, not hidden
- `causal-learn` · `pandas` · `pytest`

### 🩺 [evidentia](https://github.com/DEMONKINGKAI/evidentia): an explainable, calibrated diagnostic Bayesian network
Diagnostic tools are high-risk under the EU AI Act, which requires explainability. This is an **895-node Bayesian network**
symptom checker where every shift in diagnosis probability is attributed to the evidence that caused it.

- Evaluated on **134,529** held-out DDXPlus patients: **ECE 0.0036** vs 0.4243 for the dataset's reference differential
- Per-evidence attribution via sequential deltas and order-independent weight of evidence
- `Python` · `FastAPI` · `React` · `Cytoscape`

### ⚖️ [fons-iuris](https://github.com/DEMONKINGKAI/fons-iuris): GDPR & AI Act Q&A that cites the paragraph
LLMs make up article numbers when asked about EU regulation. This RAG system parses EUR-Lex, answers with citations to
specific provisions, and uses an **NLI verifier** to flag any claim its cited paragraph doesn't support.

- `FastAPI` · `Chroma` · `Transformers` · `React/Vite` · `Docker Compose`

<p align="center"><sub>✦ ───────────────────────────── ✦</sub></p>

<h2>The tools behind the work</h2>

<picture>
  <source media="(prefers-color-scheme: light)" srcset="https://www.gitskins.com/api/section/stack?username=demonkingkai&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F63913065%3Fu%3D1497b9cc0589a542f218f63c488d6220f474bfa0%26v%3D4&variant=wow&v=wow-stack-1&mode=light" />
  <img src="https://www.gitskins.com/api/section/stack?username=demonkingkai&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F63913065%3Fu%3D1497b9cc0589a542f218f63c488d6220f474bfa0%26v%3D4&variant=wow&v=wow-stack-1&mode=dark" width="100%" alt="Technology stack" />
</picture>

<p><b>Core ML:</b> causal discovery & inference · Bayesian networks / PGMs · RAG & claim verification · RLHF / DPO · multimodal models (CLIP fine-tuning, BLIP-2, LLaVA)</p>

<p align="center"><sub>✦ ───────────────────────────── ✦</sub></p>

<h2>Currently</h2>

- 🔬 Testing whether multimodal models' reasoning traces are *seeing* or *making things up* (TU Darmstadt project lab)
- 🎯 Running the DPO stage of **ad-fontes** and measuring base vs. tuned faithfulness
- 💼 Looking for **Werkstudent** roles in ML/AI (thesis-compatible) and full-time roles from 2027

<p align="center"><sub>✦ ───────────────────────────── ✦</sub></p>

<p align="center"><sub>Ad fontes: back to the sources.</sub></p>
