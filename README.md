# 🧭 General Knowledge Assistant

A modern, Streamlit-powered chatbot that combines **Groq’s Llama-3-70B** with **Google Gemini 1.5** and on-demand web search to answer anything from trivia to deep technical questions.  
It features multi-chat sessions, elegant UI/UX, and secure API-key handling – all in a single Python file.

---

## ✨ Features

| Capability | Details |
|------------|---------|
| **Dual-LLM pipeline** | • **Groq Llama-3-70B** (via `langchain_groq`) for core reasoning and responses.<br>• **Gemini 1.5-pro** for meta-reasoning (decides when to web-search) and safe-content filtering. |
| **Smart Web Search** | Uses **DuckDuckGo** through `langchain_community.tools.DuckDuckGoSearchRun` only when Gemini signals `<SEARCH>`. |
| **Persistent Chats** | Auto-saves each conversation (name, messages, timestamp) in Streamlit Session State; switch, rename, or delete with one click. |
| **Polished UI** | Custom CSS for clean, mobile-friendly chat bubbles, avatars, typing indicator, dark-font on light theme. |
| **Zero-backend setup** | Runs locally – no database or server-side code required. |
| **Secure Keys** | API keys loaded from a local **`.env`** file (never stored in code or state). |

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/<your-handle>/general-knowledge-assistant.git
cd general-knowledge-assistant

# 2. Create & activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate         # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt   # generate with `pip freeze > requirements.txt` if needed

# 4. Add your keys
cp .env.example .env              # then edit .env
# ────────────────────────────────
# GROQ_API_KEY=your_groq_key_here
# GEMINI_API_KEY=your_gemini_key_here
# ────────────────────────────────

# 5. Run
streamlit run app.py
```

Open <http://localhost:8501> in your browser and start chatting!

---

## 🗂️ Project Structure

```
├── app.py              # Streamlit application (this repo)
├── requirements.txt    # Python dependencies
├── .env.example        # Sample environment file
└── README.md
```

---

## 🔧 Configuration

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Obtain from <https://console.groq.com/> |
| `GEMINI_API_KEY` | Obtain from <https://aistudio.google.com/> |
| *(Optional)* `PORT` | Override Streamlit default port via `streamlit run app.py --server.port <PORT>` |

Feel free to tweak:

* **Model choice** – change `model="llama-3.3-70b-versatile"` to any Groq-hosted model.  
* **UI theme** – edit `local_css()` for colours, fonts, layouts.  
* **Search provider** – swap DuckDuckGo for another `langchain` tool or custom function.

---

## 🏗️ How It Works

1. **User prompt** ➜ stored in session history.  
2. **Gemini** decides if the query needs a web search (`<SEARCH> keywords`) or not (`NO_SEARCH`).  
3. If search required, **DuckDuckGo** fetches top results → passed to Groq with a “Search Results” prompt.  
4. **Groq Llama-3** generates the final answer.  
5. UI shows a typing indicator while processing, then streams the response.  
6. All messages & session metadata persist until the browser tab is closed (or deleted via sidebar).

![architecture diagram](docs/architecture.png)<!-- (optional: add your image) -->

---

## 🖼️ Screenshots

| Start Page | Active Chat |
|------------|-------------|
| ![screenshot1](docs/screenshot1.png) | ![screenshot2](docs/screenshot2.png) |

*(Drop your own PNGs into `docs/` and update paths.)*

---

## ✍️ Contributing

PRs are welcome!  If you:

1. **Improve UX** – animations, scroll-to-bottom, dark mode.  
2. **Add data persistence** – e.g. SQLite or supabase backend.  
3. **Integrate voice** – speech-to-text & TTS.  

…feel free to open an issue or submit a pull request.

---

## 📄 License

Licensed under the **MIT License** – see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

* [Streamlit](https://streamlit.io/) – rapid data apps.  
* [Groq API](https://groq.com/) – low-latency LLM inference.  
* [Google Gemini](https://ai.google/) – cutting-edge generative models.  
* [LangChain](https://python.langchain.com/) – orchestration glue.  
* [DuckDuckGo](https://duckduckgo.com/) – privacy-first search results.

Happy hacking!
