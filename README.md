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

<img width="1919" height="1079" alt="Screenshot 2026-02-15 102913" src="https://github.com/user-attachments/assets/17d957cd-8add-4303-8683-24d57be38144" />

<img width="1919" height="1079" alt="Screenshot 2026-02-15 102927" src="https://github.com/user-attachments/assets/d34a25ea-5ee7-4b01-a816-ec461aad825c" />
<img width="1919" height="1076" alt="Screenshot 2026-02-15 102940" src="https://github.com/user-attachments/assets/f30efaa7-15d2-4698-bcad-45b438c44ff2" />
<img width="1919" height="1079" alt="Screenshot 2026-02-15 103003" src="https://github.com/user-attachments/assets/3ccddbbe-5670-468e-a480-161de429b3b8" />

<img width="1919" height="1079" alt="Screenshot 2026-02-15 103021" src="https://github.com/user-attachments/assets/d8d0e8ef-f393-40d3-a5fa-37227eb66397" />


