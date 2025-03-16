import streamlit as st
import speech_recognition as sr
import google.generativeai as genai
import json
import re

# Configure Google AI API
google_api_key = "AIzaSyCpmcWbSmE3UwTZwNuHd3yHHQnqfyyTR30"  # Your API key
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get AI-generated post
def get_completion(prompt, temp=0.9):
    response = model.generate_content(
        prompt, generation_config=genai.types.GenerationConfig(temperature=temp),
        safety_settings=[],  # Remove any filters causing partial responses
    )
    return response.text

def extract_json(text):
    """ Extracts JSON data from a raw text response """
    match = re.search(r"\{.*\}", text, re.DOTALL)  # Extract anything between `{}` brackets
    if match:
        try:
            return json.loads(match.group())  # Convert to Python dictionary
        except json.JSONDecodeError:
            pass
    return None

def LLM_prompt(input_message, platform, post_length, audience_level):
    prompt = f"""
        Your task is to generate engaging social media posts based on the given user input.  

        - Analyze the user's message intent and context.  
        - Generate a compelling idea that aligns with the chosen platform.  
        - Ensure the post includes unique facts about the chosen topic that will captivate the audience.
        - Optimize for the target audience and preferred post length.  
        - Ensure the content is relevant, engaging, and fits the platform’s style.
        
        Return ONLY JSON format (no extra text).  

        **Strictly format response as JSON:**  
        ```json
        {{
            "Generated_post": "Engaging post text",
            "Additional_Topics": ["Topic 1", "Topic 2", "Topic 3"]
        }}
        ```

        User Input:  
        ```json
        {{
            "message": "{input_message}",
            "target_platform": "{platform}",
            "post_length": "{post_length}",
            "audience_level": "{audience_level}"
        }} 
        ```
    """

    response_text = get_completion(prompt)

    # Try extracting JSON
    response_data = extract_json(response_text)

    if response_data:
        return response_data  # Valid JSON found
    else:
        return {
            "Generated_post": "⚠️ AI response was not in expected format. Try again.",
            "Additional_Topics": []
        }

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
    user_input = st.text_area("Enter your idea or topic:", placeholder="Share your brilliant idea here... ✍️", value=st.session_state.user_input)
else:
    if 'voice_text' not in st.session_state:
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
        user_input = st.text_area("Edit Transcribed Text:", value=st.session_state.voice_text)

# Platform selection
platform = st.selectbox("Choose a social media platform:", ["Facebook", "Twitter (X)", "LinkedIn"])

# Extra options
post_length = st.selectbox("Post Length:", ["Short", "Medium", "Long"])
audience_level = st.selectbox("Audience Level:", ["Beginner", "Intermediate", "Expert"])

# Generate content
if st.button("Generate Content ✨"):
    if not user_input.strip():
        st.error("Please enter some text or record your voice!")
    else:
        with st.spinner("🧠 Generating content..."):
            response_data = LLM_prompt(user_input, platform, post_length, audience_level)

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
            st.rerun()  # Refresh the page to reflect the change
