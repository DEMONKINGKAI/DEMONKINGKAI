<h1 align="center">Kai (Archit Sharma)</h1>

<p align="center">
  <b>I build AI that shows its work.</b><br/>
  MSc AI & ML @ TU Darmstadt · causal inference · probabilistic models · grounded generative AI
</p>

<p align="center">
  <a href="https://github.com/DEMONKINGKAI"><img src="https://img.shields.io/badge/GitHub-DEMONKINGKAI-181717?style=flat-square&logo=github" /></a>
  <!-- TODO: replace with your real LinkedIn URL -->
  <a href="https://www.linkedin.com/in/YOUR-HANDLE"><img src="https://img.shields.io/badge/LinkedIn-Archit%20Sharma-0A66C2?style=flat-square&logo=linkedin" /></a>
  <img src="https://img.shields.io/badge/Based%20in-Darmstadt%2C%20DE-555?style=flat-square" />
  <img src="https://img.shields.io/badge/Open%20to-Werkstudent%20%C2%B7%20ML%20roles-2ea44f?style=flat-square" />
</p>

---

Most models will confidently tell you something they can't back up. My work is about the opposite:
systems where **every claim, edge, or probability can be traced back to the evidence that produced it**,
and where I measure how often that actually holds.

Before my master's I was a Product Engineer at **EffiGO**, shipping generative-AI applications and MLOps
pipelines across GCP, AWS and Azure. Right now I'm working on **visual hallucinations in multimodal reasoning traces**
in the Multimodal AI Project Lab at TU Darmstadt.

## Featured work

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

## What I work with

**Core ML:** causal discovery & inference · Bayesian networks / PGMs · RAG & claim verification · RLHF / DPO · multimodal models (CLIP fine-tuning, BLIP-2, LLaVA)

**Stack:**
<br/>
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" />
<img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black" />
<img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB" />
<img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" />
<img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" />
<img src="https://img.shields.io/badge/GCP-4285F4?style=flat-square&logo=googlecloud&logoColor=white" />
<img src="https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonwebservices&logoColor=white" />
<img src="https://img.shields.io/badge/Azure-0078D4?style=flat-square&logo=microsoftazure&logoColor=white" />

## Currently

- 🔬 Testing whether multimodal models' reasoning traces are *seeing* or *making things up* (TU Darmstadt project lab)
- 🎯 Running the DPO stage of **ad-fontes** and measuring base vs. tuned faithfulness
- 💼 Looking for **Werkstudent** roles in ML/AI (thesis-compatible) and full-time roles from 2027

<p align="center"><sub>Ad fontes: back to the sources.</sub></p>
