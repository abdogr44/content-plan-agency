from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from typing import List, Dict, Any

class PlatformSelector(BaseTool):
    """
    Allows users to select which social media platforms to focus on for content planning
    and sets platform priorities for strategic content distribution.
    """
    
    selected_platforms: List[str] = Field(
        ..., description="List of chosen platforms from: Facebook, Instagram, LinkedIn (e.g., ['Instagram', 'LinkedIn'] or ['Facebook', 'Instagram', 'LinkedIn'])"
    )
    platform_priorities: str = Field(
        default="Equal focus on all selected platforms", 
        description="Optional ranking or focus areas for selected platforms (e.g., 'Primary focus on Instagram, secondary on LinkedIn', 'Equal focus on all platforms')"
    )

    def run(self):
        """
        Validates platform selection and structures platform configuration.
        """
        # Step 1: Validate platform selection
        valid_platforms = ["Facebook", "Instagram", "LinkedIn"]
        invalid_platforms = [p for p in self.selected_platforms if p not in valid_platforms]
        
        if invalid_platforms:
            return f"Error: Invalid platforms selected: {invalid_platforms}. Valid options are: {valid_platforms}"
        
        if not self.selected_platforms:
            return "Error: At least one platform must be selected."
        
        # Step 2: Structure platform configuration
        platform_config = {
            "selected_platforms": self.selected_platforms,
            "platform_priorities": self.platform_priorities.strip(),
            "platform_count": len(self.selected_platforms),
            "collection_timestamp": self._get_current_timestamp()
        }
        
        # Step 3: Store in context for other tools to access
        # Note: Context storage handled by agency framework
        
        # Step 4: Return confirmation with structured data
        return json.dumps({
            "status": "success",
            "message": f"Platform selection completed for {len(self.selected_platforms)} platform(s)",
            "data": platform_config,
            "platform_guidance": self._get_platform_guidance(self.selected_platforms),
            "next_steps": "Proceed with content strategy analysis"
        }, indent=2)

    def _get_platform_guidance(self, platforms: List[str]) -> Dict[str, str]:
        """Provides platform-specific guidance for content planning"""
        guidance = {
            "Facebook": "Focus on community building, longer-form content, and video content. Optimal posting times: 9 AM - 3 PM",
            "Instagram": "Emphasize visual storytelling, stories, reels, and high-quality imagery. Optimal posting times: 11 AM - 1 PM, 5 PM - 7 PM",
            "LinkedIn": "Professional content, thought leadership, industry insights, and B2B networking. Optimal posting times: 8 AM - 10 AM, 12 PM - 2 PM"
        }
        return {platform: guidance[platform] for platform in platforms if platform in guidance}

    def _get_current_timestamp(self):
        """Helper method to get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat()

if __name__ == "__main__":
    tool = PlatformSelector(
        selected_platforms=["Instagram", "LinkedIn"],
        platform_priorities="Primary focus on Instagram for visual content, secondary on LinkedIn for professional networking"
    )
    print(tool.run())
