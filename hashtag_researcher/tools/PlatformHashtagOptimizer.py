from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from typing import Dict, Any, List

class PlatformHashtagOptimizer(BaseTool):
    """
    Optimizes hashtag strategy for specific platform best practices and limitations
    to ensure maximum effectiveness and compliance.
    """
    
    hashtag_set: List[str] = Field(
        ..., description="Base hashtag recommendations from research"
    )
    platform: str = Field(
        ..., description="Target platform (Facebook, Instagram, LinkedIn)"
    )
    content_type: str = Field(
        ..., description="Type of content (Image Post, Video, Story, etc.)"
    )

    def run(self):
        """
        Optimizes hashtag strategy for platform-specific best practices.
        """
        # Step 1: Validate inputs
        if not self.hashtag_set or not self.platform:
            return "Error: Hashtag set and platform are required."
        
        # Step 2: Get additional context from agency context
        business_data = self._context.get("business_data")
        brand_personality = self._context.get("brand_personality")
        
        if not all([business_data, brand_personality]):
            return "Error: Missing required context data. Please ensure business data and brand personality are available."
        
        # Step 3: Optimize hashtags for platform
        optimized_strategy = self._optimize_hashtags_for_platform()
        
        # Step 4: Store optimized strategy in context
        self._context.set("optimized_hashtag_strategy", optimized_strategy)
        
        # Step 5: Return optimized hashtag strategy
        return json.dumps({
            "status": "success",
            "message": "Hashtag strategy optimized for platform",
            "optimized_strategy": optimized_strategy
        }, indent=2)

    def _optimize_hashtags_for_platform(self) -> Dict[str, Any]:
        """Optimizes hashtag strategy for specific platform"""
        
        # Step 1: Get platform-specific guidelines
        platform_guidelines = self._get_platform_guidelines()
        
        # Step 2: Apply platform-specific optimizations
        optimized_hashtags = self._apply_platform_optimizations(platform_guidelines)
        
        # Step 3: Validate hashtag compliance
        compliance_check = self._validate_hashtag_compliance(optimized_hashtags)
        
        # Step 4: Create final optimized strategy
        final_strategy = self._create_final_strategy(optimized_hashtags, compliance_check)
        
        return final_strategy

    def _get_platform_guidelines(self) -> Dict[str, Any]:
        """Gets platform-specific hashtag guidelines"""
        
        guidelines = {
            "Facebook": {
                "optimal_count": {"min": 1, "max": 3},
                "best_practices": [
                    "Use sparingly to avoid appearing spammy",
                    "Focus on community and local hashtags",
                    "Place hashtags at the end of posts",
                    "Use hashtags that encourage discussion"
                ],
                "content_type_adjustments": {
                    "Image Post": "Use 1-2 relevant hashtags",
                    "Video": "Use 2-3 hashtags including #video",
                    "Link Share": "Use 1-2 hashtags related to the link content"
                },
                "avoid": [
                    "Too many hashtags (more than 5)",
                    "Irrelevant hashtags",
                    "Overly promotional hashtags",
                    "Spammy or banned hashtags"
                ]
            },
            "Instagram": {
                "optimal_count": {"min": 5, "max": 15},
                "best_practices": [
                    "Mix popular and niche hashtags",
                    "Include branded hashtags",
                    "Use hashtags in first comment or caption",
                    "Research hashtag performance before using"
                ],
                "content_type_adjustments": {
                    "Feed Post": "Use 10-15 hashtags for maximum reach",
                    "Story": "Use 1-3 hashtags with stickers",
                    "Reel": "Use 8-12 hashtags including trending ones",
                    "IGTV": "Use 5-10 hashtags in description"
                },
                "avoid": [
                    "Banned hashtags",
                    "Overused hashtags without engagement",
                    "Irrelevant hashtags",
                    "Hashtags that don't match your content"
                ]
            },
            "LinkedIn": {
                "optimal_count": {"min": 3, "max": 5},
                "best_practices": [
                    "Focus on professional and industry hashtags",
                    "Use hashtags that relate to your expertise",
                    "Include location-based hashtags if relevant",
                    "Place hashtags at the end of posts"
                ],
                "content_type_adjustments": {
                    "Article": "Use 3-5 professional hashtags",
                    "Image Post": "Use 3-4 relevant industry hashtags",
                    "Video": "Use 4-5 hashtags including #video",
                    "Text Post": "Use 3-5 professional hashtags"
                },
                "avoid": [
                    "Casual or personal hashtags",
                    "Too many hashtags (more than 5)",
                    "Irrelevant professional hashtags",
                    "Overly promotional hashtags"
                ]
            }
        }
        
        return guidelines.get(self.platform, guidelines["Facebook"])

    def _apply_platform_optimizations(self, platform_guidelines: Dict) -> Dict[str, Any]:
        """Applies platform-specific optimizations to hashtag set"""
        
        # Step 1: Filter hashtags based on platform guidelines
        filtered_hashtags = self._filter_hashtags_by_platform(platform_guidelines)
        
        # Step 2: Optimize count based on platform limits
        optimized_count = self._optimize_hashtag_count(filtered_hashtags, platform_guidelines)
        
        # Step 3: Apply content type specific adjustments
        content_adjusted = self._apply_content_type_adjustments(optimized_count, platform_guidelines)
        
        # Step 4: Rank hashtags by platform relevance
        ranked_hashtags = self._rank_hashtags_for_platform(content_adjusted)
        
        return {
            "optimized_hashtags": ranked_hashtags,
            "optimization_rationale": self._explain_optimization_decisions(platform_guidelines),
            "platform_compliance": self._check_platform_compliance(ranked_hashtags, platform_guidelines)
        }

    def _filter_hashtags_by_platform(self, platform_guidelines: Dict) -> List[str]:
        """Filters hashtags based on platform-specific criteria"""
        
        filtered = []
        
        for hashtag in self.hashtag_set:
            # Clean hashtag
            clean_hashtag = hashtag.replace("#", "").lower()
            
            # Check against platform avoid list
            avoid_keywords = platform_guidelines.get("avoid", [])
            should_avoid = any(keyword.lower() in clean_hashtag for keyword in avoid_keywords)
            
            if not should_avoid:
                # Check platform appropriateness
                if self._is_appropriate_for_platform(hashtag, self.platform):
                    filtered.append(hashtag)
        
        return filtered

    def _is_appropriate_for_platform(self, hashtag: str, platform: str) -> bool:
        """Checks if hashtag is appropriate for the platform"""
        
        clean_hashtag = hashtag.replace("#", "").lower()
        
        platform_appropriateness = {
            "Facebook": {
                "appropriate": ["business", "community", "local", "professional", "industry"],
                "inappropriate": ["casual", "personal", "trending", "viral"]
            },
            "Instagram": {
                "appropriate": ["business", "entrepreneur", "marketing", "industry", "lifestyle", "creative"],
                "inappropriate": ["spam", "fake", "irrelevant"]
            },
            "LinkedIn": {
                "appropriate": ["business", "professional", "career", "industry", "leadership", "networking"],
                "inappropriate": ["casual", "personal", "fun", "entertainment", "lifestyle"]
            }
        }
        
        platform_rules = platform_appropriateness.get(platform, platform_appropriateness["Facebook"])
        
        # Check if hashtag contains appropriate keywords
        appropriate_keywords = platform_rules["appropriate"]
        inappropriate_keywords = platform_rules["inappropriate"]
        
        has_appropriate = any(keyword in clean_hashtag for keyword in appropriate_keywords)
        has_inappropriate = any(keyword in clean_hashtag for keyword in inappropriate_keywords)
        
        return has_appropriate and not has_inappropriate

    def _optimize_hashtag_count(self, filtered_hashtags: List[str], platform_guidelines: Dict) -> List[str]:
        """Optimizes hashtag count based on platform limits"""
        
        optimal_count = platform_guidelines["optimal_count"]
        min_count = optimal_count["min"]
        max_count = optimal_count["max"]
        
        # If we have too many hashtags, select the best ones
        if len(filtered_hashtags) > max_count:
            # Rank hashtags by relevance and select top ones
            ranked = self._rank_hashtags_by_relevance(filtered_hashtags)
            return ranked[:max_count]
        
        # If we have too few hashtags, try to add more from context
        elif len(filtered_hashtags) < min_count:
            additional_hashtags = self._get_additional_hashtags(min_count - len(filtered_hashtags))
            return filtered_hashtags + additional_hashtags
        
        return filtered_hashtags

    def _rank_hashtags_by_relevance(self, hashtags: List[str]) -> List[str]:
        """Ranks hashtags by relevance to business and content"""
        
        # Simple ranking based on business context
        business_data = self._context.get("business_data", {})
        industry = business_data.get("industry", "").lower()
        
        ranked = []
        for hashtag in hashtags:
            clean_hashtag = hashtag.replace("#", "").lower()
            
            # Calculate relevance score
            score = 0
            
            # Industry relevance
            if any(word in clean_hashtag for word in industry.split()):
                score += 3
            
            # Business relevance
            business_keywords = ["business", "professional", "industry", "marketing"]
            if any(keyword in clean_hashtag for keyword in business_keywords):
                score += 2
            
            # Length optimization (prefer medium-length hashtags)
            if 4 <= len(clean_hashtag) <= 10:
                score += 1
            
            ranked.append((hashtag, score))
        
        # Sort by score (descending)
        ranked.sort(key=lambda x: x[1], reverse=True)
        
        return [hashtag for hashtag, score in ranked]

    def _get_additional_hashtags(self, needed_count: int) -> List[str]:
        """Gets additional hashtags to meet minimum count requirements"""
        
        business_data = self._context.get("business_data", {})
        industry = business_data.get("industry", "").lower()
        
        # Generate additional hashtags based on industry
        additional = []
        
        # Industry-specific hashtags
        industry_hashtags = {
            "technology": ["#tech", "#innovation", "#digital"],
            "healthcare": ["#health", "#wellness", "#medical"],
            "finance": ["#finance", "#investment", "#money"],
            "education": ["#education", "#learning", "#knowledge"],
            "e-commerce": ["#ecommerce", "#retail", "#online"]
        }
        
        for key, hashtags in industry_hashtags.items():
            if key in industry:
                additional.extend(hashtags[:needed_count])
                break
        
        # Add general business hashtags if needed
        if len(additional) < needed_count:
            general_hashtags = ["#business", "#professional", "#growth", "#success", "#marketing"]
            additional.extend(general_hashtags[:needed_count - len(additional)])
        
        return additional[:needed_count]

    def _apply_content_type_adjustments(self, hashtags: List[str], platform_guidelines: Dict) -> List[str]:
        """Applies content type specific adjustments"""
        
        content_adjustments = platform_guidelines.get("content_type_adjustments", {})
        adjustment = content_adjustments.get(self.content_type, {})
        
        if isinstance(adjustment, str):
            # Parse adjustment (e.g., "Use 1-2 relevant hashtags")
            import re
            count_match = re.search(r'(\d+)-(\d+)', adjustment)
            if count_match:
                min_count = int(count_match.group(1))
                max_count = int(count_match.group(2))
                
                # Adjust hashtag count based on content type
                if len(hashtags) > max_count:
                    hashtags = hashtags[:max_count]
                elif len(hashtags) < min_count:
                    additional = self._get_additional_hashtags(min_count - len(hashtags))
                    hashtags.extend(additional[:min_count - len(hashtags)])
        
        return hashtags

    def _rank_hashtags_for_platform(self, hashtags: List[str]) -> List[str]:
        """Ranks hashtags specifically for platform optimization"""
        
        platform_ranking_criteria = {
            "Facebook": ["community", "local", "discussion", "engagement"],
            "Instagram": ["visual", "trending", "lifestyle", "creative"],
            "LinkedIn": ["professional", "career", "industry", "networking"]
        }
        
        criteria = platform_ranking_criteria.get(self.platform, ["business", "professional"])
        
        ranked = []
        for hashtag in hashtags:
            clean_hashtag = hashtag.replace("#", "").lower()
            
            score = 0
            for criterion in criteria:
                if criterion in clean_hashtag:
                    score += 1
            
            ranked.append((hashtag, score))
        
        # Sort by platform relevance score
        ranked.sort(key=lambda x: x[1], reverse=True)
        
        return [hashtag for hashtag, score in ranked]

    def _explain_optimization_decisions(self, platform_guidelines: Dict) -> Dict[str, str]:
        """Explains the rationale behind optimization decisions"""
        
        return {
            "platform_selection": f"Optimized for {self.platform} platform best practices",
            "count_optimization": f"Adjusted to {platform_guidelines['optimal_count']} hashtags for optimal engagement",
            "content_type_consideration": f"Applied {self.content_type} specific adjustments",
            "filtering_rationale": "Filtered out inappropriate and non-compliant hashtags",
            "ranking_strategy": f"Ranked hashtags by {self.platform} relevance and engagement potential"
        }

    def _check_platform_compliance(self, hashtags: List[str], platform_guidelines: Dict) -> Dict[str, Any]:
        """Checks compliance with platform guidelines"""
        
        compliance_checks = {
            "count_compliance": len(hashtags) <= platform_guidelines["optimal_count"]["max"],
            "content_appropriateness": all(self._is_appropriate_for_platform(h, self.platform) for h in hashtags),
            "avoid_list_compliance": not any(any(avoid in h.lower() for avoid in platform_guidelines["avoid"]) for h in hashtags),
            "best_practices_adherence": self._check_best_practices_adherence(hashtags, platform_guidelines)
        }
        
        overall_compliance = all(compliance_checks.values())
        
        return {
            "overall_compliance": overall_compliance,
            "compliance_checks": compliance_checks,
            "recommendations": self._get_compliance_recommendations(compliance_checks, platform_guidelines)
        }

    def _check_best_practices_adherence(self, hashtags: List[str], platform_guidelines: Dict) -> bool:
        """Checks adherence to platform best practices"""
        
        best_practices = platform_guidelines.get("best_practices", [])
        
        # Check if hashtags align with best practices
        adherence_score = 0
        total_checks = len(best_practices)
        
        for practice in best_practices:
            if self._evaluate_practice_adherence(hashtags, practice):
                adherence_score += 1
        
        return adherence_score >= total_checks * 0.7  # 70% adherence threshold

    def _evaluate_practice_adherence(self, hashtags: List[str], practice: str) -> bool:
        """Evaluates adherence to a specific best practice"""
        
        practice_lower = practice.lower()
        
        if "relevant" in practice_lower:
            return self._check_relevance(hashtags)
        elif "sparingly" in practice_lower:
            return len(hashtags) <= 3
        elif "professional" in practice_lower:
            return self._check_professional_appropriateness(hashtags)
        elif "community" in practice_lower:
            return any("community" in h.lower() or "local" in h.lower() for h in hashtags)
        
        return True  # Default to true if practice not specifically checkable

    def _check_relevance(self, hashtags: List[str]) -> bool:
        """Checks if hashtags are relevant to content and business"""
        
        business_data = self._context.get("business_data", {})
        industry = business_data.get("industry", "").lower()
        
        relevant_count = 0
        for hashtag in hashtags:
            clean_hashtag = hashtag.replace("#", "").lower()
            if any(word in clean_hashtag for word in industry.split()):
                relevant_count += 1
        
        return relevant_count >= len(hashtags) * 0.5  # At least 50% relevant

    def _check_professional_appropriateness(self, hashtags: List[str]) -> bool:
        """Checks if hashtags are professionally appropriate"""
        
        professional_keywords = ["business", "professional", "career", "industry", "leadership"]
        casual_keywords = ["fun", "party", "casual", "personal", "lifestyle"]
        
        professional_count = sum(1 for h in hashtags if any(p in h.lower() for p in professional_keywords))
        casual_count = sum(1 for h in hashtags if any(c in h.lower() for c in casual_keywords))
        
        return professional_count >= casual_count

    def _get_compliance_recommendations(self, compliance_checks: Dict, platform_guidelines: Dict) -> List[str]:
        """Gets recommendations for improving compliance"""
        
        recommendations = []
        
        if not compliance_checks["count_compliance"]:
            recommendations.append(f"Reduce hashtag count to {platform_guidelines['optimal_count']['max']} or fewer")
        
        if not compliance_checks["content_appropriateness"]:
            recommendations.append("Replace inappropriate hashtags with platform-suitable alternatives")
        
        if not compliance_checks["avoid_list_compliance"]:
            recommendations.append("Remove hashtags that appear on the platform's avoid list")
        
        if not compliance_checks["best_practices_adherence"]:
            recommendations.append("Review and align with platform best practices")
        
        if not recommendations:
            recommendations.append("Hashtag strategy is fully compliant with platform guidelines")
        
        return recommendations

    def _create_final_strategy(self, optimized_hashtags: Dict, compliance_check: Dict) -> Dict[str, Any]:
        """Creates the final optimized hashtag strategy"""
        
        return {
            "platform": self.platform,
            "content_type": self.content_type,
            "optimized_hashtag_list": optimized_hashtags["optimized_hashtags"],
            "hashtag_count": len(optimized_hashtags["optimized_hashtags"]),
            "optimization_rationale": optimized_hashtags["optimization_rationale"],
            "platform_compliance": compliance_check,
            "implementation_guidelines": self._create_implementation_guidelines(),
            "performance_tracking": self._create_performance_tracking_guidelines(),
            "optimization_timestamp": self._get_current_timestamp()
        }

    def _create_implementation_guidelines(self) -> Dict[str, Any]:
        """Creates implementation guidelines for optimized hashtags"""
        
        placement_guidelines = {
            "Facebook": "Place hashtags at the end of the post or in the first comment",
            "Instagram": "Place hashtags at the end of the caption or in the first comment",
            "LinkedIn": "Place hashtags at the end of the post content"
        }
        
        return {
            "placement": placement_guidelines.get(self.platform, "Place hashtags at the end of content"),
            "formatting": [
                "Use proper hashtag format with # symbol",
                "Avoid spaces in hashtags",
                "Use camelCase for multi-word hashtags",
                "Test hashtag functionality before posting"
            ],
            "timing": [
                "Post when your target audience is most active",
                "Consider platform-specific optimal posting times",
                "Monitor hashtag performance and adjust timing"
            ],
            "engagement": [
                "Engage with posts using your hashtags",
                "Monitor hashtag mentions and respond appropriately",
                "Track hashtag performance metrics"
            ]
        }

    def _create_performance_tracking_guidelines(self) -> Dict[str, Any]:
        """Creates guidelines for tracking hashtag performance"""
        
        return {
            "key_metrics": [
                "Reach and impressions from hashtag posts",
                "Engagement rate on hashtag content",
                "Click-through rates from hashtag discovery",
                "Follower growth from hashtag visibility"
            ],
            "tracking_frequency": "Weekly performance review, monthly comprehensive analysis",
            "optimization_actions": [
                "Replace low-performing hashtags",
                "Test new hashtag combinations",
                "Monitor trending hashtags for opportunities",
                "Adjust hashtag strategy based on performance data"
            ],
            "success_benchmarks": {
                "engagement_rate": "Above platform average",
                "reach_growth": "Month-over-month increase",
                "hashtag_performance": "Consistent engagement across hashtag posts"
            }
        }

    def _get_current_timestamp(self):
        """Helper method to get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat()

if __name__ == "__main__":
    tool = PlatformHashtagOptimizer(
        hashtag_set=["#business", "#marketing", "#entrepreneur", "#growth", "#success"],
        platform="Instagram",
        content_type="Image Post"
    )
    print(tool.run())
