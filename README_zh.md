<p align="center">
<h1 align="center"> <img src="web-vue/public/xm.ico" width="30" /> Wheat Voice</h1>
</p>
<p align="center">
<h2 align="center">为 AI 研究人员打造的智能轻量级论文科研工具平台</h2>
</p>

<p align="center">
  	<a href="https://img.shields.io/badge/version-v1.0-blue">
      <img alt="版本" src="https://img.shields.io/badge/version-v1.0-blue?color=FF8000?color=009922" />
    </a>
  <a href="https://img.shields.io/badge/Status-building-blue">
       <img alt="状态-构建中" src="https://img.shields.io/badge/Status-building-blue" />
  	</a>
  <a href="https://github.com/Hanscal/Wheat-Voice/pulls">
       <img alt="欢迎PR" src="https://img.shields.io/badge/PRs-Welcome-red" />
  	</a>
   	<a href="https://github.com/Hanscal/Wheat-Voice/stargazers">
       <img alt="stars" src="https://img.shields.io/github/stars/Hanscal/Wheat-Voice" />
  	</a>
  	<a href="https://github.com/Hanscal/Wheat-Voice/network/members">
       <img alt="fork" src="https://img.shields.io/github/forks/Hanscal/Wheat-Voice?color=FF8000" />
  	</a>
    <a href="https://github.com/Hanscal/Wheat-Voice/issues">
      <img alt="问题反馈" src="https://img.shields.io/github/issues/Hanscal/Wheat-Voice?color=0088ff"/>
    </a>
    <br />
</p>

---

**Wheat Voice** 是一款全自动、轻量化的科研发现工具，专为 **人工智能** 社区打造。旨在帮助研究人员、学生和工程师**高效发现相关学术论文**，自动完成收集顶级 AI 会议最新研究成果，智能化辅助论文筛选、整理和分析。

立即试用 Wheat Voice，让你的科研流程更加轻松。如果你有建议或想参与贡献，欢迎提交 Issue 或 PR！

[//]: # ([![]&#40;./assets/web-demo.jpg&#41;]&#40;./assets/web-demo-v1.mp4&#41;)
https://github.com/user-attachments/assets/29a8abb2-4181-4abb-9076-9b57c3d6b312

---

### 🚀 主要特性

- **顶会论文覆盖**  
  聚焦于 NeurIPS、ACL、EMNLP、ICML、ICLR、CVPR、ICCV 等顶级会议，确保论文内容高质量、强相关。

- **强大的搜索体验**  
  支持按关键词、标题、作者、任务（如 NER、摘要生成）、模型（如 BERT、GPT）、数据集、论文类型（如综述、基准）搜索。  
  仅登录用户可使用搜索功能，以实现访问控制。

- **内置 AI 阅读助手**  
  点击标题即可查看详情，或使用 AI 驱动的 PDF 阅读器获取摘要、深入探索。  
  支持浏览器内 PDF 阅读、标注与下载。

- **论文自动收集**  
  自动脚本定期抓取、解析并存储 AI 相关论文。

- **无缝集成**  
  可导出为 CSV 或 JSON，支持通过 CLI 或 Python API 进行高级工作流集成。

---

### 📦 使用场景

- **研究人员与学生**：根据实验室研究方向，自动维护个性化的阅读清单。
- **产品团队**：跟踪特定方向、任务、模型或评测基准的演变趋势。
- **开发者**：在平台基础上构建学术摘要器、推荐机器人或洞察生成器。

---

### 📥 项目启动指南

使用 **Wheat Voice** 上手非常简单。

#### 🔍 方法一：手动部署
```bash
# 第一步：克隆仓库
git clone https://github.com/your-org/wheat-voice.git
cd Wheat-Voice

# 第二步：配置后端
cd app
conda create -n wheat-voice python=3.9
conda activate wheat-voice
pip install -r requirements.txt

# 准备数据与配置
# 1. 将 `paper_info.json` 放入 `app/cache`
# 2. 从百度云下载 `article.zip`：https://pan.baidu.com/s/1B12hVE8SRj6ZFTnQqVf7vA （提取码：MIND）
#    解压至 `app/static/article`
# 3. 配置 `app/conf/config.py` 中的阿里云短信、LLM 与 MySQL 信息
# 4. 使用 `app/conf/wheatvoice_init.sql` 初始化数据库

python run_wheat.py

# 第三步：启动前端（Vue3 + Vite4 + TypeScript）
cd web-vue
node -v  # 确保 Node.js 版本为 v22.8.0
npm install
npm run dev       # 启动开发模式
npm run build     # 可选：构建生产版本
npm run preview   # 可选：预览生产版本
```

#### ⚙️ 方法二：Docker 部署（推荐）

```bash
# 第一步：克隆仓库
git clone https://github.com/your-org/wheat-voice.git
cd Wheat-Voice

# 第二步：拉取前后端镜像
docker pull hanscal/wheatvoice-app:1.0
docker pull hanscal/wheatvoice-vue:1.0

# 第三步：使用 Docker Compose 启动
# 请先检查 `docker-compose.yml` 的配置
docker compose up -d

# 启动后端容器
docker exec -it wheatvoice-app /bin/bash
python run_wheatvoice.py

# 启动前端容器
docker exec -it wheatvoice-vue /bin/bash
npm install
npm run dev
```

### 🌐 访问网站

- **本地演示地址**：[http://127.0.0.1:11120/](http://127.0.0.1:11120/)
- **在线演示地址**：[https://mindguide.cn/#/](https://mindguide.cn/#/)  
  - 可使用注册手机号登录，或使用以下测试账户：  
    **用户名**：18817362936  
    **密码**：ch123456

---

### 💡 收录会议列表

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

### 🧪 后续开发计划

**前端功能升级**
- 更直观的关键词高亮搜索
- 便捷的标签管理与分类
- RSS 和邮件提醒支持订阅主题更新
- **订阅系统**：用户可关注特定主题、查看订阅论文、添加笔记，并与兴趣相投者交流讨论

**搜索后端增强**
- 替换为 Elasticsearch 作为主要检索引擎，应对论文量增加后的扩展性与性能需求
- 支持基于嵌入的排序与可选 RAG 摘要生成
- 密码加密加强（使用 bcrypt）
- 支持基于 Python 的高级脚本化定制流程

**AI 智能功能**
- 集成 AI FAQ 生成
- 论文内容中文翻译
- 提取模型结构图用于缩略图展示
- 自动摘要与要点提取

**数据增强与解析**
- 持续扩展论文数据库
- 自动从 ArXiv 与最新会议中提取元数据

---

### 🧠 免责声明

Wheat Voice 当前仍在积极开发中。我们努力确保论文内容的准确性与相关性，但部分论文可能无法完全满足预期，敬请理解。

主要数据来源包括 [DBLP](https://dblp.org/)、[ACL Anthology](https://aclanthology.org/)、[NeurIPS](https://papers.nips.cc/)、[OpenReview](https://openreview.net/)。若您发现任何侵权内容，请联系我们，我们将尽快处理。😊

---