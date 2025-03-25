import re
import json
import speech_recognition as sr
import google.generativeai as genai

from prompts import *

# Configure Google AI API
google_api_key = "AIzaSyCpmcWbSmE3UwTZwNuHd3yHHQnqfyyTR30"  # Your API key
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


# Function to get AI-generated post
def get_completion(prompt, temp=0.9):
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(temperature=temp),
        safety_settings=[],  # Remove any filters causing partial responses
    )
    return response.text


def extract_json(text):
    """Extracts JSON data from a raw text response"""
    match = re.search(
        r"\{.*\}", text, re.DOTALL
    )  # Extract anything between `{}` brackets
    if match:
        try:
            return json.loads(match.group())  # Convert to Python dictionary
        except json.JSONDecodeError:
            pass
    return None


def prompt_selector(
    input_message, platform, post_length, audience_level, prompt_type="general"
):
    if prompt_type == "facebook":
        return facebook_prompt(input_message, platform, post_length, audience_level)

    elif prompt_type == "twitter":
        return twitter_prompt(input_message, platform, post_length, audience_level)

    elif prompt_type == "linkedin":
        return linkedin_prompt(input_message, platform, post_length, audience_level)

    else:
        return general_prompt(input_message, platform, post_length, audience_level)


def post_generator(prompt):
    """Generates a social media post using AI"""
    response_text = get_completion(prompt)

    # Try extracting JSON
    response_data = extract_json(response_text)

    if response_data:
        return response_data  # Valid JSON found
    else:
        return {
            "Generated_post": "⚠️ AI response was not in expected format. Try again.",
            "Additional_Topics": [],
        }
