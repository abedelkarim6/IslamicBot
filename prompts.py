def general_prompt(input_message, platform, post_length, audience_level):
    return f"""
        Your task is to generate engaging social media posts based on the given user input.  

        - Analyze the user's message intent and context.  
        - Generate a compelling idea that aligns with the chosen platform.  
        - Ensure the post includes unique facts about the chosen topic that will captivate the audience.
        - Optimize for the target audience and preferred post length.  
        - Keep the post within the requested length:  
          - **Short**: 1 paragraph  
          - **Medium**: 2 paragraphs  
          - **Long**: 3 or more paragraphs  
        - The writing style should match the platform’s tone and audience expectations. 
        
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


def facebook_prompt(input_message, platform, post_length, audience_level):
    return f"""
        Your task is to generate an engaging and shareable Facebook post based on the given user input.  

        - Write in a friendly, conversational tone that encourages engagement.  
        - Include a question, call-to-action (CTA), or emotional hook to spark interaction.  
        - Use emojis where relevant to enhance appeal.  
        - Keep paragraphs short for easy readability.  
        - Optimize the post length to match Facebook's best practices for engagement.  
        
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


def twitter_prompt(input_message, platform, post_length, audience_level):
    return f"""
        Your task is to generate a concise, impactful, and viral-friendly tweet based on the given user input.  

        - Keep the message short and punchy (within 280 characters).  
        - Use hashtags strategically to boost discoverability.  
        - Include a hook in the first few words to grab attention.  
        - If relevant, use a trending topic or meme format.  
        - Add a CTA or ask a question to increase engagement.  

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


def linkedin_prompt(input_message, platform, post_length, audience_level):
    return f"""
        Your task is to generate a professional and insightful LinkedIn post based on the given user input.  

        - Write in a thought-provoking and value-driven style.  
        - Include industry insights, personal experiences, or expert opinions.  
        - Structure with short paragraphs and line breaks for readability.  
        - Add a CTA that encourages discussion or engagement.  
        - Avoid excessive emojis or slang—keep it professional yet engaging.  

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
