from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from typing import Dict, Any, List

class ContentCalendarBuilder(BaseTool):
    """
    Organizes and structures the complete 7-day content plan with all post details,
    visual concepts, and hashtag recommendations into a comprehensive calendar.
    """
    
    calendar_format: str = Field(
        default="structured", 
        description="Format for the calendar output: 'structured', 'detailed', or 'summary'"
    )

    def run(self):
        """
        Builds comprehensive content calendar by combining all daily posts and additional elements.
        """
        # Step 1: Collect all daily posts from context
        daily_posts = self._collect_daily_posts()
        
        if len(daily_posts) != 7:
            return f"Error: Expected 7 daily posts, found {len(daily_posts)}. Please ensure all daily posts are generated."
        
        # Step 2: Get additional context data
        business_data = self._context.get("business_data")
        brand_personality = self._context.get("brand_personality")
        platform_selection = self._context.get("platform_selection")
        strategy_framework = self._context.get("strategy_framework")
        
        if not all([business_data, brand_personality, platform_selection, strategy_framework]):
            return "Error: Missing required context data. Please ensure all previous steps are completed."
        
        # Step 3: Build comprehensive content calendar
        content_calendar = self._build_content_calendar(
            daily_posts, business_data, brand_personality, 
            platform_selection, strategy_framework
        )
        
        # Step 4: Store complete calendar in context
        self._context.set("content_plan", content_calendar)
        
        # Step 5: Return formatted calendar
        return json.dumps({
            "status": "success",
            "message": "Content calendar built successfully",
            "content_calendar": content_calendar
        }, indent=2)

    def _collect_daily_posts(self) -> List[Dict[str, Any]]:
        """Collects all daily posts from context"""
        
        daily_posts = []
        for day_num in range(1, 8):  # Days 1-7
            post_key = f"day_{day_num}_post"
            post_data = self._context.get(post_key)
            
            if post_data:
                daily_posts.append(post_data)
            else:
                # Create placeholder post if missing
                placeholder_post = self._create_placeholder_post(day_num)
                daily_posts.append(placeholder_post)
        
        return daily_posts

    def _create_placeholder_post(self, day_num: int) -> Dict[str, Any]:
        """Creates a placeholder post if a day is missing"""
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        return {
            "day": day_num,
            "day_name": days[day_num - 1],
            "platform": "Instagram",  # Default platform
            "goal": "Increase audience engagement",
            "type_of_post": "Image Post",
            "title": f"Day {day_num} Content",
            "caption": "Content placeholder - please generate specific content for this day.",
            "content_theme": "General Content",
            "platform_optimization": {},
            "brand_alignment": {},
            "target_audience": "General audience",
            "generation_timestamp": self._get_current_timestamp()
        }

    def _build_content_calendar(self, daily_posts: List[Dict], business_data: Dict, 
                              brand_personality: Dict, platform_selection: Dict, 
                              strategy_framework: Dict) -> Dict[str, Any]:
        """Builds comprehensive content calendar structure"""
        
        # Step 1: Organize posts by day and platform
        organized_posts = self._organize_posts_by_day_and_platform(daily_posts)
        
        # Step 2: Calculate calendar statistics
        calendar_stats = self._calculate_calendar_statistics(daily_posts)
        
        # Step 3: Create platform-specific summaries
        platform_summaries = self._create_platform_summaries(organized_posts)
        
        # Step 4: Build theme analysis
        theme_analysis = self._analyze_content_themes(daily_posts)
        
        # Step 5: Create implementation guide
        implementation_guide = self._create_implementation_guide(
            business_data, brand_personality, platform_selection
        )
        
        return {
            "calendar_overview": {
                "total_posts": len(daily_posts),
                "platforms_covered": platform_selection["selected_platforms"],
                "content_themes": [post.get("content_theme", "General") for post in daily_posts],
                "calendar_period": "1 week",
                "generation_date": self._get_current_timestamp()
            },
            "business_context": {
                "industry": business_data["industry"],
                "target_audience": business_data["target_audience"],
                "business_goals": business_data["business_goals"],
                "brand_voice": brand_personality["brand_voice"],
                "brand_tone": brand_personality["brand_tone"]
            },
            "daily_posts": self._format_daily_posts(daily_posts),
            "calendar_statistics": calendar_stats,
            "platform_distribution": platform_summaries,
            "theme_analysis": theme_analysis,
            "implementation_guide": implementation_guide,
            "content_calendar_table": self._create_calendar_table(daily_posts)
        }

    def _organize_posts_by_day_and_platform(self, daily_posts: List[Dict]) -> Dict[str, Any]:
        """Organizes posts by day and platform for analysis"""
        
        organized = {}
        
        for post in daily_posts:
            day_name = post.get("day_name", "Unknown")
            platform = post.get("platform", "Unknown")
            
            if day_name not in organized:
                organized[day_name] = {}
            
            if platform not in organized[day_name]:
                organized[day_name][platform] = []
            
            organized[day_name][platform].append(post)
        
        return organized

    def _calculate_calendar_statistics(self, daily_posts: List[Dict]) -> Dict[str, Any]:
        """Calculates comprehensive calendar statistics"""
        
        # Count content types
        content_types = {}
        platforms = {}
        themes = {}
        goals = {}
        
        for post in daily_posts:
            # Content types
            content_type = post.get("type_of_post", "Unknown")
            content_types[content_type] = content_types.get(content_type, 0) + 1
            
            # Platforms
            platform = post.get("platform", "Unknown")
            platforms[platform] = platforms.get(platform, 0) + 1
            
            # Themes
            theme = post.get("content_theme", "Unknown")
            themes[theme] = themes.get(theme, 0) + 1
            
            # Goals
            goal = post.get("goal", "Unknown")
            goals[goal] = goals.get(goal, 0) + 1
        
        return {
            "content_type_distribution": content_types,
            "platform_distribution": platforms,
            "theme_distribution": themes,
            "goal_distribution": goals,
            "total_posts": len(daily_posts),
            "unique_platforms": len(platforms),
            "unique_themes": len(themes)
        }

    def _create_platform_summaries(self, organized_posts: Dict) -> Dict[str, Any]:
        """Creates summaries for each platform"""
        
        platform_summaries = {}
        
        for day, day_data in organized_posts.items():
            for platform, posts in day_data.items():
                if platform not in platform_summaries:
                    platform_summaries[platform] = {
                        "total_posts": 0,
                        "content_types": {},
                        "themes": {},
                        "posting_schedule": {}
                    }
                
                platform_summaries[platform]["total_posts"] += len(posts)
                platform_summaries[platform]["posting_schedule"][day] = len(posts)
                
                for post in posts:
                    # Count content types
                    content_type = post.get("type_of_post", "Unknown")
                    platform_summaries[platform]["content_types"][content_type] = \
                        platform_summaries[platform]["content_types"].get(content_type, 0) + 1
                    
                    # Count themes
                    theme = post.get("content_theme", "Unknown")
                    platform_summaries[platform]["themes"][theme] = \
                        platform_summaries[platform]["themes"].get(theme, 0) + 1
        
        return platform_summaries

    def _analyze_content_themes(self, daily_posts: List[Dict]) -> Dict[str, Any]:
        """Analyzes content themes across the calendar"""
        
        theme_analysis = {
            "theme_frequency": {},
            "theme_goals": {},
            "theme_platforms": {},
            "theme_consistency": {}
        }
        
        for post in daily_posts:
            theme = post.get("content_theme", "Unknown")
            goal = post.get("goal", "Unknown")
            platform = post.get("platform", "Unknown")
            
            # Count theme frequency
            theme_analysis["theme_frequency"][theme] = \
                theme_analysis["theme_frequency"].get(theme, 0) + 1
            
            # Track goals per theme
            if theme not in theme_analysis["theme_goals"]:
                theme_analysis["theme_goals"][theme] = []
            theme_analysis["theme_goals"][theme].append(goal)
            
            # Track platforms per theme
            if theme not in theme_analysis["theme_platforms"]:
                theme_analysis["theme_platforms"][theme] = []
            theme_analysis["theme_platforms"][theme].append(platform)
        
        # Calculate theme consistency
        for theme, goals in theme_analysis["theme_goals"].items():
            unique_goals = len(set(goals))
            theme_analysis["theme_consistency"][theme] = {
                "goal_diversity": unique_goals,
                "consistency_score": 1 if unique_goals <= 2 else 0.5
            }
        
        return theme_analysis

    def _create_implementation_guide(self, business_data: Dict, brand_personality: Dict, 
                                   platform_selection: Dict) -> Dict[str, Any]:
        """Creates implementation guide for the content calendar"""
        
        return {
            "pre_launch_checklist": [
                "Review all content for brand voice alignment",
                "Prepare visual assets according to design suggestions",
                "Set up scheduling tools for each platform",
                "Prepare hashtag lists for easy copy-paste",
                "Create content approval workflow"
            ],
            "posting_schedule": {
                "frequency": "Daily posting across selected platforms",
                "optimal_times": self._get_optimal_posting_times(platform_selection["selected_platforms"]),
                "content_preparation": "Prepare content 2-3 days in advance",
                "engagement_monitoring": "Monitor comments and engagement for 2 hours after posting"
            },
            "quality_assurance": [
                "Ensure all content aligns with brand voice and tone",
                "Verify hashtags are relevant and not overused",
                "Check visual quality and brand consistency",
                "Test links and call-to-actions",
                "Review for grammar and spelling"
            ],
            "performance_tracking": [
                "Track engagement rates for each post",
                "Monitor reach and impressions",
                "Analyze which content types perform best",
                "Track hashtag performance",
                "Measure goal achievement (awareness, leads, etc.)"
            ]
        }

    def _get_optimal_posting_times(self, platforms: List[str]) -> Dict[str, str]:
        """Gets optimal posting times for each platform"""
        
        optimal_times = {
            "Facebook": "9 AM - 3 PM, Tuesday-Thursday",
            "Instagram": "11 AM - 1 PM, 5 PM - 7 PM, Monday-Friday",
            "LinkedIn": "8 AM - 10 AM, 12 PM - 2 PM, Tuesday-Thursday"
        }
        
        return {platform: optimal_times.get(platform, "Check platform analytics for optimal times") 
                for platform in platforms}

    def _format_daily_posts(self, daily_posts: List[Dict]) -> List[Dict[str, Any]]:
        """Formats daily posts for calendar presentation"""
        
        formatted_posts = []
        
        for post in daily_posts:
            formatted_post = {
                "day": post.get("day"),
                "day_name": post.get("day_name"),
                "platform": post.get("platform"),
                "goal": post.get("goal"),
                "type_of_post": post.get("type_of_post"),
                "title": post.get("title"),
                "caption": post.get("caption"),
                "content_theme": post.get("content_theme"),
                "visual_concept": "To be provided by Visual Designer",  # Placeholder
                "hashtags": "To be provided by Hashtag Researcher",  # Placeholder
                "brand_alignment": post.get("brand_alignment", {}),
                "target_audience": post.get("target_audience")
            }
            formatted_posts.append(formatted_post)
        
        return formatted_posts

    def _create_calendar_table(self, daily_posts: List[Dict]) -> List[Dict[str, str]]:
        """Creates a simple table format for the content calendar"""
        
        calendar_table = []
        
        for post in daily_posts:
            table_row = {
                "Day": post.get("day_name", ""),
                "Platform": post.get("platform", ""),
                "Type": post.get("type_of_post", ""),
                "Title": post.get("title", "")[:50] + "..." if len(post.get("title", "")) > 50 else post.get("title", ""),
                "Goal": post.get("goal", "")[:30] + "..." if len(post.get("goal", "")) > 30 else post.get("goal", ""),
                "Theme": post.get("content_theme", "")
            }
            calendar_table.append(table_row)
        
        return calendar_table

    def _get_current_timestamp(self):
        """Helper method to get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat()

if __name__ == "__main__":
    tool = ContentCalendarBuilder(calendar_format="structured")
    print(tool.run())
