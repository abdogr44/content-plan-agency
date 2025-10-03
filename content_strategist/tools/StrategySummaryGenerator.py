from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from typing import Dict, Any, List

class StrategySummaryGenerator(BaseTool):
    """
    Creates comprehensive strategy summary and content calendar overview
    combining all elements of the content plan into an executive summary.
    """
    
    summary_focus: str = Field(
        default="executive", 
        description="Type of summary to generate: 'executive', 'detailed', or 'implementation_focused'"
    )

    def run(self):
        """
        Generates comprehensive strategy summary from completed content plan.
        """
        # Step 1: Retrieve all data from context
        business_data = self._context.get("business_data")
        brand_personality = self._context.get("brand_personality")
        platform_selection = self._context.get("platform_selection")
        strategy_framework = self._context.get("strategy_framework")
        content_plan = self._context.get("content_plan")
        
        if not all([business_data, brand_personality, platform_selection, strategy_framework]):
            return "Error: Missing required data. Please complete all previous steps first."
        
        if not content_plan:
            return "Error: Content plan not found. Please ensure content creation is completed first."
        
        # Step 2: Generate comprehensive strategy summary
        strategy_summary = self._generate_strategy_summary(
            business_data, brand_personality, platform_selection, 
            strategy_framework, content_plan
        )
        
        # Step 3: Store final summary in context
        self._context.set("strategy_summary", strategy_summary)
        
        # Step 4: Return complete strategy summary
        return json.dumps({
            "status": "success",
            "message": "Strategy summary generated successfully",
            "strategy_summary": strategy_summary
        }, indent=2)

    def _generate_strategy_summary(self, business_data: Dict, brand_personality: Dict, 
                                 platform_selection: Dict, strategy_framework: Dict, 
                                 content_plan: Dict) -> Dict[str, Any]:
        """Generates comprehensive strategy summary"""
        
        return {
            "executive_summary": {
                "business_overview": {
                    "industry": business_data["industry"],
                    "target_audience": business_data["target_audience"],
                    "primary_goals": business_data["business_goals"],
                    "key_challenges": business_data["current_challenges"]
                },
                "brand_identity": {
                    "voice": brand_personality["brand_voice"],
                    "tone": brand_personality["brand_tone"],
                    "core_values": brand_personality["core_values"]
                },
                "platform_strategy": {
                    "selected_platforms": platform_selection["selected_platforms"],
                    "platform_priorities": platform_selection["platform_priorities"]
                }
            },
            "content_strategy_overview": {
                "primary_themes": [theme["theme"] for theme in strategy_framework["content_strategy"]["primary_themes"]],
                "content_mix": strategy_framework["content_strategy"]["content_mix"],
                "weekly_structure": strategy_framework["content_strategy"]["weekly_structure"]
            },
            "content_calendar_summary": {
                "total_posts": len(content_plan.get("daily_posts", [])),
                "platform_distribution": self._calculate_platform_distribution(content_plan),
                "content_type_distribution": self._calculate_content_type_distribution(content_plan),
                "posting_schedule": self._summarize_posting_schedule(content_plan)
            },
            "implementation_guidance": {
                "key_success_factors": self._identify_success_factors(strategy_framework),
                "content_creation_tips": self._provide_creation_tips(brand_personality, business_data["industry"]),
                "engagement_strategies": self._suggest_engagement_strategies(platform_selection["selected_platforms"]),
                "performance_tracking": self._define_performance_tracking(strategy_framework["success_metrics"])
            },
            "next_steps": {
                "immediate_actions": [
                    "Review and approve content plan",
                    "Prepare visual assets according to design suggestions",
                    "Schedule posts using recommended timing",
                    "Set up performance tracking tools"
                ],
                "ongoing_activities": [
                    "Monitor engagement and adjust content based on performance",
                    "Engage with audience comments and messages",
                    "Analyze weekly performance reports",
                    "Iterate and optimize content strategy"
                ]
            }
        }

    def _calculate_platform_distribution(self, content_plan: Dict) -> Dict[str, int]:
        """Calculates distribution of posts across platforms"""
        distribution = {}
        daily_posts = content_plan.get("daily_posts", [])
        
        for post in daily_posts:
            platform = post.get("platform", "Unknown")
            distribution[platform] = distribution.get(platform, 0) + 1
            
        return distribution

    def _calculate_content_type_distribution(self, content_plan: Dict) -> Dict[str, int]:
        """Calculates distribution of content types"""
        distribution = {}
        daily_posts = content_plan.get("daily_posts", [])
        
        for post in daily_posts:
            content_type = post.get("type_of_post", "Unknown")
            distribution[content_type] = distribution.get(content_type, 0) + 1
            
        return distribution

    def _summarize_posting_schedule(self, content_plan: Dict) -> Dict[str, Any]:
        """Summarizes the posting schedule and timing"""
        daily_posts = content_plan.get("daily_posts", [])
        
        schedule = {}
        for post in daily_posts:
            day = post.get("day", "Unknown")
            platform = post.get("platform", "Unknown")
            
            if day not in schedule:
                schedule[day] = {}
            schedule[day][platform] = {
                "title": post.get("title", ""),
                "type": post.get("type_of_post", ""),
                "goal": post.get("goal", "")
            }
            
        return schedule

    def _identify_success_factors(self, strategy_framework: Dict) -> List[str]:
        """Identifies key success factors for the content strategy"""
        factors = [
            "Consistent posting schedule",
            "High-quality visual content",
            "Engaging captions that reflect brand voice",
            "Strategic hashtag usage"
        ]
        
        # Add industry-specific factors
        industry = strategy_framework["business_analysis"]["industry"].lower()
        if "technology" in industry:
            factors.append("Thought leadership content")
        elif "healthcare" in industry:
            factors.append("Trust-building educational content")
        elif "e-commerce" in industry:
            factors.append("Product showcase and social proof")
            
        return factors

    def _provide_creation_tips(self, brand_personality: Dict, industry: str) -> List[str]:
        """Provides content creation tips based on brand and industry"""
        tips = [
            f"Maintain {brand_personality['brand_voice']} voice consistently",
            f"Incorporate {brand_personality['core_values']} values in messaging",
            "Use high-quality visuals that align with brand aesthetic",
            "Write captions that encourage engagement and conversation"
        ]
        
        # Add industry-specific tips
        if "technology" in industry.lower():
            tips.append("Include relevant tech trends and innovations")
        elif "healthcare" in industry.lower():
            tips.append("Focus on patient education and wellness tips")
        elif "e-commerce" in industry.lower():
            tips.append("Showcase products in real-life scenarios")
            
        return tips

    def _suggest_engagement_strategies(self, platforms: list) -> Dict[str, List[str]]:
        """Suggests engagement strategies for each platform"""
        strategies = {
            "Facebook": [
                "Respond to comments within 2 hours",
                "Ask questions in posts to encourage discussion",
                "Share user-generated content",
                "Use Facebook Groups for community building"
            ],
            "Instagram": [
                "Use Instagram Stories for behind-the-scenes content",
                "Engage with stories and posts from target audience",
                "Use relevant hashtags and location tags",
                "Post user-generated content and testimonials"
            ],
            "LinkedIn": [
                "Share industry insights and thought leadership",
                "Comment thoughtfully on others' posts",
                "Use LinkedIn Polls for engagement",
                "Share company updates and achievements"
            ]
        }
        
        return {platform: strategies.get(platform, []) for platform in platforms}

    def _define_performance_tracking(self, success_metrics: list) -> Dict[str, Any]:
        """Defines performance tracking approach"""
        return {
            "key_metrics": success_metrics,
            "tracking_frequency": "Weekly analysis, monthly comprehensive review",
            "tools_recommended": [
                "Platform native analytics",
                "Social media management tools",
                "Google Analytics for website traffic",
                "Custom tracking for lead generation"
            ],
            "success_benchmarks": {
                "engagement_rate": "Above industry average (3-6%)",
                "reach": "Steady month-over-month growth",
                "lead_generation": "Track conversion from social to leads",
                "brand_awareness": "Monitor brand mentions and sentiment"
            }
        }

if __name__ == "__main__":
    tool = StrategySummaryGenerator(summary_focus="executive")
    print(tool.run())
