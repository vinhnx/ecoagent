"""Advanced Gemini utilities for EcoAgent system."""

import google.generativeai as genai
from typing import Dict, List, Any, Optional
import os
import warnings
from google.generativeai.types import GenerationConfig

# Suppress warnings about unrecognized FinishReason enum values
warnings.filterwarnings("ignore", message="Unrecognized.*FinishReason.*enum value", category=UserWarning)

class GeminiClient:
    """A client for interacting with Google's Gemini models."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini client.

        Args:
            api_key: Gemini API key. If not provided, will use GOOGLE_API_KEY environment variable.
        """
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv("GOOGLE_API_KEY")

        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GOOGLE_API_KEY environment variable.")

        genai.configure(api_key=self.api_key)

        # Available models - using the best available for different tasks
        self.models = {
            "text": "gemini-2.5-flash-lite",
            "vision": "gemini-2.0-flash-exp",
            "embedding": "embedding-001"
        }

    def generate_content(self,
                        prompt: str,
                        model_name: str = "gemini-2.5-flash-lite",
                        generation_config: Optional[Dict] = None,
                        safety_settings: Optional[Dict] = None) -> str:
        """
        Generate content using Gemini models.

        Args:
            prompt: Input prompt for content generation
            model_name: Name of the model to use
            generation_config: Configuration for generation (temperature, max_tokens, etc.)
            safety_settings: Safety settings for content generation

        Returns:
            Generated content as string
        """
        model = genai.GenerativeModel(model_name=model_name)

        default_config = GenerationConfig(
            temperature=0.7,
            max_output_tokens=2048,
            top_p=0.95,
            top_k=40
        )

        if generation_config:
            # Update default config with provided config
            for key, value in generation_config.items():
                setattr(default_config, key, value)

        response = model.generate_content(
            prompt,
            generation_config=default_config,
            safety_settings=safety_settings
        )

        return response.text if response.text else ""

    def generate_structured_output(self,
                                 prompt: str,
                                 output_schema: Dict[str, Any],
                                 model_name: str = "gemini-2.5-flash-lite") -> Dict[str, Any]:
        """
        Generate structured output based on a schema using Gemini.

        Args:
            prompt: Input prompt for content generation
            output_schema: Schema defining the expected output structure
            model_name: Name of the model to use

        Returns:
            Structured output as dictionary
        """
        # Format the prompt to request structured output
        schema_str = str(output_schema)
        structured_prompt = f"""
        {prompt}

        Please provide your response in the following JSON format:
        {schema_str}

        Respond only with the JSON object, no additional text.
        """

        model = genai.GenerativeModel(model_name=model_name)

        response = model.generate_content(
            structured_prompt,
            generation_config=GenerationConfig(
                response_mime_type="application/json",
                temperature=0.1
            )
        )

        import json
        try:
            return json.loads(response.text) if response.text else {}
        except json.JSONDecodeError:
            # Fallback: try to extract JSON from response if Gemini didn't format properly
            import re
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"error": "Could not parse structured output", "raw_response": response.text}

    def analyze_image(self, image_path: str, prompt: str) -> str:
        """
        Analyze an image using Gemini's vision capabilities.

        Args:
            image_path: Path to the image file
            prompt: Prompt to guide the image analysis

        Returns:
            Analysis result as string
        """
        model = genai.GenerativeModel(model_name=self.models["vision"])

        import PIL.Image
        image = PIL.Image.open(image_path)

        response = model.generate_content([prompt, image])
        return response.text if response.text else ""

    def embed_content(self, text: str, model_name: str = "embedding-001") -> List[float]:
        """
        Generate embeddings for text content.

        Args:
            text: Text to generate embeddings for
            model_name: Name of the embedding model to use

        Returns:
            Embedding vector as list of floats
        """
        result = genai.embed_content(
            model=model_name,
            content=text,
            task_type="semantic_similarity"
        )
        return result['embedding']

# Global Gemini client instance (will be initialized when API key is available)
gemini_client = None

def get_gemini_client() -> Optional[GeminiClient]:
    """
    Get the global Gemini client instance.

    Returns:
        GeminiClient instance or None if not initialized
    """
    global gemini_client
    if gemini_client is None:
        try:
            gemini_client = GeminiClient()
        except ValueError:
            # API key not available, return None
            pass
    return gemini_client

# Function to use Gemini for sustainability analysis
def analyze_sustainability_practice(practice_description: str) -> Dict[str, Any]:
    """
    Use Gemini to analyze a sustainability practice for effectiveness and impact.

    Args:
        practice_description: Description of the sustainability practice

    Returns:
        Analysis of the practice including effectiveness, difficulty, and environmental impact
    """
    client = get_gemini_client()
    if not client:
        # Return mock response if Gemini is not available
        return {
            "effectiveness": "Medium",
            "difficulty": "Low",
            "environmental_impact": "Positive",
            "additional_notes": "Analysis requires Gemini API access"
        }

    prompt = f"""
    Please analyze the following sustainability practice for a personal environmental impact tracking system:

    Practice: {practice_description}

    Analyze this practice across these dimensions:
    1. Effectiveness: How effective is this practice at reducing environmental impact (High/Medium/Low)
    2. Difficulty: How difficult is this practice to implement (High/Medium/Low)
    3. Environmental Impact: What type of environmental impact does this address (Carbon/Water/Waste/Biodiversity/etc.)
    4. Additional Notes: Any other relevant information for the user

    Respond in JSON format with keys: effectiveness, difficulty, environmental_impact, additional_notes
    """

    schema = {
        "effectiveness": "string",
        "difficulty": "string",
        "environmental_impact": "string",
        "additional_notes": "string"
    }

    return client.generate_structured_output(prompt, schema)

# Function to get personalized recommendations using Gemini
def get_personalized_recommendations(user_profile: Dict[str, Any], goals: List[str]) -> List[Dict[str, Any]]:
    """
    Use Gemini to generate personalized sustainability recommendations.

    Args:
        user_profile: Dictionary containing user information (location, lifestyle, etc.)
        goals: List of user goals

    Returns:
        List of personalized recommendations
    """
    client = get_gemini_client()
    if not client:
        # Return mock recommendations if Gemini is not available
        return [
            {"action": "Reduce meat consumption", "reason": "Animal agriculture has high environmental impact", "difficulty": "Medium", "impact": "High"},
            {"action": "Use public transport", "reason": "Reduces carbon emissions from personal vehicles", "difficulty": "Medium", "impact": "High"}
        ]

    profile_str = str(user_profile)
    goals_str = ", ".join(goals)

    prompt = f"""
    Based on the following user profile and goals, provide personalized sustainability recommendations:

    User Profile: {profile_str}
    Goals: {goals_str}

    Provide 3-5 specific, actionable recommendations that are tailored to this user's situation.
    For each recommendation, include:
    1. Specific action to take
    2. Reason why it would be effective for this user
    3. Estimated difficulty of implementation
    4. Expected environmental impact

    Respond as a JSON array of recommendation objects with keys: action, reason, difficulty, impact
    """

    schema = [
        {
            "action": "string",
            "reason": "string",
            "difficulty": "string",
            "impact": "string"
        }
    ]

    return client.generate_structured_output(prompt, {"recommendations": schema}).get("recommendations", [])