from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from typing import Dict, Any

class BrandPersonalityAssessor(BaseTool):
    """
    Collects and analyzes brand personality elements including voice, tone, and core values
    to ensure content aligns with brand identity.
    """
    
    brand_voice: str = Field(
        ..., description="How the brand communicates (e.g., 'Professional and authoritative', 'Casual and friendly', 'Playful and energetic', 'Formal and sophisticated')"
    )
    brand_tone: str = Field(
        ..., description="Emotional quality of communication (e.g., 'Encouraging and supportive', 'Confident and bold', 'Warm and approachable', 'Expert and knowledgeable')"
    )
    core_values: str = Field(
        ..., description="Fundamental principles and beliefs that guide the brand (e.g., 'Innovation, quality, customer-first', 'Transparency, sustainability, community', 'Excellence, integrity, collaboration')"
    )
    brand_personality_adjectives: str = Field(
        ..., description="3-5 descriptive words that define the brand personality (e.g., 'trustworthy, innovative, reliable', 'creative, bold, authentic', 'professional, helpful, approachable')"
    )

    def run(self):
        """
        Collects and structures brand personality information for content planning.
        """
        # Step 1: Validate input completeness
        if not all([self.brand_voice, self.brand_tone, self.core_values, self.brand_personality_adjectives]):
            return "Error: All brand personality fields must be completed."
        
        # Step 2: Structure the brand personality data
        brand_personality = {
            "brand_voice": self.brand_voice.strip(),
            "brand_tone": self.brand_tone.strip(),
            "core_values": self.core_values.strip(),
            "personality_adjectives": self.brand_personality_adjectives.strip(),
            "collection_timestamp": self._get_current_timestamp()
        }
        
        # Step 3: Store in context for other tools to access
        # Note: Context storage handled by agency framework
        
        # Step 4: Return confirmation with structured data
        return json.dumps({
            "status": "success",
            "message": "Brand personality assessment completed successfully",
            "data": brand_personality,
            "next_steps": "Proceed with platform selection"
        }, indent=2)

    def _get_current_timestamp(self):
        """Helper method to get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat()

if __name__ == "__main__":
    tool = BrandPersonalityAssessor(
        brand_voice="Professional and authoritative",
        brand_tone="Encouraging and supportive",
        core_values="Innovation, quality, customer-first",
        brand_personality_adjectives="trustworthy, innovative, reliable, helpful"
    )
    print(tool.run())
