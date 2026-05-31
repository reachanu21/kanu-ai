import streamlit as st

def render_memory_view(ltm):
    st.subheader("Kanu's Long‑Term Memory")

    data = ltm.load()

    if not data or all(len(v) == 0 for v in data.values()):
        st.info("No long‑term memory stored yet.")
        return

    for category, items in data.items():
        if not items:
            continue

        with st.expander(category.capitalize()):
            for key, entry in items.items():

                # Handle new-format entries
                if isinstance(entry, dict):
                    value = entry.get("value", "")

                    # Safe confidence conversion
                    raw_conf = entry.get("confidence", 0)
                    try:
                        conf_val = float(raw_conf)
                    except Exception:
                        conf_val = 0.0

                    # Safe reinforcement conversion
                    raw_reinf = entry.get("reinforcement", 1)
                    try:
                        reinf_val = int(raw_reinf)
                    except Exception:
                        reinf_val = 1

                else:
                    # Old-format fallback
                    value = entry
                    conf_val = 0.0
                    reinf_val = 1

                st.markdown(
                    f"- **{key}** → `{value}`  "
                    f"(conf: {conf_val:.2f}, reinforced: {reinf_val}×)"
                )
