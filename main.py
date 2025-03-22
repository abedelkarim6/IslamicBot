import re
import json
import speech_recognition as sr
import google.generativeai as genai

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
            "Additional_Topics": [],
        }
