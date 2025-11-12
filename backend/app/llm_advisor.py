"""
LLM-based camera parameter suggestion module
"""

import os
from typing import Dict, Any, Optional
from openai import OpenAI


class LLMAdvisor:
    """LLM-based camera parameter advisor"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
    
    def suggest(
        self, 
        prompt: str, 
        current_settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate camera parameter suggestions from natural language prompt
        
        Args:
            prompt: User's natural language request
            current_settings: Optional current camera settings
            
        Returns:
            Dictionary with suggested parameters and explanation
        """
        if not self.client:
            return self._rule_based_suggestions(prompt, current_settings)
        
        try:
            # Build context from current settings
            context = ""
            if current_settings:
                context = f"\n\nCurrent settings: {self._format_settings(current_settings)}"
            
            # Create system message
            system_message = """You are an expert photographer and camera settings advisor. 
Your job is to suggest optimal camera settings based on user requests. 
Provide specific values for ISO, aperture (f-stop), shutter speed, and any other relevant parameters.
Always explain your reasoning briefly."""
            
            # Create user message
            user_message = f"User request: {prompt}{context}\n\nSuggest optimal camera settings."
            
            # Call LLM
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse response
            suggestion_text = response.choices[0].message.content
            
            # Extract structured parameters (simple parsing)
            suggestions = self._parse_llm_response(suggestion_text)
            suggestions["explanation"] = suggestion_text
            suggestions["source"] = "llm"
            
            return suggestions
            
        except Exception as e:
            # Fallback to rule-based
            return self._rule_based_suggestions(prompt, current_settings)
    
    def _format_settings(self, settings: Dict[str, Any]) -> str:
        """Format settings dictionary to readable string"""
        formatted = []
        for key, value in settings.items():
            formatted.append(f"{key}: {value}")
        return ", ".join(formatted)
    
    def _parse_llm_response(self, text: str) -> Dict[str, Any]:
        """
        Parse LLM response to extract structured parameters
        
        Args:
            text: LLM response text
            
        Returns:
            Dictionary with extracted parameters
        """
        settings = {}
        
        # Simple keyword extraction
        text_lower = text.lower()
        
        # Extract ISO
        if "iso" in text_lower:
            for word in text.split():
                if word.isdigit() and int(word) in [100, 200, 400, 800, 1600, 3200, 6400]:
                    settings["iso"] = int(word)
                    break
        
        # Extract aperture (f-stop)
        if "f/" in text_lower or "aperture" in text_lower:
            import re
            aperture_match = re.search(r'f/(\d+\.?\d*)', text_lower)
            if aperture_match:
                settings["aperture"] = f"f/{aperture_match.group(1)}"
        
        # Extract shutter speed
        if "shutter" in text_lower or "1/" in text:
            import re
            shutter_match = re.search(r'1/(\d+)', text)
            if shutter_match:
                settings["shutter_speed"] = f"1/{shutter_match.group(1)}s"
        
        return settings
    
    def _rule_based_suggestions(
        self, 
        prompt: str, 
        current_settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Rule-based suggestions when LLM is unavailable
        
        Args:
            prompt: User's request
            current_settings: Optional current settings
            
        Returns:
            Dictionary with suggested parameters
        """
        prompt_lower = prompt.lower()
        
        # Portrait photography
        if any(word in prompt_lower for word in ["portrait", "person", "people", "face"]):
            return {
                "iso": 400,
                "aperture": "f/2.8",
                "shutter_speed": "1/125s",
                "explanation": "Portrait settings: Wide aperture (f/2.8) for shallow depth of field, moderate ISO and shutter speed",
                "source": "rule-based"
            }
        
        # Landscape photography
        elif any(word in prompt_lower for word in ["landscape", "scenery", "mountain", "nature"]):
            return {
                "iso": 100,
                "aperture": "f/11",
                "shutter_speed": "1/60s",
                "explanation": "Landscape settings: Narrow aperture (f/11) for deep depth of field, low ISO for quality",
                "source": "rule-based"
            }
        
        # Action/Sports
        elif any(word in prompt_lower for word in ["action", "sport", "fast", "moving", "running"]):
            return {
                "iso": 800,
                "aperture": "f/4",
                "shutter_speed": "1/1000s",
                "explanation": "Action settings: Fast shutter (1/1000s) to freeze motion, moderate aperture and higher ISO",
                "source": "rule-based"
            }
        
        # Low light
        elif any(word in prompt_lower for word in ["dark", "night", "low light", "indoor"]):
            return {
                "iso": 1600,
                "aperture": "f/2.8",
                "shutter_speed": "1/60s",
                "explanation": "Low light settings: High ISO (1600), wide aperture (f/2.8) to gather more light",
                "source": "rule-based"
            }
        
        # Default general purpose
        else:
            return {
                "iso": 400,
                "aperture": "f/5.6",
                "shutter_speed": "1/125s",
                "explanation": "General purpose settings: Balanced settings suitable for most situations",
                "source": "rule-based"
            }


# Global advisor instance
_advisor = LLMAdvisor()


def suggest_parameters(
    prompt: str, 
    current_settings: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Main function to get parameter suggestions
    
    Args:
        prompt: User's natural language request
        current_settings: Optional current camera settings
        
    Returns:
        Dictionary with suggested parameters
    """
    return _advisor.suggest(prompt, current_settings)
