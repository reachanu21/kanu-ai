import streamlit as st


def render_profile_view(ltm):
    st.subheader("👤 Profile & Habits")

    data = ltm.load()

    profile = data.get("profile", {})
    habits = data.get("habits", {})
    preferences = data.get("preferences", {})
    health = data.get("health", {})

    if not any([profile, habits, preferences, health]):
        st.info("No profile, habits, or preferences stored yet.")
        return

    if profile:
        with st.expander("Profile", expanded=True):
            for key, entry in profile.items():
                st.markdown(f"- **{key}** → `{entry.get('value', '')}`")

    if habits:
        with st.expander("Habits", expanded=True):
            for key, entry in habits.items():
                st.markdown(f"- **{key}** → `{entry.get('value', '')}`")

    if preferences:
        with st.expander("Preferences", expanded=False):
            for key, entry in preferences.items():
                st.markdown(f"- **{key}** → `{entry.get('value', '')}`")

    if health:
        with st.expander("Health", expanded=False):
            for key, entry in health.items():
                st.markdown(f"- **{key}** → `{entry.get('value', '')}`")
