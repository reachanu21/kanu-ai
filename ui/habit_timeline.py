import streamlit as st
from datetime import datetime


def render_habit_timeline(ltm):
    st.subheader("🕒 Habit Timeline")

    data = ltm.load()
    habits = data.get("habits", {})

    if not habits:
        st.info("No habits detected yet.")
        return

    # Convert to list with timestamps
    timeline = []
    for key, entry in habits.items():
        ts = entry.get("last_updated", 0)
        timeline.append({
            "key": key,
            "value": entry.get("value", ""),
            "confidence": entry.get("confidence", 1.0),
            "reinforcement": entry.get("reinforcement", 0),
            "timestamp": ts,
            "dt": datetime.fromtimestamp(ts)
        })

    # Sort newest → oldest
    timeline.sort(key=lambda x: x["timestamp"], reverse=True)

    # Render timeline
    for item in timeline:
        dt_str = item["dt"].strftime("%b %d, %Y · %I:%M %p")

        st.markdown(
            f"""
            <div style="margin-bottom: 18px; padding-left: 10px; border-left: 3px solid #4a90e2;">
                <div style="font-size: 0.85rem; opacity: 0.7;">{dt_str}</div>
                <div style="font-size: 1rem; margin-top: 4px;">
                    <strong>{item['key']}</strong>: {item['value']}
                </div>
                <div style="font-size: 0.8rem; opacity: 0.7;">
                    Reinforced: {item['reinforcement']}× · Confidence: {item['confidence']:.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
