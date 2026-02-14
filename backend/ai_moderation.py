import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def is_message_supportive(message):
    """
    Check if memorial message is appropriate and supportive
    Returns: (is_safe: bool, reason: str)
    """
    try:
        response = openai.moderations.create(input=message)
        result = response.results[0]
        
        if result.flagged:
            return False, "Message contains inappropriate content"
        
        return True, "Message is supportive"
    
    except Exception as e:
        # If AI fails, allow message through (for hackathon)
        return True, "Moderation unavailable"