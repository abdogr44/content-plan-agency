from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from typing import Dict, Any

class BusinessIntakeCollector(BaseTool):
    """
    Collects comprehensive business information including industry, target audience, 
    business goals, and current challenges to provide context for content planning.
    """
    
    industry: str = Field(
        ..., description="The business industry or sector (e.g., 'Technology', 'Healthcare', 'E-commerce', 'Professional Services')"
    )
    target_audience: str = Field(
        ..., description="Demographics and characteristics of ideal customers (e.g., 'Small business owners aged 25-45', 'Tech professionals', 'Healthcare administrators')"
    )
    business_goals: str = Field(
        ..., description="Primary business objectives (e.g., 'Increase brand awareness', 'Generate leads', 'Drive sales', 'Build community engagement')"
    )
    current_challenges: str = Field(
        ..., description="Current obstacles or pain points the business is facing (e.g., 'Low engagement rates', 'Difficulty reaching target audience', 'Limited content ideas')"
    )

    def run(self):
        """
        Collects and structures business information for content planning analysis.
        """
        # Step 1: Validate input completeness
        if not all([self.industry, self.target_audience, self.business_goals, self.current_challenges]):
            return "Error: All business information fields must be completed."
        
        # Step 2: Structure the business data
        business_data = {
            "industry": self.industry.strip(),
            "target_audience": self.target_audience.strip(),
            "business_goals": self.business_goals.strip(),
            "current_challenges": self.current_challenges.strip(),
            "collection_timestamp": self._get_current_timestamp()
        }
        
        # Step 3: Store in context for other tools to access
        # Note: Context storage handled by agency framework
        
        # Step 4: Return confirmation with structured data
        return json.dumps({
            "status": "success",
            "message": "Business information collected successfully",
            "data": business_data,
            "next_steps": "Proceed with brand personality assessment"
        }, indent=2)

    def _get_current_timestamp(self):
        """Helper method to get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat()

if __name__ == "__main__":
    tool = BusinessIntakeCollector(
        industry="Technology",
        target_audience="Small business owners aged 25-45",
        business_goals="Increase brand awareness and generate leads",
        current_challenges="Low engagement rates and difficulty reaching target audience"
    )
    print(tool.run())
