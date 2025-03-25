import streamlit as st
import speech_recognition as sr
from main import post_generator, prompt_selector  # Import topic generator function

# Streamlit UI
st.title("AI Social Media Content Generator")
st.markdown("Transform your ideas into platform-ready content! 🚀")

# Initialize session state
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

if "generated_post" not in st.session_state:
    st.session_state.generated_post = ""

if "additional_topics" not in st.session_state:
    st.session_state.additional_topics = []


# User input mode
input_mode = st.radio("Choose input method:", ["Text", "Voice"], horizontal=True)
recognizer = sr.Recognizer()

if input_mode == "Text":
    user_input = st.text_area(
        "Enter your idea or topic:",
        placeholder="Share your brilliant idea here... ✍️",
        value=st.session_state.user_input,
    )
else:
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
            prompt_type = platform.lower()
            prompt = prompt_selector(
                platform.lower(), user_input, post_length, audience_level, prompt_type
            )
            response_data = post_generator(prompt)

        st.session_state.generated_post = response_data["Generated_post"]
        st.session_state.additional_topics = response_data["Additional_Topics"]

# Display generated content
if st.session_state.generated_post:
    st.markdown("### 🎉 Generated Post")
    st.write(st.session_state.generated_post)

# Display additional topics
if st.session_state.additional_topics:
    st.markdown("### 🔥 Additional Topics")
    for index, topic in enumerate(st.session_state.additional_topics):
        if st.button(topic, key=f"topic_{index}"):
            st.session_state.user_input = topic  # Update input with topic
            st._rerun()  # Refresh the UI
