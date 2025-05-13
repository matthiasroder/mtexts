"""
AI-powered summary generation for document content.

This module uses the OpenAI API to generate summaries and extract key concepts
from document text content.
"""

import logging
import json
import openai
from openai import OpenAI
import time
import random

# Configure logging
logger = logging.getLogger(__name__)

def generate_content_summary(content, api_key, max_tokens=8000):
    """
    Generate a summary and extract key concepts from document content using OpenAI.
    
    Args:
        content: The document text content to summarize
        api_key: OpenAI API key
        max_tokens: Maximum tokens to process (to prevent exceeding API limits)
    
    Returns:
        Dictionary containing the summary and key concepts
    """
    if not content or not content.strip():
        return {
            'summary': "No content available to summarize.",
            'key_concepts': []
        }
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Truncate content if too long (rough approximation of tokens)
    # About 4 chars per token for English text
    char_limit = max_tokens * 4  
    truncated_content = content[:char_limit] if len(content) > char_limit else content
    
    if len(content) > char_limit:
        logger.warning(f"Content truncated from {len(content)} to {char_limit} characters")
        truncated_content += "\n\n[Content truncated due to length]"
    
    try:
        # Create the prompt for summarization
        system_prompt = """
        You are an expert summarizer and knowledge extractor. Your task is to:
        1. Create a concise summary (3-5 sentences) of the key points in the document
        2. Extract 3-7 key concepts/ideas from the document
        3. Format your response in JSON with two fields: 'summary' and 'key_concepts' (an array)

        Focus on the most important and unique ideas in the text. Ignore routine or boilerplate content.
        """
        
        user_prompt = f"Please summarize this document and extract its key concepts:\n\n{truncated_content}"
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        # Parse the response
        result = json.loads(response.choices[0].message.content)
        
        # Ensure the response has the expected format
        if 'summary' not in result or 'key_concepts' not in result:
            logger.warning("API response missing expected fields")
            result = {
                'summary': result.get('summary', "Summary generation failed."),
                'key_concepts': result.get('key_concepts', [])
            }
        
        return result
        
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        return {
            'summary': f"Error generating summary: {str(e)}",
            'key_concepts': ["Summary generation failed"]
        }


def retry_with_exponential_backoff(func, max_retries=5, initial_delay=1):
    """
    Retry a function with exponential backoff to handle rate limits.
    
    Args:
        func: Function to retry
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
    
    Returns:
        Result of the function call
    """
    retries = 0
    delay = initial_delay
    
    while retries < max_retries:
        try:
            return func()
        except openai.RateLimitError:
            retries += 1
            if retries >= max_retries:
                raise
            
            # Exponential backoff with jitter
            sleep_time = delay * (2 ** retries) + (random.uniform(0, 1))
            logger.warning(f"Rate limited. Retrying in {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
        except Exception:
            # Don't retry other exceptions
            raise