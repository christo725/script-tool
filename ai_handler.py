import os
from typing import Dict, Any
import anthropic
import openai
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize API clients
anthropic_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Configure Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def generate_prompt(settings: Dict[str, Any], article_text: str) -> str:
    """Generate a prompt based on all settings and the input article."""
    
    # Base prompt structure
    prompt = f"""You are an expert script writer specializing in {settings['video_type']} videos.
    
Writing Style:
- Tone: {settings['tone']}
- Target Length: {settings['length']} minutes
- Information Density: {settings['density']} (0=Low, 1=High)
- Knowledge Level: {settings['knowledge_level']}
- Geographic Background: {settings['geo_background']}
- Speaking Style: Similar to {settings['similar_to']}
- Language/Region: {settings['language']}

{f'''Opinion/Stance Guidelines:
- Political: {settings["political"]}
- Economic: {settings["economic"]}
- Social: {settings["social"]}''' if settings['enable_opinions'] else 'Maintain neutral, factual stance'}

Additional Instructions:
{settings['additional_instructions']}

Please convert the following article into a video script following all the above guidelines. Format the output as a markdown table with two columns using this exact format:

| NARRATION | VISUALS |
|-----------|---------|
| (narration text) | (visual description) |

Make sure:
1. Include the header row and separator exactly as shown above
2. Each cell should start with a space after the | for readability
3. Don't include any text before or after the table
4. Keep each row's content concise and clear
5. Use proper markdown table syntax with | as column separators

Here's the article to convert:

{article_text}

Remember:
1. Break the narration into natural speaking segments
2. Only put speakable text in the NARRATION column
3. Provide specific, actionable visual suggestions in the VISUALS column
4. Maintain consistent tone and style throughout
5. Each row should represent roughly the same amount of speaking time
"""
    return prompt

def generate_script(settings: Dict[str, Any], article_text: str) -> str:
    """Generate a script using the selected AI model."""
    
    prompt = generate_prompt(settings, article_text)
    
    try:
        if settings['ai_model'] == "Claude 3.7":
            response = anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
            
        elif settings['ai_model'] == "GPT 4o":
            response = openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
                temperature=0.7
            )
            return response.choices[0].message.content
            
        elif settings['ai_model'] == "Gemini Pro":
            # Create a GenerativeModel instance with the correct model name
            model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
            
            # Generate content using the v1 API
            response = model.generate_content(
                contents=[{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            )
            return response.text
            
        else:
            return "Error: Invalid AI model selected"
            
    except Exception as e:
        return f"Error generating script: {str(e)}" 