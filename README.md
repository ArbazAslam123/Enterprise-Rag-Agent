# 🏢 Enterprise Policy AI Assistant

## Overview

The **Enterprise Policy AI Assistant** is an intelligent digital assistant designed to help employees instantly find accurate answers about company policies, IT security, hardware compliance, HR stipends, and other internal guidelines.

Instead of searching through long corporate manuals or waiting for HR or IT to respond, employees can simply ask a question and receive a clear, accurate answer based strictly on the company's approved documentation.

---

## 🎯 The Problem

In large organizations, company policies can be complex, frequently updated, and spread across lengthy documents.

Employees may struggle to find the exact rules regarding:

* Travel and expense policies
* Remote work and home-office stipends
* IT security procedures
* Hardware requirements
* HR benefits and allowances
* Internal compliance guidelines

Traditional AI chatbots introduce another major risk: **hallucinations** — when an AI generates information that sounds correct but is not actually supported by company policy.

In a corporate environment, providing an incorrect budget code, security procedure, or compliance requirement can create serious business and operational risks.

---

## 💡 How This Project Solves It

The Enterprise Policy AI Assistant is designed to **prevent AI guesswork** by ensuring that responses are generated only from the company's approved documentation.

### Key Benefits

**🔒 Strict Accuracy**

The AI operates with strict guardrails and is instructed to answer only when sufficient information is available in the company's documents. If the required information cannot be found, it clearly states that the information is unavailable rather than making up an answer.

**📚 Transparent Citations**

Every answer includes references to the source document and relevant content used to generate the response. Employees and managers can therefore verify where the information came from.

**⚡ Fast & Cost-Efficient**

The system uses a dual-search approach combining keyword-based and meaning-based search to quickly identify the most relevant policy information before generating an answer.

---

## ⚙️ How It Works

Although the technology behind the assistant is advanced, the workflow is straightforward:

### 1. 📄 Document Processing

The system reads company documents and automatically breaks them into organized, searchable sections while preserving the relevant context.

### 2. 🗄️ Intelligent Knowledge Base

These sections are stored in a secure database that understands both:

* **Exact keywords** — such as `CODE-REMOTE-99`
* **Related meanings** — such as "working from home" or "remote setup"

This allows the system to find information even when an employee doesn't use the exact wording found in the policy.

### 3. ⚖️ Intelligent Re-Ranking

When an employee asks a question, the system retrieves potentially relevant information and uses a **re-ranking model** to identify the most useful passages.

Irrelevant results are filtered out before they reach the AI.

### 4. 🤖 Grounded AI Response

The AI receives only the most relevant policy information and generates a clear, professional response based on that content.

The system is designed to keep internal reasoning private while presenting the employee with only the final answer and supporting sources.

---

## 🛠️ Technology Stack

* **Python**
* **Streamlit**
* **LangChain**
* **Groq LLM**
* **Qdrant / Vector Database**
* **Hybrid Search**
* **Re-Ranking**
* **RAG (Retrieval-Augmented Generation)**
* **AI Guardrails**
* **Document Processing**

---

## 🚀 How to Run the App Locally

### 1. Install the Requirements

Open your terminal or command prompt and run:

```bash
pip install -r requirements.txt
```

### 2. Add Your API Key

Create a `.env` file in the project's root directory and add your Groq API key:

```env
GROQ_API_KEY=your_key_here
```

### 3. Start the Assistant

Launch the Streamlit application with:

```bash
streamlit run app.py
```

The application will open in your browser.

If you want to use it this is the App 
Url: https://enterprise-rag-agent-v1.streamlit.app/

---

## 👨‍💻 Author

**Arbaz Aslam**
*Data Scientist | AI Engineer*
aarbazaslam123@gmail.com
