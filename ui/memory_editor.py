import streamlit as st


def render_memory_editor(ltm):
    st.subheader("🧹 Memory Editor")

    data = ltm.load()
    if not data or all(len(v) == 0 for v in data.values()):
        st.info("No long-term memory to edit.")
        return

    for category, items in data.items():
        if not items:
            continue

        with st.expander(f"{category.capitalize()} ({len(items)})"):
            for key, entry in list(items.items()):
                value = entry.get("value", "")
                confidence = entry.get("confidence", 1.0)
                reinforcement = entry.get("reinforcement", 0)

                cols = st.columns([4, 1])
                with cols[0]:
                    st.markdown(
                        f"**{key}** → `{value}`  "
                        f"(conf: {confidence:.2f}, reinforced: {reinforcement}×)"
                    )
                with cols[1]:
                    if st.button("Delete", key=f"del_{category}_{key}"):
                        # Simple: use forget on key (may remove multiple matches, but OK for now)
                        ltm.forget(key)
                        st.experimental_rerun()
