import re
import json
import speech_recognition as sr
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai
from datetime import datetime
from ummalqura.hijri_date import HijriDate

from prompts import *

# Configure Google AI API
google_api_key = "AIzaSyCpmcWbSmE3UwTZwNuHd3yHHQnqfyyTR30"
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel("gemini-2.0-flash")
embedding_function = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
    api_key=google_api_key
)


# Function to get AI-generated content
def get_completion(prompt, temp=0.9):
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(temperature=temp),
        safety_settings=[],
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


def prompt_selector(
    input_message,
    platform,
    post_length,
    audience_level,
    prompt_type="general",
    isAdvanced=False,
):
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


def islamic_prompt_generator(
    user_input, platform, length, audience_level, scholar, islamic_topic
):
    # Build the query based on user inputs
    base_query = ""
    if islamic_topic != "Custom Input":
        base_query += f"Focus on {islamic_topic}"
    if user_input.strip() and (user_input != islamic_topic):
        base_query += f": {user_input}" if base_query else user_input

    if scholar == "Shahid Motahari":
        return rag_post_generator(user_input, platform, length, audience_level)

    prompt = f"""
    Create {platform}-appropriate Islamic content that:
    1. Combines: {base_query or 'General Islamic Teachings'}
    2. Uses {scholar}'s methodology
    3. Includes Quran/Hadith references
    4. Audience level: {audience_level}
    5. Length: {length}
    
    Return JSON format:
    {{
        "Generated_post": "Formatted content...",
        "Additional_Topics": ["3 related topics"]
    }}
    """

    return prompt


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
        "Interfaith Dialogue",
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
        return data.get(
            "questions",
            [f"Explain {topic}", f"Importance of {topic}", f"How to practice {topic}?"],
        )
    except:
        return [
            f"Explain {topic}",
            f"Importance of {topic}",
            f"How to practice {topic}?",
        ]


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


# RAG Functionalities
def find_relevant_chunks(mutahari_collection, input_text, number_similar=10) -> None:
    """
    S2S: Student to Students matching function
    This function takes a resume_text
    returns a list of student_IDs matching his profile.
    """
    try:
        # Query the collection to get the 8 most relevant results
        results = mutahari_collection.query(
            query_texts=input_text,
            n_results=number_similar,
            include=["documents", "metadatas"],
        )

        return results
    except Exception as e:
        print(e)
        return None


def load_vectorDB(vectordb_path):
    # Load mutahari Database
    # This will automatically load any previously saved collections.
    client_mutahari = chromadb.PersistentClient(path=vectordb_path)

    # create embedding function
    embedding_function = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
        api_key=google_api_key, task_type="RETRIEVAL_QUERY"
    )
    mutahari_collection = client_mutahari.get_or_create_collection(
        name="mutahari_collection",
        embedding_function=embedding_function,
        metadata={"hnsw:space": "cosine"},  # l2 is the default
    )
    return mutahari_collection


def rag_post_generator(input_message, platform, post_length, audience_level):
    mutahari_collection = load_vectorDB(
        "vectorDBs\mutahari",
    )
    relevant_context = find_relevant_chunks(mutahari_collection, input_message)
    prompt = rag_prompt(
        input_message, platform, post_length, audience_level, relevant_context
    )
    return prompt
