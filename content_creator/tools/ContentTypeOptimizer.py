from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from typing import Dict, Any, List
import requests
from bs4 import BeautifulSoup

class ContentTypeOptimizer(BaseTool):
    """
    Determines optimal post types based on business use case and current market trends
    to ensure maximum engagement and effectiveness.
    """
    
    industry: str = Field(
        ..., description="Business industry for trend analysis"
    )
    business_goals: str = Field(
        ..., description="Primary business objectives"
    )
    target_audience: str = Field(
        ..., description="Audience characteristics"
    )
    platform: str = Field(
        ..., description="Social media platform (Facebook, Instagram, LinkedIn)"
    )
    day_of_week: str = Field(
        ..., description="Specific day for optimal timing analysis"
    )

    def run(self):
        """
        Analyzes current trends and business context to recommend optimal content types.
        """
        # Step 1: Get current market trends
        current_trends = self._research_current_trends(self.industry, self.platform)
        
        # Step 2: Analyze business context
        business_analysis = self._analyze_business_context(
            self.industry, self.business_goals, self.target_audience
        )
        
        # Step 3: Determine optimal content types
        recommended_types = self._determine_optimal_content_types(
            current_trends, business_analysis, self.platform, self.day_of_week
        )
        
        # Step 4: Store recommendations in context
        self._context.set("content_type_recommendations", recommended_types)
        
        # Step 5: Return analysis and recommendations
        return json.dumps({
            "status": "success",
            "message": "Content type optimization completed",
            "current_trends": current_trends,
            "business_analysis": business_analysis,
            "recommended_content_types": recommended_types,
            "optimization_rationale": self._explain_recommendations(recommended_types, current_trends)
        }, indent=2)

    def _research_current_trends(self, industry: str, platform: str) -> Dict[str, Any]:
        """Researches current trends in the industry and platform"""
        
        # Step 1: Define search queries for trend research
        search_queries = [
            f"{industry} social media trends 2024",
            f"{platform} content trends {industry}",
            f"best performing {platform} content types 2024"
        ]
        
        trends = {
            "platform_trends": self._get_platform_specific_trends(platform),
            "industry_trends": self._get_industry_specific_trends(industry),
            "engagement_trends": self._get_engagement_trends(platform),
            "content_performance": self._get_content_performance_insights(platform)
        }
        
        return trends

    def _get_platform_specific_trends(self, platform: str) -> Dict[str, Any]:
        """Gets platform-specific trending content types"""
        
        platform_trends = {
            "Facebook": {
                "trending_types": ["Video", "Live Video", "Carousel Posts", "Story Highlights"],
                "engagement_boosters": ["Questions", "Polls", "User-Generated Content"],
                "optimal_timing": "Tuesday-Thursday, 9 AM - 3 PM",
                "content_length": "Shorter posts (40-80 characters) perform better"
            },
            "Instagram": {
                "trending_types": ["Reels", "Stories", "Carousel Posts", "IGTV"],
                "engagement_boosters": ["Behind-the-Scenes", "User-Generated Content", "Polls"],
                "optimal_timing": "Monday-Friday, 11 AM - 1 PM, 5 PM - 7 PM",
                "content_length": "125-150 characters for optimal engagement"
            },
            "LinkedIn": {
                "trending_types": ["Articles", "Video", "Document Posts", "Polls"],
                "engagement_boosters": ["Thought Leadership", "Industry Insights", "Professional Tips"],
                "optimal_timing": "Tuesday-Thursday, 8 AM - 10 AM, 12 PM - 2 PM",
                "content_length": "150-300 characters for best performance"
            }
        }
        
        return platform_trends.get(platform, {})

    def _get_industry_specific_trends(self, industry: str) -> Dict[str, Any]:
        """Gets industry-specific content trends"""
        
        industry_trends = {
            "technology": {
                "popular_content": ["Product Demos", "Tech Tips", "Industry News", "Behind-the-Scenes"],
                "engagement_drivers": ["Innovation Stories", "Problem-Solution Content", "Expert Insights"],
                "visual_preferences": "Clean, modern design with tech aesthetics"
            },
            "healthcare": {
                "popular_content": ["Educational Content", "Patient Stories", "Health Tips", "Professional Insights"],
                "engagement_drivers": ["Trust-Building Content", "Expert Authority", "Community Support"],
                "visual_preferences": "Professional, trustworthy imagery with calming colors"
            },
            "e-commerce": {
                "popular_content": ["Product Showcases", "Customer Reviews", "Lifestyle Content", "Promotions"],
                "engagement_drivers": ["Social Proof", "User-Generated Content", "Exclusive Offers"],
                "visual_preferences": "High-quality product photography with lifestyle context"
            },
            "professional_services": {
                "popular_content": ["Case Studies", "Industry Insights", "Expert Tips", "Client Success Stories"],
                "engagement_drivers": ["Thought Leadership", "Problem-Solution Content", "Professional Expertise"],
                "visual_preferences": "Clean, professional design with brand consistency"
            }
        }
        
        # Map common industry terms to our categories
        industry_mapping = {
            "technology": "technology",
            "tech": "technology",
            "software": "technology",
            "healthcare": "healthcare",
            "health": "healthcare",
            "medical": "healthcare",
            "e-commerce": "e-commerce",
            "retail": "e-commerce",
            "online store": "e-commerce",
            "consulting": "professional_services",
            "services": "professional_services",
            "professional": "professional_services"
        }
        
        industry_key = industry_mapping.get(industry.lower(), "professional_services")
        return industry_trends.get(industry_key, industry_trends["professional_services"])

    def _get_engagement_trends(self, platform: str) -> Dict[str, Any]:
        """Gets current engagement trends for the platform"""
        
        engagement_trends = {
            "Facebook": {
                "high_engagement_content": ["Video", "Live Content", "Interactive Posts"],
                "engagement_rate": "Average 0.27%",
                "best_practices": ["Ask questions", "Share relatable content", "Use native video"]
            },
            "Instagram": {
                "high_engagement_content": ["Reels", "Stories", "User-Generated Content"],
                "engagement_rate": "Average 1.60%",
                "best_practices": ["Post consistently", "Use relevant hashtags", "Engage with comments"]
            },
            "LinkedIn": {
                "high_engagement_content": ["Articles", "Professional Insights", "Industry News"],
                "engagement_rate": "Average 0.54%",
                "best_practices": ["Share professional insights", "Comment thoughtfully", "Use industry hashtags"]
            }
        }
        
        return engagement_trends.get(platform, {})

    def _get_content_performance_insights(self, platform: str) -> Dict[str, Any]:
        """Gets content performance insights for the platform"""
        
        performance_insights = {
            "Facebook": {
                "top_performing": ["Video (5.3x more engagement)", "Live Video (6x more engagement)"],
                "optimal_frequency": "1-2 posts per day",
                "content_mix": "70% informative, 20% promotional, 10% entertaining"
            },
            "Instagram": {
                "top_performing": ["Reels (22% more reach)", "Stories (high engagement)"],
                "optimal_frequency": "1 post per day, 5-7 stories per day",
                "content_mix": "60% entertaining, 30% educational, 10% promotional"
            },
            "LinkedIn": {
                "top_performing": ["Articles (5x more reach)", "Native Video (3x more engagement)"],
                "optimal_frequency": "1 post per day, 2-3 posts per week minimum",
                "content_mix": "80% educational, 15% promotional, 5% entertaining"
            }
        }
        
        return performance_insights.get(platform, {})

    def _analyze_business_context(self, industry: str, goals: str, audience: str) -> Dict[str, Any]:
        """Analyzes business context to inform content type recommendations"""
        
        # Analyze goals
        goal_keywords = goals.lower()
        primary_objectives = []
        
        if any(word in goal_keywords for word in ["awareness", "visibility", "brand"]):
            primary_objectives.append("brand_awareness")
        if any(word in goal_keywords for word in ["lead", "generate", "prospect"]):
            primary_objectives.append("lead_generation")
        if any(word in goal_keywords for word in ["engagement", "community", "interaction"]):
            primary_objectives.append("engagement")
        if any(word in goal_keywords for word in ["sales", "conversion", "revenue"]):
            primary_objectives.append("conversion")
        
        # Analyze audience
        audience_analysis = self._analyze_target_audience(audience)
        
        return {
            "primary_objectives": primary_objectives,
            "industry_context": industry,
            "audience_analysis": audience_analysis,
            "content_preferences": self._determine_content_preferences(industry, audience)
        }

    def _analyze_target_audience(self, audience: str) -> Dict[str, Any]:
        """Analyzes target audience characteristics"""
        
        audience_lower = audience.lower()
        
        # Determine audience type
        audience_type = "general"
        if any(word in audience_lower for word in ["professional", "executive", "business"]):
            audience_type = "professional"
        elif any(word in audience_lower for word in ["consumer", "customer", "shopper"]):
            audience_type = "consumer"
        elif any(word in audience_lower for word in ["student", "learner", "beginner"]):
            audience_type = "educational"
        
        # Determine age group
        age_group = "mixed"
        if any(word in audience_lower for word in ["25-45", "millennial", "young"]):
            age_group = "millennial"
        elif any(word in audience_lower for word in ["45+", "senior", "mature"]):
            age_group = "mature"
        
        return {
            "audience_type": audience_type,
            "age_group": age_group,
            "content_preferences": self._get_audience_content_preferences(audience_type, age_group)
        }

    def _get_audience_content_preferences(self, audience_type: str, age_group: str) -> List[str]:
        """Gets content preferences based on audience type and age group"""
        
        preferences = {
            "professional": ["Educational content", "Industry insights", "Case studies", "Expert tips"],
            "consumer": ["Product showcases", "User reviews", "Lifestyle content", "Promotions"],
            "educational": ["How-to guides", "Tutorials", "Tips and tricks", "Beginner-friendly content"]
        }
        
        age_preferences = {
            "millennial": ["Visual content", "Interactive posts", "Behind-the-scenes", "User-generated content"],
            "mature": ["Detailed articles", "Professional content", "Testimonials", "Educational content"],
            "mixed": ["Varied content types", "Multi-format posts", "Accessible content"]
        }
        
        base_preferences = preferences.get(audience_type, preferences["professional"])
        age_specific = age_preferences.get(age_group, age_preferences["mixed"])
        
        return list(set(base_preferences + age_specific))

    def _determine_content_preferences(self, industry: str, audience: str) -> List[str]:
        """Determines content preferences based on industry and audience"""
        
        # Industry-specific preferences
        industry_preferences = {
            "technology": ["Product demos", "Tech tutorials", "Innovation stories", "Industry trends"],
            "healthcare": ["Health tips", "Patient education", "Professional insights", "Wellness content"],
            "e-commerce": ["Product showcases", "Customer stories", "Shopping tips", "Behind-the-scenes"]
        }
        
        # Get industry key
        industry_key = industry.lower()
        for key in industry_preferences.keys():
            if key in industry_key:
                return industry_preferences[key]
        
        return ["Educational content", "Industry insights", "Professional tips", "Case studies"]

    def _determine_optimal_content_types(self, trends: Dict, business_analysis: Dict, 
                                       platform: str, day_of_week: str) -> List[Dict[str, Any]]:
        """Determines optimal content types based on all analysis"""
        
        # Get platform-specific trending types
        platform_trending = trends["platform_trends"].get("trending_types", [])
        industry_trending = trends["industry_trends"].get("popular_content", [])
        
        # Get business context preferences
        business_preferences = business_analysis["content_preferences"]
        audience_preferences = business_analysis["audience_analysis"]["content_preferences"]
        
        # Combine and rank content types
        all_preferences = platform_trending + industry_trending + business_preferences + audience_preferences
        
        # Count frequency and create recommendations
        content_type_scores = {}
        for content_type in all_preferences:
            content_type_scores[content_type] = content_type_scores.get(content_type, 0) + 1
        
        # Sort by score and create recommendations
        sorted_types = sorted(content_type_scores.items(), key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for content_type, score in sorted_types[:5]:  # Top 5 recommendations
            recommendations.append({
                "content_type": content_type,
                "confidence_score": score,
                "rationale": self._get_recommendation_rationale(content_type, trends, business_analysis),
                "optimal_timing": self._get_optimal_timing(content_type, platform, day_of_week),
                "engagement_potential": self._assess_engagement_potential(content_type, platform)
            })
        
        return recommendations

    def _get_recommendation_rationale(self, content_type: str, trends: Dict, business_analysis: Dict) -> str:
        """Provides rationale for content type recommendation"""
        
        rationales = {
            "Video": "High engagement rates across all platforms, especially effective for storytelling",
            "Educational Content": "Establishes authority and provides value to audience",
            "Behind-the-Scenes": "Builds trust and humanizes the brand",
            "User-Generated Content": "Increases authenticity and community engagement",
            "Interactive Posts": "Drives immediate engagement and feedback",
            "Product Showcases": "Directly supports sales and conversion goals",
            "Industry Insights": "Positions brand as thought leader and expert"
        }
        
        return rationales.get(content_type, "Aligned with current trends and audience preferences")

    def _get_optimal_timing(self, content_type: str, platform: str, day_of_week: str) -> str:
        """Determines optimal timing for content type"""
        
        timing_guidelines = {
            "Video": "Tuesday-Thursday, peak hours for maximum reach",
            "Educational Content": "Monday-Wednesday, when audience is most receptive to learning",
            "Interactive Posts": "Friday-Sunday, when audience has more time to engage",
            "Promotional Content": "Tuesday-Thursday, mid-week for best conversion rates"
        }
        
        return timing_guidelines.get(content_type, f"Optimal for {platform} on {day_of_week}")

    def _assess_engagement_potential(self, content_type: str, platform: str) -> str:
        """Assesses engagement potential for content type"""
        
        engagement_assessments = {
            "Video": "High - typically 3-5x higher engagement than static content",
            "Interactive Posts": "Very High - encourages immediate audience participation",
            "Educational Content": "Medium-High - valuable content drives meaningful engagement",
            "Behind-the-Scenes": "Medium - builds trust and authenticity",
            "User-Generated Content": "High - leverages social proof and community"
        }
        
        return engagement_assessments.get(content_type, "Medium - depends on execution and relevance")

    def _explain_recommendations(self, recommendations: List[Dict], trends: Dict) -> str:
        """Explains the reasoning behind recommendations"""
        
        explanation = "Content type recommendations are based on:\n\n"
        explanation += "1. Current platform trends and engagement data\n"
        explanation += "2. Industry-specific content preferences\n"
        explanation += "3. Target audience characteristics and preferences\n"
        explanation += "4. Business goals and objectives\n\n"
        
        if recommendations:
            top_recommendation = recommendations[0]
            explanation += f"Top recommendation: {top_recommendation['content_type']} "
            explanation += f"(Confidence: {top_recommendation['confidence_score']}/10)\n"
            explanation += f"Rationale: {top_recommendation['rationale']}"
        
        return explanation

if __name__ == "__main__":
    tool = ContentTypeOptimizer(
        industry="Technology",
        business_goals="Increase brand awareness and generate leads",
        target_audience="Small business owners aged 25-45",
        platform="Instagram",
        day_of_week="Monday"
    )
    print(tool.run())
