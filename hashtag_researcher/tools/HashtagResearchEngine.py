from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from typing import Dict, Any, List
import requests
from bs4 import BeautifulSoup
import re

class HashtagResearchEngine(BaseTool):
    """
    Researches and recommends hashtag combinations for each post based on content,
    industry, and platform to maximize reach and engagement.
    """
    
    post_content: Dict[str, Any] = Field(
        ..., description="Complete post details including title, caption, and context"
    )
    industry: str = Field(
        ..., description="Business industry for industry-specific hashtags"
    )
    target_audience: str = Field(
        ..., description="Audience characteristics for targeted hashtags"
    )
    platform: str = Field(
        ..., description="Social media platform (Facebook, Instagram, LinkedIn)"
    )
    brand_hashtags: List[str] = Field(
        default=[], 
        description="Custom branded hashtags for the business"
    )

    def run(self):
        """
        Researches and recommends optimal hashtag combinations for the post.
        """
        # Step 1: Validate inputs
        if not self.post_content or not self.industry:
            return "Error: Post content and industry are required."
        
        # Step 2: Get additional context from agency context
        business_data = self._context.get("business_data")
        brand_personality = self._context.get("brand_personality")
        
        if not all([business_data, brand_personality]):
            return "Error: Missing required context data. Please ensure business data and brand personality are available."
        
        # Step 3: Research hashtags
        hashtag_research = self._conduct_hashtag_research()
        
        # Step 4: Store hashtag recommendations in context
        post_key = f"hashtag_recommendations_{self.post_content.get('day', 'unknown')}"
        self._context.set(post_key, hashtag_research)
        
        # Step 5: Return hashtag recommendations
        return json.dumps({
            "status": "success",
            "message": "Hashtag research completed successfully",
            "hashtag_recommendations": hashtag_research
        }, indent=2)

    def _conduct_hashtag_research(self) -> Dict[str, Any]:
        """Conducts comprehensive hashtag research for the post"""
        
        # Step 1: Analyze post content for hashtag opportunities
        content_analysis = self._analyze_post_content_for_hashtags()
        
        # Step 2: Research trending hashtags
        trending_hashtags = self._research_trending_hashtags()
        
        # Step 3: Research industry-specific hashtags
        industry_hashtags = self._research_industry_hashtags()
        
        # Step 4: Research audience-specific hashtags
        audience_hashtags = self._research_audience_hashtags()
        
        # Step 5: Research platform-specific hashtags
        platform_hashtags = self._research_platform_hashtags()
        
        # Step 6: Compile and rank hashtag recommendations
        hashtag_recommendations = self._compile_hashtag_recommendations(
            content_analysis, trending_hashtags, industry_hashtags, 
            audience_hashtags, platform_hashtags
        )
        
        # Step 7: Create hashtag strategy
        hashtag_strategy = self._create_hashtag_strategy(hashtag_recommendations)
        
        return {
            "content_analysis": content_analysis,
            "hashtag_categories": {
                "trending": trending_hashtags,
                "industry": industry_hashtags,
                "audience": audience_hashtags,
                "platform": platform_hashtags,
                "branded": self.brand_hashtags
            },
            "recommended_hashtags": hashtag_recommendations,
            "hashtag_strategy": hashtag_strategy,
            "implementation_guidelines": self._create_implementation_guidelines()
        }

    def _analyze_post_content_for_hashtags(self) -> Dict[str, Any]:
        """Analyzes post content to identify hashtag opportunities"""
        
        title = self.post_content.get("title", "").lower()
        caption = self.post_content.get("caption", "").lower()
        content_theme = self.post_content.get("content_theme", "").lower()
        goal = self.post_content.get("goal", "").lower()
        
        # Extract keywords from content
        content_keywords = self._extract_keywords_from_content(title, caption, content_theme, goal)
        
        # Identify hashtag opportunities
        hashtag_opportunities = self._identify_hashtag_opportunities(content_keywords)
        
        return {
            "content_keywords": content_keywords,
            "hashtag_opportunities": hashtag_opportunities,
            "content_theme": content_theme,
            "primary_topics": self._identify_primary_topics(content_keywords)
        }

    def _extract_keywords_from_content(self, title: str, caption: str, 
                                     content_theme: str, goal: str) -> List[str]:
        """Extracts relevant keywords from post content"""
        
        # Combine all text content
        all_text = f"{title} {caption} {content_theme} {goal}"
        
        # Remove common words and extract meaningful keywords
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", 
            "of", "with", "by", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "can", "this", "that", "these", "those"
        }
        
        # Extract words and filter
        words = re.findall(r'\b[a-zA-Z]{3,}\b', all_text.lower())
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Get unique keywords and count frequency
        keyword_frequency = {}
        for keyword in keywords:
            keyword_frequency[keyword] = keyword_frequency.get(keyword, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_keywords = sorted(keyword_frequency.items(), key=lambda x: x[1], reverse=True)
        return [keyword for keyword, freq in sorted_keywords[:15]]

    def _identify_hashtag_opportunities(self, keywords: List[str]) -> List[Dict[str, str]]:
        """Identifies specific hashtag opportunities from keywords"""
        
        opportunities = []
        
        for keyword in keywords[:10]:  # Top 10 keywords
            # Create hashtag variations
            hashtag_variations = [
                f"#{keyword}",
                f"#{keyword}s",  # Plural
                f"#{keyword}ing",  # Gerund
                f"#{keyword}ed",  # Past tense
            ]
            
            opportunities.append({
                "keyword": keyword,
                "hashtag_variations": hashtag_variations,
                "potential_reach": self._estimate_hashtag_potential(keyword),
                "relevance_score": self._calculate_relevance_score(keyword)
            })
        
        return opportunities

    def _estimate_hashtag_potential(self, keyword: str) -> str:
        """Estimates hashtag potential based on keyword characteristics"""
        
        # Simple estimation based on keyword length and commonness
        if len(keyword) <= 4:
            return "High - Short and memorable"
        elif len(keyword) <= 8:
            return "Medium-High - Good balance"
        else:
            return "Medium - Longer but specific"

    def _calculate_relevance_score(self, keyword: str) -> int:
        """Calculates relevance score for keyword (1-10)"""
        
        # Simple scoring based on keyword characteristics
        score = 5  # Base score
        
        # Industry relevance
        industry_keywords = self.industry.lower().split()
        if any(ind_word in keyword for ind_word in industry_keywords):
            score += 2
        
        # Length optimization
        if 4 <= len(keyword) <= 8:
            score += 1
        
        # Avoid overly generic terms
        generic_terms = ["content", "post", "social", "media", "business", "marketing"]
        if keyword not in generic_terms:
            score += 1
        
        return min(score, 10)

    def _identify_primary_topics(self, keywords: List[str]) -> List[str]:
        """Identifies primary topics from keywords"""
        
        # Group keywords into topics
        topics = []
        
        # Business/Professional topics
        business_keywords = ["business", "professional", "industry", "strategy", "marketing"]
        if any(biz_word in keywords for biz_word in business_keywords):
            topics.append("Business & Professional")
        
        # Industry-specific topics
        topics.append(f"{self.industry} Industry")
        
        # Content type topics
        content_themes = ["education", "tips", "guide", "strategy", "insights"]
        if any(theme in keywords for theme in content_themes):
            topics.append("Educational Content")
        
        return topics

    def _research_trending_hashtags(self) -> Dict[str, Any]:
        """Researches trending hashtags relevant to the content"""
        
        # Simulate trending hashtag research
        trending_hashtags = {
            "general_trending": [
                {"hashtag": "#business", "trend_level": "High", "engagement_potential": "Medium"},
                {"hashtag": "#marketing", "trend_level": "High", "engagement_potential": "High"},
                {"hashtag": "#entrepreneur", "trend_level": "Medium", "engagement_potential": "High"},
                {"hashtag": "#growth", "trend_level": "Medium", "engagement_potential": "Medium"},
                {"hashtag": "#success", "trend_level": "High", "engagement_potential": "Medium"}
            ],
            "industry_trending": self._get_industry_trending_hashtags(),
            "platform_trending": self._get_platform_trending_hashtags()
        }
        
        return trending_hashtags

    def _get_industry_trending_hashtags(self) -> List[Dict[str, str]]:
        """Gets industry-specific trending hashtags"""
        
        industry_hashtags = {
            "technology": [
                {"hashtag": "#tech", "trend_level": "High", "engagement_potential": "High"},
                {"hashtag": "#innovation", "trend_level": "Medium", "engagement_potential": "High"},
                {"hashtag": "#digital", "trend_level": "High", "engagement_potential": "Medium"},
                {"hashtag": "#software", "trend_level": "Medium", "engagement_potential": "Medium"}
            ],
            "healthcare": [
                {"hashtag": "#healthcare", "trend_level": "High", "engagement_potential": "Medium"},
                {"hashtag": "#health", "trend_level": "High", "engagement_potential": "High"},
                {"hashtag": "#wellness", "trend_level": "Medium", "engagement_potential": "High"},
                {"hashtag": "#medical", "trend_level": "Medium", "engagement_potential": "Medium"}
            ],
            "e-commerce": [
                {"hashtag": "#ecommerce", "trend_level": "Medium", "engagement_potential": "Medium"},
                {"hashtag": "#retail", "trend_level": "Medium", "engagement_potential": "Medium"},
                {"hashtag": "#online", "trend_level": "High", "engagement_potential": "Medium"},
                {"hashtag": "#shopping", "trend_level": "High", "engagement_potential": "High"}
            ]
        }
        
        industry_key = self.industry.lower()
        for key in industry_hashtags.keys():
            if key in industry_key:
                return industry_hashtags[key]
        
        # Default to general business hashtags
        return [
            {"hashtag": "#business", "trend_level": "High", "engagement_potential": "Medium"},
            {"hashtag": "#professional", "trend_level": "Medium", "engagement_potential": "Medium"},
            {"hashtag": "#industry", "trend_level": "Medium", "engagement_potential": "Low"}
        ]

    def _get_platform_trending_hashtags(self) -> List[Dict[str, str]]:
        """Gets platform-specific trending hashtags"""
        
        platform_hashtags = {
            "Facebook": [
                {"hashtag": "#business", "trend_level": "High", "engagement_potential": "Medium"},
                {"hashtag": "#community", "trend_level": "Medium", "engagement_potential": "High"}
            ],
            "Instagram": [
                {"hashtag": "#business", "trend_level": "High", "engagement_potential": "High"},
                {"hashtag": "#entrepreneur", "trend_level": "High", "engagement_potential": "High"},
                {"hashtag": "#marketing", "trend_level": "High", "engagement_potential": "High"}
            ],
            "LinkedIn": [
                {"hashtag": "#business", "trend_level": "High", "engagement_potential": "Medium"},
                {"hashtag": "#professional", "trend_level": "High", "engagement_potential": "Medium"},
                {"hashtag": "#career", "trend_level": "Medium", "engagement_potential": "High"}
            ]
        }
        
        return platform_hashtags.get(self.platform, platform_hashtags["Facebook"])

    def _research_industry_hashtags(self) -> Dict[str, List[str]]:
        """Researches industry-specific hashtags"""
        
        industry_hashtag_map = {
            "technology": {
                "primary": ["#tech", "#technology", "#innovation", "#digital", "#software"],
                "secondary": ["#startup", "#SaaS", "#AI", "#automation", "#cloud"],
                "niche": ["#techtrends", "#digitaltransformation", "#techinnovation", "#softwaredevelopment"]
            },
            "healthcare": {
                "primary": ["#healthcare", "#health", "#medical", "#wellness", "#medicine"],
                "secondary": ["#patientcare", "#healthtech", "#medicalinnovation", "#wellness", "#fitness"],
                "niche": ["#healthcareinnovation", "#digitalhealth", "#telemedicine", "#healthtech"]
            },
            "e-commerce": {
                "primary": ["#ecommerce", "#retail", "#online", "#shopping", "#business"],
                "secondary": ["#onlinestore", "#digitalcommerce", "#retailtech", "#customerservice"],
                "niche": ["#ecommercegrowth", "#onlineretail", "#digitalretail", "#ecommercetips"]
            },
            "finance": {
                "primary": ["#finance", "#fintech", "#banking", "#investment", "#money"],
                "secondary": ["#financialplanning", "#wealthmanagement", "#fintechinnovation", "#bankingtech"],
                "niche": ["#financialfreedom", "#investing", "#personalfinance", "#fintech"]
            },
            "education": {
                "primary": ["#education", "#learning", "#teaching", "#training", "#knowledge"],
                "secondary": ["#edtech", "#onlinelearning", "#professionaldevelopment", "#skills"],
                "niche": ["#educationinnovation", "#digitallearning", "#skilldevelopment", "#lifelonglearning"]
            }
        }
        
        industry_key = self.industry.lower()
        for key in industry_hashtag_map.keys():
            if key in industry_key:
                return industry_hashtag_map[key]
        
        # Default to general business hashtags
        return {
            "primary": ["#business", "#professional", "#industry", "#growth", "#success"],
            "secondary": ["#entrepreneur", "#leadership", "#strategy", "#innovation", "#marketing"],
            "niche": ["#businessgrowth", "#professionaldevelopment", "#industryinsights", "#businessstrategy"]
        }

    def _research_audience_hashtags(self) -> Dict[str, List[str]]:
        """Researches audience-specific hashtags"""
        
        audience_lower = self.target_audience.lower()
        
        # Determine audience type and demographics
        audience_type = "general"
        if any(word in audience_lower for word in ["professional", "business", "executive"]):
            audience_type = "professional"
        elif any(word in audience_lower for word in ["entrepreneur", "startup", "small business"]):
            audience_type = "entrepreneur"
        elif any(word in audience_lower for word in ["student", "learner", "education"]):
            audience_type = "student"
        
        # Age-based hashtags
        age_group = "mixed"
        if any(term in audience_lower for term in ["25-45", "millennial", "young"]):
            age_group = "millennial"
        elif any(term in audience_lower for term in ["45+", "senior", "mature"]):
            age_group = "mature"
        
        audience_hashtags = {
            "professional": {
                "primary": ["#professional", "#career", "#leadership", "#business", "#networking"],
                "secondary": ["#professionaldevelopment", "#careergrowth", "#businessnetworking", "#leadership"],
                "niche": ["#executivecoaching", "#businessstrategy", "#professionalgrowth", "#careeradvancement"]
            },
            "entrepreneur": {
                "primary": ["#entrepreneur", "#startup", "#businessowner", "#smallbusiness", "#hustle"],
                "secondary": ["#entrepreneurlife", "#startuplife", "#businessgrowth", "#entrepreneurmindset"],
                "niche": ["#startupjourney", "#entrepreneurial", "#businessbuilding", "#startupgrowth"]
            },
            "student": {
                "primary": ["#student", "#learning", "#education", "#study", "#knowledge"],
                "secondary": ["#studentlife", "#academic", "#studytips", "#learning", "#education"],
                "niche": ["#studymotivation", "#academiclife", "#learningjourney", "#education"]
            },
            "general": {
                "primary": ["#business", "#growth", "#success", "#motivation", "#inspiration"],
                "secondary": ["#businessgrowth", "#personalgrowth", "#successmindset", "#motivation"],
                "niche": ["#businessinsights", "#growthmindset", "#successstory", "#motivation"]
            }
        }
        
        return audience_hashtags.get(audience_type, audience_hashtags["general"])

    def _research_platform_hashtags(self) -> Dict[str, List[str]]:
        """Researches platform-specific hashtag best practices"""
        
        platform_guidelines = {
            "Facebook": {
                "optimal_count": "1-3 hashtags",
                "best_practices": ["Use sparingly", "Focus on community hashtags", "Avoid over-tagging"],
                "recommended_types": ["#business", "#community", "#local"],
                "avoid": ["Too many hashtags", "Irrelevant hashtags", "Spammy hashtags"]
            },
            "Instagram": {
                "optimal_count": "5-15 hashtags",
                "best_practices": ["Mix popular and niche", "Use relevant hashtags", "Include branded hashtags"],
                "recommended_types": ["#business", "#entrepreneur", "#marketing", "#industry specific"],
                "avoid": ["Banned hashtags", "Overused hashtags", "Irrelevant hashtags"]
            },
            "LinkedIn": {
                "optimal_count": "3-5 hashtags",
                "best_practices": ["Professional focus", "Industry relevance", "Business-oriented"],
                "recommended_types": ["#business", "#professional", "#industry", "#career"],
                "avoid": ["Casual hashtags", "Too many hashtags", "Personal hashtags"]
            }
        }
        
        return platform_guidelines.get(self.platform, platform_guidelines["Facebook"])

    def _compile_hashtag_recommendations(self, content_analysis: Dict, trending_hashtags: Dict,
                                       industry_hashtags: Dict, audience_hashtags: Dict,
                                       platform_hashtags: Dict) -> Dict[str, List[str]]:
        """Compiles and ranks hashtag recommendations"""
        
        # Get platform-specific optimal count
        optimal_count = int(platform_hashtags["optimal_count"].split("-")[1])
        
        # Create hashtag recommendations by category
        recommendations = {
            "popular_hashtags": self._select_popular_hashtags(trending_hashtags, optimal_count // 3),
            "niche_hashtags": self._select_niche_hashtags(industry_hashtags, audience_hashtags, optimal_count // 3),
            "branded_hashtags": self.brand_hashtags[:2],  # Limit branded hashtags
            "content_specific": self._select_content_specific_hashtags(content_analysis, optimal_count // 4)
        }
        
        # Combine and rank all hashtags
        all_hashtags = []
        for category, hashtags in recommendations.items():
            if isinstance(hashtags, list):
                all_hashtags.extend(hashtags)
        
        # Remove duplicates and rank by relevance
        unique_hashtags = list(set(all_hashtags))
        ranked_hashtags = self._rank_hashtags_by_relevance(unique_hashtags, content_analysis)
        
        # Select final recommendations
        final_recommendations = ranked_hashtags[:optimal_count]
        
        return {
            "final_hashtag_set": final_recommendations,
            "hashtag_breakdown": recommendations,
            "total_count": len(final_recommendations),
            "platform_optimized": True
        }

    def _select_popular_hashtags(self, trending_hashtags: Dict, count: int) -> List[str]:
        """Selects popular hashtags from trending research"""
        
        popular = []
        
        # Add general trending
        for hashtag_data in trending_hashtags["general_trending"][:count//2]:
            if isinstance(hashtag_data, dict):
                popular.append(hashtag_data["hashtag"])
            else:
                popular.append(hashtag_data)
        
        # Add industry trending
        for hashtag_data in trending_hashtags["industry_trending"][:count//2]:
            if isinstance(hashtag_data, dict):
                popular.append(hashtag_data["hashtag"])
            else:
                popular.append(hashtag_data)
        
        return popular[:count]

    def _select_niche_hashtags(self, industry_hashtags: Dict, audience_hashtags: Dict, count: int) -> List[str]:
        """Selects niche hashtags from industry and audience research"""
        
        niche = []
        
        # Add industry niche hashtags
        if "niche" in industry_hashtags:
            niche.extend(industry_hashtags["niche"][:count//2])
        
        # Add audience niche hashtags
        if "niche" in audience_hashtags:
            niche.extend(audience_hashtags["niche"][:count//2])
        
        return niche[:count]

    def _select_content_specific_hashtags(self, content_analysis: Dict, count: int) -> List[str]:
        """Selects content-specific hashtags from analysis"""
        
        content_hashtags = []
        
        # Add hashtags from content opportunities
        for opportunity in content_analysis["hashtag_opportunities"][:count]:
            if "hashtag_variations" in opportunity:
                # Select the best variation
                best_hashtag = opportunity["hashtag_variations"][0]
                content_hashtags.append(best_hashtag)
        
        return content_hashtags[:count]

    def _rank_hashtags_by_relevance(self, hashtags: List[str], content_analysis: Dict) -> List[str]:
        """Ranks hashtags by relevance to content"""
        
        # Simple ranking based on content keywords
        content_keywords = content_analysis["content_keywords"]
        
        ranked_hashtags = []
        for hashtag in hashtags:
            # Clean hashtag (remove #)
            clean_hashtag = hashtag.replace("#", "").lower()
            
            # Calculate relevance score
            relevance_score = 0
            for keyword in content_keywords:
                if keyword in clean_hashtag or clean_hashtag in keyword:
                    relevance_score += 1
            
            ranked_hashtags.append((hashtag, relevance_score))
        
        # Sort by relevance score (descending)
        ranked_hashtags.sort(key=lambda x: x[1], reverse=True)
        
        return [hashtag for hashtag, score in ranked_hashtags]

    def _create_hashtag_strategy(self, hashtag_recommendations: Dict) -> Dict[str, Any]:
        """Creates comprehensive hashtag strategy"""
        
        final_set = hashtag_recommendations["final_hashtag_set"]
        
        return {
            "strategy_overview": f"Use {len(final_set)} strategically selected hashtags optimized for {self.platform}",
            "hashtag_mix": {
                "popular_ratio": "30% - High-reach hashtags for visibility",
                "niche_ratio": "50% - Targeted hashtags for engagement",
                "branded_ratio": "10% - Brand-specific hashtags for consistency",
                "content_ratio": "10% - Content-specific hashtags for relevance"
            },
            "placement_recommendations": self._get_placement_recommendations(),
            "timing_considerations": self._get_timing_considerations(),
            "performance_tracking": self._get_performance_tracking_guidelines()
        }

    def _get_placement_recommendations(self) -> Dict[str, str]:
        """Gets hashtag placement recommendations by platform"""
        
        placement_guidelines = {
            "Facebook": "Place 1-2 hashtags at the end of the post or in comments",
            "Instagram": "Place all hashtags at the end of the caption or in first comment",
            "LinkedIn": "Place 3-5 hashtags at the end of the post content"
        }
        
        return {
            "platform_specific": placement_guidelines.get(self.platform, "Place hashtags at the end of content"),
            "general_guidelines": [
                "Don't overuse hashtags in the middle of sentences",
                "Group related hashtags together",
                "Use line breaks to separate hashtags from main content"
            ]
        }

    def _get_timing_considerations(self) -> List[str]:
        """Gets timing considerations for hashtag usage"""
        
        return [
            "Post when your target audience is most active",
            "Consider time zone differences for global reach",
            "Monitor trending hashtags for timely opportunities",
            "Avoid posting during hashtag spam periods",
            "Test different posting times to optimize hashtag performance"
        ]

    def _get_performance_tracking_guidelines(self) -> Dict[str, Any]:
        """Gets guidelines for tracking hashtag performance"""
        
        return {
            "key_metrics": [
                "Reach and impressions from hashtags",
                "Engagement rate on hashtag posts",
                "Click-through rates on hashtag content",
                "Follower growth from hashtag discovery"
            ],
            "tracking_tools": [
                "Platform native analytics",
                "Social media management tools",
                "Hashtag tracking apps",
                "Manual performance monitoring"
            ],
            "optimization_tips": [
                "Replace low-performing hashtags regularly",
                "Test new hashtag combinations",
                "Monitor competitor hashtag usage",
                "Adjust hashtag strategy based on performance data"
            ]
        }

    def _create_implementation_guidelines(self) -> Dict[str, Any]:
        """Creates implementation guidelines for hashtag usage"""
        
        return {
            "best_practices": [
                "Always use relevant hashtags",
                "Mix popular and niche hashtags",
                "Include branded hashtags for consistency",
                "Test and optimize hashtag performance",
                "Monitor hashtag trends and adapt"
            ],
            "common_mistakes_to_avoid": [
                "Using irrelevant hashtags",
                "Overusing popular hashtags",
                "Ignoring platform-specific guidelines",
                "Not tracking hashtag performance",
                "Using banned or spam hashtags"
            ],
            "optimization_tips": [
                "Research hashtag performance before using",
                "Create branded hashtags for campaigns",
                "Engage with posts using your hashtags",
                "Monitor hashtag trends regularly",
                "A/B test different hashtag combinations"
            ]
        }

    def _get_current_timestamp(self):
        """Helper method to get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat()

if __name__ == "__main__":
    tool = HashtagResearchEngine(
        post_content={
            "day": 1,
            "title": "How to Optimize Your Social Media Strategy",
            "caption": "Learn the best practices for social media optimization",
            "content_theme": "Educational Content",
            "goal": "Educate audience about industry topics"
        },
        industry="Technology",
        target_audience="Small business owners aged 25-45",
        platform="Instagram",
        brand_hashtags=["#MyBrand", "#BrandStrategy"]
    )
    print(tool.run())
