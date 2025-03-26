import streamlit as st
import speech_recognition as sr
from main import *

# --- Custom CSS ---
st.markdown(f"""
<style>
    [data-testid=stAppViewContainer] {{
        background-color: #e8d0af;
    }}
    .header {{
        color: #2c5f2d;
        text-align: center;
    }}
    .center-button {{
        display: flex;
        justify-content: center;
        margin: 1rem 0;
    }}
    .stTextArea textarea {{
        margin-bottom: 0.5rem !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- Mode Selection (FIRST - at the top) ---
content_type = st.radio("Content Type:",
    ["📱 General Social Media", "📖 Islamic Guidance"],
    horizontal=True,
    label_visibility="collapsed")

# --- App Structure (AFTER content_type is defined) ---
if content_type == "📖 Islamic Guidance":
    st.image("islamic_header.png", use_column_width=True)
    st.markdown('<h1 class="header">Islamic Wisdom Generator</h1>', unsafe_allow_html=True)
else:
    st.image("social_header.png", use_column_width=True)
    st.markdown('<h1 class="header">Social Media Content Creator</h1>', unsafe_allow_html=True)

    st.markdown(f"""
<style>
    [data-testid=stAppViewContainer] {{
        background-color: {'#e8f4f8' if content_type == "📱 General Social Media" else '#e8d0af'};
    }}
    .header {{
        color: {'#1DA1F2' if content_type == "📱 General Social Media" else '#2c5f2d'};
        text-align: center;
        font-family: {'Helvetica' if content_type == "📱 General Social Media" else 'Times New Roman'};
    }}
</style>
""", unsafe_allow_html=True)

# --- Input Method (Hidden in Islamic Mode) ---
if content_type == "📱 General Social Media":
    input_mode = st.radio("Input Method:", ["Text", "Voice"], 
                        horizontal=True, key="input_mode")
else:
    input_mode = "Text"  # Default for Islamic mode (hidden selector)

st.markdown('</div>', unsafe_allow_html=True)

# --- Core Parameters (Same Line) ---
col1, col2, col3 = st.columns(3)
with col1:
    platform = st.selectbox("Platform:", ["Facebook", "Twitter (X)", "LinkedIn"])
with col2:
    post_length = st.selectbox("Length:", ["Short", "Medium", "Long"])
with col3:
    audience_level = st.selectbox("Audience Level:", ["Beginner", "Intermediate", "Expert"])

# --- Show Advanced Mode ONLY for General Social Media ---
if content_type == "📱 General Social Media":
    advanced_mode = st.checkbox("Advanced Mode 🚀", 
                             help="Uses platform-specific prompts with algorithm-friendly features")
else:
    advanced_mode = False  # Hidden in Islamic mode

# --- Voice Input Handler ---
def handle_voice_input():
    st.markdown('<div class="center-button">', unsafe_allow_html=True)
    if st.button("🎤 Start Recording"):
        with st.spinner("Listening... 🎧"):
            try:
                with sr.Microphone() as source:
                    recognizer = sr.Recognizer()
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)
                    user_input = recognizer.recognize_google(audio)
                    st.session_state.user_input = user_input
                    st.success(f"Transcription: {user_input}")
            except sr.UnknownValueError:
                st.error("Sorry, I couldn't understand the audio.")
            except sr.RequestError:
                st.error("Error with the speech recognition service.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Input Handling ---
user_input = ""

if content_type == "📖 Islamic Guidance":
    st.markdown(f"### 🕌 Shia Islamic Context")
    
    if "islamic_topics" not in st.session_state:
        st.session_state.islamic_topics = get_dynamic_topics()
    
    scholar = st.radio("Scholar Perspective:",
                     ["Shahid Motahari", "Imam Khamenei"],
                     horizontal=True)
    
    islamic_topic = st.selectbox("Trending Topic:",
                               ["Custom Topic"] + st.session_state.islamic_topics,
                                help="Topics updated monthly")
    
    if islamic_topic == "Custom Topic":
        user_input = st.text_area("Your Shia Topic Idea:", 
                                value=st.session_state.get("user_input", ""),
                                placeholder="Enter topic/question...")
    else:
        if "last_topic" not in st.session_state or st.session_state.last_topic != islamic_topic:
            st.session_state.related_questions = get_related_questions(islamic_topic)
            st.session_state.last_topic = islamic_topic
        
        st.markdown("**Suggested Questions**")
        cols = st.columns(3)
        for idx, question in enumerate(st.session_state.related_questions):
            with cols[idx % 3]:
                if st.button(question, key=f"q_{idx}"):
                    st.session_state.user_input = question
                    st.rerun()
        
        user_input = st.text_area("Refine Query:", 
                                value=st.session_state.get("user_input", ""),
                                placeholder="Refine your question...")
else:
    if input_mode == "Text":
        user_input = st.text_area("Enter your idea/topic:", 
                                value=st.session_state.get("user_input", ""),
                                placeholder="Share your idea...")
    else:
        handle_voice_input()
        user_input = st.session_state.get("user_input", "")
        if user_input:
            st.text_area("Transcribed Input:", value=user_input)

# --- Generate Button (Centered) ---
if st.button("Generate Content ✨"):
    if not user_input.strip():
        st.error("Please enter text or record audio!")
    else:
        with st.spinner("🧠 Generating content..."):
            prompt_type = platform.lower()
            if content_type == "📖 Islamic Guidance":
                prompt = islamic_prompt_generator(
                    user_input=user_input,
                    platform=platform,
                    length=post_length,
                    audience_level=audience_level,
                    scholar=scholar,
                    islamic_topic=islamic_topic
                )
            else:
                prompt = prompt_selector(
                    platform.lower(), user_input, post_length, audience_level, prompt_type, isAdvanced=advanced_mode
                )
            response_data = post_generator(prompt)

        st.session_state.generated_post = response_data["Generated_post"]
        st.session_state.additional_topics = response_data["Additional_Topics"]

# --- Display Results ---
if "generated_post" in st.session_state:
    bg_color = '#f8f4e8' if content_type == "📖 Islamic Guidance" else '#ffffff'
    border_color = '#3d6b35' if content_type == "📖 Islamic Guidance" else '#1DA1F2'
    
    st.markdown(f"""
    <div style="
        background: {bg_color};
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid {border_color};
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    ">
        {st.session_state.generated_post}
    </div>
    """, unsafe_allow_html=True)

if "additional_topics" in st.session_state and st.session_state.additional_topics:
    st.markdown("### 🔍 Related Topics")
    cols = st.columns(3)
    for idx, topic in enumerate(st.session_state.additional_topics):
        with cols[idx % 3]:
            if st.button(topic, key=f"topic_{idx}"):
                if content_type == "📖 Islamic Guidance":
                    st.session_state.islamic_topic = "Custom Topic"
                    st.session_state.user_input = topic
                else:
                    st.session_state.user_input = topic
                st.rerun()