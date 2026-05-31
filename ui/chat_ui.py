import streamlit as st
from PIL import Image
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from profile_view import render_profile_view
from chat_bubble import chat_bubble
from habit_timeline import render_habit_timeline
from memory_view import render_memory_view
from llm.ollama import OllamaLLM
from agent.agent import Assistant


# ----------------------------------------------------
# Session State Initialization
# ----------------------------------------------------
if "settings" not in st.session_state:
    st.session_state.settings = {
        "mode": "Balanced",
        "show_memory": False,
        "show_profile": False,
        "show_debug": False,
        "show_habits": False,
        "memory_enabled": True
    }

if "history" not in st.session_state:
    st.session_state.history = []

if "assistant" not in st.session_state:
    st.session_state.assistant = Assistant(
        llm=OllamaLLM(mode=st.session_state.settings["mode"])
    )

assistant = st.session_state.assistant
settings = st.session_state.settings


# ----------------------------------------------------
# Page config
# ----------------------------------------------------
st.set_page_config(
    page_title="Kanu",
    page_icon="🤖",
    layout="wide"
)


# ----------------------------------------------------
# Banner
# ----------------------------------------------------
def render_banner():
    banner_path = "assets/kanu_banner.png"
    try:
        img = Image.open(banner_path)
        st.image(img, use_column_width=True)
    except Exception as e:
        st.warning(f"Banner failed to load: {e}")

render_banner()


# ----------------------------------------------------
# Title
# ----------------------------------------------------
st.markdown("### ")
st.title("Kanu · Local AI Companion")
st.markdown("---")


# ----------------------------------------------------
# Sidebar Settings
# ----------------------------------------------------
st.sidebar.header("Knowledge Base")

# -----------------------------
# Document Upload + Ingestion
# -----------------------------
uploaded = st.sidebar.file_uploader(
    "Upload documents",
    type=["pdf", "txt", "md"],
    accept_multiple_files=True
)

if uploaded:
    for file in uploaded:
        num_chunks = assistant.ingest_document(file)
        st.sidebar.success(f"Added {num_chunks} chunks from {file.name}")


# -----------------------------
# Knowledge Base Viewer
# -----------------------------
if st.sidebar.checkbox("Show Knowledge Base"):
    st.subheader("Knowledge Base Contents")
    kb = assistant.rag.store.metadata

    if kb:
        for i, chunk in enumerate(kb):
            st.markdown(f"**Chunk {i+1}:**")
            st.write(chunk[:500] + "...")
            st.markdown("---")
    else:
        st.info("Knowledge base is empty.")

if st.sidebar.button("Clear Knowledge Base"):
    assistant.rag.store.index.reset()
    assistant.rag.store.metadata = []
    assistant.rag.store._save()
    st.sidebar.success("Knowledge base cleared.")


# -----------------------------
# LLM Mode + UI Toggles
# -----------------------------
settings["mode"] = st.sidebar.radio(
    "LLM Mode",
    ["Balanced", "Creative", "Precise"],
    index=["Balanced", "Creative", "Precise"].index(settings["mode"])
)

settings["memory_enabled"] = st.sidebar.checkbox(
    "Enable Memory",
    value=settings["memory_enabled"]
)

settings["show_memory"] = st.sidebar.checkbox(
    "Show Memory Panel",
    value=settings["show_memory"]
)

settings["show_profile"] = st.sidebar.checkbox(
    "Show Profile Panel",
    value=settings["show_profile"]
)

settings["show_habits"] = st.sidebar.checkbox(
    "Show Habit Timeline",
    value=settings["show_habits"]
)

settings["show_debug"] = st.sidebar.checkbox(
    "Show Debug Panel",
    value=settings["show_debug"]
)


# Update assistant mode
assistant.llm.mode = settings["mode"]


# ----------------------------------------------------
# Optional Panels
# ----------------------------------------------------
if settings["show_memory"]:
    render_memory_view(assistant.ltm)

if settings["show_profile"]:
    render_profile_view(assistant)

if settings["show_habits"]:
    render_habit_timeline(assistant.ltm)

if settings["show_debug"]:
    st.subheader("Debug State")
    st.json(st.session_state)


# ----------------------------------------------------
# Chat Area
# ----------------------------------------------------
for msg in st.session_state.history:
    chat_bubble(msg["content"], role=msg["role"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    chat_bubble(user_input, role="user")

    reply = assistant.run(user_input)

    if settings["memory_enabled"]:
        assistant.memory_manager.update_memory(user_input, reply)

    st.session_state.history.append({"role": "assistant", "content": reply})
    chat_bubble(reply, role="assistant")
