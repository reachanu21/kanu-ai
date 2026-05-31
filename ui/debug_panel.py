import json
import streamlit as st


def render_debug_panel(assistant):
    st.subheader("🔍 Debug Panel")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Short-Term Memory (STM)**")
        try:
            stm_messages = assistant.stm.get()
        except Exception:
            stm_messages = []
        st.json(stm_messages)

    with col2:
        st.markdown("**Long-Term Memory (LTM) Raw**")
        try:
            ltm_data = assistant.ltm.load()
        except Exception:
            ltm_data = {}
        st.json(ltm_data)

    st.markdown("**System Prompt Context (Summary)**")
    try:
        summary = assistant.ltm.summarize()
    except Exception:
        summary = "Error summarizing memory."
    st.code(summary, language="markdown")
