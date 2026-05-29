Python
Streamlit
License: MIT
Status

# ☕💗 Kanu — Anu’s Local AI Assistant

Kanu is a cozy, café‑themed local AI assistant built with **Python**, **Streamlit**, and a custom **Agent + LLM architecture** powered by **Ollama**.  
It runs entirely on your machine, remembers conversations, and responds with warmth and personality.

This is my first GitHub project — and the beginning of something much bigger.

---

## ✨ Features

- 🧠 **Custom Agent architecture** (LLM + Memory + Tools)  
- 🤖 **Local LLM via Ollama** (no cloud required)  
- 💬 **Chat interface with history**  
- ☕ **Café‑themed UI** with anime banner and warm colors  
- ❤️ **Personalized assistant identity: Kanu**  
- 📝 **Memory system** for contextual conversations  
- 🔧 **Extensible tool system** (coming soon)

---

## 📸 Screenshots

### Main UI

Kanu Screenshot

---

## 🗺️ Roadmap

### ✅ Completed

- Local LLM integration via Ollama  
- Streamlit chat UI with history  
- Agent architecture (LLM + Memory + Identity)  
- Clean project structure  
- GitHub setup and documentation

### 🚧 In Progress

- Tool system (search, calculator, file ops)  
- Improved UI styling and layout  
- Persistent memory storage

### 🔮 Coming Soon

- RAG (Retrieval-Augmented Generation)  
- Voice mode (speech-to-text + text-to-speech)  
- Avatar UI with animations  
- Multi-agent support  
- Dark mode toggle

---

## 📁 Project Structure

```plaintext
kanu-ai/
├── assets/                 # Images, screenshots, future logo, demo GIF
├── logs/                   # Runtime logs (optional)
├── openclaw/               # Core agent framework
│   ├── __init__.py
│   ├── agent.py            # Agent logic + identity
│   ├── llm.py              # Ollama model wrapper
│   ├── memory.py           # Conversation memory system
│   ├── tool.py             # Tool interface (coming soon)
│   └── exceptions.py       # Custom exceptions
├── chat_ui.py              # Streamlit chat interface
├── assistant.py            # High-level assistant behavior
├── requirements.txt        # Python dependencies
├── uv.lock                 # uv dependency lockfile
└── README.md               # Documentation

---
```

## 🧰 Tech Stack

- **Language:** Python 3.10  
- **UI:** Streamlit  
- **LLM Runtime:** Ollama (local models)  
- **Agent Framework:** Custom (openclaw)  
- **Memory:** In-memory conversation history (persistent storage coming soon)  
- **Package Management:** pip / uv

## 🧱 Architecture Overview

At a high level, Kanu is built as:

```plaintext
User ⇄ Streamlit UI (chat_ui.py)
      ⇄ Assistant (assistant.py)
      ⇄ Agent (openclaw/agent.py)
      ⇄ LLM (openclaw/llm.py → Ollama)
      ⇄ Memory (openclaw/memory.py)
      ⇄ Tools (openclaw/tool.py - coming soon)
```

## 🌸 Why Kanu?

Kanu started as my first GitHub project — but also as something personal.

I wanted:

- an AI that runs **entirely on my machine**
- that feels **warm, cozy, and kind**
- that remembers me and our conversations
- that looks more like a **café companion** than a cold chatbot

Kanu is my attempt to blend:

- **local-first tech** (privacy, control, ownership)
- with a **soft, anime-inspired, café aesthetic**
- and a **real sense of presence and personality**

This repo is the beginning — I’m building it in the open, learning as I go.

## 🤝 Contributing

This is my first GitHub project, and I’m still learning — but contributions, ideas, and feedback are very welcome.

If you’d like to contribute:

1. **Fork** the repo
2. **Create a branch** for your feature or fix
3. **Make your changes**
4. **Open a Pull Request** with a clear description

You can also:

- open **Issues** for bugs, ideas, or feature requests
- suggest improvements to the agent, UI, or architecture

Be kind — Kanu is cozy on purpose. 🌸

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/kanu-ai
cd kanu-ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### ⚡ Optional: Install with uv (recommended for speed)

If you prefer using **uv** instead of pip:

```bash
uv sync
```