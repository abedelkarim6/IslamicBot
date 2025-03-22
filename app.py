import streamlit as st
from main import *

# Streamlit UI
st.title("AI Social Media Content Generator")
st.markdown("Transform your ideas into platform-ready content!")

# Initialize session state for user input
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# User input
input_mode = st.radio("Choose input method:", ["Text", "Voice"], horizontal=True)

recognizer = sr.Recognizer()

if input_mode == "Text":
    user_input = st.text_area(
        "Enter your idea or topic:",
        placeholder="Share your brilliant idea here... ✍️",
        value=st.session_state.user_input,
    )
else:
    if "voice_text" not in st.session_state:
        st.session_state.voice_text = ""

    if st.button("🎤 Start Recording"):
        with st.spinner("Listening... 🎧"):
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)

                text = recognizer.recognize_google(audio)
                st.session_state.voice_text = text
                st.success(f"Transcription: {text}")
            except sr.UnknownValueError:
                st.error("Sorry, I couldn't understand the audio.")
            except sr.RequestError:
                st.error("Error with the speech recognition service.")

    if st.session_state.voice_text:
        user_input = st.text_area(
            "Edit Transcribed Text:", value=st.session_state.voice_text
        )

# Platform selection
platform = st.selectbox(
    "Choose a social media platform:", ["Facebook", "Twitter (X)", "LinkedIn"]
)

# Extra options
post_length = st.selectbox("Post Length:", ["Short", "Medium", "Long"])
audience_level = st.selectbox("Audience Level:", ["Beginner", "Intermediate", "Expert"])

# Generate content
if st.button("Generate Content ✨"):
    if not user_input.strip():
        st.error("Please enter some text or record your voice!")
    else:
        with st.spinner("🧠 Generating content..."):
            response_data = LLM_prompt(
                user_input, platform, post_length, audience_level
            )

        # Store generated post in session state
        st.session_state.generated_post = response_data["Generated_post"]
        st.session_state.additional_topics = response_data["Additional_Topics"]

# Display generated content if available
if "generated_post" in st.session_state:
    st.markdown("### 🎉 Generated Post")
    st.write(st.session_state.generated_post)

# Display additional topics as clickable buttons
if "additional_topics" in st.session_state and st.session_state.additional_topics:
    st.markdown("### 🔥 Additional Topics")
    for topic in st.session_state.additional_topics:
        if st.button(topic, key=topic):
            st.session_state.user_input = topic  # Update user input
            st._rerun()  # Refresh the page to reflect the change
