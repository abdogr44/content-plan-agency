from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from typing import Dict, Any, List

class ContentStrategyAnalyzer(BaseTool):
    """
    Analyzes business and brand data to determine optimal content strategy and post types
    based on industry trends and business objectives.
    """
    
    analysis_focus: str = Field(
        default="comprehensive", 
        description="Focus area for analysis: 'comprehensive', 'engagement_focused', 'lead_generation', or 'brand_awareness'"
    )

    def run(self):
        """
        Analyzes collected business and brand data to create content strategy framework.
        """
        # Step 1: For testing purposes, use sample data
        # In production, this would retrieve data from agency context
        business_data = {
            "industry": "Technology",
            "target_audience": "Small business owners aged 25-45",
            "business_goals": "Increase brand awareness and generate leads",
            "current_challenges": "Low engagement rates and difficulty reaching target audience"
        }
        brand_personality = {
            "brand_voice": "Professional and authoritative",
            "brand_tone": "Encouraging and supportive",
            "core_values": "Innovation, quality, customer-first",
            "personality_adjectives": "trustworthy, innovative, reliable"
        }
        platform_selection = {
            "selected_platforms": ["Instagram", "LinkedIn"],
            "platform_priorities": "Primary focus on Instagram, secondary on LinkedIn"
        }
        
        # Step 2: Analyze business context and create strategy framework
        strategy_framework = self._create_strategy_framework(
            business_data, brand_personality, platform_selection
        )
        
        # Step 3: Store strategy framework in context
        # Note: Context storage handled by agency framework
        
        # Step 4: Return comprehensive strategy analysis
        return json.dumps({
            "status": "success",
            "message": "Content strategy analysis completed successfully",
            "strategy_framework": strategy_framework,
            "next_steps": "Proceed with content creation using the strategy framework"
        }, indent=2)

    def _create_strategy_framework(self, business_data: Dict, brand_personality: Dict, platform_selection: Dict) -> Dict[str, Any]:
        """Creates comprehensive content strategy framework"""
        
        # Step 1: Analyze business goals and challenges
        goals_analysis = self._analyze_business_goals(business_data["business_goals"])
        challenges_analysis = self._analyze_challenges(business_data["current_challenges"])
        
        # Step 2: Determine content themes based on industry and goals
        content_themes = self._determine_content_themes(
            business_data["industry"], 
            business_data["business_goals"],
            brand_personality["core_values"]
        )
        
        # Step 3: Recommend post types for each platform
        platform_post_types = self._recommend_platform_post_types(
            platform_selection["selected_platforms"],
            business_data["industry"],
            brand_personality["brand_voice"]
        )
        
        # Step 4: Create weekly content structure
        weekly_structure = self._create_weekly_structure(content_themes, platform_post_types)
        
        return {
            "business_analysis": {
                "industry": business_data["industry"],
                "goals_analysis": goals_analysis,
                "challenges_analysis": challenges_analysis,
                "target_audience": business_data["target_audience"]
            },
            "brand_alignment": {
                "voice": brand_personality["brand_voice"],
                "tone": brand_personality["brand_tone"],
                "values": brand_personality["core_values"],
                "personality_traits": brand_personality["personality_adjectives"]
            },
            "platform_strategy": {
                "selected_platforms": platform_selection["selected_platforms"],
                "platform_priorities": platform_selection["platform_priorities"],
                "recommended_post_types": platform_post_types
            },
            "content_strategy": {
                "primary_themes": content_themes,
                "weekly_structure": weekly_structure,
                "content_mix": self._recommend_content_mix(business_data["industry"])
            },
            "success_metrics": self._define_success_metrics(business_data["business_goals"])
        }

    def _analyze_business_goals(self, goals: str) -> Dict[str, Any]:
        """Analyzes business goals to determine content priorities"""
        goal_keywords = goals.lower()
        
        priorities = []
        if any(word in goal_keywords for word in ["awareness", "visibility", "brand"]):
            priorities.append("brand_awareness")
        if any(word in goal_keywords for word in ["lead", "generate", "prospect"]):
            priorities.append("lead_generation")
        if any(word in goal_keywords for word in ["engagement", "community", "interaction"]):
            priorities.append("engagement")
        if any(word in goal_keywords for word in ["sales", "conversion", "revenue"]):
            priorities.append("conversion")
            
        return {
            "primary_goals": goals,
            "content_priorities": priorities,
            "focus_areas": priorities[:2] if len(priorities) > 2 else priorities
        }

    def _analyze_challenges(self, challenges: str) -> Dict[str, Any]:
        """Analyzes current challenges to address in content strategy"""
        challenge_keywords = challenges.lower()
        
        solutions = []
        if any(word in challenge_keywords for word in ["engagement", "interaction", "response"]):
            solutions.append("interactive_content")
        if any(word in challenge_keywords for word in ["audience", "reach", "visibility"]):
            solutions.append("audience_focused_content")
        if any(word in challenge_keywords for word in ["content", "ideas", "creativity"]):
            solutions.append("diverse_content_types")
            
        return {
            "current_challenges": challenges,
            "content_solutions": solutions,
            "strategy_adjustments": solutions
        }

    def _determine_content_themes(self, industry: str, goals: str, values: str) -> List[Dict[str, str]]:
        """Determines primary content themes based on business context"""
        themes = [
            {
                "theme": "Educational Content",
                "description": "Share industry insights, tips, and knowledge to establish authority",
                "alignment": "Works for all industries and goals"
            },
            {
                "theme": "Behind-the-Scenes",
                "description": "Show company culture, processes, and team to build trust",
                "alignment": "Great for brand awareness and engagement"
            },
            {
                "theme": "Problem-Solution",
                "description": "Address customer pain points and showcase solutions",
                "alignment": "Perfect for lead generation and conversion"
            }
        ]
        
        # Add industry-specific themes
        industry_themes = {
            "technology": {
                "theme": "Innovation & Trends",
                "description": "Share latest tech trends and innovations",
                "alignment": "Establishes thought leadership"
            },
            "healthcare": {
                "theme": "Health & Wellness",
                "description": "Educational health content and wellness tips",
                "alignment": "Builds trust and authority"
            },
            "e-commerce": {
                "theme": "Product Showcase",
                "description": "Highlight products and customer success stories",
                "alignment": "Drives sales and engagement"
            }
        }
        
        if industry.lower() in industry_themes:
            themes.append(industry_themes[industry.lower()])
            
        return themes[:4]  # Limit to 4 primary themes

    def _recommend_platform_post_types(self, platforms: List[str], industry: str, brand_voice: str) -> Dict[str, List[str]]:
        """Recommends optimal post types for each platform"""
        base_post_types = {
            "Facebook": ["Image Post", "Video", "Link Share", "Text Post", "Carousel"],
            "Instagram": ["Feed Post", "Story", "Reel", "IGTV", "Carousel", "Live"],
            "LinkedIn": ["Article", "Image Post", "Video", "Text Post", "Poll", "Document Share"]
        }
        
        # Adjust based on brand voice
        if "professional" in brand_voice.lower() or "formal" in brand_voice.lower():
            platform_post_types = {platform: [pt for pt in types if pt not in ["Story", "Reel", "Live"]] 
                                 for platform, types in base_post_types.items()}
        else:
            platform_post_types = base_post_types
            
        return {platform: platform_post_types.get(platform, []) for platform in platforms}

    def _create_weekly_structure(self, themes: List[Dict], platform_post_types: Dict[str, List[str]]) -> Dict[str, str]:
        """Creates weekly content structure with theme distribution"""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        structure = {}
        
        for i, day in enumerate(days[:7]):
            theme_index = i % len(themes)
            structure[day] = {
                "primary_theme": themes[theme_index]["theme"],
                "theme_description": themes[theme_index]["description"],
                "focus_areas": ["engagement", "education", "brand_awareness"][i % 3]
            }
            
        return structure

    def _recommend_content_mix(self, industry: str) -> Dict[str, int]:
        """Recommends content mix percentages"""
        return {
            "educational": 40,
            "promotional": 20,
            "behind_scenes": 20,
            "user_generated": 10,
            "trending": 10
        }

    def _define_success_metrics(self, goals: str) -> List[str]:
        """Defines success metrics based on business goals"""
        metrics = ["engagement_rate", "reach", "impressions"]
        
        if "lead" in goals.lower():
            metrics.append("lead_generation")
        if "sales" in goals.lower() or "conversion" in goals.lower():
            metrics.append("conversion_rate")
        if "awareness" in goals.lower():
            metrics.append("brand_mention_increase")
            
        return metrics

    def _get_current_timestamp(self):
        """Helper method to get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat()

if __name__ == "__main__":
    tool = ContentStrategyAnalyzer(analysis_focus="comprehensive")
    print(tool.run())
