# 📚 RAGChatBot：基於 Embedchain 的 AI 教學助理

本專案是一個使用 [Embedchain] 與 [Ollama] 架構的 RAG 聊天機器人，支援上傳 PDF 並根據其內容進行問答，內建多種 LLM 與 Embedding 模型可切換。

---

## 🚀 環境安裝

建議使用 Conda 建立獨立虛擬環境：

```bash
conda create --name RAGChatBot python==3.10
conda activate RAGChatBot

# 1. 下載專案
git clone https://github.com/reeeeeta/RAGChatBot.git
cd RAGChatBot

# 2. 安裝必要套件
pip install django embedchain ollama langchain_huggingface
pip install gpt4all==2.0.2

# 3. 進入 Django 專案資料夾並啟動伺服器
cd dbsproject
python manage.py runserver
```
