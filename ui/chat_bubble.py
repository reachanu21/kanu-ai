import streamlit as st


def chat_bubble(message: str, role: str = "assistant"):
    is_user = role == "user"

    align = "flex-end" if is_user else "flex-start"
    bg = "#1f6feb" if is_user else "#2d333b"
    text_color = "#ffffff"
    label = "You" if is_user else "Kanu"

    html = f"""
    <div style="display: flex; justify-content: {align}; margin: 4px 0;">
      <div style="
          max-width: 80%;
          background: {bg};
          color: {text_color};
          padding: 8px 12px;
          border-radius: 12px;
          font-size: 0.9rem;
          line-height: 1.4;
      ">
        <div style="font-size: 0.7rem; opacity: 0.7; margin-bottom: 2px;">{label}</div>
        <div>{message}</div>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
