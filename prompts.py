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
        Your task is to generate an engaging Facebook post based on the input, then suggest 3-5 relevant topics for future posts.  

        **Step 1: Generate Post**  
        - Write in a friendly, conversational tone with emojis and a CTA/question.  
        - Keep paragraphs short and match the requested length:  
          - **Short**: 1 paragraph  
          - **Medium**: 2 paragraphs  
          - **Long**: 3+ paragraphs  

        **Step 2: Suggest Topics**  
        - Extract 3-5 concise topics from the generated post.  
        - Topics should be keywords/phrases (e.g., "Sustainable Packaging") that a user could select to generate a new post.  

        **Examples:**  
        Example 1:  
        User Input:  
        {{  
            "message": "Launching a reusable water bottle campaign",  
            "target_platform": "Facebook",  
            "post_length": "Short",  
            "audience_level": "General"  
        }}  
        Generated Post: "💧 Stay hydrated, save the planet! Our new reusable bottles are here to replace single-use plastics. 🌍 Tag a friend who needs this!  #EcoFriendly"  
        Additional_Topics: ["Reusable Products", "Plastic-Free Living", "Eco-Friendly Gifts"]  

        Example 2:  
        User Input:  
        {{  
            "message": "Host a virtual cooking class",  
            "target_platform": "Facebook",  
            "post_length": "Medium",  
            "audience_level": "Expert"  
        }}  
        Generated Post: "👨🍳 Sharpen your skills! Join our live virtual cooking class this Sunday. We’ll master 3 gourmet recipes in 60 minutes. Limited spots—comment “Cooking” to reserve! 🔥 What recipe should we tackle next? #FoodieFun"  
        Additional_Topics: ["Virtual Events", "Gourmet Cooking", "Interactive Learning"]  

        Now, generate a post and topics for this input:  
        User Input:  
        ```json  
        {{  
            "message": "{input_message}",  
            "target_platform": "{platform}",  
            "post_length": "{post_length}",  
            "audience_level": "{audience_level}"  
        }}  
        ```  

        **Strict Output Format (JSON):**  
        ```json  
        {{  
            "Generated_post": "Engaging post text",  
            "Additional_Topics": ["Topic 1", "Topic 2", "Topic 3"]  
        }}  
        ```  
    """


def twitter_prompt(input_message, platform, post_length, audience_level):
    return f"""
        Your task is to generate a concise, viral-friendly tweet based on the input, then suggest 3-5 relevant topics for future posts.  

        **Step 1: Generate Tweet**  
        - Keep it punchy (≤280 characters), with a hook in the first 5 words.  
        - Use hashtags, emojis, slang/memes, and a CTA (e.g., "Retweet," "Tag a friend").  
        - Match the requested length:  
          - **Short**: 1 paragraph (≤2 sentences)  
          - **Medium**: 2 paragraphs (3-4 sentences)  
          - **Long**: 3+ paragraphs (5+ sentences)  

        **Step 2: Suggest Topics**  
        - Extract 3-5 concise topics from the tweet for follow-up content.  

        **Examples:**  
        Example 1 (Short, #FreePalestine):  
        User Input:  
        {{  
            "message": "Raise awareness about Gaza humanitarian crisis",  
            "target_platform": "Twitter",  
            "post_length": "Short",  
            "audience_level": "General"  
        }}  
        Generated Post: "🚨 Gaza hospitals at breaking point. 150+ lives lost today. Retweet to demand action. #SaveGaza #HumanitarianCrisis 💔"  
        Additional_Topics: ["Humanitarian Aid", "Ceasefire Now", "Gaza Crisis"]  

        Example 2 (Medium, Tech Hack):  
        User Input:  
        {{  
            "message": "Share a viral coding shortcut",  
            "target_platform": "Twitter",  
            "post_length": "Medium",  
            "audience_level": "Expert"  
        }}  
        Generated Post: "🔥 HACK: Use `git stash` to save unfinished work WITHOUT committing. 🚀\n\nTag a dev who still uses `git commit -m 'WIP'` 👇 #GitTips #CodeLife"  
        Additional_Topics: ["Dev Hacks", "Git Tricks", "Coding Efficiency"]  

        Now, generate a tweet and topics for this input:  
        User Input:  
        ```json  
        {{  
            "message": "{input_message}",  
            "target_platform": "{platform}",  
            "post_length": "{post_length}",  
            "audience_level": "{audience_level}"  
        }}  
        ```  

        **Strict Output Format (JSON):**  
        ```json  
        {{  
            "Generated_post": "Engaging tweet text",  
            "Additional_Topics": ["Topic 1", "Topic 2", "Topic 3"]  
        }}  
        ```  
    """


def linkedin_prompt(input_message, platform, post_length, audience_level):
    return f"""
        Your task is to generate a professional LinkedIn post based on the input, then suggest 3-5 relevant topics for future posts.  

        **Step 1: Generate Post**  
        - Use a thought-provoking, value-driven tone with industry insights.  
        - Include a CTA (e.g., "Share your thoughts," "Tag a colleague").  
        - Match the requested length:  
          - **Short**: 1 paragraph  
          - **Medium**: 2 paragraphs  
          - **Long**: 3+ paragraphs  

        **Step 2: Suggest Topics**  
        - Extract 3-5 concise topics from the post for follow-up content.  
        - Topics should be keywords/phrases (e.g., "AI in Healthcare") that a user could select to generate a new post.  

        **Examples:**  
        Example 1:  
        User Input:  
        {{  
            "message": "Promote Harvard alumni networking event",  
            "target_platform": "LinkedIn",  
            "post_length": "Medium",  
            "audience_level": "Expert"  
        }}  
        Generated Post: "🎓 Harvard alumni, mark your calendars! Join us on Oct 15th for an exclusive virtual networking event. Reconnect with classmates, share career insights, and hear from keynote speaker Jane Smith (HBS '08). Let’s leverage our collective wisdom—what’s one lesson from your time at Harvard that still drives you today?  #HarvardAlumni #Networking"  
        Additional_Topics: ["Alumni Success Stories", "Leadership Development", "Harvard Networking"]  

        Example 2:  
        User Input:  
        {{  
            "message": "Hiring a Senior Software Engineer",  
            "target_platform": "LinkedIn",  
            "post_length": "Short",  
            "audience_level": "Expert"  
        }}  
        Generated Post: "🚀 We’re hiring! Seeking a Senior Software Engineer to lead our cloud infrastructure team. If you’re passionate about scalable systems and mentorship, reach out. Let’s build the future of tech together! 💻 Apply now → [link] #Hiring #SoftwareEngineering"  
        Additional_Topics: ["Tech Careers", "Cloud Infrastructure", "Engineering Leadership"]  

        Now, generate a post and topics for this input:  
        User Input:  
        ```json  
        {{  
            "message": "{input_message}",  
            "target_platform": "{platform}",  
            "post_length": "{post_length}",  
            "audience_level": "{audience_level}"  
        }}  
        ```  

        **Strict Output Format (JSON):**  
        ```json  
        {{  
            "Generated_post": "Engaging post text",  
            "Additional_Topics": ["Topic 1", "Topic 2", "Topic 3"]  
        }}  
        ```  
    """


def rag_prompt(input_message, platform, post_length, audience_level, relevant_context):
    return f"""
         Your task is to generate an engaging social media post using the context given below.  

        - Utilize the provided chunks as a knowledge base to craft an informative and captivating post.  
        - Analyze the user's intent and ensure the content aligns with the chosen platform.  
        - Structure the post to highlight unique insights from the retrieved information.  
        - Optimize for the target audience, preferred post length, and platform-specific style.  
        - Ensure coherence, fluency, and engagement while maintaining factual accuracy.  

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
        main title: {input_message}
        context: {relevant_context}

    """
