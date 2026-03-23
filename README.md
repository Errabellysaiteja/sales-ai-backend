# 🚀 AI Sales Coaching Platform

An AI application that analyzes sales calls to provide automated scoring, objection handling feedback, and coaching insights.

## 🔗 Live Demo
https://sales-ai-backend-twbi.vercel.app/  
---

## 📖 Project Overview
This platform acts as an automated "Sales Manager" for teams. It allows users to upload raw audio recordings of sales conversations and receive instant, actionable feedback.

**Key Capabilities:**
* **🗣️ Speech-to-Text:** Converts MP3 audio to text using **AWS Transcribe**.
* **🧠 AI Analysis:** Uses **Mistral AI** (LLM) to analyze tone, clarity, and sales techniques.
* **📚 RAG (Retrieval-Augmented Generation):** Checks the conversation against a knowledge base of "Best Sales Practices" stored in **FAISS**.
* **📊 Scoring Engine:** Generates a 0-100 score based on objection handling and empathy.

---

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend Framework** | Python 3.10, FastAPI |
| **AI & LLM** | LangChain, Mistral AI API |
| **Vector Database** | FAISS |
| **Cloud Services** | AWS S3, AWS Transcribe |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Deployment** | Vercel |

---


**Architecture**
<img width="1466" height="654" alt="architecture" src="https://github.com/user-attachments/assets/0b8e7ab6-96cc-4bf7-b420-bb7883fc5ae5" />


## ⚙️ Local Setup Instructions

Follow these steps to run the backend on your local machine.

1. Clone github
git clone [https://github.com/YOUR_GITHUB_USERNAME/sales-ai-backend.git](https://github.com/YOUR_GITHUB_USERNAME/sales-ai-backend.git)
cd sales-ai-backend


2. Create Virtual Environment
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

3. Install Dependencies-
pip install -r requirements.txt

4. Configure Environment Variables-
Create a file named .env in the root directory and add your keys:

5. Run the Server-
python main.py

# ScreenShot

<img width="1919" height="1079" alt="Screenshot 2026-02-15 102913" src="https://github.com/user-attachments/assets/b8b60c87-58c8-4cb9-8743-88d97889cb85" />

