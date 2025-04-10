import streamlit as st
import random
import time
import pandas as pd
import os

# Sample sentences
sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Typing fast is a valuable skill for programmers.",
    "Streamlit makes it easy to build web apps in Python.",
    "Practice makes perfect, especially with typing speed.",
    "Focus on accuracy before increasing your speed."
]

# Load or create leaderboard CSV
leaderboard_file = "leaderboard.csv"
if not os.path.exists(leaderboard_file):
    pd.DataFrame(columns=["Name", "WPM", "Accuracy", "Time"]).to_csv(leaderboard_file, index=False)

# Title
st.title("⌨️ Typing Speed Tester")

# Input player name
player_name = st.text_input("Enter your name to begin:")

# Select a random sentence
if 'sentence' not in st.session_state:
    st.session_state.sentence = random.choice(sentences)

# Show sentence
if player_name:
    st.markdown("### Type this sentence:")
    st.code(st.session_state.sentence)

    if 'start_time' not in st.session_state:
        if st.button("Start Typing"):
            # Countdown
            with st.empty():
                for i in range(3, 0, -1):
                    st.write(f"Starting in {i}...")
                    time.sleep(1)
                st.write("Go!")
            st.session_state.start_time = time.time()

    # Typing input
    if 'start_time' in st.session_state:
        typed_text = st.text_input("Start typing here:")

        if typed_text == st.session_state.sentence:
            end_time = time.time()
            total_time = round(end_time - st.session_state.start_time, 2)

            words = len(typed_text.split())
            wpm = round((words / total_time) * 60)

            correct_chars = sum(1 for a, b in zip(typed_text, st.session_state.sentence) if a == b)
            accuracy = round((correct_chars / len(st.session_state.sentence)) * 100)

            st.success(f"🎉 Done in {total_time} seconds!")
            st.info(f"📈 WPM: **{wpm}**")
            st.info(f"🎯 Accuracy: **{accuracy}%**")

            # Save to leaderboard
            new_score = pd.DataFrame([[player_name, wpm, accuracy, total_time]],
                                     columns=["Name", "WPM", "Accuracy", "Time"])
            leaderboard = pd.read_csv(leaderboard_file)
            leaderboard = pd.concat([leaderboard, new_score], ignore_index=True)
            leaderboard.sort_values(by="WPM", ascending=False, inplace=True)
            leaderboard.to_csv(leaderboard_file, index=False)

            # Show leaderboard
            st.markdown("## 🏆 Leaderboard (Top 5)")
            st.dataframe(leaderboard.head(5), use_container_width=True)

            # Reset option
            if st.button("Try Again"):
                st.session_state.clear()
