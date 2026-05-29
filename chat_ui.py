from openclaw import Agent, Memory
from openclaw.llm import Ollama   # adjust path if needed
import streamlit as st
# Initialize LLM
llm = Ollama(model="llama3.2")

# Optional memory
memory = Memory()

# Create agent
agent = Agent(llm=llm, memory=memory)



# Display Kanu banner
st.image("assets/kanu_banner.png", use_column_width=True)

# ❤️☕ Kanu Header — Cozy Café Style
st.markdown("""
<style>
.title-container {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 700;
    color: #ff4b5c;
    background: linear-gradient(90deg, #fff5f5, #ffe0e0);
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(255, 75, 92, 0.3);
    font-family: 'Poppins', sans-serif;
}
</style>

<div class="title-container">
    ❤️ Kanu — Anu’s Local AI Assistant ☕
</div>
""", unsafe_allow_html=True)

# Chat container
st.markdown("### 💬 Chat with Kanu")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
user_input = st.chat_input("Type your message…")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Generate assistant response using the already-created agent
    response = agent.run(user_input)

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)

