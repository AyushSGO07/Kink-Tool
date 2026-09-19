from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
    template = 
    """User Preferences:
    - User Sexuality / Orientation: {sexuality}
    - Preferred Body Features (e.g., petite, curvy, muscular, tall): {body_features}
    - Age Range Preference: {age}   
    
    Instructions:
    1. Analyze the user preferences provided above.
    2. Search your knowledge base to identify 3 to 5 well-known adult performers who closely match these specific physical characteristics and aesthetic vibes.
    3. Ensure the performers match the requested gender and sexuality alignment.
    4. For each recommendation, provide a brief, objective summary of why they are a good match based on the provided body features.
    5. Do not generate explicit sexual narratives or graphic descriptions; focus strictly on matching the physical characteristics, aesthetic, and
  professional persona of the performers to the user request.
    
    Output Format:
    Return the response EXCLUSIVELY as a valid JSON array containing objects with the following structure. Do not include markdown formatting or introductory
  text.
  
    ]""",
    input_variables= ['sexuality','body_features','age'],validate_template=True
)
template.save('prompt.json')