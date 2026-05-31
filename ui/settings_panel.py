import streamlit as st


def render_settings_panel(default_mode: str = "Balanced"):
    st.subheader("⚙️ Settings")

    mode = st.radio(
        "LLM Mode",
        ["Balanced", "Creative", "Precise"],
        index=["Balanced", "Creative", "Precise"].index(default_mode),
    )

    half_life_days = st.slider(
        "Memory half-life (days)",
        min_value=7,
        max_value=90,
        value=30,
        step=1,
        help="How quickly long-term memories decay. Lower = faster forgetting.",
    )

    threshold = st.slider(
        "Memory strength threshold",
        min_value=0.1,
        max_value=0.9,
        value=0.25,
        step=0.05,
        help="Memories weaker than this are removed during decay.",
    )

    return {
        "mode": mode,
        "half_life_days": half_life_days,
        "threshold": threshold,
    }
