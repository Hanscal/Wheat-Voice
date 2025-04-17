<p align="center">
<h1 align="center"> <img src="web-vue/public/xm.ico" width="30" /> Wheat Voice</h1>
</p
<p align="center">
<h2 align="center">Smart and Lightweight Paper Discovery for AI Researchers</h2>
</p

<div align="center">

  <a href="https://img.shields.io/badge/version-v1.0-blue">
    <img alt="version" src="https://img.shields.io/badge/version-v1.0-blue?color=FF8000" />
  </a>

  <a>
    <img alt="PRs" src="https://img.shields.io/badge/PRs-Welcome-red" />
  </a>

  <a href="https://github.com/Hanscal/Wheat-Voice/stargazers">
    <img alt="stars" src="https://img.shields.io/github/stars/Hanscal/Wheat-Voice" />
  </a>

  <a href="https://github.com/Hanscal/Wheat-Voice/issues">
    <img alt="issues" src="https://img.shields.io/github/issues/Hanscal/Wheat-Voice?color=0088ff"/>
  </a>

</div>

---

**Wheat Voice** is a fully-automated and lightweight research discovery tool tailored for the **Artificial Intelligent** community. Designed to help researchers, students, and engineers **efficiently find relevant academic papers**, Wheat Voice is powered by AI to collect, filter, and analyze the latest research across top AI conferences and repositories.

Try Wheat Voice today and let your research workflow breathe. Got feedback or want to contribute? Open an issue or pull request!

\[ English | [中文](README_zh.md) \]

[//]: # ([![]&#40;./assets/web-demo.jpg&#41;]&#40;./assets/web-demo-v1.mp4&#41;)
https://github.com/user-attachments/assets/29a8abb2-4181-4abb-9076-9b57c3d6b312

---

### 🚀 Key Features

- **Top-Tier AI Conference Coverage**  
  Focused on collecting papers from top-tier venues like NeurIPS, ACL, EMNLP, ICML, ICLR, CVPR and ICCV, ensuring high-quality and relevant content for researchers.

- **Powerful Search Experience**  
  Search by keywords, titles, authors, tasks (e.g., NER, summarization), models (e.g., BERT, GPT), datasets, or paper types (e.g., survey, benchmark).  
  Search is gated to logged-in users for access control.

- **Built-In AI Reading Assistant**  
  Click a paper title for detailed views or use the AI-powered PDF reader for summaries and exploration.  
  In-browser PDF viewing, annotation, and downloads supported.  

- **Automated Paper Collection**  
  Automated scripts periodically fetch, parse, and store AI-related papers.

- **Seamless Integration**  
  Export results in CSV or JSON, or integrate via CLI or Python API for advanced workflows.

---

### 📦 User Cases

- **For Researchers & Students**: Automatically maintain a curated reading list tailored to your lab's focus.
- **For Product Teams**: Track specific trends, tasks, models, or benchmarks over time.
- **For Developers**: Build academic summarizers, recommender bots, or insight generators on top of the platform.
---

### 📥 Project Setup

Getting started with **Wheat Voice** is quick and simple.

#### 🔍 Method 1: Manual Setup
```bash
# step 1: Clone the repository
git clone https://github.com/your-org/wheat-voice.git
cd Wheat-Voice

# step 2: Setup backend server
cd app
conda create -n wheat-voice python=3.9
conda activate wheat-voice
pip install -r requirements.txt

# Prepare data and configuration
# 1. Place `paper_info.json` into `app/cache`
# 2. Download `article.zip` from Baidu Cloud: https://pan.baidu.com/s/1B12hVE8SRj6ZFTnQqVf7vA (password: MIND)
#    and extract it to `app/static/article`
# 3. Configure `app/conf/config.py` with ALIBABA_CLOUD SMS, LLM, and MySQL info
# 4. Initialize the DB using `app/conf/wheatvoice_init.sql`

python run_wheat.py

# Step 3: Start frontend (Vue3 + Vite4 + TypeScript)
cd web-vue
node -v  # Ensure Node.js v22.8.0 is installed
npm install
npm run dev       # Start in development mode
npm run build     # Optional: build for production
npm run preview   # Optional: preview production build
```

#### ⚙️ Method 2: Docker (Recommended)

```bash
# Step 1: Clone the repository
git clone https://github.com/your-org/wheat-voice.git
cd Wheat-Voice

# step 2
# download backend and frontend image
docker pull hanscal/wheatvoice-app:1.0
dcker pull hanscal/wheatvoice-vue:1.0

# Step 3: Launch using Docker Compose
# Make sure to review `docker-compose.yml` settings
docker compose up -d

# Start backend inside container
docker exec -it wheatvoice-app /bin/bash
python run_wheatvoice.py

# Start frontend inside container
docker exec -it wheatvoice-vue /bin/bash
npm install
npm run dev
```

### 🌐 View the website
- **View the local demo website**: [http:/127.0.0.1:11120/](http:/127.0.0.1:11120/)  
- **View the online demo website**: [https://mindguide.cn/#/](https://mindguide.cn/#/) 
  - login with your cellphone when you registered or use the following account to login  
    **Username**: 18817362936  
    **Password**: ch123456  

---


### 💡 Categories

<!-- confs-list-start -->

```text
- [AAAI 2019-2022] [ACL 2019-2023] [EMNLP 2019-2022] [NAACL 2019-2022] [COLING 2020-2022] [IJCAI 2019-2022]
- [ICLR 2019-2023] [ICML 2019-2022] [CVPR 2019-2023] [ICCV 2019-2021] [ICASSP 2019-2022] [WWW 2019-2022] 
- [NIPS 2019-2022] [TPAMI 2020-2022] [KDD 2019-2022] [CIKM 2019-2022] [SIGIR 2019-2022] [MM 2019-2022] 
- [WSDM 2019-2023] [ECIR 2019-2022] [ECCV 2020-2022] [COLT 2019-2022] [ICME 2019-2022] [ICDM 2019-2021]
- [AISTATS 2019-2022] [INTERSPEECH 2019-2022] [ISWC 2019-2022] [JMLR 2019-2022] [VLDB 2019-2021] [TIP 2020-2022]
- [RECSYS 2019-2022] [TKDE 2020-2022] [TOIS 2020-2022] [MLSYS 2020-2022] [WACV 2020-2022] [SIGMOD 2019-2022] 
- [TASLP 2020-2022] [BMVC 2019-2021] [MICCAI 2019-2022] [IJCV 2020-2022] [TNNLS 2020-2022] [FAST 2019-2023]
-  ...
```

<!-- confs-list-end -->

---

### 🧪 Next Steps

**Web Interface Improvements**
  - Intuitive search with keyword highlighting
  - Tagging system for better organization
  - RSS and Email notifications for topic-specific updates
  - **Subscription support**: users can follow specific topics, view subscribed papers, add personal notes, and join discussion groups with others who share similar interests.

**Enhanced Search Backend**
  - Transition to Elasticsearch as the primary search engine; as the paper volume grows, search speed and scalability will improve significantly
  - Embedding-based ranking and optional RAG-based summarization support
  - Enhanced security with bcrypt password encryption
  - Python-based scripting support for advanced workflows and customization

**AI-Powered Intelligence**
  - Integration of AI-generated FAQs
  - Paper content translation into Chinese
  - Structural analysis of papers and extraction of model architecture figures for use as thumbnails
  - Automatic paper summarization and extraction of key insights

**Data Enrichment and Parsing**
  - Ongoing expansion of the paper database
  - Automated metadata extraction from sources like ArXiv and recent AI conference proceedings

---

### 🧠 Disclaimer

Wheat Voice is under active development. While we strive for high accuracy and relevance, some papers may not fully match your expectations. Thanks for your understanding.

Sources include [DBLP](https://dblp.org/), [ACL Anthology](https://aclanthology.org/), [NeurIPS](https://papers.nips.cc/) and [OpenReview](https://openreview.net/). If you believe any content violates copyright, please contact us, and we will remove it promptly. 😊