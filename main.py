import re
import json
import speech_recognition as sr
import google.generativeai as genai
from datetime import datetime
from ummalqura.hijri_date import HijriDate

from prompts import *

# Configure Google AI API
google_api_key = "AIzaSyCpmcWbSmE3UwTZwNuHd3yHHQnqfyyTR30"  # Replace with your actual API key
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# Function to get AI-generated content
def get_completion(prompt, temp=0.9):
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(temperature=temp),
        safety_settings=[]
    )
    return response  # Return the full response object

# Extract JSON from response
def extract_json(text):
    match = re.search(
        r"\{.*\}", text, re.DOTALL
    )  # Extract anything between `{}` brackets
    if match:
        try:
            return json.loads(match.group())  # Convert to Python dictionary
        except json.JSONDecodeError:
            pass
    return None

def prompt_selector(input_message, platform, post_length, audience_level, prompt_type="general", isAdvanced=False):
    # Use general prompt for non-advanced mode
    if not isAdvanced:
        return general_prompt(input_message, platform, post_length, audience_level)
    
    # Platform-specific prompts for advanced mode
    if prompt_type == "facebook":
        return facebook_prompt(input_message, platform, post_length, audience_level)
    elif prompt_type == "twitter":
        return twitter_prompt(input_message, platform, post_length, audience_level)
    elif prompt_type == "linkedin":
        return linkedin_prompt(input_message, platform, post_length, audience_level)
    
    # Fallback to general prompt
    return general_prompt(input_message, platform, post_length, audience_level)

# Get current Gregorian month and year
gregorian_month = datetime.now().strftime("%B")  # e.g., "March"
gregorian_year = datetime.now().year  # e.g., 2025

# Get current Hijri month and year
hijri_date = HijriDate.today()
hijri_month = hijri_date.month_name  # e.g., "Sha'ban"
hijri_year = hijri_date.year  # e.g., 1446

def get_dynamic_topics():
    """Fetch trending Shia Islamic topics based on both Gregorian & Hijri months and years."""
    
    # Format the prompt with both calendar systems
    prompt = f"""
    Suggest **10 trending Shia Islamic discussion topics** for {gregorian_month} {gregorian_year} ({hijri_month} {hijri_year}).
    The topics must be **short (3-4 words each)**.
    
    Format the response as a JSON array:
    {{
        "topics": ["Topic 1", ..., "Topic 10"]
    }}
    """

    try:
        response = model.generate_content(prompt)
        data = extract_json(response.text)
        return data.get("topics", get_default_topics())
    except:
        return get_default_topics()

def get_default_topics():
    """Fallback topics"""
    return [
        "Social Justice",
        "Family Values",
        "Modern Challenges",
        "Spiritual Growth",
        "Daily Worship",
        "Community Service",
        "Personal Development",
        "Faith & Reason",
        "Ethical Living",
        "Interfaith Dialogue"
    ]

# Add to main.py
def get_related_questions(topic):
    """Generate 3 discussion questions related to an Islamic topic"""
    prompt = f"""
    Provide **3 trending Islamic discussion questions** about '{topic}' that are highly relevant in **{hijri_month} {hijri_year}**.

    - Keep each question **very short (max 7-10 words)**.
    - Focus on **what Muslims are discussing this month**.
    
    Return as JSON: {{"questions": ["Question 1", ...]}}
    """
    try:
        response = model.generate_content(prompt)
        data = extract_json(response.text)
        return data.get("questions", [f"Explain {topic}", f"Importance of {topic}", f"How to practice {topic}?"])
    except:
        return [f"Explain {topic}", f"Importance of {topic}", f"How to practice {topic}?"]
    
def post_generator(prompt):
    """Generates a social media post using AI"""
    response = get_completion(prompt)  # This returns a GenerateContentResponse object
    
    # Try extracting JSON from the response text
    response_data = extract_json(response.text)  # Access the .text property

    if response_data:
        return response_data  # Valid JSON found
    else:
        return {
            "Generated_post": "⚠️ AI response was not in expected format. Try again.",
            "Additional_Topics": [],
        }
